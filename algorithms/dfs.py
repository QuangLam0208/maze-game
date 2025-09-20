from collections import deque
import pygame
import time

def run_dfs(game):
    """Chạy DFS, cập nhật trạng thái của MazeGame"""
    stack = [(0, 0, [])]  # Sử dụng stack thay vì queue cho DFS
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0
    max_steps_per_frame = 3

    while stack and game.is_running:
        if step_count >= max_steps_per_frame:
            # Khi duyệt hết 4 hướng (step 0 -> 3) thì tạm dừng để tạo animation
            step_count = 0
            pygame.time.wait(80)
            # Draw frame of present state
            game.draw_frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        stop_rect = pygame.Rect(20 + 90, 720, 80, 35)
                        if stop_rect.collidepoint(event.pos):
                            game.is_running = False
                            return

        # Lấy node kế tiếp từ stack (LIFO) thay vì queue (FIFO)
        x, y, current_path = stack.pop()
        key = (x, y)
        if key in visited_set:
            continue

        visited_set.add(key)
        game.visited.add(key)
        game.current_node = (x, y)
        # Update statistic
        game.stats["nodes_visited"] += 1
        game.stats["time"] = (time.time() - game.start_time) * 1000

        step_count += 1

        # Check Goal state
        if x == len(game.maze) - 1 and y == len(game.maze[0]) - 1:
            game.path = current_path + [(x, y)]
            game.stats["path_length"] = len(game.path)
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
