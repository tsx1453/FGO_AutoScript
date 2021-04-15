import random
import time
import numpy

import lib.battle.global_status as global_status
import lib.battle.interfaces as interfaces
from lib.base import cv_util, logger, resources, ui_util


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
            logger.log(
                "wait for {} has run for {} times, break out".format(logger.resource_path_to_name(template), count))
            break


class SimpleMatchAndClickTask(interfaces.Task):
    def accept(self, capture):
        return cv_util.has_match(self.template, capture)

    def on_execute(self, capture):
        ui_util.match_and_click(self.template, delete_after_match=True)

    def __init__(self, template):
        super().__init__()
        self.template = template


class SelectLastRunTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_last_run_flag)


class RandomSelectFriendTask(interfaces.Task):

    def accept(self, capture):
        return not global_status.is_in_battle and cv_util.has_match(resources.battle_friend_select_title, capture)

    def on_execute(self, capture):
        ui_util.match_and_click(resources.battle_friend_select_normal_item)


class ClickStartBattleTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_start_button)

    def execute(self, capture):
        super().execute(capture)
        logger.log(
            "click start battle task ,before reset status ,skill history is {}".format(global_status.skill_history))
        global_status.is_in_battle = True
        global_status.turn_num = 1
        global_status.skill_history = {}
        global_status.skill_history.clear()
        # global_status.skill_position_cache = {}
        global_status.hougu_status = [False, False, False]
        global_status.loop_number = global_status.loop_number + 1
        logger.log(
            "click start battle task ,after reset status ,skill history is {}".format(global_status.skill_history))
        logger.log_with_echo("start new battle {}".format(global_status.loop_number))


class BattleUpdateGlobalStatusTask(interfaces.Task):

    def accept(self, capture):
        return cv_util.has_match(resources.battle_attack_button, capture, match_threshold=0.7)

    def on_execute(self, capture):
        global_status.is_in_battle = True
        turns = [
            ([resources.battle_turn_1_of_3, resources.battle_turn_1_of_2, resources.battle_turn_1_of_1], 1),
            ([resources.battle_turn_2_of_3, resources.battle_turn_2_of_2], 2),
            ([resources.battle_turn_3_of_3], 3),
        ]
        for templates in turns:
            for t in templates[0]:
                if cv_util.has_match(t, capture):
                    original = global_status.turn_num
                    if original != templates[1]:
                        global_status.turn_num = templates[1]
                        logger.log_with_echo("update turn num from {} to {}".format(original, templates[1]))
                    return


class BattleClickSkillTask(interfaces.Task):
    def __init__(self, template, skill_index, turn_num=-1, accept_extra=None):
        super().__init__()
        self.template = template
        self.skill_index = skill_index
        self.turn_num = turn_num
        self.accept_extra = accept_extra

    def accept(self, capture):
        ac = global_status.is_in_battle
        if self.turn_num != -1:
            logger.log("skill check turn, target is {} and current is {}".format(self.turn_num,
                                                                                 global_status.turn_num))
            ac = ac and (self.turn_num == global_status.turn_num)
        if self.accept_extra is not None:
            ac = ac and self.accept_extra(capture)
        logger.log("skill task accept result is {}".format(ac))
        return ac

    def on_execute(self, capture):
        skill_used = global_status.skill_history.get(self.template, {})
        logger.log("skill history for {} is {}".format(logger.resource_path_to_name(self.template), skill_used))
        can_use_skill = False
        for skill in self.skill_index:
            if not skill_used.get(skill, False):
                can_use_skill = True
                break
        if not can_use_skill:
            return
        wait_for(resources.battle_attack_button)
        skill_position = global_status.skill_position_cache.get(self.template, ())
        if len(skill_position) == 0:
            logger.log("not find cached skill position, start match in capture")
            local_count = 0
            while local_count < 5:
                local_count = local_count + 1
                capture = ui_util.get_new_capture()
                max_val, tl_loc, br_loc = cv_util.match_template(self.template, capture)
                if max_val > 0.6:
                    left, top, right, bottom = tl_loc[0], tl_loc[1], br_loc[0], br_loc[1]
                    skill_position = (left, top, right, bottom)
                    global_status.skill_position_cache[self.template] = skill_position
                    logger.log("find skill template ,position is {}".format(skill_position))
                    break
                else:
                    wait_for(self.template)

        if len(skill_position) == 0:
            logger.log("not find skill position, return")
            return
        left, top, right, bottom = skill_position[0], skill_position[1], skill_position[2], skill_position[3]
        width = right - left
        item_width = width / 3
        center_y = (top + bottom) / 2
        for skill in self.skill_index:
            if not skill_used.get(skill, False):
                wait_for(resources.battle_attack_button)
                x = left + item_width * (skill - 1) + item_width / 2
                random_x = random.Random().randrange(start=-10, stop=10)
                random_y = random.Random().randrange(start=-10, stop=10)
                logger.log_with_echo(
                    "click skill {}, original position is ({} ,{}), random_delta = ({}, {})".format(
                        logger.resource_path_to_name(self.template), x, center_y, random_x, random_y))
                ui_util.click(x + random_x, center_y + random_y)
                skill_used = global_status.skill_history.get(self.template, {})
                skill_used[skill] = True
                global_status.skill_history[self.template] = skill_used
                time.sleep(random.randrange(2, 3))


class BattleClickAttackTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_attack_button)

    def execute(self, capture):
        super().execute(capture)
        time.sleep(random.randrange(2, 5))


