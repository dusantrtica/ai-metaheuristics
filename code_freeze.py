import os
import re

algorithms = [
    "algo_auto_assign_multi_problem",
    "algo_auto_assign_single_problem",
    "algo_auto_schedule_multi_problem",
    "algo_auto_schedule_single_problem",
    "algo_production_labour_planning_multi_problem",
    "algo_production_labour_planning_single_problem",
    "algo_demand_forecasting"
]


def create_commands(sprint_number):
    checkout_master_cmd = "git checkout master"
    commands = ["git checkout master", "git pull"]

    for algorithm in algorithms:
        commands.extend(create_commands_set_for_algo(algorithm, sprint_number))
        commands.append(checkout_master_cmd)

    return commands


def run_commands(commands):
    def is_error(error_code): return error_code != 0

    for command in commands:
        return_code = os.system(command)
        if is_error(return_code):
            print('Aborting.')
            break


def create_commands_set_for_algo(algorithm, sprint_number):
    base_checkout_cmd = "git checkout -b"
    base_push_cmd = "git push --set-upstream origin"

    new_branch_name = f"{algorithm}-release/0{sprint_number}"
    checkout_branch_cmd = f"{base_checkout_cmd} {new_branch_name}"
    push_branch_cmd = f"{base_push_cmd} {new_branch_name}"

    return [checkout_branch_cmd, push_branch_cmd]


def confirm_action(get_input):
    proceed = get_input('You are about to start code freeze for all algorithms. Continue? (yes/no) ')
    if proceed.lower() not in ['yes', 'no']:
        return confirm_action(get_input)
    return proceed.lower() == 'yes'


def get_and_verify_sprint_number(get_input):
    release_number = get_input("Please enter sprint number you are releasing for (ex. 154): ")
    if not re.match("[0-9]{3}", release_number):
        return get_and_verify_sprint_number(get_input)
    return release_number


def prompt_action_and_verify_sprint_number(get_input):
    should_proceed = confirm_action(get_input)
    if should_proceed:
        sprint_number = get_and_verify_sprint_number(get_input)
        return sprint_number


if __name__ == '__main__':
    sprint_number = prompt_action_and_verify_sprint_number(input)
    if sprint_number:
        code_freeze_commands = create_commands(sprint_number)
        run_commands(code_freeze_commands)
