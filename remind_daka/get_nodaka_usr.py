# from paddleocr import PaddleOCR, draw_ocr
# from PIL import Image
#
# ocr = PaddleOCR()  # need to run only once to download and load model into memory
# img_path = 'img_data/best.jpg'
# result = ocr.ocr(img_path)
# for line in result:
#     print(line)
#
# # 显示结果
#
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')
import hashlib
import os
import base64
import random
import string
import time
from urllib.parse import urlencode
from PIL import Image

import wget
import json
import requests


class TXApiUse:
    def __init__(self, image_url):
        self.image_url = image_url
        with open('remind_daka/config.json', 'r') as f:
            self.config = json.load(f)
        self.general_ocr_url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr"
        self.pic_base64 = ""
        self.timestamp = 0
        self.nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.app_id = 2157248105
        self.sign = ""

    def get_pic_base64(self):
        wget.download(self.image_url, out="temp.png")
        img = Image.open("temp.png")
        cropped = img.crop((0, 550, 200, 2640))
        cropped.save("temp.png")
        with open("temp.png", 'rb') as fileByte:
            self.pic_base64 = base64.b64encode(fileByte.read())
        if os.path.exists("temp.png"):
            os.remove("temp.png")
        time.sleep(1)

    def get_timestamp(self):
        self.timestamp = int(time.time())

    def get_sign(self, params: dict, app_key: str):
        params_new = {}
        for key in sorted(params):
            params_new[key] = params[key]
        sign_temp = urlencode(params_new)
        sign_temp += "&app_key=%s" % app_key
        self.sign = hashlib.md5(sign_temp.encode("utf-8")).hexdigest().upper()

    def get_result(self):
        self.get_pic_base64()
        self.get_timestamp()
        result = {
            "app_id": self.app_id,
            "time_stamp": self.timestamp,
            "nonce_str": self.nonce_str,
            "image": self.pic_base64
        }
        self.get_sign(result, "zPA2BaAlSLGRXkvY")
        result['sign'] = self.sign
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.request("POST", url=self.general_ocr_url, data=result)


class CleanAPIData:
    def __init__(self, api_response):
        self.api_data = json.loads(api_response.text.replace("\n", ""))
        self.item_list = []
        self.nodata_list = []
        self.prepare_data()
        self.clean_data()

    def prepare_data(self):
        if self.api_data['msg'] == "ok":
            self.item_list = self.api_data['data']['item_list']

    def clean_data(self):
        def filter_ul(item):
            for word in item['words']:
                if word["confidence"] < 0.99:
                    return False
            return True

        self.nodata_list = [item['itemstring'] for item in filter(filter_ul, self.item_list)]
        self.nodata_list.remove("姓名")


# if __name__ == '__main__':
#     temp = TXApiUse(
#         "http://c2cpicdw.qpic.cn/offpic_new/2075351675/2646677495-3385731726-D33EB2A6967504FFF667CF88B78A25B0/0")
#     response = temp.get_result()
#     clean_it = CleanAPIData(response)
#     print(clean_it.nodata_list)
