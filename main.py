import random

# left, down, right, up
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
WALL_CHECK_MASKS = [0b0001, 0b0010, 0b0100, 0b1000]
WALL_BREAK_MASKS = [0b1110, 0b1101, 0b1011, 0b0111]
def create_wall(cell: int) -> list: 
    wall = [[" " for _ in range(3)] for _ in range(3)]
    wall[0][0] = wall[0][2] = wall[2][0] = wall[2][2] = "#"
    for index, mask in enumerate(WALL_CHECK_MASKS):
        if cell & mask != 0:
            match index:
                case 0: 
                    wall[1][0] = "#"
                case 1:
                    wall[0][1] = "#"
                case 2:
                    wall[1][2] = "#"
                case 3:
                    wall[2][1] = "#"
    return wall



def add_offset(position, vector) -> tuple:
    return position[0] + vector[0], position[1] + vector[1]

def new_loop(start_pos: tuple, active_positions: set, max_x: int, max_y: int) -> list:
    path_raster = [[(0, 0) for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    next_dir = random.choice(DIRECTIONS)
    dir_to_previous = DIRECTIONS[DIRECTIONS.index(next_dir) - 2]
    head = start_pos
    while head not in active_positions:
        dir_to_previous = DIRECTIONS[DIRECTIONS.index(next_dir) - 2]
        while next_dir == dir_to_previous or (add_offset(head, next_dir)[0] not in range(0, max_x + 1)) or (add_offset(head, next_dir)[1] not in range(0, max_y + 1)):
            next_dir = random.choice(DIRECTIONS)
        path_raster[head[0]][head[1]] = next_dir
        head = add_offset(head, next_dir)
    print("a")
    
    return path_raster

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
    active_cells = {random_inactive_position(szelesseg -1, magassag -1, set())}
    raster_maze = [[0b1111 for _ in range(magassag)] for _ in range(szelesseg)]

    while len(active_cells) < szelesseg * magassag:
        start_pos = random_inactive_position(szelesseg - 1, magassag -1, active_cells)
        path_raster = new_loop(start_pos, active_cells, szelesseg -1, magassag -1, )
        last_dir = (0,0)
        head_dir = (-1, -1)
        head = start_pos
        while head_dir != (0,0):
            head_dir = path_raster[head[0]][head[1]]
            active_cells.add(head)
            try:
                raster_maze[head[0]][head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(last_dir) - 2]
                raster_maze[head[0]][head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(head_dir)]
            except:
                pass
            head = add_offset(head, head_dir)
            last_dir = head_dir
        try:
            raster_maze[head[0]][head[1]] &= WALL_BREAK_MASKS[DIRECTIONS.index(last_dir) - 2]
        except:
            pass

    return raster_maze


def draw_maze(maze: list) -> None:
    for y in maze:
        line = ["", "", ""]
        # print(y)
        for x in y: 
            # print(x)
            for wall in create_wall(x):
                for index, cell in enumerate(wall):
                    # print(cell)
                    line[index] += cell
        for i in line:
            # print(i)
            print()
            print("".join(i), end="")
    print()


draw_maze(new_maze(10, 10))

# for i in create_wall(0b1111):
#     print(i)


