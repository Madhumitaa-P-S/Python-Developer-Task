from __future__ import annotations

import argparse
import logging
import sys

from .bot import BasicBot
from .config import load_settings
from .logger import setup_logging, get_log_level_from_env


def positive_float(value: str) -> float:
    try:
        f = float(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("Must be a number") from e
    if f <= 0:
        raise argparse.ArgumentTypeError("Must be > 0")
    return f


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side")
    parser.add_argument(
        "--type",
        required=True,
        choices=["market", "limit", "stop_limit"],
        help="Order type",
    )
    parser.add_argument("--quantity", required=True, type=positive_float, help="Order quantity")
    parser.add_argument("--price", type=positive_float, help="Limit or stop-limit price")
    parser.add_argument("--stop-price", dest="stop_price", type=positive_float, help="Stop price for stop-limit")
    parser.add_argument("--time-in-force", dest="tif", default="GTC", choices=["GTC", "IOC", "FOK"], help="Time in force")

    parser.add_argument("--api-key", dest="api_key", help="API key (overrides env)")
    parser.add_argument("--api-secret", dest="api_secret", help="API secret (overrides env)")
    parser.add_argument("--testnet", dest="testnet", default="true", choices=["true", "false"], help="Use testnet (default true)")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    setup_logging(get_log_level_from_env())
    logger = logging.getLogger("cli")

    try:
        settings = load_settings(
            api_key=args.api_key,
            api_secret=args.api_secret,
            testnet=args.testnet.lower() == "true",
        )
    except Exception as e:  # noqa: BLE001
        logger.error("Config error: %s", e)
        return 2

    bot = BasicBot(settings.api_key, settings.api_secret, testnet=settings.testnet)

    order_type = args.type.lower()
    side = args.side.upper()
    symbol = args.symbol.upper()

    logger.info("Placing %s %s %s", order_type, side, symbol)

    if order_type == "market":
        result = bot.place_market_order(symbol=symbol, side=side, quantity=args.quantity)
    elif order_type == "limit":
        if args.price is None:
            logger.error("--price is required for limit orders")
            return 2
        result = bot.place_limit_order(
            symbol=symbol, side=side, quantity=args.quantity, price=args.price, time_in_force=args.tif
        )
    elif order_type == "stop_limit":
        if args.price is None or args.stop_price is None:
            logger.error("--price and --stop-price are required for stop_limit orders")
            return 2
        result = bot.place_stop_limit_order(
            symbol=symbol,
            side=side,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
            time_in_force=args.tif,
        )
    else:
        logger.error("Unsupported order type: %s", order_type)
        return 2

    if result.success:
        logger.info("Order placed successfully: %s", result.data)
        print("success", result.data)
        return 0
    else:
        logger.error("Order failed: %s", result.error)
        print("error", result.error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


