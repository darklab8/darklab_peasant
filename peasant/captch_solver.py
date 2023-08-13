# -*- coding: utf-8 -*-
"""
Created on 11/03/2021
Last edit on 11/03/2021
version 3

@author: T.Vic
note:	
This version can bypass the captcha by utilising cv2 filters, BFS and pytesseract OCR. The script will attempt to make a number of attempts to inference the captcha and log in with the provided username and password. The number of try depends on your luck, the average number of try I got is usually around 10. 

Chrome driver will be automatically downloaded

For SUTD account username and password, you can either hardcode inside the script or parse it as arguments to the script. Please ensure they are correct!

Telegram me @Vhektor if you have any question regards to the script!

"""

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

import argparse
import os
import time
import datetime
import cv2
import sys
import os
import numpy as np
import pytesseract
from PIL import Image
from matplotlib import cm
import pathlib

class RecognitionError(Exception):
    pass

class captchaSolver:
    def __init__(self, captcha_filepath):
        self.project_path: pathlib.Path = pathlib.Path(__file__).parent.parent
        self.captcha_filepath = captcha_filepath
            
    def run(self):
        captcha_abs_path = str(self.project_path / self.captcha_filepath)
        img = cv2.imread(captcha_abs_path)

        captcha_result = self.bypassCaptcha(img)

        allowed_symbols = "0123456789"

        result_array = []

        for character in captcha_result:
            if character not in allowed_symbols:
                continue

            result_array.append(character)

        if len(result_array) != 6:
            raise RecognitionError("Expected to see 6 digits in result")

        return "".join(result_array)

    def bypassCaptcha(self, img):
        out = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        out = cv2.medianBlur(out,3)

        filter_threshold = 230
        a = np.where(out>filter_threshold, 1, out)
        out = np.where(a!=1, 0, a)

        out = self.removeIsland(out, 5)

        out = cv2.medianBlur(out,5)

        im = Image.fromarray(out*255)
        im.save(str(self.project_path / "processed.jpeg"))

        out_captcha = pytesseract.image_to_string(im)
        print(out_captcha)
        return out_captcha

    def bfs(self, visited, queue, array, node):
        # I make BFS itterative instead of recursive to accomodate my WINDOWS friends >:]
        def getNeighboor(array, node):
            neighboors = []
            if node[0]+1<array.shape[0]:
                if array[node[0]+1,node[1]] == 0:
                    neighboors.append((node[0]+1,node[1]))
            if node[0]-1>0:
                if array[node[0]-1,node[1]] == 0:
                    neighboors.append((node[0]-1,node[1]))
            if node[1]+1<array.shape[1]:
                if array[node[0],node[1]+1] == 0:
                    neighboors.append((node[0],node[1]+1))
            if node[0]-1>0:
                if array[node[0],node[1]-1] == 0:
                    neighboors.append((node[0],node[1]-1))
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
            
    def removeIsland(self, img_arr, threshold):
        while 0 in img_arr:
            x,y = np.where(img_arr == 0)
            point = (x[0],y[0])

            visited = set()
            queue = []

            self.bfs(visited, queue, img_arr, point)

            if len(visited) <= threshold:
                for i in visited:
                    img_arr[i[0],i[1]] = 1
            else:
                for i in visited:
                    img_arr[i[0],i[1]] = 2

        img_arr = np.where(img_arr==2, 0, img_arr)
        return img_arr
        
    
if __name__ == "__main__":
    captchaSolver(pathlib.Path("data") / "CodeImage5.jpeg").run()