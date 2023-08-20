from .seleniumer import Loginner
import pytest
import os
from . import types
from .settings import Settings


def test_opening_example(settings: Settings) -> None:
    with Loginner(settings=settings).open_browser() as driver: # type: ignore[call-arg]
        driver.get(types.SeleniumLink("https://example.com/"))
        assert "Example Domain" in driver.title

        elem = driver.find_element("a")

        elem.click()

        body = driver.find_element("body")

        assert "As described in RFC 2606" in body.text


# never run with all tests :scream:
@pytest.mark.skipif(
    condition=os.environ.get("PYTEST_ALLOW_VISUAL_DEBUG_ONLY") != "true",
    reason="You get banned if u ran this more than 24 times per day",
)
@pytest.mark.allow_visual_debug_only
def test_check_queue(settings: Settings) -> None:
    Loginner(settings=settings).login()  # type: ignore[call-arg]
