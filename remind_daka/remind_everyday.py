import time
from websocket_sevice import ws_service
import json


def remind_everyday(config: dict):
    localtime = time.localtime(time.time())
    # if localtime.tm_hour == 9 and localtime.tm_min == 00:
    if True:
        for group in config["solve_qq_group"]:
            response = ws_service.GetGroupUserList_nowait(config["host"], config["current_qq"], group)
            for usr in [(x["GroupCard"], x["MemberUin"]) for x in json.loads(response.content.decode('utf-8'))["MemberList"]]:
                if usr[0] != '' and usr[0] != '李险峰' and usr[1] != 2075351675:
                    # ws_service.send_private_msg_v2(config['host'],
                    #                                config['current_qq'],
                    #                                group_id=json.loads(response.text)['GroupUin'],
                    #                                to_usr_id=usr[1],
                    #                                send_msg="请同学尽快打卡，如果打了请忽略")
                    pass


if __name__ == '__main__':
    with open("config.json") as config:
        config = json.load(config)
    remind_everyday(config)
