def manhattan_heuristic(x, y, goal_x, goal_y):
    return abs(x - goal_x) + abs(y - goal_y)