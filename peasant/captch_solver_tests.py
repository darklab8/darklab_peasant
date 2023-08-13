import pytest
from .captch_solver import captchaSolver
import pathlib

@pytest.mark.parametrize("img_num,expected", 
    [
        (1, 336174),
        (2, 422401),
        (3, 612100),
        (4, 667604),
        (5, 863981),
        (6, 999357),
        (7, 841558),
        (8, 253930),
        (9, 971693),
        (10, 326454),
        (11, 833485),
        (12, 206296),
    ])
def test_captcha(img_num,expected):
    result = captchaSolver(pathlib.Path("data") / f"CodeImage{img_num}.jpeg").run()
    assert result == str(expected)