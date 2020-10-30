import hashlib
import os
import base64
import random
import string
import subprocess
import time
from urllib.parse import urlencode
from PIL import Image

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
        # headers = {
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.11 Safari/537.36 Edg/87.0.664.8',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        # }
        # response_download = requests.request("GET", self.image_url, headers=headers)
        # with open("temp.png", "wb") as code:
        #     code.write(response_download.content)
        subprocess.call(['aria2c', self.image_url, '-o', 'temp.png'])
        img = Image.open("temp.png")
        w, h = img.size
        cropped = img.crop((0, int(h * 0.1), int(w * 0.16), int(h * 0.95)))
        cropped.thumbnail(tuple(map(lambda x: x * 0.4, img.size)))
        cropped.save("temp.png")
        with open("temp.png", 'rb') as fileByte:
            self.pic_base64 = base64.b64encode(fileByte.read())
        if os.path.exists("temp.png"):
            os.remove("temp.png")
        # time.sleep(1)

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
        return requests.request("POST", url=self.general_ocr_url, data=result)


class CleanAPIData:
    def __init__(self, api_response):
        if "\n" in api_response.text:
            self.api_data = json.loads(api_response.text.replace("\n", ""))
        else:
            self.api_data = json.loads(api_response.text.replace("\r", ""))
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
        if "姓名" in self.nodata_list:
            self.nodata_list.remove("姓名")
