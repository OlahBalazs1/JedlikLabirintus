import random

# left, down, right, up
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
WALL_BREAK_MASKS = [0b1110, 0b1101, 0b1011, 0b0111]
WALL_CHECK_MASKS = [~a for a in WALL_BREAK_MASKS]

def add_offset(position, vector) -> tuple:
    return position[0] + vector[0], position[1] + vector[1]

def random_direction_in_bounds(current_pos: tuple, max_x: int, max_y: int) -> tuple:
    valid_ones = []
    for i in DIRECTIONS:
        if add_offset(i, current_pos)[0] in range(0, max_x + 1) and add_offset(i, current_pos)[1] in range(0, max_y + 1):
            valid_ones.append(i)

    return random.choice(valid_ones)

def new_loop(start_pos: tuple, active_positions: set, max_x: int, max_y: int) -> list:
    path_raster = [[(0, 0) for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    head = start_pos
    next_dir = random_direction_in_bounds(head, max_x, max_y)
    # dir_to_previous = DIRECTIONS[DIRECTIONS.index(next_dir) - 2]
    
    while head not in active_positions:
        neighbors = []
        dir_to_previous = DIRECTIONS[DIRECTIONS.index(next_dir) - 2]

        for i in DIRECTIONS:
            if i != dir_to_previous and add_offset(head, i)[0] in range(0, max_x + 1) and add_offset(head, i)[1] in range(0, max_y + 1):
                neighbors.append(i)
        next_dir = random.choice(neighbors)

        path_raster[head[0]][head[1]] = next_dir
        if add_offset(head, next_dir) in active_positions:
            return path_raster
        head = add_offset(head, next_dir)
    
    return path_raster


def random_inactive_position(max_x: int, max_y: int, active_positions: set) -> tuple:
    rand_x = random.randint(0, max_x)
    rand_y = random.randint(0, max_y)
    while (rand_x, rand_y) in active_positions: 
        rand_x = random.randint(0, max_x)
        rand_y = random.randint(0, max_y)
    return (rand_x, rand_y)

def pick_end(maze, start_pos) -> tuple:
    visited_squares = set()
    next_squares = [start_pos]
    furthest_ends = []

    while len(visited_squares) < (len(maze) * len(maze[0])): 
        furthest_ends = []
        visitable_neighbours = []

        for square in next_squares:
            if maze[square[0]][square[1]] in WALL_BREAK_MASKS:
                furthest_ends.append(square)
                
            for (index, i) in enumerate(WALL_CHECK_MASKS):
                if maze[square[0]][square[1]] & 0b1111 & i == 0 and add_offset(square, DIRECTIONS[index]) not in visited_squares:
                    visitable_neighbours.append(add_offset(square, DIRECTIONS[index]))
            visited_squares.add(square)

        next_squares = []
        for i in visitable_neighbours:
            next_squares.append(i)

    return random.choice(furthest_ends)


# az algoritmust ezen forrásokból állítottam össze:
# https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm
# https://weblog.jamisbuck.org/2011/1/17/maze-generation-aldous-broder-algorithm
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
def new_maze(width: int, height: int) -> list:
    active_cells = {(random.randint(0, width - 1), 0)}
    raster_maze = [[0b1111 for _ in range(height)] for _ in range(width)]

    ABo_head = list(active_cells)[0]

    while len(active_cells) < int((width * height) * 0.33):
        next_dir = random_direction_in_bounds(ABo_head, width -1, height -1)
        if add_offset(ABo_head, next_dir) in active_cells:
            ABo_head = add_offset(ABo_head, next_dir)
        else:
            raster_maze[ABo_head[0]][ABo_head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index((next_dir))]
            ABo_head = add_offset(ABo_head, next_dir)
            raster_maze[ABo_head[0]][ABo_head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index((next_dir)) - 2]
        active_cells.add(ABo_head)


    while len(active_cells) < width * height:
        # start_pos = (4,1)
        # start_pos = random_inactive_position(width - 1, height -1, active_cells)
        head = random_inactive_position(width - 1, height -1, active_cells)
        # head = (4, 4)
        path_raster = new_loop(head, active_cells, width -1, height -1, )
        last_dir = (0,0)
        head_dir = (-1, -1)
        while head_dir != (0,0):
            head_dir = path_raster[head[0]][head[1]]
            active_cells.add(head)
            try:
                raster_maze[head[0]][head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(head_dir)]
            except:
                pass
            head = add_offset(head, head_dir)
            if head_dir != (0,0):
                last_dir = head_dir

            raster_maze[head[0]][head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(last_dir) - 2]
    player_pos = random.choice([(0, 0), (0,height -1),(width -1,0),(width -1,height-1,)])
    raster_maze[player_pos[0]][player_pos[1]] |= 0b10000
    end_pos = pick_end(raster_maze, player_pos)
    raster_maze[end_pos[0]][end_pos[1]] |= 0b100000

    return raster_maze
