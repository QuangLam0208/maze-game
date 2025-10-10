from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
import pygame
import time
import math

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_minimax(game):
    """
    Thuật toán Minimax thuần túy (không Alpha-Beta pruning):
    - Max Player (Xanh): Cố gắng đến goal, tránh Monster
    - Min Monster (Đỏ): Cố gắng bắt Player
    - Sử dụng Minimax đơn giản với simultaneous moves
    """
    game.alg_name = "Minimax Pure (Player vs Monster)"

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
    
    def get_possible_moves(pos, is_player=True, recent_positions=None):
        """Lấy các nước đi hợp lệ từ vị trí, tránh vòng lặp"""
        moves = []
        x, y = pos
        
        # Tất cả hướng di chuyển, không có đứng yên
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(game.maze) and 0 <= new_y < len(game.maze[0]) and 
                game.maze[new_x][new_y] == 0):
                moves.append((new_x, new_y))
        
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
        - Positive: Tốt cho Max (Player)
        - Negative: Tốt cho Min (Monster)
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
        
        # Heuristic cải tiến - ưu tiên SIÊU MẠNH
        score = 0
        
        # Player: SIÊU MẠNH ưu tiên tiến về goal (quan trọng nhất!)
        score -= dist_to_goal * 100  # Tăng lên 100 để goal là ưu tiên tuyệt đối
        
        # Monster: Mạnh ưu tiên tiến gần player (ưu tiên thứ hai)
        score += dist_player_monster * 20  # Giảm xuống để không cản trở Player về goal
        
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
        monster_moves = get_possible_moves(monster_pos, is_player=False, recent_positions=monster_hist)
        
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
                
                # Player perspective: SIÊU MẠNH ưu tiên goal
                # Bonus SIÊU MẠNH cho Player tiến về goal
                goal_dist_current = manhattan_distance(player_pos, goal_pos)
                goal_dist_new = manhattan_distance(p_move, goal_pos)
                if goal_dist_new < goal_dist_current:
                    eval_score += 50  # Tăng lên 50 - goal là ưu tiên tuyệt đối
                elif goal_dist_new > goal_dist_current:
                    eval_score -= 30  # Penalty MẠNH cho việc xa goal hơn
                
                # Penalty cho Player quay lại vị trí cũ
                if player_hist and p_move in player_hist[-3:]:
                    penalty = len([pos for pos in player_hist[-3:] if pos == p_move]) * 5
                    eval_score -= penalty  # Tăng penalty
                
                # Monster perspective: MẠNH MẼ ưu tiên đuổi theo Player
                # Bonus MẠNH cho Monster tiến gần Player
                player_dist_current = manhattan_distance(monster_pos, player_pos)
                player_dist_new = manhattan_distance(m_move, player_pos)
                if player_dist_new < player_dist_current:
                    eval_score -= 20  # Tăng MẠNH bonus cho Monster (xấu cho Player)
                elif player_dist_new > player_dist_current:
                    eval_score += 8   # Penalty cho Monster xa Player (tốt cho Player)
                
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
            print(" Player (Max) thắng! Đã đến đích!")
            game_over = True
            break
        
        if player_pos == monster_pos:
            print(" Monster (Min) thắng! Đã bắt được Player!")
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
