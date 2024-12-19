#!/usr/bin/env python3

import os

cache = dict()

def rules(num: str) -> list:
    # print(f"num is {num}")
    if num in cache:
        # print("cached num found")
        return cache[num]

    num_length = len(num)
    new_num = []
    
    if num == "0":
        new_num.append("1")
        return new_num
    
    elif num_length % 2 == 0:
        mid = int(num_length / 2)
        left_num = str(int(num[0:mid]))
        right_num = str(int(num[mid:num_length]))
        new_num.append(left_num)
        new_num.append(right_num)

    else:
        new_num.append(str(int(num)*2024))

    cache[num] = new_num
    return new_num

def update_or_cache(cache: dict, num: int, count: int):
    if num in cache:
        cache[num] += count
    else:
        cache[num] = count
    return


def generate_stones(cache: dict) -> dict:
    
    new_cache = dict()
    
    for num, count in cache.items():
        # print(f"num is {num} count is {count}")
        num_length = len(num)
        
        if num == "0":
            new_num = "1"
            update_or_cache(new_cache, new_num, count)
        
        elif num_length % 2 == 0:
            mid = int(num_length / 2)
            left_num = str(int(num[0:mid]))
            right_num = str(int(num[mid:num_length]))
            update_or_cache(new_cache, left_num, count)
            update_or_cache(new_cache, right_num, count)

        else:
            new_num = str(int(num)*2024)
            update_or_cache(new_cache, new_num, count)

    return new_cache


def generate_new_list(num_list: list, count:int, blinks:int) -> list:
    
    if count == blinks:
        return num_list

    new_list = []
    for num in num_list:
        new_num_list = rules(num)
        for new_num in new_num_list:
            new_list.append(new_num)

    count += 1
    # print(f"count: {count} | {new_list}")
    return generate_new_list(new_list, count, blinks)


def solve_part1(num_list: list) -> int:
    blinks = 75
    new_list = generate_new_list(num_list, 0, blinks)
    return len(new_list)



def solve_part2(num_list: list) -> int:
    
    new_stones = dict()
    for item in num_list:
        new_stones[item] = 1
    
    blinks = 75
    for _ in range(blinks):
        new_stones = generate_stones(new_stones)

    return sum(new_stones.values())


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_string = file.read().split(" ")

    part_one_solution = solve_part1(problem_string)
    print(part_one_solution)
    assert(part_one_solution == 209412)

    # part_two_solution = solve_part2(problem_string)
    # print(part_two_solution)
    # assert(part_two_solution == 248967696501656)