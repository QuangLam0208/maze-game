import random
from core.path_finding import reset_pathfinding

def generate_maze(size: int, wall_prob: float = 0.3):
    """
    Sinh ngẫu nhiên một maze size x size.
    0 = đường đi, 1 = tường.
    """
    maze = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if random.random() < wall_prob and not (i == 0 and j == 0) and not (i == size - 1 and j == size - 1):
                maze[i][j] = 1  # Tường

    state = reset_pathfinding()
    return maze, state