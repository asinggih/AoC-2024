#!/usr/bin/env python3

import os

def solve_part1(location_ids: list) -> int:
    first_list = []
    second_list = []

    for pair in location_ids:
        combo = pair.split()
        first_list.append(int(combo[0]))
        second_list.append(int(combo[1]))

    first_list.sort()
    second_list.sort()

    diff_list = []
    for idx in range(len(first_list)):
        first_num = first_list[idx]
        second_num = second_list[idx]

        diff = abs(first_num-second_num)
        diff_list.append(diff)
    
    total = sum(diff_list)

    return total

def solve_part2(location_ids: list) -> int:
    first_list = []
    lookup_table = dict()

    for pair in location_ids:
        combo = pair.split()
        first_list.append(int(combo[0]))
        
        lookup_key = int(combo[1])
        if lookup_key in lookup_table:
            lookup_table[lookup_key] += 1
        else:
            lookup_table[lookup_key] = 1


    scores = []
    for num in first_list:
        score = 0
        if num in lookup_table:
            score = num * lookup_table[num]
        scores.append(score)

    total = sum(scores)

    return total


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_list = file.read().splitlines()

    part_one_solution = solve_part1(problem_list)
    assert(part_one_solution == 2344935)
    print(part_one_solution)

    part_two_solution = solve_part2(problem_list)
    assert(part_two_solution == 27647262)
    print(part_two_solution)