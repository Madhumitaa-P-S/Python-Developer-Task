from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class Settings:
    api_key: str
    api_secret: str
    testnet: bool = True
    request_timeout: int = 10


def load_settings(
    api_key: str | None = None,
    api_secret: str | None = None,
    testnet: bool | None = None,
) -> Settings:
    load_dotenv(override=False)

    resolved_api_key = api_key or os.getenv("BINANCE_API_KEY", "")
    resolved_api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
    resolved_testnet = (
        testnet if testnet is not None else os.getenv("BINANCE_TESTNET", "true").lower() == "true"
    )

    if not resolved_api_key or not resolved_api_secret:
        raise ValueError("API key/secret are required. Set BINANCE_API_KEY and BINANCE_API_SECRET or pass via CLI.")

    return Settings(
        api_key=resolved_api_key,
        api_secret=resolved_api_secret,
        testnet=resolved_testnet,
    )


