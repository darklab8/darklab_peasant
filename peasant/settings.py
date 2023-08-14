from . import config

cfg = config.Config()

DEBUG = cfg.get_bool("debug", False)
DRIVER_VERSION = cfg.get_str("driver_version", "114.0.5735.90")

REDIS_HOST = cfg.get_str("redis_host", "redis://localhost:6379/0")

DISCORD_WEB_HOOK_HEALTH = cfg.get_str("discord_web_hook_health")
DISCORD_WEB_HOOK_IMPORTANT = cfg.get_str("discord_web_hook_health")

PEASANT_TELEGRAM_TOKEN = cfg.get_str("telegram_token")
