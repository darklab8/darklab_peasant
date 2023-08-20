import pathlib
from peasant import exceptions
import requests
import time
import base64
from peasant.settings import Settings
from .notificator.aggregator import iNotificator, NotificatorAggregator

# import cv2
# import numpy as np
# import pytesseract  # type: ignore
# from PIL import Image
# import cv2.typing
# from typing import TYPE_CHECKING, Any


# if TYPE_CHECKING:
#     from _typeshed import Incomplete
# else:
#     Incomplete = Any


class RecognitionError(exceptions.PeasantException):
    pass


class RecognitionNotStrError(RecognitionError):
    pass


# def sum_of_squares(point: list[float]) -> float:
#     return point[0]*point[0] + point[1]*point[1]


class captchaSolver:
    def __init__(self, captcha_filepath: pathlib.Path, settings: Settings):
        self.settings = settings
        self.project_path: pathlib.Path = pathlib.Path(__file__).parent.parent
        self.captcha_filepath = captcha_filepath
        self.logger: iNotificator = NotificatorAggregator(settings=settings)

    def run(self) -> str:
        captcha_abs_path = str(self.project_path / self.captcha_filepath)
        with open(captcha_abs_path, "rb") as f:
            encoded_image = base64.b64encode(f.read())

        resp = requests.post(
            url="http://2captcha.com/in.php",
            json=dict(
                key=self.settings.twocaptcha_api_key,
                body=encoded_image.decode("utf8"),
                method="base64",
                min_len=6,
                max_len=6,
                numeric=1,
            ),
        )
        if not "OK" in resp.text:
            panic_msg = f"Post request is not having ok. {resp.text=}"
            self.logger.panic(panic_msg)
            raise RecognitionError(panic_msg)

        request_id = resp.text.split("|")[1]
        for i in range(15):
            resp2 = requests.get(
                f"http://2captcha.com/res.php",
                params=dict(
                    key=self.settings.twocaptcha_api_key,
                    action="get",
                    id=request_id,
                ),
            )

            if not "OK" in resp2.text:
                time.sleep(2)
                continue

            break
        else:  
            panic_msg = "Captcha is not solved"
            self.logger.panic(panic_msg)
            raise RecognitionError(panic_msg)

        captcha_result = resp2.text.split("|")[1]
        return captcha_result

    # def run_broken_tesseract(self) -> str:
    #     captcha_abs_path = str(self.project_path / self.captcha_filepath)

    #     captcha_result = self.bypassCaptcha(captcha_abs_path)

    #     allowed_symbols = "0123456789"

    #     result_array: list[str] = []

    #     for character in captcha_result:
    #         if character not in allowed_symbols:
    #             continue

    #         result_array.append(character)

    #         if len(result_array) == 6:
    #             break

    #     if len(result_array) != 6:
    #         logger.panic(
    #             f"Expected to see 6 digits in result. {result_array=}", error_cls=RecognitionError
    #         )

    #     return "".join(result_array)

    # def bypassCaptcha(self, captcha_abs_path: str) -> str:
    #     img: np.ndarray = cv2.imread(captcha_abs_path)
    #     out = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #     out = cv2.medianBlur(out, 5)
    #     filter_threshold = 220
    #     a = np.where(out > filter_threshold, 1, out)
    #     out = np.where(a != 1, 0, a)
    #     out = self.removeIsland(out, 5)
    #     out = cv2.medianBlur(out, 5)

    #     # invert
    #     # a = np.where(out > filter_threshold, 255, out)
    #     # im = Image.fromarray(out * 255)
    #     # Defining the end points of the image
    #     # out = cv2.absdiff(out,1)

    #     # Finding corners
    #     # corners = cv2.goodFeaturesToTrack(out, 27, 0.01, 10)
    #     # left_top_corner = np.array([200,50])
    #     # left_bottom_corner = np.array([200,0])
    #     # right_top_corner = np.array([0,50])
    #     # right_bottom_corner = np.array([0,0])
    #     # for corner in corners:
    #     #     for pair in corner:
    #     #         if sum_of_squares(pair - [0,0]) < sum_of_squares(left_top_corner - [0,0]):
    #     #             left_top_corner = pair
    #     #         if sum_of_squares(pair - [0,50]) < sum_of_squares(left_bottom_corner - [0,50]):
    #     #             left_bottom_corner = pair
    #     #         if sum_of_squares(pair - [200,0]) < sum_of_squares(right_top_corner - [200,0]):
    #     #             right_top_corner = pair
    #     #         if sum_of_squares(pair - [200,50]) < sum_of_squares(right_bottom_corner - [200,50]):
    #     #             right_bottom_corner = pair

    #     # Perceptive transform
    #     # pts1 = np.float32([[22,11],[22,33],[142,6],[163,37]]) # type: ignore
    #     # pts1 = np.float32([left_top_corner,left_bottom_corner,right_top_corner,right_bottom_corner]) # type: ignore
    #     # pts2 = np.float32([[22,11],[22,33],[160,11],[160,33]]) # type: ignore
    #     # M = cv2.getPerspectiveTransform(pts1,pts2)
    #     # dst = cv2.warpPerspective(out,M,(200,50))
    #     # out2 = dst.copy()
    #     # out = np.where(out > filter_threshold, 1, out)
    #     # out = cv2.absdiff(out,1)

    #     im = Image.fromarray(out * 255)
    #     im.save(str(self.project_path / "processed.jpeg"))
    #     out_captcha = pytesseract.image_to_string(im)

    #     if not isinstance(out_captcha, str):
    #         logger.panic(
    #             "captchaSolver: RecognitionNotStrError",
    #             error_cls=RecognitionNotStrError,
    #         )
    #         raise RecognitionNotStrError()

    #     print(out_captcha)
    #     return out_captcha

    # def bfs(
    #     self,
    #     visited: Incomplete,
    #     queue: Incomplete,
    #     array: Incomplete,
    #     node: Incomplete,
    # ) -> Incomplete:
    #     """
    #     Code from https://medium.com/geekculture/bypassing-captcha-with-breadth-first-search-opencv-and-tesseract-8ea374ee1754
    #     https://github.com/victorpham1997/Automatic-health-declaration-for-SUTD/tree/master
    #     """

    #     # I make BFS itterative instead of recursive to accomodate my WINDOWS friends >:]
    #     def getNeighboor(array: Incomplete, node: Incomplete) -> Incomplete:
    #         neighboors = []
    #         if node[0] + 1 < array.shape[0]:
    #             if array[node[0] + 1, node[1]] == 0:
    #                 neighboors.append((node[0] + 1, node[1]))
    #         if node[0] - 1 > 0:
    #             if array[node[0] - 1, node[1]] == 0:
    #                 neighboors.append((node[0] - 1, node[1]))
    #         if node[1] + 1 < array.shape[1]:
    #             if array[node[0], node[1] + 1] == 0:
    #                 neighboors.append((node[0], node[1] + 1))
    #         if node[0] - 1 > 0:
    #             if array[node[0], node[1] - 1] == 0:
    #                 neighboors.append((node[0], node[1] - 1))
    #         return neighboors

    #     queue.append(node)
    #     visited.add(node)

    #     while queue:
    #         current_node = queue.pop(0)
    #         for neighboor in getNeighboor(array, current_node):
    #             if neighboor not in visited:
    #                 #             print(neighboor)
    #                 visited.add(neighboor)
    #                 queue.append(neighboor)

    # def removeIsland(self, img_arr: Incomplete, threshold: int) -> Incomplete:
    #     """
    #     Code from https://medium.com/geekculture/bypassing-captcha-with-breadth-first-search-opencv-and-tesseract-8ea374ee1754
    #     https://github.com/victorpham1997/Automatic-health-declaration-for-SUTD/tree/master
    #     """
    #     while 0 in img_arr:
    #         x, y = np.where(img_arr == 0)
    #         point = (x[0], y[0])

    #         visited: Incomplete = set()
    #         queue: Incomplete = []

    #         self.bfs(visited, queue, img_arr, point)

    #         if len(visited) <= threshold:
    #             for i in visited:
    #                 img_arr[i[0], i[1]] = 1
    #         else:
    #             for i in visited:
    #                 img_arr[i[0], i[1]] = 2

    #     img_arr = np.where(img_arr == 2, 0, img_arr)
    #     return img_arr
