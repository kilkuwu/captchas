import re
import time
import requests

import io
import numpy as np

import cv2
from openpyxl import Workbook

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_captcha(image_bytes: io.BytesIO):
  gray = cv2.imdecode(np.frombuffer(
      image_bytes.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
  thre = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
  PADDING = 10
  thre = cv2.copyMakeBorder(thre, PADDING, PADDING, 0,
                            0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
  text: str = pytesseract.image_to_string(
      thre, config="--psm 12 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz")

  return text

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
  pass

def get_info(id):
  session = requests.Session()
  session.get(BASE_URL, verify=False)

  while True:
    t = int(time.time() * 1000)

    captcha_image = io.BytesIO(session.get(CAPTCHA_URL + str(t)).content)

    captcha = get_captcha(captcha_image).strip()

    print("Trying captcha", captcha)

    data = {
      'layout': 'Decl.DataSet.Detail.default',
      'itemsPerPage': '1000',
      'pageNo': '1',
      'service': 'Content.Decl.DataSet.Grouping.select',
      'itemId': ITEM_ID,
      'gridModuleParentId': '17',
      'type': 'Decl.DataSet',
      'page': '',
      'modulePosition': '0',
      'moduleParentId': '-1',
      'orderBy': '',
      'unRegex': '',
      'keyword': id,
      'BDC_UserSpecifiedCaptchaId': captcha,
      'captcha_check': captcha,
      'captcha_code': captcha,
      '_t': t,
    }

    response = session.post(BASE_URL, params=FIXED_PARAMS, data=data)

    if response.text != "BotDetect" and "Nhập sai mã bảo mật" not in response.text:
      data = re.findall(r"<td  >(.*?)</td>", response.text)
      return data

def main():
  workbook = Workbook()
  sheet = workbook.active
  assert sheet is not None

  start = 1000
  end = 1015

  SBD = range(start, end)

  for id in SBD:
    data = get_info(id) 
    print()
    print(data)
    print()
    sheet.append(data)

  workbook.save(f"{end}.xlsx")


if __name__ == "__main__":
  main()
