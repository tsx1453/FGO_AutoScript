import time

import cv_util
import interfaces
import resources
import ui_util
import random
import common_util
import config
from common_util import wait_for as _wait_for


def battle(battle_state_list, battle_count=None, apple_count=None):
    if battle_count is None and apple_count is None:
        print("please select battleCount or appleCount")
        return
    battle_count_local = 0
    apple_count_local = 0
    try:
        running = True
        while running:
            for state in battle_state_list:
                capture = ui_util.get_new_capture()
                if state.match(capture):
                    if isinstance(state, SelectFriendState):
                        battle_count_local = battle_count_local + 1
                        common_util.write_log("start battle {}/{}".format(battle_count_local, battle_count))
                    if isinstance(state, AppleEatState):
                        apple_count_local = apple_count_local + 1
                        common_util.write_log("eat apple {}/{}".format(apple_count_local, apple_count))
                    if isinstance(state, BattleSettleConfirmState):
                        common_util.write_log("finish battle {}/{}".format(battle_count_local, battle_count))
                        if battle_count is not None and battle_count_local >= battle_count:
                            running = False
                            break
                        if apple_count is not None and apple_count_local >= apple_count:
                            running = False
                            break
                    state.execute()
                    time.sleep(1)
    except StopBattleException:
        common_util.write_log(
            "stop battle {}/{}(apple {}/{}) by StopBattleException".format(battle_count_local, battle_count,
                                                                           apple_count_local, apple_count))


class SimpleMatchAndClickState(interfaces.State):
    def __init__(self, template):
        super().__init__()
        self.template = template

    def match(self, capture_path):
        return cv_util.has_match(self.template, capture_path)

    def execute(self):
        common_util.write_log("SimpleMatchAndClick execute on {} , {}".format(self.template, type(self)))
        ui_util.match_and_click(self.template, delete_after_match=True)


class SelectLastRunState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_last_run_flag)


class SelectFriendState(interfaces.State):
    def __init__(self):
        super().__init__()

    def match(self, capture_path):
        return cv_util.has_match(resources.battle_friend_select_title, capture_path)

    def execute(self):
        ui_util.match_and_click(resources.battle_friend_select_normal_item)


class StartBattleState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_start_button)


class NormalTemplateBattleState(interfaces.State):
    def __init__(self, name, match_templates, runner_list, last_turn=False):
        super().__init__()
        self.name = name
        self.match_templates = match_templates
        self.runner_list = runner_list
        self.last_turn = last_turn

    def match(self, capture_path):
        if not cv_util.has_match(resources.battle_attack_button, capture_path):
            return False
        for t in self.match_templates:
            if cv_util.has_match(t, capture_path, match_threshold=0.94):
                common_util.write_log("battle {} match {}".format(self.name, capture_path))
                return True
        return False

    def execute(self):
        for runner in self.runner_list:
            runner.run(ui_util.get_new_capture())
        if not self.last_turn:
            time.sleep(5)
            _wait_for(resources.battle_attack_button, step=4)
        else:
            time.sleep(10)


class SkillRunner(interfaces.Runner):
    def __init__(self, skill_template, skill_index):
        self.skill_template = skill_template
        self.skill_index = skill_index

    def run(self, capture_path):
        common_util.delete_file(capture_path)
        common_util.write_log("use skill")
        _wait_for(self.skill_template)
        capture_path = ui_util.get_new_capture()
        max_val, tl_loc, br_loc = cv_util.match_template(self.skill_template, capture_path)
        common_util.delete_file(capture_path)
        if max_val < 0.6:
            return
        left, top, right, bottom = tl_loc[0], tl_loc[1], br_loc[0], br_loc[1]
        width = right - left
        item_width = width / 3
        center_y = (top + bottom) / 2
        for index in self.skill_index:
            x = left + item_width * (index - 1) + item_width / 2
            random_x = random.Random().randrange(start=-10, stop=10)
            random_y = random.Random().randrange(start=-10, stop=10)
            common_util.write_log(
                "click skill {}, origin_position = ({}, {}), random_delta = ({}, {})".format(index, x, center_y,
                                                                                             random_x,
                                                                                             random_y))
            ui_util.click(x + random_x, center_y + random_y)
            time.sleep(2)
            _wait_for(resources.battle_attack_button)


class SelectCardRunner(interfaces.Runner):

    def __init__(self, card_list):
        self.card_list = card_list

    def run(self, capture_path):
        common_util.write_log("select card")
        _wait_for(resources.battle_attack_button)
        ui_util.match_and_click(resources.battle_attack_button, delete_after_match=True)
        time.sleep(random.randrange(2, stop=4))
        selected_card_count = 0
        while selected_card_count < 3:
            for card in self.card_list:
                if ui_util.match_and_click(card, delete_after_match=True):
                    selected_card_count = selected_card_count + 1
                    common_util.write_log("select card {}".format(selected_card_count))
                    time.sleep(random.randrange(2, stop=3))
                    break


