"""FastAPI HTTP server for the trading bot."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Optional, List, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from bot.client import DEFAULT_BASE_URL, APIError, BinanceClient, NetworkError
from bot.confidence import ConfidenceScorer
from bot.logging_config import get_logger
from bot.orders import OrderManager, load_order_history
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = get_logger("api")

app = FastAPI(title="Trading Bot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_client = BinanceClient()
_scorer = ConfidenceScorer(_client)
_order_manager = OrderManager(_client, _scorer)


class OrderRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None


class OrderResponse(BaseModel):
    order: Dict[str, Any]
    confidence: Dict[str, Any]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    testnet: bool
    server_time: int


def _is_testnet() -> bool:
    base_url = os.getenv("BASE_URL", DEFAULT_BASE_URL).lower()
    return "testnet" in base_url


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _collect_field_errors(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str],
) -> List[Dict[str, Any]]:
    """Run validators and return FastAPI-compatible field error details."""
    errors: List[Dict[str, Any]] = []

    try:
        validate_symbol(symbol)
    except ValueError as exc:
        errors.append({"loc": ["body", "symbol"], "msg": str(exc), "type": "value_error"})

    try:
        validate_side(side)
    except ValueError as exc:
        errors.append({"loc": ["body", "side"], "msg": str(exc), "type": "value_error"})

    validated_order_type: Optional[str] = None
    try:
        validated_order_type = validate_order_type(order_type)
    except ValueError as exc:
        errors.append({"loc": ["body", "order_type"], "msg": str(exc), "type": "value_error"})

    try:
        validate_quantity(quantity)
    except ValueError as exc:
        errors.append({"loc": ["body", "quantity"], "msg": str(exc), "type": "value_error"})

    price_context = validated_order_type or order_type.strip().upper()
    if price_context in {"MARKET", "LIMIT"}:
        try:
            validate_price(price, price_context)
        except ValueError as exc:
            errors.append({"loc": ["body", "price"], "msg": str(exc), "type": "value_error"})

    return errors


def _collect_confidence_field_errors(
    symbol: str,
    side: str,
    order_type: str,
    price: Optional[str],
) -> List[Dict[str, Any]]:
    """Validate fields needed for a confidence score request."""
    errors: List[Dict[str, Any]] = []

    try:
        validate_symbol(symbol)
    except ValueError as exc:
        errors.append({"loc": ["query", "symbol"], "msg": str(exc), "type": "value_error"})

    try:
        validate_side(side)
    except ValueError as exc:
        errors.append({"loc": ["query", "side"], "msg": str(exc), "type": "value_error"})

    validated_order_type: Optional[str] = None
    try:
        validated_order_type = validate_order_type(order_type)
    except ValueError as exc:
        errors.append({"loc": ["query", "order_type"], "msg": str(exc), "type": "value_error"})

    price_context = validated_order_type or order_type.strip().upper()
    if price_context in {"MARKET", "LIMIT"}:
        try:
            validate_price(price, price_context)
        except ValueError as exc:
            errors.append({"loc": ["query", "price"], "msg": str(exc), "type": "value_error"})

    return errors


def _validate_order_request(body: OrderRequest) -> Dict[str, Any]:
    price_arg = str(body.price) if body.price is not None else None
    field_errors = _collect_field_errors(
        symbol=body.symbol,
        side=body.side,
        order_type=body.order_type,
        quantity=str(body.quantity),
        price=price_arg,
    )
    if field_errors:
        raise HTTPException(status_code=422, detail=field_errors)

    from bot.validators import validate_all

    return validate_all(
        symbol=body.symbol,
        side=body.side,
        order_type=body.order_type,
        quantity=str(body.quantity),
        price=price_arg,
    )


@app.on_event("startup")
def on_startup() -> None:
    logger.info("API server starting", extra={"testnet": _is_testnet()})


@app.on_event("shutdown")
def on_shutdown() -> None:
    _client.close()


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        server_time_payload = _client.get_server_time()
        server_time = int(server_time_payload["serverTime"])
    except (APIError, NetworkError, KeyError, TypeError) as exc:
        logger.warning("Health check could not fetch server time: %s", exc)
        server_time = 0

    return HealthResponse(
        status="ok",
        testnet=_is_testnet(),
        server_time=server_time,
    )


@app.get("/api/confidence")
def get_confidence(
    symbol: str = Query(...),
    side: str = Query(...),
    order_type: str = Query(...),
    price: Optional[float] = Query(None),
) -> Dict[str, Any]:
    price_arg = str(price) if price is not None else None
    field_errors = _collect_confidence_field_errors(
        symbol=symbol,
        side=side,
        order_type=order_type,
        price=price_arg,
    )
    if field_errors:
        raise HTTPException(status_code=422, detail=field_errors)

    return _scorer.score(symbol=symbol, side=side, order_type=order_type, price=price)


@app.post("/api/orders", response_model=OrderResponse)
def create_order(body: OrderRequest) -> OrderResponse:
    validated = _validate_order_request(body)

    try:
        confidence = _scorer.score(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            price=validated["price"],
        )
        result = _order_manager.place_order(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"],
            confidence=confidence,
        )
    except (APIError, NetworkError) as exc:
        logger.error("Order placement failed", extra={"error": str(exc)})
        status_code = 503 if isinstance(exc, NetworkError) else 502
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    return OrderResponse(
        order=result["order"],
        confidence=result["confidence"],
        timestamp=_utc_timestamp(),
    )


@app.get("/api/orders/history")
def order_history() -> List[Dict[str, Any]]:
    return load_order_history()


@app.get("/api/account")
def get_account() -> Dict[str, Any]:
    try:
        account = _client.get_account()
    except (APIError, NetworkError) as exc:
        logger.error("Account fetch failed", extra={"error": str(exc)})
        status_code = 503 if isinstance(exc, NetworkError) else 502
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    assets = [
        {
            "asset": asset.get("asset"),
            "walletBalance": asset.get("walletBalance"),
            "unrealizedProfit": asset.get("unrealizedProfit"),
        }
        for asset in account.get("assets", [])
        if float(asset.get("walletBalance", 0)) != 0
        or float(asset.get("unrealizedProfit", 0)) != 0
    ]

    return {
        "assets": assets,
        "totalWalletBalance": account.get("totalWalletBalance"),
        "totalUnrealizedProfit": account.get("totalUnrealizedProfit"),
    }


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=False)
