from collections import deque
from utils.algorithm_runner import update_game_state, check_goal, handle_frame

def run_bfs(game):
    """Chạy BFS, cập nhật trạng thái của MazeGame"""
    queue = deque([(0, 0, [])])
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0

    while queue and game.is_running:
        step_count, ok = handle_frame(game, step_count)

        if not ok:
            return
        
        # Lấy node kế tiếp
        x, y, current_path = queue.popleft()
        if (x, y) in visited_set:
            continue

        update_game_state(game, x, y, visited_set)

        step_count += 1

        if check_goal(game, x, y, current_path):
            break
            
        # Expand Next state
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and
                game.maze[nx][ny] == 0 and (nx, ny) not in visited_set):
                queue.append((nx, ny, current_path + [(x, y)]))

    game.is_running = False
    game.current_node = None