import heapq
import pygame
import time
from utils.algorithm_runner import update_game_state, check_goal, handle_frame

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan giữa hai điểm"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_gbf(game):
    """Chạy Greedy Best-First Search, cập nhật trạng thái của MazeGame"""
    # Priority queue: (heuristic_cost, x, y, path)
    # Sử dụng heuristic là khoảng cách Manhattan đến đích
    goal = (len(game.maze) - 1, len(game.maze[0]) - 1)
    start_heuristic = manhattan_distance((0, 0), goal)
    
    priority_queue = [(start_heuristic, 0, 0, [])]
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    step_count = 0

    while priority_queue and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        # Lấy node có heuristic tốt nhất (thấp nhất)
        heuristic_cost, x, y, current_path = heapq.heappop(priority_queue)
        
        if (x, y) in visited_set:
            continue

        # Cập nhật trạng thái game
        update_game_state(game, x, y, visited_set)
        step_count += 1

        # Kiểm tra đích
        if check_goal(game, x, y, current_path):
            return

        # Thêm các node kế tiếp vào priority queue
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(game.maze) and 
                0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0 and 
                (new_x, new_y) not in visited_set):
                
                # Tính heuristic cho node mới (khoảng cách Manhattan đến đích)
                h_cost = manhattan_distance((new_x, new_y), goal)
                heapq.heappush(priority_queue, (h_cost, new_x, new_y, current_path + [(x, y)]))

    # Animation khi kết thúc
    game.draw_frame()
    pygame.time.wait(50)
