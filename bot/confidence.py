"""Market-condition confidence scoring."""

from __future__ import annotations

from typing import Any

from bot.client import APIError, BinanceClient, NetworkError
from bot.logging_config import get_logger

logger = get_logger("confidence")

_FALLBACK_SCORE = 50
_VOLATILITY_WEIGHT = 0.30
_DEPTH_WEIGHT = 0.40
_PRICE_PROXIMITY_WEIGHT = 0.30

_GRADE_THRESHOLDS: tuple[tuple[int, str, str], ...] = (
    (80, "A", "Excellent conditions to place order"),
    (60, "B", "Good conditions to place order"),
    (40, "C", "Proceed with caution"),
    (0, "D", "High risk — consider waiting"),
)


class ConfidenceScorer:
    """Score order placement confidence using live market data."""

    def __init__(self, client: BinanceClient) -> None:
        self._client = client

    def score(
        self,
        symbol: str,
        side: str,
        order_type: str,
        price: float | None = None,
    ) -> dict[str, Any]:
        """Return weighted confidence score and breakdown for an order."""
        symbol = symbol.strip().upper()
        side = side.strip().upper()
        order_type = order_type.strip().upper()

        breakdown = {
            "volatility": self._run_sub_score(
                "volatility",
                lambda: self.volatility_score(symbol),
            ),
            "depth": self._run_sub_score(
                "depth",
                lambda: self.depth_score(symbol, side),
            ),
            "price_proximity": self._run_sub_score(
                "price_proximity",
                lambda: self.price_proximity_score(symbol, order_type, price),
            ),
        }

        total_score = round(
            breakdown["volatility"] * _VOLATILITY_WEIGHT
            + breakdown["depth"] * _DEPTH_WEIGHT
            + breakdown["price_proximity"] * _PRICE_PROXIMITY_WEIGHT
        )
        grade, recommendation = self._grade(total_score)

        return {
            "total_score": total_score,
            "grade": grade,
            "recommendation": recommendation,
            "breakdown": breakdown,
        }

    def volatility_score(self, symbol: str) -> int:
        """Score 0–100 from recent 1-minute candle volatility."""
        klines = self._client.get_klines(symbol, interval="1m", limit=10)
        ranges: list[float] = []

        for candle in klines:
            high = float(candle[2])
            low = float(candle[3])
            close = float(candle[4])
            if close <= 0:
                continue
            ranges.append((high - low) / close * 100)

        if not ranges:
            raise ValueError(f"No usable kline data for {symbol}")

        avg_range = sum(ranges) / len(ranges)

        if avg_range < 0.1:
            return 90
        if avg_range < 0.3:
            return 70
        if avg_range < 0.7:
            return 50
        return 25

    def depth_score(self, symbol: str, side: str) -> int:
        """Score 0–100 from order-book bid/ask volume imbalance."""
        book = self._client.get_order_book(symbol, limit=20)
        bid_volume = sum(float(level[1]) for level in book.get("bids", []))
        ask_volume = sum(float(level[1]) for level in book.get("asks", []))
        total_volume = bid_volume + ask_volume

        if total_volume <= 0:
            raise ValueError(f"Empty order book for {symbol}")

        if side == "BUY":
            raw_score = int((bid_volume / total_volume) * 200)
        elif side == "SELL":
            raw_score = int((ask_volume / total_volume) * 200)
        else:
            raise ValueError(f"side must be BUY or SELL, got {side!r}")

        return max(0, min(100, raw_score))

    def price_proximity_score(
        self,
        symbol: str,
        order_type: str,
        price: float | None,
    ) -> int:
        """Score 0–100 from limit price proximity to mid; neutral for market orders."""
        if order_type == "MARKET":
            return 80

        if order_type != "LIMIT":
            raise ValueError(f"order_type must be MARKET or LIMIT, got {order_type!r}")

        if price is None or price <= 0:
            raise ValueError("price is required for LIMIT orders")

        book = self._client.get_order_book(symbol, limit=20)
        bids = book.get("bids", [])
        asks = book.get("asks", [])
        if not bids or not asks:
            raise ValueError(f"Insufficient order book depth for {symbol}")

        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])
        mid = (best_bid + best_ask) / 2
        if mid <= 0:
            raise ValueError(f"Invalid mid price for {symbol}")

        deviation = abs(price - mid) / mid * 100

        if deviation < 0.5:
            return 95
        if deviation < 2:
            return 75
        if deviation < 5:
            return 50
        return 20

    def _run_sub_score(self, name: str, scorer: Any) -> int:
        try:
            return scorer()
        except (APIError, NetworkError, ValueError, TypeError, KeyError, IndexError) as exc:
            logger.warning(
                "%s sub-score failed, using fallback score=%s: %s",
                name,
                _FALLBACK_SCORE,
                exc,
                extra={"sub_score": name, "error": str(exc)},
            )
            return _FALLBACK_SCORE

    @staticmethod
    def _grade(total_score: int) -> tuple[str, str]:
        for threshold, grade, recommendation in _GRADE_THRESHOLDS:
            if total_score >= threshold:
                return grade, recommendation
        return "D", _GRADE_THRESHOLDS[-1][2]
