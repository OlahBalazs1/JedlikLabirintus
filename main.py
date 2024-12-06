from maze_generator import WALL_CHECK_MASKS, new_maze
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

def draw_maze(maze: list) -> None:
    for y in maze:
        line = ["", "", ""]
        for x in y: 
            for wall in create_wall(x):
                for index, cell in enumerate(wall):
                    line[index] += cell
        for i in line:
            print()
            print("".join(i), end="")
    print()

draw_maze(new_maze(10, 10))
