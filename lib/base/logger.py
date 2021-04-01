import lib.base.config as config
import time


def resource_path_to_name(path):
    return path.replace(config.template_img_path, "")


def log(log_msg):
    msg = "{} -> {}\n".format(time.strftime("%H:%M:%S", time.localtime()), log_msg)
    print(msg)
    if config.currentDebugLevel.value > config.DebugLevel.NONE.value:
        with open(config.log_file_path, mode="a") as f:
            f.write(msg)
