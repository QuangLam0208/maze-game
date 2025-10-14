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

def generate_beautiful_maze(size: int):
    """
    Sinh maze đẹp, không trùng cạnh, đảm bảo có đường từ start -> goal
    """
    # 1 = tường, 0 = đường
    maze = [[1 for _ in range(size)] for _ in range(size)]

    # DFS đệ quy để carve maze
    def dfs(x, y):
        maze[x][y] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < size-1 and 0 < ny < size-1 and maze[nx][ny] == 1:
                maze[x + dx//2][y + dy//2] = 0
                dfs(nx, ny)

    # Bắt đầu từ (1,1) để tránh biên
    dfs(1, 1)

    # Mở lối vào (start) và lối ra (goal)
    maze[0][0] = 0
    maze[1][0] = 0
    maze[size-1][size-1] = 0
    maze[size-2][size-1] = 0

    state = reset_pathfinding()
    return maze, state
