from . import homework_info
import pandas as pd
import requests
import json
from websocket_sevice import ws_service

homework_list = []
host = "http://47.115.62.125:1133"
current_qq = 2075351675
group_id = 659523903
admin_list = [2646677495]


def get_usr(file_path):
    usr_dict = {}
    df = pd.read_excel(file_path)
    usr_name_list = df[df["无形教"] != 1]
    response = ws_service.GetGroupUserList_nowait(host, current_qq, group_id)
    if response != 1:
        result = json.loads(response.text.encode('utf8'))
        if result["GroupUin"] == group_id:
            for mem in result["MemberList"]:
                if mem['GroupCard'] in usr_name_list["姓名"].values:
                    usr_dict[mem["MemberUin"]] = mem["GroupCard"]
        return usr_dict


def new_XinJiao_homework(name, times, ddl_input, owner):
    # ddl_input: "%Y-%m-%d %H"
    new_work = homework_info.HomeworkInfo(name, times, ddl_input + ":00:00", owner)
    new_work.set_usr(get_usr("./homework_collect/物联网信息统计表.xlsx"))
    homework_list.append(new_work)
    ws_service.SendMsg(host, current_qq, "作业情况如下:\\r%s" % str(new_work), new_work.get_own())
