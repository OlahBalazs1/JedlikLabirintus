from maze_generator import *
try:
    from pynput import keyboard
except:
    print("A pynput library nem megtalálható.")
    print("Kérem, futtassa az alábbi programot: ")
    print("\tpython -m pip install pynput")
    exit()
import os

LEFT = [keyboard.Key.left, keyboard.KeyCode.from_char("a"), keyboard.KeyCode.from_char("h")]
RIGHT= [keyboard.Key.right, keyboard.KeyCode.from_char("d"), keyboard.KeyCode.from_char("l")]
DOWN = [keyboard.Key.down, keyboard.KeyCode.from_char("s"), keyboard.KeyCode.from_char("j")]
UP = [keyboard.Key.up, keyboard.KeyCode.from_char("w"), keyboard.KeyCode.from_char("k")]
GIVE_UP = [keyboard.Key.esc]

CLEAR_COMMAND = "clear"
PYNPUT_ERROR = "A pynput modul jelenleg nem működik linux alapú rendszereken, ha a python verziója 3.13 feletti.\nVagy használjon a Pythonból egy régebbi verziót, vagy váltson Windows alapú rendszerre."
if os.name == "nt":
    os.system('color')
    CLEAR_COMMAND = "cls"
    PYNPUT_ERROR = "A pynput modul jelenleg nem működik, ha a Python verziója 3.13 felett van.\nHasználjon egy régebbi verziót."


print("Jedlik labirintus")
print("Készítette: Oláh Balázs")
print("Irányítások:")
print("\tEscape: feladás / kilépés")
print("\tMozgás: ")
print("\t\tW, K, és felfele nyíl")
print("\t\tS, J, és lefele nyíl")
print("\t\tA, H és balra nyíl")
print("\t\tD, L és jobbra nyíl")
print("Nyomjon meg egy gombot a folytatáshoz.")

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


def draw_maze(maze: list, is_over: bool) -> list[str]:
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

    for index, i in enumerate(completed_maze):
        i = i.replace(PLAYER*3, PLAYER_FANCY)
        i = i.replace(END*3, END_FANCY)
        i = i.replace(WIN*3, WIN_FANCY)
        i = i.replace(PLAYER_PATH_PLACEHOLDER, PLAYER_PATH)
        i = i.replace(WIN_PATH_PLACEHOLDER, WIN_PATH)
        completed_maze[index] = i
    return completed_maze

def draw_size_choose(width, height) -> None:
    map = [[15 for _ in range(width)] for _ in range(height)]
    map = draw_maze(map, False)
    map += [] + ["←" + "".join(["─" for _ in range(width * 4)]) + "→"]
    map[0] += "  ↑"
    for i in range(1, (height*2)):
        map[i] += "  │"
    map[-2] += "  ↓"

    for i in map:
        print(i)


IS_CHOOSING_STYLE = False
IS_PLAYING = False
IS_CHOOSING_SIZE = False

TERM_SIZE = os.get_terminal_size()
TERM_WIDTH, TERM_HEIGHT = TERM_SIZE.columns, TERM_SIZE.lines

#
# for i in draw_maze(maze, False):
#     print(i)

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


# TODO ne lehessen nagyobb a terminálnál
width = 5
height = 5
def on_press(key):
    global IS_PLAYING
    global IS_CHOOSING_SIZE
    global IS_CHOOSING_STYLE
    if IS_PLAYING:
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
            maze[player_pos[0]][player_pos[1]] ^= 0b010000
            path_taken.add(player_pos)
            draw_maze(maze, True)
            print("\33[31mFeladtad.\033[0m")
            return
        if move == (0,0):
            return
        os.system(CLEAR_COMMAND)
        maze, player_pos = make_move(maze, player_pos, move)
        if maze[player_pos[0]][player_pos[1]] & 0b110000 == 0b110000:
            listener.stop()
            draw_maze(maze, True)
            print("\033[92mNyertél!\033[0m")
            return

        draw_maze(maze, False)
    elif IS_CHOOSING_SIZE:
        global width
        global height
        if key in LEFT:
            if width - 1 >= 2:
                width = width - 1
            else:
                return
        elif key in RIGHT:
            # TODO terminál mérete, villogástalanítás
            if width * 4 + 4 < TERM_WIDTH:
                width = width + 1
            else:
                return
        elif key in DOWN:
            # TODO terminál mérete, villogástalanítás
            if height + 2 + 4 < TERM_HEIGHT:
                height = height + 1
            else:
                return
        elif key in UP:
            if height - 1 >= 2:
                height = height - 1
            else:
                return
        elif key in GIVE_UP:
            print("Viszlát!")
            listener.stop()
        elif key == keyboard.Key.enter:
            IS_CHOOSING_SIZE = False
            IS_CHOOSING_STYLE = True
            return
        os.system(CLEAR_COMMAND)
        draw_size_choose(width, height)
    elif IS_CHOOSING_STYLE:
        pass
    else:
        IS_CHOOSING_SIZE = True


for i in draw_maze(new_long_hall(2,2), False):
    print(i)

#try:
    #with keyboard.Listener(
            #on_press=on_press,
            #) as listener:
        #listener.join()
#except:
    #print(PYNPUT_ERROR)
    #exit()
