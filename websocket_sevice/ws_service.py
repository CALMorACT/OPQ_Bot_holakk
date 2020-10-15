import requests
import time
import json


def SendMsg(host: str, current_qq: int, send_content: str, to_user: int):
    url = "%s/v1/LuaApiCaller?qq=%d&funcname=SendMsg&timeout=10" % (host, current_qq)
    payload = "{\n  \"toUser\":%d,\n  \"sendToType\":1,\n  \"sendMsgType\":\"TextMsg\",\n  \"content\":\"%s\"," \
              "\n  \"groupid\":0,\n  \"atUser\":0,\n  \"replayInfo\":null\n}" % (to_user, send_content)
    headers = {'Content-Type': 'application/json'}
    try:
        time.sleep(1)
        requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
        return 0
    except BaseException as e:
        print(e)
        return 1


def SendMsg_nowait(host: str, current_qq: int, send_content: str, to_user: int):
    url = "%s/v1/LuaApiCaller?qq=%d&funcname=SendMsg&timeout=10" % (host, current_qq)
    payload = "{\n  \"toUser\":%d,\n  \"sendToType\":1,\n  \"sendMsgType\":\"TextMsg\",\n  \"content\":\"%s\"," \
              "\n  \"groupid\":0,\n  \"atUser\":0,\n  \"replayInfo\":null\n}" % (to_user, send_content)
    headers = {'Content-Type': 'application/json'}
    try:
        requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
        return 0
    except BaseException as e:
        print(e)
        return 1


def GetGroupUserList_nowait(host: str, current_qq: int, group_id: int):
    url = "%s/v1/LuaApiCaller?qq=%d&funcname=GetGroupUserList&timeout=10" % (host, current_qq)

    payload = "{\n  \"GroupUin\":%d,\n  \"LastUin\":0\n}" % group_id
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
        return response
    except BaseException as e:
        print(e)
        return 1


def GetFileUrl(host: str, current_qq: int, file_id: str):
    url = "%s/v1/LuaApiCaller?qq=%d&funcname=OfflineFilleHandleSvr.pb_ftn_CMD_REQ_APPLY_DOWNLOAD-1200&timeout=10" % (
        host, current_qq)
    payload = "{\r\n    \"FileID\": \"" + file_id + "\"\r\n}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
        return response
    except BaseException as e:
        print(e)
        return 1


def send_private_msg_v2(host: str, current_qq: int, to_usr_id: int, group_id: int, send_msg: str):
    time.sleep(1)
    url = "%s/v1/LuaApiCaller?qq=%d&funcname=SendMsgV2" % (host, current_qq)
    payload = {"ToUserUid": to_usr_id, "GroupID": group_id, "SendToType": 3, "SendMsgType": "TextMsg",
               "Content": send_msg}
    try:
        data = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=data)
        return response
    except BaseException as e:
        print(e)
        return 1
