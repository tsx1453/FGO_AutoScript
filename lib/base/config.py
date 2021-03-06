from enum import Enum
import os

project_path = os.path.split(os.path.realpath(__file__))[0].replace("lib/base", "")
temp_folder_path = os.path.join(project_path, "temp_folder")
template_img_path = os.path.join(project_path, "template")
match_result_save_path = os.path.join(project_path, "match_results")
log_file_path = os.path.join(temp_folder_path, "log.txt")
battle_info_path = os.path.join(temp_folder_path, "battle_info.txt")
capture_cache_size = 200
# window_size = (0, 0)

if not os.path.exists(temp_folder_path):
    os.mkdir(path=temp_folder_path)

if not os.path.exists(match_result_save_path):
    os.mkdir(path=match_result_save_path)


class DebugLevel(Enum):
    NONE = 0
    JUST_LOG = 1
    SAVE_IMG = 2
    SHOW_IMG = 3


currentDebugLevel = DebugLevel.JUST_LOG

if __name__ == '__main__':
    all_path, all_name = [], []
    for file in os.listdir(template_img_path):
        path = os.path.join(template_img_path, file)
        if os.path.isfile(path):
            all_path.append(path)
            all_name.append(file.split(".")[0])
    with open(os.path.join(project_path, "lib/base/resources.py"), mode="w") as f:
        for i in range(0, len(all_path)):
            f.write("{} = '{}'\n".format(all_name[i], all_path[i]))
