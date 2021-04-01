import lib.base.ui_support as ui_support
import time
import lib.base.cv_util as cv_util
import os
import lib.base.config as config
import lib.base.resources as resources
import random
import lib.base.logger as logger

impl = ui_support.CommandLineTool()
capture_queue = []
special_random_position_delta = [
    (lambda x: "action" in x, (-20, -60, 20, 5)),
    (lambda x: "skill" in x, (-10, -10, 10, 10)),
    (lambda x: resources.battle_last_run_flag == x, (-2, 0, 60, 20)),
    (lambda x: resources.battle_friend_select_normal_item == x, (-10, -4, 30, 2)),
    (lambda x: True, (-4, -4, 4, 4))
]


def delete_file(path):
    try:
        os.remove(path)
    except:
        pass


def get_new_capture():
    global impl, capture_queue
    path = os.path.join(config.temp_folder_path,
                        "window_capture_{}.png".format(time.strftime("%m-%d-%H-%M-%S", time.localtime())))
    capture_queue.append(path)
    if len(capture_queue) > config.capture_cache_size:
        delete_file(capture_queue[0])
        capture_queue = capture_queue[1:]
    if impl.capture(path):
        return path
    return None


def get_new_capture_and_match(template, threshold=0.9, remove_after_match=False):
    global impl
    capture = get_new_capture()
    result = cv_util.has_match(template, capture, match_threshold=threshold)
    if remove_after_match:
        delete_file(capture)
    return result


def click(x, y):
    global impl
    impl.click(x, y)


def match_and_click(template, source=None, delete_after_match=False, match_threshold=0.6):
    global impl, special_random_position_delta
    if source is None:
        source = get_new_capture()
    max_val, tl_loc, br_loc = cv_util.match_template(template, source)
    if delete_after_match:
        delete_file(source)
    if max_val > match_threshold:
        x = (br_loc[0] + tl_loc[0]) / 2
        y = (br_loc[1] + tl_loc[1]) / 2
        random_delta_x, random_delta_y = 0, 0
        for delta in special_random_position_delta:
            if delta[0](template):
                random_delta_x = random.Random().randrange(start=delta[1][0], stop=delta[1][2])
                random_delta_y = random.Random().randrange(start=delta[1][1], stop=delta[1][3])
                break
        logger.log(
            "match and click template = {}, source = {}, position = ({}, {}), random_delta = ({}, {})".format(template,
                                                                                                              source, x,
                                                                                                              y,
                                                                                                              random_delta_x,
                                                                                                              random_delta_y))
        click(x + random_delta_x, y + random_delta_y)
        return True
    return False
