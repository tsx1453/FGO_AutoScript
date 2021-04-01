import time
import common_util
import resources
import ui_util
import cv_util


def launch():
    if ui_util.get_new_capture() is not None:
        common_util.execute_shell("open /Applications/命运-冠位指定.app")
        print("game has launched")
        return
    count = 0
    while ui_util.get_new_capture() is None:
        print("try launch {}".format(count + 1))
        common_util.execute_shell("open /Applications/命运-冠位指定.app")
        count = count + 1
        if count > 5:
            print("error!!! cant launch game!!!")
            raise Exception()
        time.sleep(4)
    common_util.wait_for(resources.launch_first_step_click_screen, step=5, max_count=10)
    if not ui_util.match_and_click(resources.launch_first_step_click_screen):
        print("error!!! cant enter game")
        raise Exception()
    common_util.wait_for(resources.launch_second_step_game_slogen, step=5, max_count=10)
    count = 0
    while ui_util.match_and_click(resources.launch_second_step_game_slogen):
        count = count + 1
        if count > 10:
            print("error!!! login error")
            raise Exception()
        time.sleep(5)
    common_util.wait_for(resources.launch_game_post)
    ui_util.match_and_click(resources.launch_game_post_close_button)
    print("launch finish!!!")


def go_to_exp():
    if cv_util.has_match(resources.daily_task_title, ui_util.get_new_capture()):
        return
    common_util.wait_for(resources.launch_chaldea_gate)
    ui_util.match_and_click(resources.launch_chaldea_gate)
    common_util.wait_for(resources.launch_daily_task)
    ui_util.match_and_click(resources.launch_daily_task)
    common_util.wait_for(resources.launch_exp_ap_40_unpass, extra_resources=[resources.launch_exp_ap_40_passed])
    for t in [resources.launch_exp_ap_40_passed, resources.launch_exp_ap_40_unpass]:
        if ui_util.match_and_click(t):
            break
    print("go to exp finished!!!")
