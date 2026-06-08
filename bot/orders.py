"""Order placement and management."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rich import print as rprint
from rich.console import Console
from rich.table import Table

from bot.client import APIError, BinanceClient, NetworkError
from bot.confidence import ConfidenceScorer
from bot.logging_config import get_logger

logger = get_logger("orders")
console = Console()

_HISTORY_PATH = Path(__file__).resolve().parent.parent / "logs" / "orders_history.json"


class OrderManager:
    """Coordinates confidence scoring, order submission, and history tracking."""

    def __init__(self, client: BinanceClient, scorer: ConfidenceScorer) -> None:
        self._client = client
        self._scorer = scorer

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str | float,
        price: float | None = None,
        *,
        dry_run: bool = False,
        confidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Score confidence, submit an order, log history, and return the result."""
        if confidence is None:
            confidence = self._scorer.score(symbol, side, order_type, price)
        self._log_and_print_confidence(confidence)

        normalized_type = order_type.strip().upper()
        params: dict[str, Any] = {
            "symbol": symbol.strip().upper(),
            "side": side.strip().upper(),
            "type": normalized_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
        }

        if normalized_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = "GTC"

        self._print_request_summary(params)

        if dry_run:
            rprint("[bold yellow][DRY RUN] Order NOT submitted.[/bold yellow]")
            return {"order": None, "confidence": confidence, "dry_run": True}

        try:
            response = self._client.place_order(**params)
        except (APIError, NetworkError) as exc:
            logger.error(
                "Order placement failed",
                extra={"error": str(exc), "params": params},
            )
            rprint(f"[bold red]Order failed:[/bold red] {exc}")
            raise

        self._print_response_table(response)

        result = {"order": response, "confidence": confidence}
        self._append_history(params, confidence, response)

        return result

    def _log_and_print_confidence(self, confidence: dict[str, Any]) -> None:
        logger.info("Confidence result", extra={"confidence": confidence})

        table = Table(title="Confidence Score", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="dim")
        table.add_column("Value")

        table.add_row("Total Score", str(confidence["total_score"]))
        table.add_row("Grade", confidence["grade"])
        table.add_row("Recommendation", confidence["recommendation"])

        breakdown = confidence["breakdown"]
        table.add_row("Volatility", str(breakdown["volatility"]))
        table.add_row("Depth", str(breakdown["depth"]))
        table.add_row("Price Proximity", str(breakdown["price_proximity"]))

        console.print(table)

    def _print_request_summary(self, params: dict[str, Any]) -> None:
        table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="dim")
        table.add_column("Value")

        for key, value in params.items():
            table.add_row(key, str(value))

        console.print(table)

    def _print_response_table(self, response: dict[str, Any]) -> None:
        table = Table(title="Order Response", show_header=True, header_style="bold green")
        table.add_column("Field", style="dim")
        table.add_column("Value")

        for field in ("orderId", "status", "executedQty", "avgPrice", "cumQuote"):
            table.add_row(field, str(response.get(field, "N/A")))

        console.print(table)

    def _append_history(
        self,
        params: dict[str, Any],
        confidence: dict[str, Any],
        response: dict[str, Any],
    ) -> None:
        _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

        history: list[dict[str, Any]] = []
        if _HISTORY_PATH.exists():
            try:
                history = json.loads(_HISTORY_PATH.read_text(encoding="utf-8"))
                if not isinstance(history, list):
                    history = []
            except json.JSONDecodeError:
                logger.warning("Corrupt orders history file; starting fresh")
                history = []

        entry = {
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "request": params,
            "confidence": confidence,
            "response": response,
        }
        history.append(entry)

        _HISTORY_PATH.write_text(
            json.dumps(history, indent=2, default=str),
            encoding="utf-8",
        )
        logger.info(
            "Order appended to history",
            extra={"history_file": str(_HISTORY_PATH), "order_id": response.get("orderId")},
        )


def load_order_history() -> list[dict[str, Any]]:
    """Load persisted order history from disk."""
    if not _HISTORY_PATH.exists():
        return []

    try:
        data = json.loads(_HISTORY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Corrupt orders history file; returning empty list")
        return []

    if not isinstance(data, list):
        return []

    return data
