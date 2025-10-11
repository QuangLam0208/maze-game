from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
import pygame
import time
import math

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_minimax(game):
    """
    Thuật toán Minimax cải tiến:
    - Player: Tìm đường đến goal nhưng TRÁNH Monster 
    - Monster: Di chuyển 2 ô mỗi lượt để đuổi theo Player
    - Sử dụng Minimax thuần túy với defensive strategy
    """
    game.alg_name = "Minimax Defense (Player vs Fast Monster)"

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
    
    print(f"Bắt đầu: Player tại {player_pos}, Monster tại {monster_pos}, Goal tại {goal_pos}")
    
    visited = set()
    game.backtracked_nodes = set()
    step_count = 0
    max_depth = 3  # Giảm độ sâu để tăng tốc độ
    
    # Tracking để tránh vòng lặp
    player_history = []  # Lưu lịch sử di chuyển của player
    monster_history = []  # Lưu lịch sử di chuyển của monster
    position_frequency = {}  # Đếm số lần đến mỗi vị trí
    
    # Thêm thuộc tính để tracking positions
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
        """
        Hàm đánh giá trạng thái:
        - Player tìm đường đến goal nhưng TRÁNH Monster
        - Monster đuổi theo Player với tốc độ 2 ô/lượt
        """
        # Khoảng cách từ player đến goal
        dist_to_goal = manhattan_distance(player_pos, goal_pos)
        
        # Khoảng cách giữa player và monster
        dist_player_monster = manhattan_distance(player_pos, monster_pos)
        
        # Player thắng nếu đến goal
        if player_pos == goal_pos:
            return 1000
        
        # Monster thắng nếu bắt được player
        if player_pos == monster_pos:
            return -1000
        
        # Heuristic cân bằng: Player tránh Monster, Monster tích cực bắt Player
        score = 0
        
        # 1. Player ưu tiên tiến về goal (nhưng không quá cao)
        score -= dist_to_goal * 20
        
        # 2. Monster ưu tiên BẮT Player (MỨC ĐỘ CAO NHẤT!)
        if dist_player_monster <= 2:  # Monster rất gần = cực kỳ nguy hiểm cho Player
            score -= dist_player_monster * 100  # Tăng MẠNH để Monster ưu tiên bắt
        elif dist_player_monster <= 4:  # Monster gần = nguy hiểm
            score -= dist_player_monster * 60
        else:  # Monster xa = Monster cần tiến gần
            score -= dist_player_monster * 30
        
        # 3. Player MẠNH MẼ tránh Monster khi gần
        if dist_player_monster <= 3:  # Monster gần = Player cần tránh gấp
            score += dist_player_monster * 80  # Bonus MẠNH cho việc xa Monster
        elif dist_player_monster <= 5:  # Monster hơi gần = cẩn thận
            score += dist_player_monster * 40
        
        # 4. Khi Player an toàn (Monster xa), tập trung về goal
        if dist_player_monster > 5:
            score -= dist_to_goal * 15  # Tăng ưu tiên goal khi an toàn
        
        # Bonus mạnh cho việc di chuyển đúng hướng
        if player_prev and player_pos != player_prev:
            # Kiểm tra nếu Player tiến gần goal hơn
            prev_dist_to_goal = manhattan_distance(player_prev, goal_pos)
            if dist_to_goal < prev_dist_to_goal:
                score += 15  # Bonus lớn cho việc tiến về goal
            else:
                score -= 5   # Penalty cho việc xa goal hơn
        
        if monster_prev and monster_pos != monster_prev:
            # Kiểm tra nếu Monster tiến gần player hơn
            prev_dist_to_player = manhattan_distance(monster_prev, player_pos)
            if dist_player_monster < prev_dist_to_player:
                score -= 15  # Bonus lớn cho Monster (xấu cho Player)
            else:
                score += 5   # Penalty cho Monster (tốt cho Player)
        
        # Penalty mạnh cho việc đứng yên
        if player_prev and player_pos == player_prev:
            score -= 20  # Player đứng yên = rất xấu
        if monster_prev and monster_pos == monster_prev:
            score += 10  # Monster đứng yên = khá tốt cho player
        
        return score
    
    def minimax_pure(player_pos, monster_pos, depth, player_hist=None, monster_hist=None):
        """
        Minimax thuần túy - không có Alpha-Beta pruning
        Duyệt tất cả các nước đi có thể để tìm nước đi tốt nhất
        Trả về (eval_score, best_player_move, best_monster_move)
        """
        # Base cases
        if depth == 0:
            p_prev = player_hist[-1] if player_hist else None
            m_prev = monster_hist[-1] if monster_hist else None
            return evaluate_state(player_pos, monster_pos, p_prev, m_prev), None, None
        
        if player_pos == goal_pos:
            return 1000, None, None
        
        if player_pos == monster_pos:
            return -1000, None, None
        
        # Player tối đa hóa, Monster tối thiểu hóa
        best_eval = -math.inf
        best_player_move = None
        best_monster_move = None
        
        player_moves = get_possible_moves(player_pos, is_player=True, recent_positions=player_hist)
        monster_moves = get_possible_moves(monster_pos, is_player=False, recent_positions=monster_hist, target_pos=player_pos)
        
        # Thử tất cả kết hợp player-monster moves
        for p_move in player_moves:
            for m_move in monster_moves:
                # Kiểm tra nếu move collision (cả hai đến cùng vị trí)
                if p_move == m_move:
                    continue  # Skip moves va chạm
                
                new_player_hist = (player_hist + [player_pos]) if player_hist else [player_pos]
                new_monster_hist = (monster_hist + [monster_pos]) if monster_hist else [monster_pos]
                
                eval_score, _, _ = minimax_pure(p_move, m_move, depth-1, 
                                              new_player_hist, new_monster_hist)
                
                # Player perspective: Cân bằng giữa goal và tránh Monster
                goal_dist_current = manhattan_distance(player_pos, goal_pos)
                goal_dist_new = manhattan_distance(p_move, goal_pos)
                monster_dist_current = manhattan_distance(player_pos, monster_pos)
                monster_dist_new = manhattan_distance(p_move, m_move)
                
                # Bonus cho Player tiến về goal (nhưng không quá mạnh)
                if goal_dist_new < goal_dist_current:
                    eval_score += 15
                elif goal_dist_new > goal_dist_current:
                    eval_score -= 10
                
                # Bonus MẠNH cho Player tránh Monster
                if monster_dist_current <= 3:  # Monster gần = ưu tiên tránh
                    if monster_dist_new > monster_dist_current:
                        eval_score += 25  # Bonus lớn cho việc tránh Monster
                    else:
                        eval_score -= 20  # Penalty cho việc đến gần Monster
                elif monster_dist_current <= 5:  # Monster hơi gần = cẩn thận
                    if monster_dist_new > monster_dist_current:
                        eval_score += 10
                    else:
                        eval_score -= 8
                
                # Penalty cho Player quay lại vị trí cũ
                if player_hist and p_move in player_hist[-3:]:
                    penalty = len([pos for pos in player_hist[-3:] if pos == p_move]) * 5
                    eval_score -= penalty  # Tăng penalty
                
                # Monster perspective: SIÊU TÍCH CỰC đuổi theo Player
                player_dist_current = manhattan_distance(monster_pos, player_pos)
                player_dist_new = manhattan_distance(m_move, p_move)  # Khoảng cách sau khi cả hai di chuyển
                
                # Bonus MẠNH MẼ cho Monster tiến gần Player
                distance_improvement = player_dist_current - player_dist_new
                if distance_improvement > 0:  # Monster tiến gần Player
                    # Bonus tăng theo cấp số khi Monster gần Player
                    if player_dist_new <= 2:  # Rất gần = bonus cực lớn
                        eval_score -= distance_improvement * 50
                    elif player_dist_new <= 4:  # Gần = bonus lớn
                        eval_score -= distance_improvement * 30
                    else:  # Xa = bonus thường
                        eval_score -= distance_improvement * 20
                elif distance_improvement < 0:  # Monster xa Player hơn
                    penalty = abs(distance_improvement) * 15
                    eval_score += penalty  # Penalty cho Monster
                
                # Bonus đặc biệt nếu Monster có thể bắt Player trong 1-2 move
                if player_dist_new <= 1:  # Monster sắp bắt được Player
                    eval_score -= 100  # Bonus cực lớn cho tình huống này
                
                # Monster penalty cho việc quay lại
                if monster_hist and m_move in monster_hist[-2:]:
                    eval_score += 3  # Tăng penalty cho Monster lặp lại
                
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
            print("🎉 PLAYER THẮNG! 🎉")
            print("Player đã đến được đích thành công!")
            game_over = True
            break
        
        if player_pos == monster_pos:
            print("💀 GAME OVER! 💀")
            print("Monster đã bắt được Player!")
            print(f"Player bị bắt tại vị trí: {player_pos}")
            game_over = True
            break
        
        # Chạy Minimax thuần túy để tìm nước đi tốt nhất
        _, best_player_move, best_monster_move = minimax_pure(
            player_pos, monster_pos, max_depth, 
            player_history[-5:], monster_history[-5:]  # Chỉ xét 5 bước gần nhất
        )
        
        # Debug thông tin
        if moves_count < 5:  # Chỉ debug 5 move đầu
            print(f"  Minimax suggest: Player {player_pos} -> {best_player_move}, Monster {monster_pos} -> {best_monster_move}")
        
        # Thực hiện nước đi và cập nhật lịch sử
        if best_player_move and best_player_move != player_pos:
            player_history.append(player_pos)  # Lưu vị trí cũ
            player_pos = best_player_move
        
        # Monster đi sau (có thể điều chỉnh để đi cùng lúc)
        if best_monster_move and best_monster_move != monster_pos:
            monster_history.append(monster_pos)  # Lưu vị trí cũ
            monster_pos = best_monster_move
        
        moves_count += 1
        step_count += 1
        
        # Hiển thị thông tin
        print(f"Move {moves_count}: Player at {player_pos}, Monster at {monster_pos}")
    
    if moves_count >= max_moves:
        print(" Game kết thúc do quá nhiều nước đi!")
    
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
