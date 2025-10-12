from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
import pygame
import time
import math

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_minimax(game):
    """
    Thuật toán Minimax tối ưu:
    - Player: Siêu ưu tiên goal, chỉ né Monster khi cực gần
    - Monster: Di chuyển 2 ô/lượt đuổi Player tích cực
    - Code đã được tối ưu và làm gọn
    """
    game.alg_name = "Minimax Optimized (Aggressive Goal-Seeking)"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal_pos = (len(game.maze)-1, len(game.maze[0])-1)

    # Vị trí ban đầu
    player_pos = start_pos  # Max player (xanh)
    
    # Tìm vị trí hợp lệ cho monster (xa player nhất có thể, nhưng không trùng goal)
    monster_pos = None
    max_distance = 0
    for i in range(len(game.maze)):
        for j in range(len(game.maze[0])):
            if (game.maze[i][j] == 0 and  # Vị trí hợp lệ
                (i, j) != goal_pos and    # Không trùng goal
                (i, j) != player_pos):    # Không trùng player
                distance = manhattan_distance((i, j), player_pos)
                if distance > max_distance:
                    max_distance = distance
                    monster_pos = (i, j)
    
    if monster_pos is None:
        # Fallback: tìm vị trí gần goal nhưng không trùng
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            new_x, new_y = goal_pos[0] + dx, goal_pos[1] + dy
            if (0 <= new_x < len(game.maze) and 0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0):
                monster_pos = (new_x, new_y)
                break
        
        if monster_pos is None:
            monster_pos = player_pos  # Last resort
    
    # Khởi tạo vị trí
    print(f"🎮 Bắt đầu: Player {player_pos}, Monster {monster_pos}, Goal {goal_pos}")
    
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
            # Monster di chuyển tối đa 2 ô mỗi lượt về phía Player - HIỆU QUẢ HỒN
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
            
            # Lấy các moves tốt nhất (chỉ những moves cải thiện khoảng cách)
            for improvement, move in move_candidates:
                if improvement > 0:  # Chỉ lấy moves làm gần Player hơn
                    moves.append(move)
            
            # Nếu không có move nào cải thiện, lấy move ít xấu nhất
            if not moves and move_candidates:
                moves.append(move_candidates[0][1])
            
            # Loại bỏ trùng lặp và giới hạn số lượng
            moves = list(dict.fromkeys(moves))  # Giữ thứ tự và loại trùng
            if len(moves) > 6:  # Giới hạn để tránh quá nhiều options
                moves = moves[:6]
        
        # Tránh vòng lặp: ưu tiên moves chưa đi gần đây
        if recent_positions and len(moves) > 1:
            # Sắp xếp moves theo mức độ "mới"
            def move_priority(move):
                if move in recent_positions[-3:]:  # Đã đi trong 3 bước gần đây
                    return 1  # Ưu tiên thấp
                elif move in recent_positions:
                    return 2  # Ưu tiên trung bình
                else:
                    return 0  # Ưu tiên cao (chưa đi)
            
            moves.sort(key=move_priority)
        
        # Nếu không có nước đi nào, cho phép đứng yên
        if not moves:
            moves.append(pos)
            
        return moves
    
    def evaluate_state(player_pos, monster_pos, player_prev=None, monster_prev=None):
        """Đánh giá trạng thái: Player ưu tiên goal, Monster đuổi Player"""
        dist_to_goal = manhattan_distance(player_pos, goal_pos)
        dist_player_monster = manhattan_distance(player_pos, monster_pos)
        
        # Win/Loss conditions
        if player_pos == goal_pos:
            return 1000
        if player_pos == monster_pos:
            return -1000
        
        score = 0
        
        # Player siêu ưu tiên goal
        score -= dist_to_goal * 60
        
        # Monster ưu tiên bắt Player
        if dist_player_monster <= 2:
            score -= dist_player_monster * 100
        elif dist_player_monster <= 4:
            score -= dist_player_monster * 60
        else:
            score -= dist_player_monster * 30
        
        # Player chỉ tránh khi Monster cực kỳ gần
        if dist_player_monster <= 1:
            score += dist_player_monster * 120
        elif dist_player_monster <= 2:
            score += dist_player_monster * 60
        
        # Luôn ưu tiên goal
        score -= dist_to_goal * 25
        
        # Bonus cho movement về goal
        if player_prev and player_pos != player_prev:
            prev_dist_to_goal = manhattan_distance(player_prev, goal_pos)
            if dist_to_goal < prev_dist_to_goal:
                score += 30
            else:
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
            return 1000, None, None
        if player_pos == monster_pos:
            return -1000, None, None
        
        best_eval = -math.inf
        best_player_move = None
        best_monster_move = None
        
        player_moves = get_possible_moves(player_pos, is_player=True, recent_positions=player_hist)
        monster_moves = get_possible_moves(monster_pos, is_player=False, recent_positions=monster_hist, target_pos=player_pos)
        
        for p_move in player_moves:
            for m_move in monster_moves:
                if p_move == m_move:  # Tránh collision
                    continue
                
                new_player_hist = (player_hist + [player_pos]) if player_hist else [player_pos]
                new_monster_hist = (monster_hist + [monster_pos]) if monster_hist else [monster_pos]
                
                eval_score, _, _ = minimax_pure(p_move, m_move, depth-1, new_player_hist, new_monster_hist)
                
                # Evaluation adjustments
                goal_dist_current = manhattan_distance(player_pos, goal_pos)
                goal_dist_new = manhattan_distance(p_move, goal_pos)
                monster_dist_current = manhattan_distance(player_pos, monster_pos)
                monster_dist_new = manhattan_distance(p_move, m_move)
                
                # Player goal bonus
                if goal_dist_new < goal_dist_current:
                    eval_score += 15
                elif goal_dist_new > goal_dist_current:
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
                
                # Monster chase player
                player_dist_current = manhattan_distance(monster_pos, player_pos)
                player_dist_new = manhattan_distance(m_move, p_move)
                distance_improvement = player_dist_current - player_dist_new
                
                if distance_improvement > 0:
                    if player_dist_new <= 2:
                        eval_score -= distance_improvement * 50
                    elif player_dist_new <= 4:
                        eval_score -= distance_improvement * 30
                    else:
                        eval_score -= distance_improvement * 20
                elif distance_improvement < 0:
                    penalty = abs(distance_improvement) * 15
                    eval_score += penalty
                
                if player_dist_new <= 1:
                    eval_score -= 100
                
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
            print("🎉 PLAYER THẮNG!")
            game_over = True
            break
        
        if player_pos == monster_pos:
            print("💀 GAME OVER! Monster bắt được Player!")
            game_over = True
            break
        
        # Chạy Minimax để tìm nước đi tốt nhất
        _, best_player_move, best_monster_move = minimax_pure(
            player_pos, monster_pos, max_depth, 
            player_history[-5:], monster_history[-5:]
        )
        
        # Thực hiện nước đi
        if best_player_move and best_player_move != player_pos:
            player_history.append(player_pos)
            player_pos = best_player_move
        
        if best_monster_move and best_monster_move != monster_pos:
            monster_history.append(monster_pos)
            monster_pos = best_monster_move
        
        moves_count += 1
        step_count += 1
    
    if moves_count >= max_moves:
        print("⏰ Game timeout!")
    
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
