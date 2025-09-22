def h_manhattan_cost(cell, goal):
    x, y = cell
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)

DEFAULT_HEURISTIC = h_manhattan_cost