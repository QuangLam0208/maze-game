from utils.algorithm_runner import update_game_state, check_goal, handle_frame
import pygame
from collections import deque

def run_ac3_csp(game):
    """
    Thuật toán AC-3 (Arc Consistency) áp dụng cho bài toán tìm đường trong mê cung.
    - Biến: mỗi ô trong mê cung (cell).
    - Domain: tập các vị trí còn hợp lệ có thể gán cho biến.
    - Constraint: ràng buộc giữa các ô kề (neighbor). 
      Nếu Xi và Xj là ô kề nhau thì giá trị gán cho Xi và Xj phải khác nhau.
    - Backtracking: nếu AC-3 phát hiện domain rỗng → quay lui (backtrack).
    """

    game.alg_name = "AC-3"

    # Lấy vị trí start và goal
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos
    goal_pos = getattr(game, 'custom_end',
                       (len(game.maze)-1, len(game.maze[0])-1))

    step_count = 0
    # Hướng di chuyển 4 chiều: phải, xuống, trái, lên
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Tập tất cả ô trống trong mê cung
    all_cells = {(i, j) for i in range(len(game.maze))
                           for j in range(len(game.maze[0]))
                           if game.maze[i][j] == 0}

    # Domain ban đầu: mỗi biến (cell) có domain = all_cells
    # (có thể gán bất kỳ vị trí trống nào, AC-3 sẽ thu hẹp dần)
    domains = {cell: set(all_cells) for cell in all_cells}

    visited = set()
    
    # Khởi tạo backtracked_nodes để theo dõi các node đã đi qua
    game.backtracked_nodes = set()

    def ac3(domains):
        """
        Duy trì arc consistency cho mê cung.
        - Hàng đợi khởi tạo: tất cả các cung (Xi, Xj) với Xj là neighbor của Xi.
        - Khi revise domain[Xi], nếu thay đổi thì thêm lại (Xk, Xi) với mọi neighbor Xk của Xi.
        """
        queue = deque()
        for xi in domains:
            for dx, dy in directions:
                nx, ny = xi[0] + dx, xi[1] + dy
                if (nx, ny) in domains:
                    queue.append((xi, (nx, ny)))

        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                if not domains[xi]:
                    # Nếu domain Xi rỗng => dead-end
                    return False
                # Thêm lại các neighbor của Xi (trừ Xj) để duy trì consistency
                for dx, dy in directions:
                    xk = (xi[0] + dx, xi[1] + dy)
                    if xk in domains and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(domains, xi, xj):
        """
        Revise domain[xi] dựa trên domain[xj].
        - Constraint: giá trị gán cho xi phải khác giá trị gán cho xj.
        - Nếu không tồn tại giá trị nào ở domain[xj] thỏa mãn → loại bỏ val khỏi domain[xi].
        """
        removed = False
        to_remove = []
        for val in domains[xi]:
            ok = False
            for val_j in domains[xj]:
                if val != val_j:   # Điều kiện (khác nhau)
                    ok = True
                    break
            if not ok:
                to_remove.append(val)

        for v in to_remove:
            domains[xi].remove(v)
            removed = True
        return removed

    #Backtracking 
    def backtrack(x, y, path):
        nonlocal step_count

        if not game.is_running:
            return False

        # Cập nhật frame
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return False

        # Đánh dấu đang thăm
        update_game_state(game, x, y, visited)
        
        # Cập nhật đường đi hiện tại để hiển thị màu vàng cho node đang xét
        game.path = path + [(x, y)]
        game.current_node = (x, y)
        
        game.draw_frame()
        pygame.time.wait(80)

        # Kiểm tra goal
        if check_goal(game, x, y, path):
            return True

        visited.add((x, y))

        # Khi gán ô (x,y), loại bỏ (x,y) khỏi domain của các biến khác
        pruned = []
        for var in domains:
            if var not in visited and (x, y) in domains[var]:
                domains[var].remove((x, y))
                pruned.append((var, (x, y)))

        # Duy trì arc-consistency bằng AC-3
        if not ac3(domains):
            # Nếu fail → backtrack, restore lại domain
            for (var, val) in pruned:
                domains[var].add(val)
            visited.remove((x, y))
            
            # Chuyển node sang backtracked_nodes thay vì xóa khỏi game.visited
            if (x, y) in game.visited:
                game.visited.remove((x, y))
                game.backtracked_nodes.add((x, y))
                
                # Cập nhật path và current_node khi backtrack
                game.path = path
                if path:
                    game.current_node = path[-1]
                else:
                    game.current_node = None
                    
                game.draw_frame()
                pygame.time.wait(50)
            return False

        # Tiếp tục mở rộng neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in domains and (nx, ny) not in visited:
                if backtrack(nx, ny, path + [(x, y)]):
                    return True

        # Backtrack 
        visited.remove((x, y))
        
        # Chuyển node sang backtracked_nodes thay vì xóa khỏi game.visited
        if (x, y) in game.visited:
            game.visited.remove((x, y))
            game.backtracked_nodes.add((x, y))
            
            # Cập nhật path và current_node khi backtrack
            game.path = path
            if path:
                game.current_node = path[-1]
            else:
                game.current_node = None
                
            game.draw_frame()
            pygame.time.wait(50)

        for (var, val) in pruned:
            domains[var].add(val)

        return False

    # Bắt đầu tìm đường
    backtrack(start_x, start_y, [])
    game.is_running = False
    game.current_node = None