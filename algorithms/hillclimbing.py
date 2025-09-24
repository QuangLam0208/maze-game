from utils.algorithm_runner import update_game_state, check_goal, handle_frame
from .heuristic import DEFAULT_HEURISTIC


def run_hill_climbing(game, heuristic=DEFAULT_HEURISTIC):
    """Chạy Hill Climbing"""
    start = game.start
    goal = game.end

    # current_state = (cell, path, cost)
    current = (start, [start], heuristic(start, goal))
    step_count = 0
    visited_set = set()

    while game.is_running:
        # animation & sự kiện
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        (x, y), path, cost = current
        update_game_state(game, x, y, visited_set)
        step_count += 1


        # Nếu tới Goal
        if check_goal(game, x, y, path):
            return

        # Sinh neighbors
        neighbors = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and 
                game.maze[nx][ny] == 0 and (nx, ny) not in visited_set):
                new_cell = (nx, ny)
                neighbors.append((new_cell, path + [new_cell], heuristic(new_cell, goal)))

        if not neighbors:
            break

        # Tìm neighbor tốt nhất
        best_neighbor = min(neighbors, key=lambda n: n[2])

        #state(current_cell, path, cost) ,state[2]: giá trị Heuristic
        if best_neighbor[2] < cost:
            # Nếu tốt hơn thì nhận ngay
            current = best_neighbor
        else:
            # Không có neighbor nào tốt hơn thì dừng
            break

    # kết thúc
    game.is_running = False
    game.current_node = None
