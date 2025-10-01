from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


_logger = logging.getLogger(__name__)
_req_logger = logging.getLogger("requests")


TESTNET_FUTURES_URL = "https://testnet.binancefuture.com"  # Per assignment


@dataclass
class OrderResult:
    success: bool
    data: Dict[str, Any] | None
    error: str | None


class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        # Ensure futures testnet base URL
        if testnet:
            # For python-binance, set the API URL for futures
            self.client.FUTURES_URL = TESTNET_FUTURES_URL
        _logger.info("Initialized BasicBot (testnet=%s)", testnet)

    def _place_order(self, params: Dict[str, Any]) -> OrderResult:
        try:
            _req_logger.info("REQUEST create_order | %s", params)
            resp = self.client.futures_create_order(**params)
            _req_logger.info("RESPONSE create_order | %s", resp)
            return OrderResult(success=True, data=resp, error=None)
        except (BinanceAPIException, BinanceRequestException) as e:
            _logger.error("Binance error: %s", e, exc_info=True)
            return OrderResult(success=False, data=None, error=str(e))
        except Exception as e:  # noqa: BLE001
            _logger.exception("Unexpected error placing order")
            return OrderResult(success=False, data=None, error=str(e))

    def place_market_order(self, symbol: str, side: str, quantity: float) -> OrderResult:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": quantity,
        }
        return self._place_order(params)

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC"
    ) -> OrderResult:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "LIMIT",
            "timeInForce": time_in_force,
            "quantity": quantity,
            "price": price,
        }
        return self._place_order(params)

    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        stop_price: float,
        time_in_force: str = "GTC",
    ) -> OrderResult:
        # Binance Futures uses STOP or STOP_MARKET; stop-limit is STOP with price + stopPrice
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "STOP",
            "timeInForce": time_in_force,
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            # Optional: workingType
        }
        return self._place_order(params)


