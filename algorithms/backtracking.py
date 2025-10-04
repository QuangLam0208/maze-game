from utils.algorithm_runner import update_game_state, check_goal, handle_frame
import pygame
import time

def run_backtracking(game):
    """Chạy thuật toán Backtracking với visited tạm thời trong vòng lặp"""
    
    game.alg_name = "Backtracking"

    # Sử dụng custom start và end nếu có
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal_pos = (len(game.maze)-1, len(game.maze[0])-1)

    # Khởi tạo - thêm tracking cho directions đã thử
    path = [start_pos]
    directions_tried = [0]  # Index của direction tiếp theo cần thử cho mỗi node trong path
    global_visited = set()  # Tất cả nodes đã thăm (hiển thị màu xanh nhạt)
    backtracked_nodes = set()  # Nodes đã backtrack (có thể hiển thị màu khác)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    step_count = 0
    
    # Backtracking iterative với visited tạm thời
    while path and game.is_running:
        # Animation & sự kiện - xử lý an toàn với handle_frame
        try:
            result = handle_frame(game, step_count)
        except:
            # Nếu có lỗi, tiếp tục với giá trị mặc định
            result = (step_count, True)
        
        if result is None:
            # Handle_frame có thể trả về None, cần xử lý
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.is_running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Kiểm tra nút stop
                    stop_rect = pygame.Rect(110, 720, 80, 35)
                    if stop_rect.collidepoint(event.pos):
                        game.is_running = False
                        return
            
            # Vẽ frame và delay thủ công
            game.draw_frame()
            time.sleep(0.08)
            step_count = 0
            continue
        
        if isinstance(result, tuple) and len(result) == 2:
            step_count, ok = result
            if not ok:
                return
        else:
            # Trường hợp result không phải tuple hoặc sai format
            step_count += 1
        
        current_pos = path[-1]  # Vị trí hiện tại (top của stack)
        x, y = current_pos
        
        # Thêm vào visited toàn cục để vẽ
        global_visited.add(current_pos)
        
        # Cập nhật trạng thái node hiện tại
        update_game_state(game, x, y, global_visited)
        
        # Kiểm tra goal
        if current_pos == goal_pos:
            if check_goal(game, x, y, path):
                return
        
        # Tạo visited tạm thời cho lần duyệt này (bao gồm toàn bộ path hiện tại)
        temp_visited = set(path)
        
        # Lấy direction index hiện tại cho node này
        current_dir_index = directions_tried[-1]
        
        # Tìm move hợp lệ tiếp theo từ direction chưa thử
        found_move = False
        for i in range(current_dir_index, len(directions)):
            dx, dy = directions[i]
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            
            if is_valid_move_temp(game, nx, ny, temp_visited):
                # Tìm thấy move hợp lệ
                path.append(next_pos)
                directions_tried[-1] = i + 1  # Cập nhật direction tiếp theo cho node hiện tại
                directions_tried.append(0)    # Node mới bắt đầu từ direction 0
                found_move = True
                break
        
        if not found_move:
            # Đã thử hết directions - cập nhật để báo hiệu đã thử hết
            directions_tried[-1] = len(directions)
        
        # Kiểm tra nếu node hiện tại đã thử hết directions
        if directions_tried[-1] >= len(directions):
            # Không tìm thấy move hợp lệ - backtrack
            if len(path) > 1:
                # Xóa node hiện tại khỏi path (backtrack)
                removed_pos = path.pop()
                directions_tried.pop()  # Xóa tracking cho node bị xóa
                
                # Thêm vào backtracked_nodes để có thể hiển thị khác màu
                backtracked_nodes.add(removed_pos)
                
                # KHÔNG xóa visual - giữ lại tất cả nodes đã thăm
                # Chỉ xóa khỏi path nhưng vẫn giữ trong visited để hiển thị
                # if removed_pos in game.visited:
                #     game.visited.discard(removed_pos)
                if removed_pos in game.path:
                    game.path.remove(removed_pos)
                    
                # Đánh dấu là node đã backtrack (có thể dùng màu khác)
                # game.visited vẫn giữ node này để hiển thị màu "đã thăm"
            else:
                # Không còn đường để backtrack
                print("Không tìm thấy đường đi!")
                game.is_running = False
                break
        
        step_count += 1

def is_valid_move_temp(game, x, y, temp_visited):
    """Kiểm tra move hợp lệ với visited tạm thời"""
    # Kiểm tra biên
    if x < 0 or x >= len(game.maze) or y < 0 or y >= len(game.maze[0]):
        return False
    
    # Kiểm tra tường
    if game.maze[x][y] == 1:
        return False
    
    # Kiểm tra đã thăm trong path hiện tại (visited tạm thời)
    if (x, y) in temp_visited:
        return False
    
    return True
