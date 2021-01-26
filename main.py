import battle
import resources

# 刷狗粮
battle_list = [
    battle.SelectLastRunState(),
    battle.SelectFriendState(),
    battle.StartBattleState(),
    battle.BattleState(name="Battle1", match_templates=[resources.battle_turn_1_of_3],
                       runner_list=[battle.SkillRunner(resources.skill_avenger_yste, [1, 3]),
                                    battle.SelectCardRunner(
                                        [resources.action_final_avenger_yste, resources.action_buster,
                                         resources.action_arts, resources.action_quick]
                                    )]
                       ),
    battle.BattleState(name="Battle2", match_templates=[resources.battle_turn_2_of_3],
                       runner_list=[battle.SkillRunner(resources.skill_berserker_sbd, [2, 3]),
                                    battle.SelectCardRunner(
                                        [resources.action_final_berserker_sbd, resources.action_buster,
                                         resources.action_arts, resources.action_quick]
                                    )]
                       ),
    battle.BattleState(name="Battle3", match_templates=[resources.battle_turn_3_of_3],
                       runner_list=[battle.SkillRunner(resources.skill_berserker_azn, [1, 2]),
                                    battle.SelectCardRunner(
                                        [resources.action_final_berserker_azn, resources.action_buster,
                                         resources.action_arts, resources.action_quick]
                                    )],
                       last_turn=True
                       ),
    battle.BattleSettleJiBanState(),
    battle.BattleSettleExpState(),
    battle.BattleSettleConfirmState(),
    battle.BattleQuickStartState(),
    battle.AppleEatState(),
    battle.CardSelectExceptionState(),
    battle.UsedSkillClickDialogState(),
    battle.ServantClickedStatusDialogState(),
    battle.ServantCountOverflowDialogState()
]
battle.battle(battle_list, battle_count=300)
