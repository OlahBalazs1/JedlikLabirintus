from maze_generator import DIRECTIONS, WALL_BREAK_MASKS, WALL_CHECK_MASKS, add_offset, new_maze
import random
import os

CLEAR_COMMAND = "clear"
if os.name == "nt":
    os.system('color')
    CLEAR_COMMAND = "cls"

PLAYER="p"
PLAYER_FANCY="\033[92mOwO\033[0m"
END="e"
END_FANCY="\033[103m   \033[0m"
def create_wall(cell: int) -> list: 
    wall = [[ 0 for _ in range(3)] for _ in range(3)]
    if cell & 0b10000 != 0:
        wall[1][1] = 0b10000
    if cell & 0b100000 != 0:
        wall[1][1] = 0b100000
    for index, mask in enumerate(WALL_CHECK_MASKS):
        if cell & 0b001111 & mask != 0:
            match index:
                # left down right up
                # left
                case 0: 
                    wall[0][0] |= 0b0100
                    wall[1][0] |= 0b0101
                    wall[2][0] |= 0b0001
                #down
                case 1:
                    wall[0][0] |= 0b0010
                    wall[0][1] |= 0b1010
                    wall[0][2] |= 0b1000
                #right
                case 2:
                    wall[0][2] |= 0b0100
                    wall[1][2] |= 0b0101
                    wall[2][2] |= 0b0001
                #up
                case 3:
                    wall[2][0] |= 0b0010
                    wall[2][1] |= 0b1010
                    wall[2][2] |= 0b1000
    return wall

def num_to_wall(input: int) -> str:
    if input == 0b10000:
        return PLAYER
    if input == 0b100000:
        return END
    WALLS = [" ","╸", "╻", "┓", "╺", "━", "┏", "┳", "╹", "┛", "┃", "┫", "┗", "┻", "┣", "╋"]
    return WALLS[input]

def draw_maze(maze: list) -> None:
    # maze[player_pos[1]][player_pos[0]] |= 0b10000
    # maze[end_pos[0]][end_pos[1]] |= 0b100000
    maze_lines = []
    for y in maze:
        line = [[], [], []]
        for x in y: 
            for wall in create_wall(x):
                for index, cell in enumerate(wall):
                    line[index].append(cell)
        for i in line:
            maze_lines.append(i)
    to_merge = []

    for i in range(1, len(maze_lines) - 1):
        if (i + 1) % 3 == 0:
            to_merge.append(i)

    for line in reversed(to_merge):
        for index in range(len(maze_lines[line])):
            maze_lines[line][index] |= maze_lines[line + 1][index]
        del maze_lines[line + 1]
    to_merge = []
    for i in range(1, len(maze_lines[0]) - 1):
        if (i + 1) % 3 == 0:
            to_merge.append(i)

    for column in reversed(to_merge):
        for index in reversed(range(len(maze_lines))):
            maze_lines[index][column + 1] |= maze_lines[index][column]
            maze_lines[index][column] = maze_lines[index][column - 1] 
            maze_lines[index].insert(column, maze_lines[index][column])

    # fix last column
    for line in range(len(maze_lines)):
        maze_lines[line].append(maze_lines[line][-1])
        maze_lines[line][-2] = maze_lines[line][-3]
        maze_lines[line].insert(-1, maze_lines[line][-2])
    completed_maze = []

    for line in maze_lines:
        completed_maze.append("".join(map(num_to_wall, line)))
    # print(completed_maze)

    for index, i in enumerate(completed_maze):

        i = i.replace(PLAYER*3, PLAYER_FANCY)
        i = i.replace(END*3, END_FANCY)
        print(i)

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

maze = new_maze(20,20)
draw_maze(maze)
