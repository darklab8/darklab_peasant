import cv2
import numpy as np
import pytesseract  # type: ignore
from PIL import Image
import pathlib
import cv2.typing
from typing import TYPE_CHECKING, Any
from .notificator import logger
from peasant import exceptions

if TYPE_CHECKING:
    from _typeshed import Incomplete
else:
    Incomplete = Any


class RecognitionError(exceptions.PeasantException):
    pass


class RecognitionNotStrError(RecognitionError):
    pass


class captchaSolver:
    def __init__(self, captcha_filepath: pathlib.Path):
        self.project_path: pathlib.Path = pathlib.Path(__file__).parent.parent
        self.captcha_filepath = captcha_filepath

    def run(self) -> str:
        captcha_abs_path = str(self.project_path / self.captcha_filepath)
        img: np.ndarray = cv2.imread(captcha_abs_path)

        captcha_result = self.bypassCaptcha(img)

        allowed_symbols = "0123456789"

        result_array = []

        for character in captcha_result:
            if character not in allowed_symbols:
                continue

            result_array.append(character)

        if len(result_array) != 6:
            logger.panic(
                f"Expected to see 6 digits in result. {result_array=}", error_cls=RecognitionError
            )

        return "".join(result_array)

    def bypassCaptcha(self, img: np.ndarray) -> str:
        out = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        out = cv2.medianBlur(out, 3)

        filter_threshold = 230
        a = np.where(out > filter_threshold, 1, out)
        out = np.where(a != 1, 0, a)

        out = self.removeIsland(out, 5)

        out = cv2.medianBlur(out, 5)

        im = Image.fromarray(out * 255)
        im.save(str(self.project_path / "processed.jpeg"))

        out_captcha = pytesseract.image_to_string(im)

        if not isinstance(out_captcha, str):
            logger.panic(
                "captchaSolver: RecognitionNotStrError",
                error_cls=RecognitionNotStrError,
            )
            raise RecognitionNotStrError()

        print(out_captcha)
        return out_captcha

    def bfs(
        self,
        visited: Incomplete,
        queue: Incomplete,
        array: Incomplete,
        node: Incomplete,
    ) -> Incomplete:
        """
        Code from https://medium.com/geekculture/bypassing-captcha-with-breadth-first-search-opencv-and-tesseract-8ea374ee1754
        https://github.com/victorpham1997/Automatic-health-declaration-for-SUTD/tree/master
        """

        # I make BFS itterative instead of recursive to accomodate my WINDOWS friends >:]
        def getNeighboor(array: Incomplete, node: Incomplete) -> Incomplete:
            neighboors = []
            if node[0] + 1 < array.shape[0]:
                if array[node[0] + 1, node[1]] == 0:
                    neighboors.append((node[0] + 1, node[1]))
            if node[0] - 1 > 0:
                if array[node[0] - 1, node[1]] == 0:
                    neighboors.append((node[0] - 1, node[1]))
            if node[1] + 1 < array.shape[1]:
                if array[node[0], node[1] + 1] == 0:
                    neighboors.append((node[0], node[1] + 1))
            if node[0] - 1 > 0:
                if array[node[0], node[1] - 1] == 0:
                    neighboors.append((node[0], node[1] - 1))
            return neighboors

        queue.append(node)
        visited.add(node)

        while queue:
            current_node = queue.pop(0)
            for neighboor in getNeighboor(array, current_node):
                if neighboor not in visited:
                    #             print(neighboor)
                    visited.add(neighboor)
                    queue.append(neighboor)

    def removeIsland(self, img_arr: Incomplete, threshold: int) -> Incomplete:
        """
        Code from https://medium.com/geekculture/bypassing-captcha-with-breadth-first-search-opencv-and-tesseract-8ea374ee1754
        https://github.com/victorpham1997/Automatic-health-declaration-for-SUTD/tree/master
        """
        while 0 in img_arr:
            x, y = np.where(img_arr == 0)
            point = (x[0], y[0])

            visited: Incomplete = set()
            queue: Incomplete = []

            self.bfs(visited, queue, img_arr, point)

            if len(visited) <= threshold:
                for i in visited:
                    img_arr[i[0], i[1]] = 1
            else:
                for i in visited:
                    img_arr[i[0], i[1]] = 2

        img_arr = np.where(img_arr == 2, 0, img_arr)
        return img_arr


if __name__ == "__main__":
    captchaSolver(pathlib.Path("data") / "CodeImage5.jpeg").run()
