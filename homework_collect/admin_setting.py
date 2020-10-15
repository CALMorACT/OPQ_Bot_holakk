from . import setting_config
import queue
import time
from websocket_sevice import ws_service

admin_queue = queue.Queue(100)


def if_solve(msg: dict, homework_type: str):
    if msg['CurrentPacket']['Data']['FromUin'] in setting_config.admin_list:
        if msg['CurrentPacket']['Data']['Content'] == "设定" + homework_type + "作业":
            if_not_ok = ws_service.SendMsg(setting_config.host,
                                           setting_config.current_qq,
                                           "开始设定%s作业，请输入作业名，作业次数，作业ddl；并用空格分隔开" % homework_type,
                                           msg['CurrentPacket']['Data']['FromUin'])
            if not if_not_ok:
                data = {
                    "User": msg['CurrentPacket']['Data']['FromUin'],
                    "msg": "start_new_homework",
                    "type": homework_type
                }
                admin_queue.put(data)
            else:
                print("error")


def set_setting(msg: dict, homework_type: str, homework_index: int):
    if msg['CurrentPacket']['Data']['FromUin'] in setting_config.admin_list and \
            msg['CurrentPacket']['Data']['MsgType'] == "TextMsg":
        if len(setting_config.homework_list) < homework_index + 1 and \
                "配置作业" in msg['CurrentPacket']['Data']['Content']:
            data = data_first = admin_queue.get()
            while admin_queue.not_empty:
                if data["msg"] == "start_new_homework" and data["type"] == homework_type:
                    break
                admin_queue.put(data)
                data = admin_queue.get()
                if data is data_first:
                    break
            if msg['CurrentPacket']['Data']['FromUin'] == data["User"] and \
                    data["msg"] == "start_new_homework":
                setting_content = msg['CurrentPacket']['Data']['Content'].split('\n')
                setting_content.pop(0)
                setting_content.append(data["User"])
                if data["type"] == "形教":
                    time.sleep(1)
                    setting_config.new_XinJiao_homework(*setting_content)


def get_no_finish_usr(msg: dict, homework_type: str, homework_index: int):
    if msg['CurrentPacket']['Data']['FromUin'] in setting_config.admin_list and \
            msg['CurrentPacket']['Data']['Content'] == "查看未交%s作业的人" % homework_type and \
            len(setting_config.homework_list) >= homework_index + 1:
        no_finish_usr_list = list(setting_config.homework_list[homework_index].homework_no_finish_usr.values())
        ws_service.SendMsg(setting_config.host, setting_config.current_qq,
                           "%s\\r共有%d人" % ('\\r'.join(no_finish_usr_list), len(no_finish_usr_list)),
                           msg['CurrentPacket']['Data']['FromUin'])
