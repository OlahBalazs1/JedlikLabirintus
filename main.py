from sys import exception
from maze_generator import DIRECTIONS, WALL_BREAK_MASKS, WALL_CHECK_MASKS, add_offset, new_maze
from pynput import keyboard
import random
import os

LEFT = [keyboard.Key.left, keyboard.KeyCode.from_char("a"), keyboard.KeyCode.from_char("h")]
RIGHT= [keyboard.Key.right, keyboard.KeyCode.from_char("d"), keyboard.KeyCode.from_char("l")]
DOWN = [keyboard.Key.down, keyboard.KeyCode.from_char("s"), keyboard.KeyCode.from_char("j")]
UP = [keyboard.Key.up, keyboard.KeyCode.from_char("w"), keyboard.KeyCode.from_char("k")]
GIVE_UP = [keyboard.Key.esc]

CLEAR_COMMAND = "clear"
if os.name == "nt":
    os.system('color')
    CLEAR_COMMAND = "cls"

os.system(CLEAR_COMMAND)
maze, player_pos, end_path = new_maze(5,5)
path_taken = set()


PLAYER="p"
PLAYER_FANCY="\033[92mOwO\033[0m"
END="e"
END_FANCY="\033[103m   \033[0m"
WIN="w"
WIN_FANCY="\033[30m\033[103mOWO\033[0m"

PLAYER_PATH_PLACEHOLDER = "P"
PLAYER_PATH = "\33[31m●\33[0m"

WIN_PATH_PLACEHOLDER = "Q"
WIN_PATH = "\33[93m●\33[0m"

game_ended = False
def create_wall(cell: int) -> list: 
    wall = [[ 0 for _ in range(3)] for _ in range(3)]
    if cell & 0b10000 != 0:
        wall[1][1] |= 0b10000
    if cell & 0b100000 != 0:
        wall[1][1] |= 0b100000
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
    if input == 0b110000:
        return WIN
    if input == 0b10000:
        return PLAYER
    if input == 0b100000:
        return END
    WALLS = [" ","╸", "╻", "┓", "╺", "━", "┏", "┳", "╹", "┛", "┃", "┫", "┗", "┻", "┣", "╋"]
    return WALLS[input]

def replace_at(input: str, index: int, to: str) -> str:
    input_list = list(input)
    input_list[index] = to
    return "".join(input_list)


def draw_maze(maze: list, is_over) -> None:
    global player_pos
    global end_path
    global path_taken
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

    if is_over:
        for i in path_taken:
            completed_maze[i[0] * 2 + 1] = replace_at(completed_maze[i[0]* 2 + 1], i[1] * 3 + 2 + i[1], PLAYER_PATH_PLACEHOLDER)
        for i in end_path[:-1]:
            completed_maze[i[0] * 2 + 1] = replace_at(completed_maze[i[0] * 2 + 1], i[1] * 3 + 2 + i[1], WIN_PATH_PLACEHOLDER)

    for i in completed_maze:
        i = i.replace(PLAYER*3, PLAYER_FANCY)
        i = i.replace(END*3, END_FANCY)
        i = i.replace(WIN*3, WIN_FANCY)
        i = i.replace(PLAYER_PATH_PLACEHOLDER, PLAYER_PATH)
        i = i.replace(WIN_PATH_PLACEHOLDER, WIN_PATH)
        
        print(i)
draw_maze(maze, False)


def make_move(maze, player_pos, move) -> tuple:
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    try: 
        if maze[player_pos[0]][player_pos[1]] & 0b1111 & WALL_CHECK_MASKS[DIRECTIONS.index(move)] != 0:
            return maze, player_pos
    except: 
        return maze, player_pos

    path_taken.add(player_pos)
    maze[player_pos[0]][player_pos[1]] &= ~0b010000
    player_pos = add_offset(player_pos, move)
    maze[player_pos[0]][player_pos[1]] |= 0b010000

    return maze, player_pos



def on_press(key):
    global maze
    global player_pos
    global end_path
    possible_directions = []
    for index, i in enumerate(DIRECTIONS):
        if maze[player_pos[0]][player_pos[1]] & 0b1111 & WALL_CHECK_MASKS[index] == 0:
            possible_directions.append(i)
    move = (0,0)
    if key in LEFT:
        move = DIRECTIONS[1]
    elif key in RIGHT:
        move = DIRECTIONS[3]
    elif key in DOWN:
        move = DIRECTIONS[2]
    elif key in UP:
        move = DIRECTIONS[0]
    elif key in GIVE_UP:
        listener.stop()
        os.system(CLEAR_COMMAND)
        draw_maze(maze, True)
        return
    os.system(CLEAR_COMMAND)
    maze, player_pos = make_move(maze, player_pos, move)
    if maze[player_pos[0]][player_pos[1]] & 0b110000 == 0b110000:
        print("won")
    draw_maze(maze, False)
    

with keyboard.Listener(
        on_press=on_press,
        ) as listener:
    listener.join()

