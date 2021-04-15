import lib.base.config as config
import lib.battle.global_status as global_status
import time
import os


def resource_path_to_name(path):
    return path.replace(config.template_img_path, "")


def temp_path_to_name(path):
    return path.replace(config.temp_folder_path, "")


def log_with_echo(log_msg):
    log(log_msg, True)


def log(log_msg, echo=False):
    msg = "{} -> {} (current loop is {})\n".format(time.strftime("%H:%M:%S", time.localtime()), log_msg,
                                                   global_status.loop_number)
    if echo:
        print(msg)
    if config.currentDebugLevel.value > config.DebugLevel.NONE.value:
        if os.stat(config.log_file_path).st_size > 1024 * 1024 * 6:
            os.remove(config.log_file_path)
        with open(config.log_file_path, mode="a") as f:
            f.write(msg)


def save_battle_info(battle_count, apple_count):
    print("update battle info: battle count = {}, apple count = {}".format(battle_count, apple_count))
    with open(config.battle_info_path, mode="w") as f:
        f.write("battleCount: {}\nappleCount: {}".format(battle_count, apple_count))
