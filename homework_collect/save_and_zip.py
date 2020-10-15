import json
import os
import wget
import zipfile

import requests
from websocket_sevice import ws_service
from . import setting_config


# Test over
class SaveAndZip:
    def __init__(self, homework_info):
        self.homework_info = homework_info
        self.out_name = "物联网-第" + self.homework_info.get_times() + "次作业.zip"
        self.save_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "save_homework",
                                          "第" + self.homework_info.get_times() + "次作业")
        self.zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "save_homework", self.out_name)

    # 针对形教课作业要求命名保存
    def save_XinJiao(self, file_id, sendfile_name: str, usr_name: str):
        if not os.path.exists(self.save_dir_path):
            os.makedirs(self.save_dir_path)
        file_name = "物联网-" + usr_name + "-第" + self.homework_info.get_times() + "次作业." + sendfile_name.split(".")[-1]
        file_save_path = os.path.join(self.save_dir_path, file_name)
        response = ws_service.GetFileUrl(setting_config.host, setting_config.current_qq, file_id)
        results = json.loads(response.text.encode('utf8'))
        wget.download(results["Url"], file_save_path)
        return os.path.exists(file_save_path)

    # 对某一次作业进行压缩
    def zip_file(self):
        with zipfile.ZipFile(self.zip_file_path, "w") as z:
            for root, dirs, files in os.walk(self.save_dir_path):
                for single_file in files:
                    if single_file != self.out_name:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath, os.path.basename(filepath))
