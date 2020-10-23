import time
from websocket_sevice import ws_service
import json


def remind_everyday(config: dict):
    localtime = time.localtime(time.time())
    if localtime.tm_hour == 10 and localtime.tm_min == 0 and localtime.tm_sec <= 1:
        # if True:
        for group in config["solve_qq_group"]:
            response = ws_service.GetGroupUserList_nowait(config["host"], config["current_qq"], group)
            print(response.text)
            mem_list = [(x["GroupCard"], x["MemberUin"]) for x in json.loads(response.text)["MemberList"]]
            print(mem_list[5][0])
            for usr in mem_list:
                if usr[0] != '' and usr[0] != '李险峰' and usr[1] != 2075351675:
                    ws_service.send_private_msg_v2(config['host'],
                                                   config['current_qq'],
                                                   group_id=json.loads(response.text)['GroupUin'],
                                                   to_usr_id=usr[1],
                                                   send_msg="请同学尽快打卡，如果打了请忽略")
                    time.sleep(1)
