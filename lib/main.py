from battle import task_runner, task_set

if __name__ == '__main__':
    task_runner.run_tasks(task_set.build_normal_daily_exp_task_set())
    # print(config.project_path)
