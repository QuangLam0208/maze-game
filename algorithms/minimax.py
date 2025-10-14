from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
import pygame
import time
import math
from collections import deque

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Global cache cho BFS distance để tối ưu performance
_bfs_distance_cache = {}

def bfs_real_distance(game, start, goal):
    """
    Tính khoảng cách thực tế từ start đến goal qua đường hợp lệ bằng BFS
    Trả về: (distance, path) hoặc (float('inf'), []) nếu không có đường
    """
    cache_key = (start, goal)
    if cache_key in _bfs_distance_cache:
        return _bfs_distance_cache[cache_key]
    
    if start == goal:
        _bfs_distance_cache[cache_key] = (0, [start])
        return (0, [start])
    
    queue = deque([(start, 0, [start])])  # (position, distance, path)
    visited = {start}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        current_pos, dist, path = queue.popleft()
        
        for dx, dy in directions:
            x, y = current_pos
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)
            
            # Kiểm tra tính hợp lệ của move
            if (0 <= new_x < len(game.maze) and 
                0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0 and  # 0 là đường đi
                new_pos not in visited):
                
                new_distance = dist + 1
                new_path = path + [new_pos]
                
                if new_pos == goal:
                    result = (new_distance, new_path)
                    _bfs_distance_cache[cache_key] = result
                    return result
                
                visited.add(new_pos)
                queue.append((new_pos, new_distance, new_path))
    
    # Không tìm được đường đi
    result = (float('inf'), [])
    _bfs_distance_cache[cache_key] = result
    return result

def validate_path_exists(game, player_pos, goal_pos):
    """
    Kiểm tra xem có đường đi từ player đến goal không
    Trả về: (có_đường_đi, khoảng_cách, đường_đi)
    """
    distance, path = bfs_real_distance(game, player_pos, goal_pos)
    has_path = distance != float('inf')
    return (has_path, distance, path)

