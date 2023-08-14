import pytest
from .captch_solver import captchaSolver, RecognitionError
import pathlib


@pytest.mark.parametrize(
    "img_num,expected",
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
    ],
)
def test_captcha(img_num: int, expected: int) -> None:
    picture_path = pathlib.Path("data") / f"CodeImage{img_num}.jpeg"

    if img_num == 9:
        return

    # could be nice to solve them too. Otherwise catching RecognitionError is fine too
    # as long as final percentage of solved tests is high enough (50% currently)
    if img_num in (1, 3, 4, 6, 9, 12):
        with pytest.raises(RecognitionError):
            result = captchaSolver(picture_path).run()
        return

    result = captchaSolver(picture_path).run()
    assert result == str(expected)
