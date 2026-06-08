"""Structured logging: JSON file output with rotation and Rich console."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.logging import RichHandler

_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOG_FILE = _LOG_DIR / "trading.log"
_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
_BACKUP_COUNT = 5

_STANDARD_RECORD_ATTRS = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
) | {"message"}


class JSONFormatter(logging.Formatter):
    """Emit one JSON object per log line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key not in _STANDARD_RECORD_ATTRS:
                payload[key] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def setup_logging(
    level: int | str = logging.INFO,
    *,
    logger_name: str = "trading_bot",
) -> logging.Logger:
    """Configure root-style logger with JSON file + Rich console handlers."""
    _LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    file_handler = RotatingFileHandler(
        _LOG_FILE,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        rich_tracebacks=True,
        markup=False,
    )
    rich_handler.setFormatter(
        logging.Formatter("%(message)s", datefmt="[%X]")
    )
    logger.addHandler(rich_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a child logger under the trading_bot namespace."""
    if name:
        return logging.getLogger(f"trading_bot.{name}")
    return logging.getLogger("trading_bot")


# Initialize on import so other modules can import get_logger directly.
if not logging.getLogger("trading_bot").handlers:
    setup_logging()
