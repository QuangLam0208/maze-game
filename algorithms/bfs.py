from collections import deque
import pygame
import time
from utils.algorithm_runner import update_game_state, check_goal, handle_frame

def run_bfs(game):
    """Chạy BFS, cập nhật trạng thái của MazeGame"""
    queue = deque([(0, 0, [])])
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0
    # max_steps_per_frame = 3

    while queue and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return
        # ------------------------------------
        # animation & event loop cũng bị lặp
        # -> có thể tách ra thành hàm handle_frame
        # if step_count >= max_steps_per_frame:
        #     # Khi duyệt hết 4 hướng (step 0 -> 3) thì tạm dừng để tạo animation: pygame.time.wait(..) 
        #     step_count = 0
        #     pygame.time.wait(80) 
        #     # Draw frame of present state (ghi đè lên frame của previous state)
        #     game.draw_frame()

        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return
        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             if event.button == 1:
        #                 stop_rect = pygame.Rect(20 + 90, 720, 80, 35)
        #                 if stop_rect.collidepoint(event.pos):
        #                     game.is_running = False
        #                     return
        # ------------------------------------

        # Lấy node kế tiếp
        x, y, current_path = queue.popleft()
        if (x, y) in visited_set:
            continue

        # key = (x, y)
        # if key in visited_set:
        #     continue

        update_game_state(game, x, y, visited_set)
        
        # ------------------------------------
        # Đoạn này sẽ bị lặp (vì mỗi thuật toán đều cần update state) 
        # -> có thể tách ra thành một hàm update_game_state
        # visited_set.add(key)
        # game.visited.add(key) # cập nhật vào visited của game.py gọi draw_maze() (renderer.py) 
        # game.current_node = (x, y) # highlight node được xét ở frame (như trên)
        # Update statistic
        # game.stats["nodes_visited"] += 1
        # game.stats["time"] = (time.time() - game.start_time) * 1000
        # ------------------------------------

        step_count += 1

        if check_goal(game, x, y, current_path):
            break

        # ------------------------------------
        # Check goal và lưu path cũng sẽ bị lặp
        # -> có thể tách ra thành 1 hàm check_goal
        # Check Goal state & save path
        # if x == len(game.maze) - 1 and y == len(game.maze[0]) - 1:
        #     game.path = current_path + [(x, y)]
        #     game.stats["path_length"] = len(game.path)
        #     game.current_node = None
        #     game.is_running = False
        #     break
        # ------------------------------------
        
        # Expand Next state
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and
                game.maze[nx][ny] == 0 and (nx, ny) not in visited_set):
                queue.append((nx, ny, current_path + [(x, y)]))

    game.is_running = False
    game.current_node = None