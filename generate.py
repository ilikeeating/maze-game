import random
import numpy as np

def neighboring_cells(x, y):
    if (y % 2) == 0:
        return [
            (x, y + 1),
            (x, y - 1)
        ]
    else:
        return [
            (x + 1, y),
            (x - 1, y)
        ]

def generate_maze(width, height):
    def get_walls(x, y):
        """Get the walls neighboring the cell (x, y)."""
        neighboring_walls = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]
        valid_wall = lambda x, y: (0 < x < width-1) and (0 < y < height-1)
        return set([w for w in neighboring_walls if valid_wall(*w)])

    board = np.ones(shape=(width, height), dtype=int)
    board[1::2, 1::2] = 0

    visited = [(1, 1)]
    walls = get_walls(*visited[0])

    while walls:
        wall = random.choice(list(walls))
        cell_a, cell_b = neighboring_cells(*wall)
        if not (cell_a in visited and cell_b in visited):
            unvisited_cell = cell_a if (cell_b in visited) else cell_b
            board[wall] = 0
            visited.append(unvisited_cell)
            walls |= get_walls(*unvisited_cell) # list.extend but for sets
        walls.remove(wall)

    return board


#characters = ['  ', '██']
#
#for row in board.T:
#    for i in row:
#        print(characters[i], end='')
#    print()
