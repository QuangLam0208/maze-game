import heapq
import time
import pygame
from .heuristic import manhattan_heuristic
import heapq
from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished

def run_astar(game):
    """Chạy thuật toán A* cho MazeGame"""
    
    game.alg_name = "A* Search"

    # Sử dụng custom start và end nếu có
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start = start_pos
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal = (len(game.maze)-1, len(game.maze[0])-1)
    else:
        goal = goal_pos

    # Queue chứa tuple (f, g, x, y, path)
    # f = g + h, g = chi phí từ start đến node hiện tại, h = heuristic tới goal
    Queue = [(manhattan_heuristic(*start, *goal), 0, start[0], start[1], [])]
    heapq.heapify(Queue)
    visited_set = set()
    directions = [(0,1), (1,0), (0,-1), (-1,0)] # 4 hướng đi (Right, Down, Left, Up)
    
    step_count = 0
    
    while Queue and game.is_running:
        # animation & sự kiện   
        result = handle_frame(game, step_count)
        if result is None:
            return
        step_count, ok = result
        if not ok:
            return
        
        f, g, x, y, path = heapq.heappop(Queue) # Lấy node f nhỏ nhất từ heap
        if (x, y) in visited_set:
            continue
        
        # cập nhật trạng thái node hiện tại
        update_game_state(game, x, y, visited_set)
        
        # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
        game.path = path + [(x, y)]
        
        step_count += 1
        
        # Nếu tới Goal
        if check_goal(game, x, y, path):
            break
        
        # Mở rộng các node kế tiếp
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]):
                # Nếu là đường trống và chưa duyệt
                if game.maze[nx][ny] == 0 and (nx, ny) not in visited_set:
                    new_g = g + 1    # Chi phí g từ start tới node này
                    new_h = manhattan_heuristic(nx, ny, *goal)  # Ước lượng còn lại tới goal
                    heapq.heappush(Queue, (new_g + new_h, new_g, nx, ny, path + [(x, y)]))  # Đẩy node mới vào heap với f = g + h
    
    game.is_running = False
    game.current_node = None
    
    # Add to history if no path was found
    algorithm_finished(game)
