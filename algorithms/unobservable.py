from collections import deque
from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
import pygame
import time

def run_unobservable_dfs(game):
    """
    DFS trong môi trường hoàn toàn không nhìn thấy (unobservable / blind search)
    """
    game.alg_name = "Unobservable"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos

    stack = [(start_x, start_y, [])]  # (x, y, đường đi)
    visited_set = set()
    step_count = 0

    while stack and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        x, y, path = stack.pop()

        # Nếu đã thăm hoặc là tường thì bỏ qua
        if (x, y) in visited_set or game.maze[x][y] == 1:
            continue

        # Node hợp lệ
        visited_set.add((x, y))
        path = path + [(x, y)]

        # Cập nhật trạng thái game với hiển thị màu vàng cho node hiện tại
        update_game_state(game, x, y, visited_set)
        
        # Cập nhật đường đi hiện tại và node đang xét để hiển thị màu vàng
        game.path = path
        game.current_node = (x, y)
        
        step_count += 1

        # Kiểm tra goal
        if check_goal(game, x, y, path):
            return

        # Thêm 4 ô kề vào stack 
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(game.maze) and 0 <= new_y < len(game.maze[0]):
                if (new_x, new_y) not in visited_set:
                    stack.append((new_x, new_y, path))

    # Nếu stack rỗng mà chưa tới goal
    game.is_running = False
    game.current_node = None
    game.draw_frame()
    pygame.time.wait(50)
    
    # Add to history if no path was found
    algorithm_finished(game)
