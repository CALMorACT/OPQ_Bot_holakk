from . import homework_info
from . import setting_config
from websocket_sevice import ws_service
import queue, json

submit_queue = queue.Queue(100)


def start_collect_one(msg: dict, homework_type: str):
    if msg['CurrentPacket']['Data']['Content'] == "交" + homework_type + "作业":
        if str(msg['CurrentPacket']['Data']['FromUin']) in setting_config.homework_list[0].homework_no_finish_usr:
            data = {
                "User": msg['CurrentPacket']['Data']['FromUin'],
                "msg": "submit_homework",
                "type": homework_type
            }
            submit_queue.put(data)


def get_one_homework(msg: dict, homework_type: str):
    if msg['CurrentPacket']['Data']['MsgType'] == 'FriendFileMsg':
        data = data_first = submit_queue.get()
        if_have = False
        while submit_queue.not_empty:
            if data["msg"] == "submit_homework" and \
                    data["type"] == homework_type and \
                    data['User'] == msg['CurrentPacket']['Data']['FromUin']:
                if_have = True
                break
            submit_queue.put(data)
            data = submit_queue.get()
            if data is data_first:
                break
        if if_have:
            file_info = json.loads(msg['CurrentPacket']['Data']['Content'])
            fun_save = setting_config.homework_list[0].homework_save_and_zip
            fun_save.save_XinJiao(file_info["FileID"], file_info["FileName"],
                                  setting_config.homework_list[0].homework_usr[str(data['User'])])
