from lib.base import ui_util
import time
import random
import lib.battle.global_status as global_status
import lib.battle.atomic_tasks as atomic_tasks


def run_tasks(tasks, battle_count=None, apple_count=None):
    try:
        running = True
        while running:
            capture = ui_util.get_new_capture()
            for task in tasks:
                if apple_count is not None and apple_count == global_status.apple_eat_count:
                    running = False
                    break
                if battle_count is not None and battle_count == global_status.loop_number:
                    running = False
                if task.accept(capture):
                    task.execute(capture)
                    capture = ui_util.get_new_capture()
                    time.sleep(random.randrange(0, 2))
        print("****** finished !! *******")
    except atomic_tasks.StopBattleException:
        print("****** finished by error ********")
