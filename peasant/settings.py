from . import config

cfg = config.Config()

DEBUG = cfg.get_bool("debug", False)
DRIVER_VERSION = cfg.get_str("driver_version", "114.0.5735.90")
