"""Input validation for trading operations."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

_ALLOWED_QUOTE_SUFFIXES = ("USDT", "BUSD")


def validate_symbol(symbol: str) -> str:
    """Normalize and validate a trading pair symbol."""
    normalized = symbol.strip().upper()

    if len(normalized) < 6:
        raise ValueError(
            f"symbol must be at least 6 characters long, got {len(normalized)} ({normalized!r})"
        )

    if not any(normalized.endswith(suffix) for suffix in _ALLOWED_QUOTE_SUFFIXES):
        raise ValueError(
            f"symbol must end with USDT or BUSD, got {normalized!r}"
        )

    return normalized


def validate_side(side: str) -> str:
    """Validate order side and return uppercase BUY or SELL."""
    normalized = side.strip().upper()

    if normalized not in {"BUY", "SELL"}:
        raise ValueError(
            f"side must be BUY or SELL (case-insensitive), got {side!r}"
        )

    return normalized


def validate_order_type(order_type: str) -> str:
    """Validate order type and return uppercase MARKET or LIMIT."""
    normalized = order_type.strip().upper()

    if normalized not in {"MARKET", "LIMIT"}:
        raise ValueError(
            f"order_type must be MARKET or LIMIT (case-insensitive), got {order_type!r}"
        )

    return normalized


def validate_quantity(quantity: str) -> float:
    """Validate quantity as a positive float with at most 8 decimal places."""
    raw = quantity.strip()

    if not raw:
        raise ValueError("quantity is required and must be a positive number")

    try:
        decimal_value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(
            f"quantity must be a valid number, got {quantity!r}"
        ) from exc

    if not decimal_value.is_finite():
        raise ValueError(f"quantity must be a finite number, got {quantity!r}")

    if decimal_value <= 0:
        raise ValueError(
            f"quantity must be greater than zero, got {quantity!r}"
        )

    exponent = decimal_value.as_tuple().exponent
    if isinstance(exponent, int) and exponent < -8:
        raise ValueError(
            f"quantity supports at most 8 decimal places, got {quantity!r}"
        )

    return float(decimal_value)


def validate_price(price: str | None, order_type: str) -> float | None:
    """Validate price for LIMIT orders; return None for MARKET orders."""
    normalized_type = order_type.strip().upper()

    if normalized_type == "MARKET":
        return None

    if normalized_type != "LIMIT":
        raise ValueError(
            f"order_type must be MARKET or LIMIT to validate price, got {order_type!r}"
        )

    if price is None or not str(price).strip():
        raise ValueError("price is required for LIMIT orders")

    raw = str(price).strip()

    try:
        decimal_value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(
            f"price must be a valid number for LIMIT orders, got {price!r}"
        ) from exc

    if not decimal_value.is_finite():
        raise ValueError(f"price must be a finite number, got {price!r}")

    if decimal_value <= 0:
        raise ValueError(
            f"price must be greater than zero for LIMIT orders, got {price!r}"
        )

    return float(decimal_value)


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> dict[str, Any]:
    """Run all validators and return normalized order fields."""
    errors: list[str] = []

    validated_symbol: str | None = None
    validated_side: str | None = None
    validated_order_type: str | None = None
    validated_quantity: float | None = None
    validated_price: float | None = None

    try:
        validated_symbol = validate_symbol(symbol)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        validated_side = validate_side(side)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        validated_order_type = validate_order_type(order_type)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        validated_quantity = validate_quantity(quantity)
    except ValueError as exc:
        errors.append(str(exc))

    price_context = validated_order_type or order_type.strip().upper()
    if price_context in {"MARKET", "LIMIT"}:
        try:
            validated_price = validate_price(price, price_context)
        except ValueError as exc:
            errors.append(str(exc))

    if errors:
        report = "\n".join(f"  - {message}" for message in errors)
        raise ValueError(f"Order validation failed with {len(errors)} error(s):\n{report}")

    return {
        "symbol": validated_symbol,
        "side": validated_side,
        "type": validated_order_type,
        "quantity": validated_quantity,
        "price": validated_price,
    }


def validate_order(order: dict[str, Any]) -> dict[str, Any]:
    """Validate a raw order dict; raises ValueError on invalid input."""
    raw_price = order.get("price")
    return validate_all(
        symbol=str(order.get("symbol", "")),
        side=str(order.get("side", "")),
        order_type=str(order.get("type") or order.get("order_type", "")),
        quantity=str(order.get("quantity", "")),
        price=str(raw_price) if raw_price is not None else None,
    )
