import heapq
import pygame
import time
from utils.algorithm_runner import update_game_state, check_goal, handle_frame
from algorithms.heuristic import h_manhattan_cost

def run_beam(game, beam_width=3):
    """Chạy Beam Search, cập nhật trạng thái của MazeGame"""

    game.alg_name = "Beam"

    # Sử dụng custom start và end nếu có
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal = (len(game.maze) - 1, len(game.maze[0]) - 1)
    else:
        goal = goal_pos

    # Beam search duy trì một tập hợp các trạng thái tốt nhất (beam)
    
    # Khởi tạo beam với trạng thái ban đầu
    # Mỗi phần tử trong beam: (heuristic_cost, x, y, path)
    start_heuristic = h_manhattan_cost(start_pos, goal)
    current_beam = [(start_heuristic, start_pos[0], start_pos[1], [])]
    
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    step_count = 0

    while current_beam and game.is_running:
        result = handle_frame(game, step_count)
        if result is None:
            return
        step_count, ok = result
        if not ok:
            return

        # Tạo tập hợp tất cả successors từ beam hiện tại
        all_successors = []
        
        for heuristic_cost, x, y, current_path in current_beam:
            # Bỏ qua nếu đã thăm
            if (x, y) in visited_set:
                continue
                
            # Cập nhật trạng thái game cho node hiện tại
            update_game_state(game, x, y, visited_set)
            
            # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
            game.path = current_path + [(x, y)]
            
            step_count += 1

            # Kiểm tra đích
            if check_goal(game, x, y, current_path):
                return

            # Tạo tất cả successors từ node hiện tại
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < len(game.maze) and 
                    0 <= new_y < len(game.maze[0]) and 
                    game.maze[new_x][new_y] == 0 and 
                    (new_x, new_y) not in visited_set):
                    
                    # Tính heuristic cho successor
                    h_cost = h_manhattan_cost((new_x, new_y), goal)
                    new_path = current_path + [(x, y)]
                    all_successors.append((h_cost, new_x, new_y, new_path))

        # Nếu không có successor nào, kết thúc
        if not all_successors:
            break

        # Sắp xếp tất cả successors theo heuristic (tốt nhất trước)
        all_successors.sort(key=lambda x: x[0])
        
        # Chọn beam_width successors tốt nhất để tạo beam mới
        current_beam = all_successors[:beam_width]
        
        # Loại bỏ duplicates trong beam mới
        unique_beam = []
        seen_positions = set()
        for item in current_beam:
            pos = (item[1], item[2])  # (x, y)
            if pos not in seen_positions:
                seen_positions.add(pos)
                unique_beam.append(item)
        
        current_beam = unique_beam

    game.is_running = False
    game.current_node = None
    game.draw_frame()
    pygame.time.wait(50)
