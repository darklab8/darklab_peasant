import pytest
import pathlib
import json
from .settings import Settings

@pytest.fixture
def settings() -> Settings:
    with open(str(pathlib.Path(__file__).parent.parent / ".env.json")) as file:
        data = file.read()

    settings = Settings(**json.loads(data))
    return settings