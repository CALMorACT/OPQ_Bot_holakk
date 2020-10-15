from . import admin_setting
from . import submit_homework


def homework_collect_main(msg: dict, homework_type: str):
    admin_setting.if_solve(msg, homework_type)
    admin_setting.set_setting(msg, homework_type, 0)
    admin_setting.get_no_finish_usr(msg, homework_type, 0)
    submit_homework.start_collect_one(msg, homework_type)
    submit_homework.get_one_homework(msg, homework_type)
