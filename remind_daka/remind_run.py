import queue
import json
from . import get_nodaka_usr
from . import remind_everyday
from websocket_sevice import ws_service

admin_queue = queue.Queue(100)


def if_solve(msg: dict, config: dict):
    if msg['CurrentPacket']['Data']['FromUin'] in config["admin_list"]:
        if msg['CurrentPacket']['Data']['Content'] == "提醒打卡":
            if_not_ok = ws_service.SendMsg(config['host'],
                                           config['current_qq'],
                                           "请发送图片",
                                           msg['CurrentPacket']['Data']['FromUin'])
            if not if_not_ok:
                data = {
                    "User": msg['CurrentPacket']['Data']['FromUin'],
                    "msg": "remind_daka",
                    "type": "物联网"
                }
                admin_queue.put(data)
            else:
                print("error")


def solve_nodaka(msg: dict, config: dict):
    if msg['CurrentPacket']['Data']['FromUin'] in config['admin_list'] and \
            msg['CurrentPacket']['Data']['MsgType'] == "PicMsg":
        data = data_first = admin_queue.get()
        while admin_queue.not_empty:
            if data["msg"] == "remind_daka" and data["type"] == '物联网':
                break
            admin_queue.put(data)
            data = admin_queue.get()
            if data is data_first:
                break
        if msg['CurrentPacket']['Data']['FromUin'] == data["User"] and \
                data["msg"] == "remind_daka":
            if data["type"] == "物联网":
                api_result = get_nodaka_usr.TXApiUse(
                    json.loads(msg['CurrentPacket']['Data']['Content'])['FriendPic'][0]["Url"])
                clean_it = get_nodaka_usr.CleanAPIData(api_result.get_result())
                ws_service.SendMsg(config['host'],
                                   config['current_qq'],
                                   "开始记录并解决当天未打开同学\\r%s" % " ".join(clean_it.nodata_list),
                                   msg['CurrentPacket']['Data']['FromUin'])
                send_nodaka(clean_it.nodata_list, config)


def send_nodaka(nodaka_list: list, config: dict):
    nodaka_usr = []
    for group in config["solve_qq_group"]:
        response = ws_service.GetGroupUserList_nowait(config["host"], config["current_qq"], group)
        for usr in [(x["GroupCard"], x["MemberUin"]) for x in json.loads(response.text)["MemberList"]]:
            if usr[0] in nodaka_list:
                nodaka_usr.append((usr[0], usr[1], group))
    if not nodaka_usr:
        ws_service.SendMsg(config['host'], config['current_qq'], "无人未打卡", config['admin_list'][0])
    for each_remind in nodaka_usr:
        response = ws_service.send_private_msg_v2(config['host'],
                                                  config['current_qq'],
                                                  group_id=each_remind[2],
                                                  to_usr_id=each_remind[1],
                                                  send_msg="同学，老师那边显示你未打卡，请同学尽快打卡")
        if response.text != "" and response.status_code == 200:
            ws_service.SendMsg(config['host'], config['current_qq'], "已提醒%s" % each_remind[0], config['admin_list'][0])


def solve(msg):
    with open("remind_daka/config.json") as config:
        config = json.load(config)
    remind_everyday.remind_everyday(config)
    if_solve(msg, config)
    solve_nodaka(msg, config)
