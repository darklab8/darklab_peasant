from . import config, types

cfg = config.Config()

DEBUG = cfg.get_bool("debug", False)
DRIVER_VERSION = types.ChromeDriverVersion(
    cfg.get_str("driver_version", "114.0.5735.90")
)

REDIS_HOST = types.RedisHostAddress(
    cfg.get_str("redis_host", "redis://localhost:6379/0")
)

DISCORD_CHANNEL_HEALTH = types.DiscordWebhookUrl(cfg.get_str("discord_channel_health"))
DISCORD_CHANNEL_NEWS = types.DiscordWebhookUrl(cfg.get_str("discord_channel_news"))

TELEGRAM_BOT_TOKEN = types.TelegramBotToken(cfg.get_str("telegram_bot_token"))
TELEGRAM_CHANNEL_HEALTH = types.TelegramChannelID(
    cfg.get_str("telegram_channel_health")
)
TELEGRAM_CHANNEL_NEWS = types.TelegramChannelID(cfg.get_str("telegram_channel_news"))


class LogLev:
    """
    Change to Enum later :smile:
    """

    DEBUG = types.LogLevel("DEBUG")
    INFO = types.LogLevel("INFO")
    ERROR = types.LogLevel("ERROR")
    PANIC = types.LogLevel("PANIC")


LOG_LEVEL = cfg.get_str("log_level", LogLev.DEBUG)

SELENIUM_REG_LINK = types.GovRegistryLink(
    types.SeleniumLink(cfg.get_str("selenium_reg_link"))
)
SELENIUM_AWAIT_TIME = types.Seconds(cfg.get_int("selenium_await_time", "30"))