from lib.battle import atomic_tasks
from lib.base import resources


def build_normal_daily_exp_task_set():
    return [
        atomic_tasks.EatAppleTask(),
        atomic_tasks.SelectLastRunTask(),
        atomic_tasks.SimpleMatchAndClickTask(resources.launch_exp_ap_40_unpass),
        atomic_tasks.SimpleMatchAndClickTask(resources.launch_exp_ap_40_passed),
        atomic_tasks.RandomSelectFriendTask(),
        atomic_tasks.ClickStartBattleTask(),

        atomic_tasks.BattleClickSkillTask(resources.skill_avenger_yste, [1, 3], turn_num=1),
        atomic_tasks.BattleClickSkillTask(resources.skill_berserker_sbd, [2, 3], turn_num=2),
        atomic_tasks.BattleClickSkillTask(resources.skill_berserker_azn, [1, 2], turn_num=3),

        atomic_tasks.BattleClickAttackTask(),

        atomic_tasks.BattleSelectActionCardTask(special_templates={
            1: [resources.action_final_avenger_yste],
            2: [resources.action_final_berserker_sbd],
            3: [resources.action_final_berserker_azn]
        }),

        atomic_tasks.BattleSettleJiBanTask(),
        atomic_tasks.BattleSettleExpTask(),
        atomic_tasks.BattleSettleConfirmTask(),
        atomic_tasks.BattleQuickStartTask(),

        atomic_tasks.UsedSkillClickDialogTask(),
        atomic_tasks.ServantClickedStatusDialogTask(),
        atomic_tasks.ServantCountOverflowDialogTask(),
    ]
