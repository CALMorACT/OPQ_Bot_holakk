import time
import uuid
from . import save_and_zip


class HomeworkInfo:
    def __init__(self, name: str, times: str, ddl: str, owner: int):
        self.homework_own = owner
        self.homework_name = name
        self.homework_times = times
        self.homework_ddl = int(time.mktime(time.strptime(ddl, "%Y-%m-%d %H:%M:%S")))
        self.homework_usr = {}
        self.homework_no_finish_usr = {}
        self.homework_save_and_zip = save_and_zip.SaveAndZip(self)
        self.homework_id = uuid.uuid1()

    def get_own(self):
        return self.homework_own

    def set_own(self, owner: str):
        self.homework_own = owner

    def get_times(self):
        return self.homework_times

    def set_times(self, times: str):
        self.homework_times = times

    def add_usr(self, usr_qq: str, usr_name: str):
        self.homework_usr[usr_qq] = usr_name

    def set_usr(self, usr_dict: dict):
        self.homework_usr = usr_dict
        self.homework_no_finish_usr = self.homework_usr

    def __str__(self):
        return self.homework_name + "\\r第" + self.homework_times + "次作业\\r" + str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.homework_ddl))) + "\\r" + "共有" + str(
            len(self.homework_usr)) + "个成员需要交作业"
