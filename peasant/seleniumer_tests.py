from .seleniumer import Loginner, open_browser
from . import loggus as logging

def test_opening_example():
    with open_browser(debug=True, url="https://example.com/") as driver:
        logging.info("opened browser")

    # loginner = Loginner(debug=True, url="")
    # loginner.login()
    