import socketio
import time
import threading
from homework_collect import homework_collect, submit_homework, setting_config, homework_info
from remind_daka import remind_run

sio = socketio.Client()
QQ = 2075351675


# 对群消息进行回调
@sio.event()
def OnGroupMsgs(msg):
    print(msg)


# 对好友消息进行回调
@sio.event()
def OnFriendMsgs(msg):
    print(msg)
    homework_collect.homework_collect_main(msg, "形教")
    remind_run.solve(msg)


# 对一些特别的事件进行返回
@sio.on("OnEvents")
def on_message(data_event_m):
    print(data_event_m)


# 对连接成功的项目显示接入成功
@sio.on('connect')
def connect():
    sio.emit('GetWebConn', str(QQ), callback=lambda str_web_conn: print(str_web_conn))


@sio.on('disconnect')
def disconnect():
    print('disconnected from server')


if __name__ == '__main__':
    try:
        sio.connect("http://47.115.62.125:1133", transports='websocket')
        print('my sid is', sio.sid)
    except BaseException as e:
        print(e)
    # temp = homework_info.HomeworkInfo("有关王天行的作业", "3", "2020-10-10 2:00:00", 2646677495)
    # temp.set_usr({"2646677495": "李昊"})
    # setting_config.homework_list.append(temp)
    # test2 = {'CurrentPacket': {'WebConnId': '904sYQTwPNrE2FinndDe',
    #                            'Data': {'FromUin': 2646677495, 'ToUin': 2075351675, 'MsgType': 'FriendFileMsg',
    #                                     'MsgSeq': 9655,
    #                                     'Content': '{"FileID":"f717c19df95b09df4de35ea1c783c368_23d8cadc-0529-11eb-b621-eb11aabdb12e","FileName":"test.docx","FileSize":12159,"Tips":"[好友文件]"}',
    #                                     'RedBaginfo': None}}, 'CurrentQQ': 2075351675}
    # test1 = {'CurrentPacket': {'WebConnId': '904sYQTwPNrE2FinndDe',
    #                            'Data': {'FromUin': 2646677495, 'ToUin': 2075351675, 'MsgType': 'FriendFileMsg',
    #                                     'MsgSeq': 9655,
    #                                     'Content': '交形教作业',
    #                                     'RedBaginfo': None}}, 'CurrentQQ': 2075351675}
    # submit_homework.start_collect_one(test1, "形教")
    # submit_homework.get_one_homework(test2, "形教")
