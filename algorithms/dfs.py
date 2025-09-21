from collections import deque
import pygame
import time
from utils.algorithm_runner import update_game_state, check_goal, handle_frame

def run_dfs(game):
    """Chạy DFS, cập nhật trạng thái của MazeGame"""
    stack = [(0, 0, [])]  # Sử dụng stack thay vì queue cho DFS
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0

    while stack and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        # Lấy node kế tiếp từ stack (LIFO)
        x, y, current_path = stack.pop()
        if (x, y) in visited_set:
            continue

        # Cập nhật trạng thái game
        update_game_state(game, x, y, visited_set)
        step_count += 1

        # Kiểm tra đích
        if check_goal(game, x, y, current_path):
            return
            return

        # Thêm các node kế tiếp vào stack (DFS)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(game.maze) and 
                0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0 and 
                (new_x, new_y) not in visited_set):
                stack.append((new_x, new_y, current_path + [(x, y)]))

    # Animation khi kết thúc
    game.draw_frame()
    pygame.time.wait(50)
