import os
import config
import time


def delete_file(path):
    try:
        os.remove(path)
    except:
        pass


def write_log(log):
    print(log)
    with open(config.log_file_path, mode="a") as f:
        f.write("{} -> {}\n".format(time.strftime("%H:%M:%S", time.localtime()), log))


def notify_release_space():
    pass