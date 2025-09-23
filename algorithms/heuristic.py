def h_manhattan_cost(cell, goal):
    x, y = cell
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)

def manhattan_heuristic(x, y, goal_x, goal_y):
    return abs(x - goal_x) + abs(y - goal_y)
  
DEFAULT_HEURISTIC = h_manhattan_cost