import os
from typing import NewType, Optional, Any

EnvVar = NewType("EnvVar", str)

class ConfigException(Exception):
    pass
class Config:
    EnvTrue: EnvVar = EnvVar("true")
    Prefix = "PEASANT_"
    
    def get(self, key: str, default:Optional[Any]=None) -> Optional[str]:
        return os.environ.get(f"{self.Prefix}{key.upper()}",default)
    
    def get_bool(self, key: str, default: Optional[bool]=None) -> Optional[bool]:
        return self.get(key,default) == self.EnvTrue
    
    def get_str(self, key: str, default: str= "") -> str:
        result = self.get(key,default)

        if not isinstance(result, str):
            raise ConfigException()
        
        return result

config = Config()

DEBUG = config.get_bool("debug", False)
DRIVER_VERSION = config.get_str("driver_version", "114.0.5735.90")
