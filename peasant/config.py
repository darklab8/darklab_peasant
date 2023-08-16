import os
from typing import NewType, Optional, Any
import json
import pathlib
from contextlib import suppress
from peasant import exceptions

EnvVar = NewType("EnvVar", str)

project_path = pathlib.Path(__file__).parent.parent
env_path = project_path / ".env.json"


class ConfigException(exceptions.PeasantException):
    pass


class NotFoundValueAndNotDefinedDefault(ConfigException):
    pass


class Config:
    """
    Default must be defined when requesting value. Otherwise if None is found, it will yield ConfigException
    """

    EnvTrue: EnvVar = EnvVar("true")
    Prefix = "PEASANT_"

    def __init__(self) -> None:
        self.file_config: dict[str, str] = {}
        with suppress(FileNotFoundError):
            with open(str(env_path), "r") as file:
                data = file.read()
                self.file_config = json.loads(data)

    def get(self, key: str, default: Optional[Any] = None) -> Optional[str]:
        full_key = f"{self.Prefix}{key.upper()}"

        with suppress(KeyError):
            return self.file_config[full_key]

        if full_key not in os.environ and default is None:
            raise NotFoundValueAndNotDefinedDefault()

        return os.environ.get(full_key, default)

    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        value = self.get(key, default)

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value == self.EnvTrue

        return default

    def get_str(self, key: str, default: Optional[str] = None) -> str:
        result = self.get(key, default)

        if not isinstance(result, str):
            raise ConfigException()

        return result

    def get_int(self, key: str, default: Optional[str] = None) -> int:
        result = self.get(key, default)

        if isinstance(result, int):
            return result

        if not isinstance(result, str):
            raise ConfigException()

        return int(result)
