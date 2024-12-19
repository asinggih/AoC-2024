#!/usr/bin/env python3

import sys
import os
from dataclasses import dataclass
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

VISITED_MAP = set()


@dataclass
class State:
    x: int
    y: int
    direction: str


def _generate_map(loc_map: list) -> tuple:
    target = "^"
    obstacle = "#"

    obstacles_locations_x = dict()
    obstacles_locations_y = dict()
    for i in range(len(loc_map)):
        for j in range(len(loc_map[i])):
            point = loc_map[i][j]
            if point == obstacle:
                # { 
                #   0: [4, 6] 
                # }
                if i in obstacles_locations_x:
                    obstacles_locations_x[i].append(j)
                else:
                    obstacles_locations_x[i] = [j]

                if j in obstacles_locations_y:
                    obstacles_locations_y[j].append(i)
                else:
                    obstacles_locations_y[j] = [i]

            elif point == target:
                starting_state = State(i, j, "U")

    # make sure
    for values in obstacles_locations_x.values():
        values.sort()
    for values in obstacles_locations_y.values():
        values.sort()

    starting_state.obstacles_locations_x = obstacles_locations_x

    return obstacles_locations_x, obstacles_locations_y, starting_state


def _get_bounds(num: int, list_of_obs) -> tuple:
    lower_bound = None
    upper_bound = None

    for obs in list_of_obs:
        if obs <= num:
            lower_bound = obs
        if obs > num and upper_bound is None:
            upper_bound = obs
            break

    return lower_bound, upper_bound

@dataclass
class Direction:
    direction: str
    limit: int


# config = {
#     "U": {
        
#     }
# }

def _move(starting_state: State, obs_x: dict, obs_y: dict) -> State:
    direction = starting_state.direction
    x, y = starting_state.x, starting_state.y

    move_functions = {
        "U": __move_vertical,
        "D": __move_vertical,
        "R": __move_horizontal,
        "L": __move_horizontal
    }

    if direction == "U" or direction == "D":
        return __move_vertical(x, y, direction, obs_y, max_x=len(obs_y))
    return __move_horizontal(x, y, direction, obs_x, max_y=len(obs_y))

def __move_vertical(x:int, y:int, direction:str, obs_y:dict, max_x:int):
    is_up = direction == "U"
    list_of_obs = obs_y.get(y, [])
    lower_bound, upper_bound = _get_bounds(x, list_of_obs)
    
    if is_up:
        limit = lower_bound if lower_bound is not None and lower_bound < x else -1
        new_direction = "R" if limit != -1 else "EXIT"
        step = -1
    else:
        limit = upper_bound if upper_bound is not None and upper_bound > x else max_x + 2
        new_direction = "L" if limit != max_x + 2 else "EXIT"
        step = 1

    for i in range(x, limit, step):
        VISITED_MAP.add(f"{i},{y}")

    return State(limit + (1 if is_up else -1), y, new_direction)

def __move_horizontal(x:int, y:int, direction:str, obs_x, max_y):
    is_right = direction == "R"
    list_of_obs = obs_x.get(x, [])
    lower_bound, upper_bound = _get_bounds(y, list_of_obs)
    
    if is_right:
        limit = upper_bound if upper_bound is not None and upper_bound > y else max_y + 2
        new_direction = "D" if limit != max_y + 2 else "EXIT"
        step = 1
    else:
        limit = lower_bound if lower_bound is not None and lower_bound < y else -1
        new_direction = "U" if limit != -1 else "EXIT"
        step = -1

    for i in range(y, limit, step):
        VISITED_MAP.add(f"{x},{i}")

    return State(x, limit + (1 if not is_right else -1), new_direction)


# 0 ....#.....
# 1 .........#
# 2 ..........
# 3 ..#.......
# 4 .......#..
# 5 ..........
# 6 .#..^.....
# 7 ........#.
# 8 #.........
# 9 ......#...
def solve_part2(input_list: list) -> int:
    x = len(input_list[0])
    y = len(input_list)

    obstacles_locations_x, obstacles_locations_y, starting_state = _generate_map(input_list)

    logging.debug(f"obs_x:{obstacles_locations_x}")
    logging.debug(f"obs_y:{obstacles_locations_y}")
    logging.debug(f"x:{starting_state.x} , y:{starting_state.y}")
    logging.debug("")

    # latest_state = _move(State(x=7, y=7, direction='D'), obstacles_locations_x, obstacles_locations_y)
    latest_state = _move(starting_state, obstacles_locations_x, obstacles_locations_y)
    while latest_state.direction != "EXIT":
        logging.debug(latest_state)
        latest_state = _move(latest_state, obstacles_locations_x, obstacles_locations_y)

    logging.debug(VISITED_MAP)
    return len(VISITED_MAP)


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_string = file.read().splitlines()

    part2_solution = solve_part2(problem_string)
    print(part2_solution) # 4982
