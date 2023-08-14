from . import config

cfg = config.Config()

DEBUG = cfg.get_bool("debug", False)
DRIVER_VERSION = cfg.get_str("driver_version", "114.0.5735.90")

REDIS_HOST = cfg.get_str("redis_host", 'redis://localhost:6379/0')