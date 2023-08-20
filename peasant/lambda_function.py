"""
Lambda handler
"""
from .settings import Settings
from .seleniumer import Loginner
from typing import Any

def handler(event: dict[str, Any], context: Any) -> str:
    settings = Settings(**event)

    if settings.test_mode:
        return "Test is made succesfully"

    Loginner(settings=settings).login()

    return 'Lambda is executed succesfully'

# if __name__=="__main__":
#     import pathlib
#     import json
#     with open(str(pathlib.Path(__file__).parent.parent / ".env.json")) as file:
#         data = file.read()
#     print(handler(event=json.loads(data), context = None))

    