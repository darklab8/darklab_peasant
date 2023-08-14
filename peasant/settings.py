from . import config
from typing import NewType

DiscordWebhookUrl = NewType("DiscordWebhookUrl", str)
TelegramChannelID = NewType("TelegramChannelID", str)
TelegramBotToken = NewType("TelegramBotToken", str)
RedisHostAddress = NewType("RedisHostAddress", str)
ChromeDriverVersion = NewType("ChromeDriverVersion", str)
LogLevel = NewType("LogLevel", str)

cfg = config.Config()

DEBUG = cfg.get_bool("debug", False)
DRIVER_VERSION = ChromeDriverVersion(cfg.get_str("driver_version", "114.0.5735.90"))

REDIS_HOST = RedisHostAddress(cfg.get_str("redis_host", "redis://localhost:6379/0"))

DISCORD_CHANNEL_HEALTH = DiscordWebhookUrl(cfg.get_str("discord_channel_health"))
DISCORD_CHANNEL_NEWS = DiscordWebhookUrl(cfg.get_str("discord_channel_news"))

TELEGRAM_BOT_TOKEN = TelegramBotToken(cfg.get_str("telegram_bot_token"))
TELEGRAM_CHANNEL_HEALTH = TelegramChannelID(cfg.get_str("telegram_channel_health"))
TELEGRAM_CHANNEL_NEWS = TelegramChannelID(cfg.get_str("telegram_channel_news"))

class LogLev:
    """
    Change to Enum later :smile:
    """
    DEBUG = LogLevel("DEBUG")
    INFO = LogLevel("INFO")
    ERROR = LogLevel("ERROR")

LOG_LEVEL = cfg.get_str("log_level", LogLev.DEBUG)