def run_minimax(game):
    """
    Thuật toán Minimax cải tiến với BFS validation:
    - Trước mỗi lượt: chạy BFS từ Player đến Goal để đảm bảo có đường đi
    - Sử dụng khoảng cách thực tế qua đường hợp lệ thay vì Manhattan
    - Monster: Goal Guardian + Active Hunter
    - Player: Tránh ngõ cụt và tìm đường tối ưu
    """
    game.alg_name = "Minimax"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal_pos = (len(game.maze)-1, len(game.maze[0])-1)

    # Vị trí ban đầu
    player_pos = start_pos  # Max player (xanh)
    
    # Monster luôn đặt ở goal để bảo vệ đích
    monster_pos = goal_pos
    
    # Kiểm tra đường đi ban đầu
    has_initial_path, initial_distance, initial_path = validate_path_exists(game, player_pos, goal_pos)
    if not has_initial_path:
        print(f" Không có đường đi từ {player_pos} đến {goal_pos}!")
        return
    
    # Khởi tạo vị trí
    print(f" BFS-Minimax Start: Player {player_pos}, Monster {monster_pos}, Goal {goal_pos}")
    print(f" Initial path distance: {initial_distance} steps")
    
    visited = set()
    step_count = 0
    max_depth = 3
    
    # Tracking cho game loop
    player_history = []
    monster_history = []
    
    # Game state setup
    game.player_pos = player_pos
    game.monster_pos = monster_pos
    
    def get_possible_moves(pos, is_player=True, recent_positions=None, target_pos=None):
        """Lấy các nước đi hợp lệ từ vị trí, tránh vòng lặp"""
        moves = []
        x, y = pos
        
        if is_player:
            # Player di chuyển 1 ô mỗi lượt
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < len(game.maze) and 0 <= new_y < len(game.maze[0]) and 
                    game.maze[new_x][new_y] == 0):
                    moves.append((new_x, new_y))
        else:
            # Monster di chuyển tối đa 2 ô mỗi lượt về phía Player - mỗi bước 1 ô
            if not target_pos:
                moves.append(pos)  # Đứng yên nếu không có target
                return moves
            
            # Tính khoảng cách hiện tại đến Player
            current_dist = manhattan_distance(pos, target_pos)
            
            # Thử tất cả các combo di chuyển có thể và đánh giá hiệu quả
            move_candidates = []
            
            # Thử di chuyển 1 ô theo tất cả hướng
            all_dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in all_dirs:
                mid_x, mid_y = x + dx, y + dy
                if (0 <= mid_x < len(game.maze) and 0 <= mid_y < len(game.maze[0]) and 
                    game.maze[mid_x][mid_y] == 0):
                    
                    # Đánh giá move 1 ô
                    dist_1_step = manhattan_distance((mid_x, mid_y), target_pos)
                    improvement_1 = current_dist - dist_1_step
                    move_candidates.append((improvement_1, (mid_x, mid_y)))
                    
                    # Thử tiếp di chuyển ô thứ 2 theo cùng hướng
                    final_x, final_y = mid_x + dx, mid_y + dy
                    if (0 <= final_x < len(game.maze) and 0 <= final_y < len(game.maze[0]) and 
                        game.maze[final_x][final_y] == 0):
                        dist_2_step = manhattan_distance((final_x, final_y), target_pos)
                        improvement_2 = current_dist - dist_2_step
                        move_candidates.append((improvement_2, (final_x, final_y)))
                    
                    # Thử di chuyển ô thứ 2 theo hướng khác (di chuyển chéo)
                    for dx2, dy2 in all_dirs:
                        if (dx2, dy2) != (dx, dy):  # Hướng khác
                            final_x, final_y = mid_x + dx2, mid_y + dy2
                            if (0 <= final_x < len(game.maze) and 0 <= final_y < len(game.maze[0]) and 
                                game.maze[final_x][final_y] == 0):
                                dist_corner = manhattan_distance((final_x, final_y), target_pos)
                                improvement_corner = current_dist - dist_corner
                                move_candidates.append((improvement_corner, (final_x, final_y)))
            
            # Sắp xếp theo mức độ cải thiện (tốt nhất trước)
            move_candidates.sort(reverse=True, key=lambda x: x[0])
            
            # Lấy các moves tốt nhất (ưu tiên moves cải thiện khoảng cách)
            for improvement, move in move_candidates:
                if improvement > 0:  # Chỉ lấy moves làm gần Player hơn
                    moves.append(move)
            
            # Nếu không có move nào cải thiện, lấy ALL moves để tránh kẹt
            if not moves and move_candidates:
                # Thêm tất cả moves có thể, không chỉ move tốt nhất
                for improvement, move in move_candidates[:4]:  # Lấy 4 moves tốt nhất
                    moves.append(move)
            
            # Nếu vẫn không có moves, thêm basic moves
            if not moves:
                for dx, dy in all_dirs:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < len(game.maze) and 0 <= new_y < len(game.maze[0]) and 
                        game.maze[new_x][new_y] == 0):
                        moves.append((new_x, new_y))
            
            # Loại bỏ trùng lặp và giới hạn số lượng
            moves = list(dict.fromkeys(moves))  # Giữ thứ tự và loại trùng
            if len(moves) > 6:  # Giới hạn để tránh quá nhiều options
                moves = moves[:6]
        
        # Tránh vòng lặp: ưu tiên moves chưa đi gần đây (chỉ cho player)
        if is_player and recent_positions and len(moves) > 1:
            # Sắp xếp moves theo mức độ "mới"
            def move_priority(move):
                if move in recent_positions[-3:]:  # Đã đi trong 3 bước gần đây
                    return 1  # Ưu tiên thấp
                elif move in recent_positions:
                    return 2  # Ưu tiên trung bình
                else:
                    return 0  # Ưu tiên cao (chưa đi)
            
            moves.sort(key=move_priority)
        elif not is_player and recent_positions and len(moves) > 3:
            # Monster chỉ tránh lặp lại nếu có nhiều hơn 3 moves
            # Loại bỏ move vừa đi (chỉ move cuối cùng)
            if recent_positions and len(recent_positions) > 0:
                last_pos = recent_positions[-1]
                if last_pos in moves and len(moves) > 1:
                    moves.remove(last_pos)
        
        # Nếu không có nước đi nào, cho phép đứng yên
        if not moves:
            moves.append(pos)
            
        return moves
    
    def evaluate_state(player_pos, monster_pos, player_prev=None, monster_prev=None):
        """Đánh giá trạng thái với BFS distance thực tế"""
        # Sử dụng BFS distance thay vì Manhattan
        real_dist_to_goal, _ = bfs_real_distance(game, player_pos, goal_pos)
        dist_player_monster = manhattan_distance(player_pos, monster_pos)  # Monster vẫn dùng Manhattan cho tốc độ
        
        # Win/Loss conditions
        if player_pos == goal_pos:
            return 1000
        if player_pos == monster_pos:
            return -1000
        
        # Nếu không có đường đi đến goal = penalty cực lớn
        if real_dist_to_goal == float('inf'):
            return -5000  # Ngõ cụt = rất tệ
        
        score = 0
        
        # Player ưu tiên goal với BFS distance (chính xác hơn)
        score -= real_dist_to_goal * 300  # Tăng weight vì BFS distance chính xác hơn
        
        # Monster ưu tiên BẮT Player (trùng vị trí) - mục tiêu dừng game
        if dist_player_monster == 0:
            score -= 10000  # Monster đã bắt Player = thắng lớn
        elif dist_player_monster == 1:
            score -= 5000   # Sắp bắt được = ưu tiên cực cao
        elif dist_player_monster <= 2:
            score -= dist_player_monster * 200  # Tăng mạnh penalty để Monster tiến gần
        elif dist_player_monster <= 4:
            score -= dist_player_monster * 100
        else:
            score -= dist_player_monster * 50
        
        # Player chỉ tránh khi Monster cực kỳ gần
        if dist_player_monster <= 1:
            score += dist_player_monster * 120
        elif dist_player_monster <= 2:
            score += dist_player_monster * 60
        
        # Bonus cho movement về goal (sử dụng BFS)
        if player_prev and player_pos != player_prev:
            prev_real_dist, _ = bfs_real_distance(game, player_prev, goal_pos)
            if prev_real_dist != float('inf') and real_dist_to_goal < prev_real_dist:
                score += 40  # Bonus lớn hơn vì tiến bộ thực sự
            elif real_dist_to_goal > prev_real_dist:
                score -= 15  # Penalty khi đi xa goal
                score -= 2
        
        # Monster movement evaluation
        if monster_prev and monster_pos != monster_prev:
            prev_dist_to_player = manhattan_distance(monster_prev, player_pos)
            if dist_player_monster < prev_dist_to_player:
                score -= 15
            else:
                score += 5
        
        # Penalty cho đứng yên
        if player_prev and player_pos == player_prev:
            score -= 20
        if monster_prev and monster_pos == monster_prev:
            score += 10
        
        return score
    
    def minimax_pure(player_pos, monster_pos, depth, player_hist=None, monster_hist=None):
        """Minimax thuần túy tìm nước đi tốt nhất"""
        # Base cases
        if depth == 0:
            p_prev = player_hist[-1] if player_hist else None
            m_prev = monster_hist[-1] if monster_hist else None
            return evaluate_state(player_pos, monster_pos, p_prev, m_prev), None, None
        
        if player_pos == goal_pos:
            return 1200, None, None
        if player_pos == monster_pos:
            return -1000, None, None
        
        best_eval = -math.inf
        best_player_move = None
        best_monster_move = None
        
        player_moves = get_possible_moves(player_pos, is_player=True, recent_positions=player_hist)
        monster_moves = get_possible_moves(monster_pos, is_player=False, recent_positions=monster_hist, target_pos=player_pos)
        
        for p_move in player_moves:
            for m_move in monster_moves:
                # Monster BẮT Player = Monster thắng ngay lập tức
                if p_move == m_move:
                    return -10000, p_move, m_move  # Monster thắng = điểm rất âm cho Player
                
                new_player_hist = (player_hist + [player_pos]) if player_hist else [player_pos]
                new_monster_hist = (monster_hist + [monster_pos]) if monster_hist else [monster_pos]
                
                eval_score, _, _ = minimax_pure(p_move, m_move, depth-1, new_player_hist, new_monster_hist)
                
                # Evaluation adjustments
                # Sử dụng BFS distance cho player goal
                player_goal_dist_current, _ = bfs_real_distance(game, player_pos, goal_pos)
                player_goal_dist_new, _ = bfs_real_distance(game, p_move, goal_pos)
                monster_dist_current = manhattan_distance(player_pos, monster_pos)
                monster_dist_new = manhattan_distance(p_move, m_move)
                
                # Player goal bonus (dùng BFS distance)
                if (player_goal_dist_new != float('inf') and player_goal_dist_current != float('inf') and
                    player_goal_dist_new < player_goal_dist_current):
                    eval_score += 15
                elif (player_goal_dist_new != float('inf') and player_goal_dist_current != float('inf') and
                      player_goal_dist_new > player_goal_dist_current):
                    eval_score -= 10
                
                # Player avoid monster
                if monster_dist_current <= 3:
                    if monster_dist_new > monster_dist_current:
                        eval_score += 25
                    else:
                        eval_score -= 20
                elif monster_dist_current <= 5:
                    if monster_dist_new > monster_dist_current:
                        eval_score += 10
                    else:
                        eval_score -= 8
                
                # History penalty
                if player_hist and p_move in player_hist[-3:]:
                    penalty = len([pos for pos in player_hist[-3:] if pos == p_move]) * 5
                    eval_score -= penalty
                
                # Monster chase player - MỤC TIÊU BẮT PLAYER TẠI VỊ TRÍ CHÍNH XÁC
                player_dist_current = manhattan_distance(monster_pos, player_pos)
                player_dist_new = manhattan_distance(m_move, p_move)
                
                # Ưu tiên CỰC CAO nếu Monster có thể trùng vị trí với Player
                if m_move == p_move:
                    eval_score -= 20000  # BONUS CỰC LỚN cho việc bắt Player
                elif player_dist_new == 0:
                    eval_score -= 15000  # Monster đã ở vị trí Player
                elif player_dist_new == 1:
                    eval_score -= 8000   # Sắp bắt được Player
                else:
                    # Logic cải tiến cho việc tiến gần - MẠNH HƠN
                    distance_improvement = player_dist_current - player_dist_new
                    if distance_improvement > 0:
                        # Monster tiến gần = reward lớn
                        if player_dist_new <= 2:
                            eval_score -= distance_improvement * 200  # Tăng từ 100
                        elif player_dist_new <= 4:
                            eval_score -= distance_improvement * 120   # Tăng từ 60
                        elif player_dist_new <= 8:
                            eval_score -= distance_improvement * 80    # Thêm level mới
                        else:
                            eval_score -= distance_improvement * 50    # Tăng từ 30
                    elif distance_improvement < 0:
                        # Monster đi xa = penalty lớn
                        penalty = abs(distance_improvement) * 50      # Tăng từ 25
                        eval_score += penalty
                    else:
                        # Monster đứng yên = penalty nhỏ
                        eval_score += 5
                
                if monster_hist and m_move in monster_hist[-2:]:
                    eval_score += 3
                
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_player_move = p_move
                    best_monster_move = m_move
        
        return best_eval, best_player_move, best_monster_move
    
    # Game loop
    game_over = False
    moves_count = 0
    max_moves = 200  # Giới hạn số nước đi
    player_history = []  # Theo dõi lịch sử Player
    monster_history = []  # Theo dõi lịch sử Monster
    
    while game.is_running and not game_over and moves_count < max_moves:
        # Handle frame
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return
        
        # Cập nhật trạng thái hiển thị
        visited.add(player_pos)
        update_game_state(game, player_pos[0], player_pos[1], visited)
        
        # Cập nhật vị trí hiện tại để hiển thị
        game.current_node = player_pos
        game.path = [player_pos]
        game.player_pos = player_pos
        game.monster_pos = monster_pos
        
        # Vẽ frame
        game.draw_frame()
        time.sleep(0.5)
        
        # Kiểm tra điều kiện thắng/thua
        if player_pos == goal_pos:
            print(" PLAYER THẮNG! BFS-Enhanced Minimax thành công!")
            game_over = True
            break
        
        if player_pos == monster_pos:
            print(" GAME OVER! Monster bắt được Player!")
            game_over = True
            break
        
        # BFS VALIDATION: Kiểm tra đường đi trước mỗi lượt
        has_path, current_distance, current_path = validate_path_exists(game, player_pos, goal_pos)
        
        if not has_path:
            print(f"  Không có đường đi từ {player_pos} đến goal! Trying to escape...")
            # Thử tìm nước đi thoát khỏi ngõ cụt
            escape_moves = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x, y = player_pos
                new_pos = (x + dx, y + dy)
                if (0 <= new_pos[0] < len(game.maze) and 
                    0 <= new_pos[1] < len(game.maze[0]) and 
                    game.maze[new_pos[0]][new_pos[1]] == 0):
                    test_path, test_distance, _ = validate_path_exists(game, new_pos, goal_pos)
                    if test_path:
                        escape_moves.append((new_pos, test_distance))
            
            if escape_moves:
                # Chọn move có đường đi ngắn nhất đến goal
                escape_moves.sort(key=lambda x: x[1])
                best_player_move = escape_moves[0][0]
                print(f" Escape move: {player_pos} → {best_player_move}")
            else:
                print(" Bị kẹt hoàn toàn!")
                break
        else:
            # Hiển thị thông tin BFS mỗi 5 moves
            if moves_count % 5 == 0:
                print(f"  BFS Path: distance={current_distance}, preview={current_path[:3]}...")
            
            # Chạy Minimax để tìm nước đi tốt nhất
            _, best_player_move, best_monster_move = minimax_pure(
                player_pos, monster_pos, max_depth, 
                player_history[-5:], monster_history[-5:]
            )
        
        # Thực hiện nước đi với validation
        if best_player_move and best_player_move != player_pos:
            # Kiểm tra xem move có tạo ra ngõ cụt không
            post_move_path, post_move_distance, _ = validate_path_exists(game, best_player_move, goal_pos)
            if post_move_path or moves_count == 0:  # Cho phép move đầu tiên
                player_history.append(player_pos)
                player_pos = best_player_move
            else:
                print(f" Skipping move {player_pos} → {best_player_move} (tạo ngõ cụt)")
        
        if best_monster_move and best_monster_move != monster_pos:
            monster_history.append(monster_pos)
            monster_pos = best_monster_move
        
        moves_count += 1
        step_count += 1
    
    if moves_count >= max_moves:
        final_distance, _, _ = validate_path_exists(game, player_pos, goal_pos)
        initial_distance, _, _ = validate_path_exists(game, start_pos, goal_pos)
        if final_distance != float('inf') and initial_distance != float('inf'):
            progress = ((initial_distance - final_distance) / initial_distance) * 100
            print(f" Game timeout! Progress: {progress:.1f}% (BFS: {final_distance} steps from goal)")
        else:
            print(f"⏰ Game timeout! Position: {player_pos}")

    # Kết thúc
    game.is_running = False
    game.current_node = None
    
    # Kiểm tra goal cuối cùng
    if player_pos == goal_pos:
        if check_goal(game, player_pos[0], player_pos[1], [player_pos]):
            return
    
    algorithm_finished(game)

def is_valid_move(game, x, y):
    """Kiểm tra nước đi hợp lệ"""
    return (0 <= x < len(game.maze) and 0 <= y < len(game.maze[0]) and 
            game.maze[x][y] == 0)
