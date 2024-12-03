#!/usr/bin/env python3

import os
import re

def solve_part1(long_string: str) -> int:
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, long_string)

    result = []
    for num1, num2 in matches:
        result.append(int(num1) * int(num2))

    total = sum(result)

    return total

def solve_part2(long_string: str) -> int:
    pattern = r"(do\(\)|don't\(\))|mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, long_string)

    result = []
    do_multiply = True
    for action, num1, num2 in matches:
        
        if num1 != "" and num2 != "" and do_multiply:
            result.append(int(num1) * int(num2))
        
        if action == "don't()":
            do_multiply = False
        elif action == "do()":
            do_multiply = True

    total = sum(result)

    return total


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_string = file.read()

    part_one_solution = solve_part1(problem_string)
    print(part_one_solution)
    assert(part_one_solution == 189600467)

    part_two_solution = solve_part2(problem_string)
    print(part_two_solution)
    assert(part_two_solution == 107069718)