import logging
import logging.handlers
from pathlib import Path
import os


def setup_logging(log_level: str | int = "INFO") -> None:
    """Configure application loggers and file handlers.

    Creates rotating file handlers:
      - logs/bot.log for general bot activity
      - logs/requests.log for API request/response payloads
    """

    level = logging.getLevelName(log_level) if isinstance(log_level, str) else log_level

    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid duplicate handlers on re-init
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # bot.log handler
    bot_file = logs_dir / "bot.log"
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) and getattr(h, "baseFilename", "").endswith(str(bot_file)) for h in root_logger.handlers):
        bot_handler = logging.handlers.RotatingFileHandler(
            bot_file, maxBytes=2_000_000, backupCount=5, encoding="utf-8"
        )
        bot_handler.setFormatter(formatter)
        root_logger.addHandler(bot_handler)

    # requests logger dedicated file
    requests_logger = logging.getLogger("requests")
    requests_logger.setLevel(level)
    requests_file = logs_dir / "requests.log"
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) and getattr(h, "baseFilename", "").endswith(str(requests_file)) for h in requests_logger.handlers):
        req_handler = logging.handlers.RotatingFileHandler(
            requests_file, maxBytes=2_000_000, backupCount=5, encoding="utf-8"
        )
        req_handler.setFormatter(formatter)
        requests_logger.addHandler(req_handler)


def get_log_level_from_env(default: str = "INFO") -> str:
    return os.getenv("BOT_LOG_LEVEL", default)


