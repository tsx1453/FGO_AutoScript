import interfaces
import os
import json
import subprocess
import config

target_product_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                                   "../MacOSScriptImpl/Build/Release/MacOSScriptImpl")


def execute_shell(cmd):
    sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    sub.wait()
    return str(sub.stdout.read(), encoding="utf-8")


def check_build_product():
    if not os.path.exists(target_product_path):
        execute_shell("cd MacOSScriptImpl && xcodebuild")


class CommandLineTool(interfaces.EventSender, interfaces.ScreenFetcher):

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__w = 0
        self.__h = 0

    def click(self, x, y):
        check_build_product()
        x = x + self.__x
        y = y + self.__y
        execute_shell("{} click {} {}".format(target_product_path, int(x), int(y)))

    def capture(self, path):
        check_build_product()
        result = execute_shell("{} capture {} {}".format(target_product_path, path, "命运-冠位指定"))
        # common_util.write_log(result)
        json_data = json.loads(result)
        if len(json_data) != 4:
            return False
        # common_util.write_log(json_data, type(json_data))
        self.__x, self.__y, self.__w, self.__h = json_data['x'], json_data['y'], json_data['w'], json_data['h']
        config.window_size = (self.__w, self.__h)
        return True