class BattleSettleJiBanState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_jiban_title)

    def execute(self):
        _wait_for(resources.battle_click_ui_tip)
        super().execute()


class BattleSettleExpState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_exp_title)

    def execute(self):
        _wait_for(resources.battle_click_ui_tip)
        super().execute()


class BattleSettleConfirmState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_finish_next_step_button)


class BattleQuickStartState(SimpleMatchAndClickState):
    def __init__(self):
        super().__init__(resources.battle_go_on_button)


class AppleEatState(interfaces.State):
    def match(self, capture_path):
        return cv_util.has_match(resources.item_sliver_apple, capture_path)

    def execute(self):
        ui_util.match_and_click(resources.item_sliver_apple)
        _wait_for(resources.apple_eat_dialog_confirm_button, step=1)
        ui_util.match_and_click(resources.apple_eat_dialog_confirm_button)
        time.sleep(2)


class CardSelectExceptionState(interfaces.State):

    def match(self, capture_path):
        return cv_util.has_match(resources.battle_speed_set_button, capture_path)

    def execute(self):
        for card in [resources.action_buster, resources.action_arts, resources.action_quick]:
            if ui_util.match_and_click(card):
                break


class UsedSkillClickDialogState(interfaces.State):
    def match(self, capture_path):
        return cv_util.has_match(resources.skill_used_click_dialog_title, capture_path)

    def execute(self):
        ui_util.match_and_click(resources.cancel_button)
        _wait_for(resources.battle_attack_button, step=1)


class ServantClickedStatusDialogState(interfaces.State):
    def match(self, capture_path):
        return cv_util.has_match(resources.servant_selected_ststus_title, capture_path)

    def execute(self):
        ui_util.match_and_click(resources.close_button)
        _wait_for(resources.battle_attack_button, step=1)


class ServantCountOverflowDialogState(interfaces.State):

    def match(self, capture_path):
        return cv_util.has_match(resources.need_release_space_buttons, capture_path)

    def execute(self):
        common_util.notify_release_space()
        raise StopBattleException()


class StopBattleException(Exception):
    pass


class CheckNpBattleState(interfaces.State):

    def __init__(self, name, match_templates, use_skill=False):
        super().__init__()
        self.name = name
        self.match_templates = match_templates
        self.use_skill = use_skill

    def match(self, capture_path):
        if not cv_util.has_match(resources.battle_attack_button, capture_path):
            return False
        for t in self.match_templates:
            if cv_util.has_match(t, capture_path, match_threshold=0.94):
                common_util.write_log("battle {} match {}".format(self.name, capture_path))
                return True
        return False

    def execute(self):
        _wait_for(resources.battle_attack_button)
        # if self.use_skill:
        #     skill_list = [resources.skill_single_np_up, resources.skill_single_defense_up,
        #                   resources.skill_single_attack_up]
        #     skill_used_state = ServantClickedStatusDialogState()
        #     for skill in skill_list:
        #         if skill_used_state.match(ui_util.get_new_capture()):
        #             skill_used_state.execute()
        #         _wait_for(resources.battle_attack_button)
        #         ui_util.match_and_click(skill, match_threshold=0.9)
        #     if skill_used_state.match(ui_util.get_new_capture()):
        #         skill_used_state.execute()
        # _wait_for(resources.battle_attack_button)
        max_val, tl_loc, br_loc = cv_util.match_template(resources.np_progress_full, ui_util.get_new_capture())
        print("match baoju", max_val, tl_loc, br_loc, config.window_size)
        baoju_position = -1
        if max_val > 0.9:
            center_x = (br_loc[0] + tl_loc[0]) / 2
            window_w = config.window_size[0]
            if window_w is not None and window_w > 0:
                p = center_x / window_w
                print(property)
                if p < 1 / 4:
                    baoju_position = 0
                elif p < 2 / 4:
                    baoju_position = 1
                elif p < 3 / 4:
                    baoju_position = 2
        print("baoju rsult ", baoju_position)
        ui_util.match_and_click(resources.battle_attack_button)
        time.sleep(3)
        _wait_for(resources.battle_speed_set_button)
        while cv_util.has_match(resources.battle_speed_set_button, ui_util.get_new_capture()):
            if baoju_position != -1:
                position_set = [(250, 250), (400, 250), (550, 250)]
                ui_util.click(position_set[baoju_position][0] + random.randrange(-10, 10),
                              position_set[baoju_position][1] + random.randrange(-10, 10))
                baoju_position = -1
                time.sleep(3)
            for card in [resources.action_buster, resources.action_arts, resources.action_quick]:
                if ui_util.match_and_click(card):
                    time.sleep(3)
                    break
