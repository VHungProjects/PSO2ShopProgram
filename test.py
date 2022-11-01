import cv2
import pytesseract as py
import pyautogui as h
import time
from PIL import Image
py.pytesseract.tesseract_cmd = r'D:\Queens Univeristy\CISC121\Code\ShopProgram\Tesseract\tesseract.exe'
h.FAILSAFE = True

x = 1
while x == 1:
        time.sleep(2)
        print(h.position())