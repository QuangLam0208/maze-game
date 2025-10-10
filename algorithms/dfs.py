import pygame
import time
from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished

def run_dfs(game):
    """Chạy DFS, cập nhật trạng thái của MazeGame"""

    game.alg_name = "Depth-First Search"

    # Sử dụng custom_start nếu có và không phải None, ngược lại dùng (0, 0)
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos
    stack = [(start_x, start_y, [])]  # Sử dụng stack thay vì queue cho DFS
    
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0

    while stack and game.is_running:
        result = handle_frame(game, step_count)
        if result is None:
            return
        step_count, ok = result
        if not ok:
            return

        # Lấy node kế tiếp từ stack (LIFO)
        x, y, current_path = stack.pop()
        if (x, y) in visited_set:
            continue

        # Cập nhật trạng thái game
        update_game_state(game, x, y, visited_set)
       
        # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
        game.path = current_path + [(x, y)]
        
        step_count += 1

        # Kiểm tra đích
        if check_goal(game, x, y, current_path):
            return

        # Thêm các node kế tiếp vào stack (DFS)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(game.maze) and 
                0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0 and 
                (new_x, new_y) not in visited_set):
                stack.append((new_x, new_y, current_path + [(x, y)]))

    game.is_running = False
    game.current_node = None

    # Add to history if no path was found
    algorithm_finished(game)

    # Animation khi kết thúc
    game.draw_frame()
    pygame.time.wait(50)
