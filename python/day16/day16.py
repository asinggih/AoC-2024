#!/usr/bin/env python3

import os
import sys


def find_possbile_paths(puzzle):
    rows, cols = len(puzzle), len(puzzle[0])
    result = []
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1), # Left
        (-1, 0)  # Up
    ]

    def is_valid(r, c, visited):
        return (
            1 <= r < rows and
            1 <= c < cols and
            (puzzle[r][c] == "." or puzzle[r][c] == "E") and
            (r, c) not in visited
        )

    def dfs(path, r, c, visited):
        # path.append((r, c))
        # visited.add((r, c))

        # if puzzle[r][c] == "E":
        #     result.append(path[:-1])  # Make a copy of the path

        # else:
        #     for dr, dc in directions:
        #         new_r, new_c = r + dr, c + dc
        #         if is_valid(new_r, new_c, visited):
        #             dfs(path, new_r, new_c, visited)

        # # Backtrack
        # path.pop()
        # visited.remove((r, c))
        stack = [(path, r, c, visited)]

        while stack:
            current_path, current_r, current_c, current_visited = stack.pop()
            current_path.append((current_r, current_c))
            current_visited.add((current_r, current_c))

            if puzzle[current_r][current_c] == "E":
                result.append(current_path[:-1])  # Make a copy of the path
            else:
                for dr, dc in directions:
                    new_r, new_c = current_r + dr, current_c + dc
                    if is_valid(new_r, new_c, current_visited):
                        stack.append((current_path[:], new_r, new_c, current_visited.copy()))

            # Backtrack
            current_path.pop()
            current_visited.remove((current_r, current_c))

    # Start DFS if the start and end cells are passable
    # if puzzle[0][0] == 0 and puzzle[rows - 1][cols - 1] == 0:
    start_r = len(puzzle)-2
    start_c = 1
    dfs([], start_r, start_c, set())

    return result

# (13, 1), (12, 1), (11, 1), (10, 1), (9, 1), (9, 2), (9, 3)
def get_trend(point_a: tuple, point_b: tuple) -> str:
    col_diff = abs(point_a[0]-point_b[0])
    if col_diff == 1:
        trend = "v"
    else:
        trend = "h"

    return trend

def get_score(possible_path: list) -> int:
    base_score = len(possible_path)
    bonus = 1000

    multiplier = 1
    trend = "v"
    for idx in range(len(possible_path)-1):
        point_a = possible_path[idx]
        point_b = possible_path[idx+1]

        current_trend = get_trend(point_a, point_b)

        if current_trend != trend:
            multiplier += 1
            trend = current_trend
        
    return bonus*multiplier + base_score


def solve_part1(puzzle: list) -> int:

    possible_paths = find_possbile_paths(puzzle)

    all_scores = []
    for possibility in possible_paths:
        score = get_score(possibility)
        all_scores.append(score)
        # print(possibility)
        # print(len(possibility))
        # print()

    # print(all_scores)
    return min(all_scores)

def solve_part2(input_string: str) -> int:
    pass


if __name__ == "__main__":
    # sys.setrecursionlimit(10**6)
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        puzzle = file.read().splitlines()

    part_one_solution = solve_part1(puzzle)
    print(part_one_solution)
    # print(sys.getrecursionlimit())
    # assert(part_one_solution == 189600467)

    # part_two_solution = solve_part2(problem_string)
    # print(part_two_solution)
    # assert(part_two_solution == 107069718)