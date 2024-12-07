from maze_generator import WALL_CHECK_MASKS, new_maze
def create_wall(cell: int) -> list: 
    wall = [[ 0 for _ in range(3)] for _ in range(3)]
    for index, mask in enumerate(WALL_CHECK_MASKS):
        if cell & mask != 0:
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

def num_list_to_wall_str(input: list) -> str:
    WALLS = [" ","╸", "╻", "┓", "╺", "━", "┏", "┳", "╹", "┛", "┃", "┫", "┗", "┻", "┣", "╋"]
    return "".join(WALLS[i] for i in input)

def draw_maze(maze: list) -> None:
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
    

    for i in maze_lines:
        print(num_list_to_wall_str(i))

draw_maze(new_maze(21, 21))
