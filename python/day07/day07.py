#!/usr/bin/env python3

import sys
import os
import logging
from itertools import product

logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler(sys.stdout))

def generate_combos(nums_list: list, ops: list) -> list:
    
    # use cartesian product to generate all combos
    operator_combinations = product(ops, repeat=len(nums_list) - 1)
    
    expressions = []
    for operators in operator_combinations:
        # logger.debug(operators)
        expression = []
        for idx in range(len(nums_list)):
            if idx < len(operators):
                # expression += str(nums_list[idx]) + operators[idx]
                expression.append(nums_list[idx])
                expression.append(operators[idx])
            else: # for the last item
                expression.append(nums_list[idx])
                
        expressions.append(expression)
        
    return expressions


def handle_concat(result: int, num:int) -> int:    
    return int(str(result)+str(num))

def get_result(expressions: list, ops: list) -> int:
    logger.debug(f"expressions: {expressions}")
    # init first result with first number
    result = expressions[0]
    ops_stack = []
    for item in expressions[1:]:
        
        if item in ops:
            ops_stack.append(item)
            continue
        
        if ops_stack != []:
            operator = ops_stack.pop()
            
            if operator == "+":
                result += item
            elif operator == "*":
                result *= item
            else:
                result = handle_concat(result, item)
    
    logger.debug(f"this is the result: {result}")
    return result


def valid_combo(target: int, nums_list: list, possible_combos: list, ops: list) -> bool:

    # quick check
    if sum(nums_list) == target: 
        logger.info(f"sum of: {nums_list}")
        return True
    total = 1
    for item in nums_list:
        total *= item
    if total == target: 
        logger.info(f"mul of: {nums_list}")
        return True

    for combo in possible_combos:
        result = get_result(combo, ops)
        if result == target:
            logger.info(f"combo: {combo}")
            return True

    return False

def _solve_problem(calibrations_list: list, ops:list) -> int:

    hash_lookup = dict()
    calibration_map = dict()

    for idx, line in enumerate(calibrations_list):
        calibration = line.split(":")

        result = int(calibration[0])
        hashed_result = hash((result, idx))
        hash_lookup[hashed_result] = (result, idx)
        calibration_map[hashed_result] = [int(num) for num in calibration[1].split()]

    valid_calibrations = []
    invalid_calibrations = []
    for hashed_result, nums_list in calibration_map.items():

        result = hash_lookup[hashed_result][0]

        logger.info(f"target: {result}")
        possible_combos = generate_combos(nums_list, ops)
        is_valid = valid_combo(result, nums_list, possible_combos, ops)
        if is_valid:
            valid_calibrations.append(result)
        else:
            invalid_calibrations.append(result)
        logger.info("")

    total = sum(valid_calibrations)
    logger.info("==============================================")
    logger.debug(f"Valid Calibrations: {valid_calibrations}")
    # logger.info(f"Total: {total}")

    # logger.info(f"Invalid Calibrations: {invalid_calibrations}")

    return total

def solve_part1(calibrations_list: list) -> int:
    return _solve_problem(calibrations_list, ['+', '*'])


def solve_part2(calibrations_list: list) -> int:
    return _solve_problem(calibrations_list, ['+', '*', '||'])


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_list = file.read().splitlines()

    part_one_solution = solve_part1(problem_list)
    print(f"Total calibration result: {part_one_solution}")
    assert(part_one_solution == 4122618559853)
    print("") 
 
    part_two_solution = solve_part2(problem_list)
    print(f"Total calibration result: {part_two_solution}")
    assert(part_two_solution == 227615740238334)
