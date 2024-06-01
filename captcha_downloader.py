import time
import requests

import io
import numpy as np

import cv2

BASE_URL = "http://hatinh.edu.vn/"
PAGE = "tracuudiemthihsg"
ITEM_ID = '65fd00992bf36065700fbe74'
CAPTCHA_URL = "http://hatinh.edu.vn/api/Common/Captcha/getCaptcha?returnType=image&site=32982&width=300&height=100&t="; 

FIXED_PARAMS = [
  ('module', 'Content.Listing'),
  ('moduleId', '1017'),
  ('cmd', 'redraw'),
  ('site', '32982'),
  ('url_mode', 'rewrite'),
  ('submitFormId', '1017'),
  ('moduleId', '1017'),
  ('page', ''),
  ('site', '32982'),
]

def get_captcha_image(t):
  session = requests.Session()
  session.get(BASE_URL, verify=False)
  captcha_image = io.BytesIO(session.get(CAPTCHA_URL + str(t)).content)
  return captcha_image 

def process_captcha(captcha: io.BytesIO):
  img = cv2.imdecode(np.frombuffer(captcha.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
  img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1]
  img = cv2.medianBlur(img, 5)
  img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1]
  return img

def main():
  count = int(input("Number of captchas to download: "))
  # count = 1
  for i in range(count):
    t = int(time.time()) * 1000
    img = get_captcha_image(t)
    img = process_captcha(img)
    cv2.imwrite(f'./captchas/_{i}.jpeg', img)
    print(f"Captcha #{i} downloaded")

if __name__ == "__main__":
  
  main()
