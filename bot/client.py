"""Binance Futures API client."""

from __future__ import annotations

import hashlib
import hmac
import os
import time
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

from bot.logging_config import get_logger

load_dotenv()

logger = get_logger("client")

DEFAULT_BASE_URL = "https://testnet.binancefuture.com"


class APIError(Exception):
    """Raised when the Binance API returns a non-200 response."""

    def __init__(self, message: str, status_code: int, response_body: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class NetworkError(Exception):
    """Raised when an HTTP request fails due to a network-level error."""

    def __init__(self, message: str, cause: RequestException | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class BinanceClient:
    """HTTP client for Binance Futures testnet/mainnet."""

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.secret_key = secret_key or os.getenv("BINANCE_SECRET_KEY", "")
        self.base_url = (
            base_url or os.getenv("BASE_URL", DEFAULT_BASE_URL)
        ).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Add timestamp and HMAC SHA256 signature to request parameters."""
        signed = dict(params or {})
        signed["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(signed)
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed["signature"] = signature
        return signed

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        signed: bool = False,
    ) -> Any:
        request_params = self._sign(params) if signed else (params or {})
        url = f"{self.base_url}{path}"

        logger.info(
            "Request %s %s",
            method,
            url,
            extra={"method": method, "url": url, "params": request_params},
        )

        try:
            response = self._session.request(
                method,
                url,
                params=request_params,
                timeout=self.timeout,
            )
        except RequestException as exc:
            logger.error("Network error for %s %s: %s", method, url, exc)
            raise NetworkError(f"Network error during {method} {path}: {exc}", cause=exc) from exc

        logger.info(
            "Response %s %s",
            response.status_code,
            url,
            extra={
                "method": method,
                "url": url,
                "status_code": response.status_code,
            },
        )

        if response.status_code != 200:
            body = response.text
            raise APIError(
                f"Binance API error: {method} {path} returned {response.status_code}",
                response.status_code,
                body,
            )

        return response.json()

    def get_server_time(self) -> dict[str, Any]:
        """GET /fapi/v1/time"""
        return self._request("GET", "/fapi/v1/time")

    def get_exchange_info(self, symbol: str) -> dict[str, Any]:
        """GET /fapi/v1/exchangeInfo"""
        return self._request("GET", "/fapi/v1/exchangeInfo", {"symbol": symbol})

    def get_order_book(self, symbol: str, limit: int = 20) -> dict[str, Any]:
        """GET /fapi/v1/depth"""
        return self._request(
            "GET",
            "/fapi/v1/depth",
            {"symbol": symbol, "limit": limit},
        )

    def get_klines(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 10,
    ) -> list[Any]:
        """GET /fapi/v1/klines"""
        return self._request(
            "GET",
            "/fapi/v1/klines",
            {"symbol": symbol, "interval": interval, "limit": limit},
        )

    def place_order(self, **params: Any) -> dict[str, Any]:
        """POST /fapi/v1/order (signed)"""
        return self._request("POST", "/fapi/v1/order", params, signed=True)

    def get_account(self) -> dict[str, Any]:
        """GET /fapi/v2/account (signed)"""
        return self._request("GET", "/fapi/v2/account", signed=True)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> BinanceClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
