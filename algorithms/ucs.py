import heapq
from utils.algorithm_runner import update_game_state, check_goal, handle_frame
from .cost import DEFAULT_COST

def run_ucs(game, cost_func=DEFAULT_COST):
    """
    Uniform Cost Search (UCS)
    """
    # Sử dụng custom_start nếu có và không phải None, ngược lại dùng (0, 0)
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos
    
    # Priority queue: (cost, x, y, path)
    pq = [(0, start_x, start_y, [])]
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0

    while pq and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        cost, x, y, current_path = heapq.heappop(pq)

        if (x, y) in visited_set:
            continue

        update_game_state(game, x, y, visited_set)
        step_count += 1

        # Check goal
        if check_goal(game, x, y, current_path):
            break

        # Expand neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and game.maze[nx][ny] == 0:
                new_cost = cost + cost_func(x, y, nx, ny)
                heapq.heappush(pq, (new_cost, nx, ny, current_path + [(x, y)]))

    game.is_running = False
    game.current_node = None