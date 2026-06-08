"""Command-line interface for the trading bot."""

from __future__ import annotations

from typing import Optional

import typer
import uvicorn
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.client import APIError, BinanceClient, NetworkError
from bot.confidence import ConfidenceScorer
from bot.logging_config import get_logger, setup_logging
from bot.orders import OrderManager
from bot.validators import validate_all

app = typer.Typer(help="Trading bot CLI")
logger = get_logger("cli")
console = Console()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
) -> None:
    level = "DEBUG" if verbose else "INFO"
    setup_logging(level)


def _print_validation_errors(exc: ValueError) -> None:
    for line in str(exc).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            rprint(f"[red]{stripped[2:]}[/red]")
        elif stripped:
            rprint(f"[bold red]{stripped}[/bold red]")


def _print_welcome_banner(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> None:
    price_display = str(price) if price is not None else "—"
    body = (
        f"[bold]Symbol:[/bold]   {symbol}\n"
        f"[bold]Side:[/bold]     {side}\n"
        f"[bold]Type:[/bold]     {order_type}\n"
        f"[bold]Quantity:[/bold] {quantity}\n"
        f"[bold]Price:[/bold]    {price_display}"
    )
    console.print(Panel(body, title="[bold cyan]Onion Trader[/bold cyan]", border_style="cyan"))


def _confirm_low_confidence() -> bool:
    rprint(
        "[bold yellow]⚠ Confidence is LOW. Continue? [y/N][/bold yellow]",
        end=" ",
    )
    answer = input().strip().lower()
    return answer in {"y", "yes"}


@app.command("place-order")
def place_order(
    symbol: str = typer.Option(..., "--symbol", help="Trading pair symbol"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", help="Order quantity"),
    price: Optional[float] = typer.Option(None, "--price", help="Limit price (required for LIMIT)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate and preview without submitting"),
) -> None:
    """Place a futures order with confidence scoring."""
    price_arg = str(price) if price is not None else None

    try:
        validated = validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=str(quantity),
            price=price_arg,
        )
    except ValueError as exc:
        _print_validation_errors(exc)
        raise typer.Exit(1) from exc

    _print_welcome_banner(
        symbol=validated["symbol"],
        side=validated["side"],
        order_type=validated["type"],
        quantity=validated["quantity"],
        price=validated["price"],
    )

    client = BinanceClient()
    scorer = ConfidenceScorer(client)
    order_manager = OrderManager(client, scorer)

    try:
        confidence = scorer.score(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            price=validated["price"],
        )

        if confidence["grade"] == "D" and not _confirm_low_confidence():
            rprint("[yellow]Order cancelled.[/yellow]")
            raise typer.Exit(0)

        order_manager.place_order(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"],
            dry_run=dry_run,
            confidence=confidence,
        )
    except (APIError, NetworkError) as exc:
        logger.error("place-order failed", extra={"error": str(exc)})
        rprint("[bold red]❌ Order failed. Check logs/trading.log[/bold red]")
        raise typer.Exit(1) from exc
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("place-order failed")
        rprint("[bold red]❌ Order failed. Check logs/trading.log[/bold red]")
        raise typer.Exit(1) from exc
    finally:
        client.close()

    if not dry_run:
        rprint("[bold green]✅ Order placed successfully![/bold green]")


@app.command("account-info")
def account_info() -> None:
    """Fetch and display futures account balances."""
    client = BinanceClient()

    try:
        account = client.get_account()
    except (APIError, NetworkError) as exc:
        logger.error("account-info failed", extra={"error": str(exc)})
        rprint(f"[bold red]Failed to fetch account: {exc}[/bold red]")
        rprint("[bold red]Check logs/trading.log[/bold red]")
        raise typer.Exit(1) from exc
    finally:
        client.close()

    table = Table(title="Account Balances", show_header=True, header_style="bold green")
    table.add_column("Asset", style="cyan")
    table.add_column("Wallet Balance", justify="right")
    table.add_column("Unrealized PnL", justify="right")

    assets = account.get("assets", [])
    has_rows = False
    for asset in assets:
        wallet_balance = float(asset.get("walletBalance", 0))
        unrealized_profit = float(asset.get("unrealizedProfit", 0))
        if wallet_balance == 0 and unrealized_profit == 0:
            continue
        has_rows = True
        table.add_row(
            str(asset.get("asset", "N/A")),
            str(asset.get("walletBalance", "0")),
            str(asset.get("unrealizedProfit", "0")),
        )

    if not has_rows:
        table.add_row("—", "0", "0")

    console.print(table)


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Bind host"),
    port: int = typer.Option(8000, help="Bind port"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
) -> None:
    """Start the FastAPI server."""
    logger.info("Starting server", extra={"host": host, "port": port})
    uvicorn.run("api.server:app", host=host, port=port, reload=reload)


@app.command()
def status() -> None:
    """Print bot status."""
    rprint("[bold green]Trading bot[/bold green] is ready.")
    logger.info("Status check")


if __name__ == "__main__":
    app()