class BattleSelectActionCardTask(interfaces.Task):
    def __init__(self, special_templates=None):
        super().__init__()
        if special_templates is None:
            special_templates = {}
        self.special_templates = special_templates

    def accept(self, capture):
        return cv_util.has_match(resources.battle_speed_set_button, capture)

    def on_execute(self, capture):
        if len(self.special_templates) > 0:
            target_card = self.special_templates.get(global_status.turn_num, [])
            if len(target_card) == 0:
                target_card = self.special_templates.get(-1, [])
            if len(target_card) > 0:
                for card in target_card:
                    local_count = 0
                    while local_count < 2:
                        local_count = local_count + 1
                        if ui_util.match_and_click(card, delete_after_match=True):
                            time.sleep(random.randrange(1, 3))
                            logger.log_with_echo("selected card {}".format(logger.resource_path_to_name(card)))
                            break
        else:
            for index in range(3):
                if global_status.hougu_status[index]:
                    # 此处坐标获取方法同NP检测，均为手动比划得来
                    top, bottom = 170, 300
                    item_width = 100
                    left = 96 * (index + 1) + 100 * index
                    right = left + item_width
                    x = random.randrange(left, right)
                    y = random.randrange(top, bottom)
                    ui_util.click(x, y)
                    global_status.hougu_status[index] = False
                    time.sleep(random.randrange(0, 2))
                    logger.log_with_echo("select hougo card at {}".format(index))
                    break
        card_queue = [resources.action_buster, resources.action_arts, resources.action_quick]
        for card in card_queue:
            if ui_util.match_and_click(card, delete_after_match=True):
                logger.log_with_echo("selected card {}".format(logger.resource_path_to_name(card)))
                time.sleep(random.randrange(1, 3))
                break


class BattleSettleJiBanTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_jiban_title)

    def execute(self, capture):
        super().execute(capture)
        wait_for(resources.battle_click_ui_tip)


class BattleSettleExpTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_exp_title)

    def execute(self, capture):
        super().execute(capture)
        wait_for(resources.battle_click_ui_tip)


class BattleSettleConfirmTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_finish_next_step_button)

    def on_execute(self, capture):
        super().on_execute(capture)
        global_status.is_in_battle = False
        logger.log_with_echo("battle {} finish".format(global_status.loop_number))
        logger.save_battle_info(global_status.turn_num, global_status.apple_eat_count)


class BattleQuickStartTask(SimpleMatchAndClickTask):
    def __init__(self):
        super().__init__(resources.battle_go_on_button)


class EatAppleTask(interfaces.Task):

    def accept(self, capture):
        return not global_status.is_in_battle and cv_util.has_match(resources.item_sliver_apple, capture)

    def on_execute(self, capture):
        ui_util.match_and_click(resources.item_sliver_apple)
        wait_for(resources.apple_eat_dialog_confirm_button, step=1)
        ui_util.match_and_click(resources.apple_eat_dialog_confirm_button)
        global_status.apple_eat_count = global_status.apple_eat_count + 1
        logger.log_with_echo("eat apple, total is {}".format(global_status.apple_eat_count))
        time.sleep(random.randrange(1, 3))


class UsedSkillClickDialogTask(interfaces.Task):
    def accept(self, capture_path):
        return global_status.is_in_battle and cv_util.has_match(resources.skill_used_click_dialog_title, capture_path)

    def on_execute(self, capture):
        ui_util.match_and_click(resources.cancel_button)
        wait_for(resources.battle_attack_button, step=1)


class ServantClickedStatusDialogTask(interfaces.Task):
    def accept(self, capture_path):
        return global_status.is_in_battle and cv_util.has_match(resources.servant_selected_ststus_title, capture_path)

    def on_execute(self, capture):
        ui_util.match_and_click(resources.close_button)
        wait_for(resources.battle_attack_button, step=1)


class ServantCountOverflowDialogTask(interfaces.Task):

    def accept(self, capture_path):
        return cv_util.has_match(resources.need_release_space_buttons, capture_path)

    def on_execute(self, capture):
        logger.log_with_echo("need clear space, auto battle count is {}".format(global_status.loop_number))
        raise StopBattleException()


class NpCheckTask(interfaces.Task):

    def accept(self, capture):
        return global_status.is_in_battle and cv_util.has_match(resources.battle_attack_button, capture)

    def on_execute(self, capture):
        img = cv_util.read_img(capture)
        has_ready = False
        for i in range(3):
            has_ready = has_ready or self.check(img, i)
        # 如果第一次检测不成功那么再重新截图检测一次
        if not has_ready:
            img = cv_util.read_img(ui_util.get_new_capture())
            for i in range(3):
                self.check(img, i)
        logger.log_with_echo("check hougo result is {}".format(global_status.hougu_status))

    # 检查方案：截取NP条区域，计算其像素值的平均值，因为未充满的话基本是比较暗（更靠近0）的状态，满了之后亮度提升（更靠近255）
    # 所以根据这个数值来判断是不是满了
    def check(self, capture, index):
        # 这个数值是试出来的，反正能用
        threshold = 40
        top = 518
        bottom = 524
        np_bar_width = 86
        left = 96 * (index + 1) + 100 * index
        right = left + np_bar_width
        crop = capture[top:bottom, left:right]
        result = numpy.mean(crop) > threshold
        logger.log("check np at {}, result is {}".format(index, result))
        global_status.hougu_status[index] = result
        return result


class StopBattleException(Exception):
    pass
