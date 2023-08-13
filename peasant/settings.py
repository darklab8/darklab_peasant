import os
from typing import NewType

EnvVar = NewType("EnvVar", str)
class Config:
    EnvTrue: EnvVar = "true"
    Prefix = "PEASANT_"
    
    def get(self, key: str, default=None):
        return os.environ.get(f"{self.Prefix}{key.upper()}",default)
    
    def get_bool(self, key: str, default=None):
        return self.get(key,default) == self.EnvTrue
    
    def get_str(self, key: str, default=None) -> str:
        return self.get(key,default)

config = Config()

DEBUG = config.get_bool("debug", False)
DRIVER_VERSION = config.get_str("driver_version", "114.0.5735.90")