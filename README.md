## Simplified Binance Futures Testnet Trading Bot

This project provides a reusable Python CLI bot to place Market, Limit, and Stop-Limit orders on Binance USDT-M Futures Testnet.

### Features
- Place Market and Limit orders (BUY/SELL)
- Optional Stop-Limit orders
- Uses Binance Futures Testnet (`https://testnet.binancefuture.com`)
- Structured `BasicBot` class with clear I/O and error handling
- CLI with input validation
- Detailed logging of requests, responses, and errors to `logs/`

### Quick Start
1. Create a Testnet account and API keys for Binance Futures Testnet.
2. Clone/download this repo to your machine.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Configure environment variables:
   - Copy `.env.example` to `.env` and fill in your keys.

### Usage
Place a market order:
```bash
python -m src.cli --symbol BTCUSDT --side BUY --type market --quantity 0.001
```

Place a limit order:
```bash
python -m src.cli --symbol BTCUSDT --side SELL --type limit --quantity 0.001 --price 65000
```

Place a stop-limit order (optional feature):
```bash
python -m src.cli --symbol BTCUSDT --side SELL --type stop_limit --quantity 0.001 --price 64500 --stop-price 64750
```

Common options:
- `--testnet true|false` (default: true)
- `--time-in-force GTC|IOC|FOK` (default: GTC)

### Logs
Logs are written to `logs/`:
- `bot.log` – high-level bot activity and errors
- `requests.log` – request parameters and API responses

Include these logs with your submission email.

### Config
Set API credentials via `.env` or CLI flags.
Priority: CLI flags > environment variables.

Environment variables supported:
- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`
- `BOT_LOG_LEVEL` (optional, default INFO)

### Notes
- This bot targets USDT-M Futures Testnet. It does not place Spot orders.
- Ensure your symbol (e.g., `BTCUSDT`) is available on the Testnet and you have sufficient testnet balance.

### Submission
Email your resume, repository link, and the generated `logs/` files to the addresses in the assignment brief with the subject:
"Junior Python Developer – Crypto Trading Bot"


