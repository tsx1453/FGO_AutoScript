import os
import config
import time
import subprocess
import ui_util


def execute_shell(cmd):
    sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    sub.wait()
    return str(sub.stdout.read(), encoding="utf-8")


def wait_for(template, step=3, threshold=0.9, max_count=5, extra_resources=None):
    if extra_resources is None:
        extra_resources = []
    count = 0
    while not ui_util.get_new_capture_and_match(template, threshold=threshold, remove_after_match=True):
        for extra in extra_resources:
            if ui_util.get_new_capture_and_match(extra, threshold=threshold, remove_after_match=True):
                return
        time.sleep(step)
        count = count + 1
        if count > max_count:
            write_log("wait for {} has run for {} times, break out".format(template, count))
            break


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
