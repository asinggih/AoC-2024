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

def _get_bounds(num:int, list_of_obs) -> tuple:
    
    lower_bound = None
    upper_bound = None
    
    for obs in list_of_obs:
        if obs <= num:
            lower_bound = obs
        if obs > num and upper_bound is None:
            upper_bound = obs
            break
    
    return lower_bound, upper_bound


def _move(starting_state: State, obs_x: dict, obs_y: dict) -> State:

    if starting_state.direction == "U":
        # look at the y axis
        if starting_state.y in obs_y:
            list_of_obs = obs_y[starting_state.y]
            bounds = _get_bounds(starting_state.x, list_of_obs)
            closest_obs = bounds[0]
            try:
                obs_in_path = closest_obs < starting_state.x
                if obs_in_path:
                    x_limit = closest_obs # will stop 1 block below the obstacle + 1
                    direction = "R"
            except:
                x_limit = -1
                direction = "EXIT"
        else:
            x_limit = -1
            direction = "EXIT"

        for i in range(starting_state.x, x_limit, -1):
            visited = f"{str(i)},{starting_state.y}"
            logging.debug(visited)
            VISITED_MAP.add(visited)
        
        latest_state = State(x_limit+1, starting_state.y, direction)

    # latest state: State(x=1, y=4, direction='R')
    elif starting_state.direction == "R":
        # look at the x axis
        if starting_state.x in obs_x:
            list_of_obs = obs_x[starting_state.x]
            bounds = _get_bounds(starting_state.y, list_of_obs)
            closest_obs = bounds[1]
            try:
                obs_in_path = closest_obs > starting_state.y
                if obs_in_path:
                    y_limit = closest_obs # will stop 1 block left of the obstacle
                    direction = "D"
            except:
                y_limit = len(obs_y)+2
                direction = "EXIT"

        else:
            y_limit = len(obs_y)+2
            direction = "EXIT"

        for i in range(starting_state.y, y_limit, 1):
            visited = f"{starting_state.x},{str(i)}"
            logging.debug(visited)
            VISITED_MAP.add(visited)
        
        latest_state = State(starting_state.x, y_limit-1, direction)

    # State(x=1, y=8, direction='D')
    elif starting_state.direction == "D":
        # look at the y axis
        if starting_state.y in obs_y:
            list_of_obs = obs_y[starting_state.y]
            bounds = _get_bounds(starting_state.x, list_of_obs)
            logging.debug(f"boudns are: {bounds}")
            closest_obs = bounds[1]
            try:
                obs_in_path = closest_obs > starting_state.x
                if obs_in_path:
                    x_limit = closest_obs # will stop 1 block above the obstacle - 1
                    direction = "L"
            except:
                print("here")
                x_limit = len(obs_x)+2
                direction = "EXIT"

        else:
            x_limit = len(obs_x)+2
            direction = "EXIT"

        # print(f"x limit is {x_limit}")
        for i in range(starting_state.x, x_limit):
            visited = f"{str(i)},{starting_state.y}"
            logging.debug(visited)
            VISITED_MAP.add(visited)
    
        latest_state = State(x_limit-1, starting_state.y, direction)

    # State(x=6, y=8, direction='L')
    elif starting_state.direction == "L":
        # look at the x axis
        if starting_state.x in obs_x:
            list_of_obs = obs_x[starting_state.x]
            bounds = _get_bounds(starting_state.y, list_of_obs)
            closest_obs = bounds[0]
            try:
                obs_in_path = closest_obs < starting_state.y
                if obs_in_path:
                    y_limit = closest_obs # will stop 1 block left of the obstacle
                    direction = "U"
            except:
                y_limit = -1
                direction = "EXIT"
        else:
            y_limit = -1
            direction = "EXIT"

        # print(f"y limit is {y_limit}")
        for i in range(starting_state.y, y_limit, -1):
            visited = f"{starting_state.x},{str(i)}"
            logging.debug(visited)
            VISITED_MAP.add(visited)
        
        # print("in dir L")
        # print(VISITED_MAP)
        latest_state = State(starting_state.x, y_limit+1, direction)

    return latest_state

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
def solve_part1(input_list: list) -> int:

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

def solve_part2(input_list: list) -> int:
    pass


if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(directory, "input.txt"), encoding="utf-8") as file:
        problem_string = file.read().splitlines()

    part_one_solution = solve_part1(problem_string)
    print(part_one_solution)
    assert(part_one_solution == 4982)


