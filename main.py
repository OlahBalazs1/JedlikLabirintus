import random

# left, down, right, up
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
WALL_CHECK_MASKS = [0b0001, 0b0010, 0b0100, 0b1000]
WALL_BREAK_MASKS = [0b1110, 0b1101, 0b1011, 0b0111]

def step_to_square_mask(earlier_direction: tuple, later_direction: tuple) -> tuple:
    return 0b1111 & WALL_BREAK_MASKS[DIRECTIONS.index(earlier_direction)] & WALL_BREAK_MASKS[DIRECTIONS.index(later_direction)]
    

def add_vector_to_position(position, vector) -> list:
    return position[0] + vector[0], position[1] + vector[1]

def position_delta(earlier_position, later_position) -> tuple:
    return later_position[0] - earlier_position[0], later_position[1] - earlier_position[1]

def next_step(previous_steps: list, max_x: int, max_y: int) -> tuple:
    next = add_vector_to_position(previous_steps[-1], random.choice(DIRECTIONS))
    while next == previous_steps[-1] or next[0] not in range(0, max_x + 1) or next[1] not in range(0, max_y + 1):
#        print("Anyád")
        next = add_vector_to_position(previous_steps[-1], random.choice(DIRECTIONS))
    while next in previous_steps:
        del previous_steps[-1]

    previous_steps.append(next)
    
    return previous_steps

def random_inactive_position(max_x: int, max_y: int, active_positions: set) -> tuple:
    rand_x = -1
    rand_y = -1
    while True: 
        rand_x = random.randint(0, max_x)
        rand_y = random.randint(0, max_y)
        if (rand_x, rand_y) not in active_positions: 
            return (rand_x, rand_y)

# az algoritmust ezen forrásokból állítottam össze:
# https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm
def new_maze(szelesseg: int, magassag: int) -> list:
    maze = {random_inactive_position(szelesseg -1, magassag -1, set())}
    raster_maze = [[0b1111 for _ in range(szelesseg)] for _ in range(magassag)]

    while len(maze) < szelesseg * magassag:
        start_pos = random_inactive_position(szelesseg -1, magassag -1, maze)
        steps = []
        steps.append(start_pos)
        steps.append(add_vector_to_position(start_pos, random.choice(DIRECTIONS)))
#        print(raster_maze)
        while steps[-1] not in maze:
#            print(steps)
            steps = next_step(steps, szelesseg -1, magassag - 1)
#            print("something happened")
        raster_maze[steps[-1][0]][steps[-1][1]] &=  WALL_BREAK_MASKS[DIRECTIONS.index(position_delta(steps[-2], steps[-1])) - 2]
        
        while len(steps) != 2:
            print(raster_maze)
            maze.add(steps[0])
            raster_maze[steps[-1][0]][steps[-1][1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(position_delta(steps[0], steps[1]))]
            if len(steps) != 3:
                del steps[0]
        
        
    return raster_maze


for i in new_maze(10, 10):
    print(" ".join(map(lambda x: str(x), i)))