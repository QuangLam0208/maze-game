from utils.algorithm_runner import update_game_state, check_goal, handle_frame
import pygame

def run_forward_checking(game):
    """
    Forward Checking (CSP style - domain động + restore):
    - Biến: mỗi ô trong maze.
    - Domain: tập các ô trống còn khả thi (ban đầu = all_cells).
    - Khi gán (visit node): loại ô đó khỏi domain của tất cả biến khác.
    - Nếu có biến nào domain rỗng (trừ goal) -> backtrack sớm.
    - Khi backtrack: restore domain.
    """

    game.alg_name = "Forward Checking (CSP)"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos
    goal_pos = getattr(game, 'custom_end', (len(game.maze)-1, len(game.maze[0])-1))

    step_count = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Ban đầu: all_cells = mọi ô trống trong maze
    all_cells = {(i, j) for i in range(len(game.maze))
                           for j in range(len(game.maze[0]))
                           if game.maze[i][j] == 0}

    # Domain động: mỗi biến (cell) có domain riêng = all_cells ban đầu
    domains = {cell: set(all_cells) for cell in all_cells}

    visited = set()
    
    # Khởi tạo backtracked_nodes để theo dõi các node đã đi qua
    game.backtracked_nodes = set()

    def forward_check(x, y, path):
        nonlocal step_count

        if not game.is_running:
            return False

        # Frame update
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return False

        # Gán giá trị cho biến (visit node)
        update_game_state(game, x, y, visited)
        
        # Cập nhật đường đi hiện tại để hiển thị màu vàng cho node đang xét
        game.path = path + [(x, y)]
        game.current_node = (x, y)
        
        game.draw_frame()
        pygame.time.wait(80)

        # Nếu tới goal thì kết thúc
        if check_goal(game, x, y, path):
            return True

        visited.add((x, y))

        # --- Forward checking toàn cục ---
        pruned = []
        dead = False
        for var in domains:
            if var not in visited:  # chỉ xét biến chưa gán
                if (x, y) in domains[var]:
                    domains[var].remove((x, y))
                    pruned.append((var, (x, y)))
                # Nếu domain rỗng và không phải goal -> dead-end
                if not domains[var] and var != goal_pos:
                    dead = True
                    break

        if dead:
            # Restore domain
            for (var, val) in pruned:
                domains[var].add(val)
            visited.remove((x, y))
            
            # Chuyển node sang backtracked_nodes thay vì xóa khỏi game.visited
            if (x, y) in game.visited:
                game.visited.remove((x, y))
                game.backtracked_nodes.add((x, y))
                
                # Cập nhật path và current_node khi dead-end
                game.path = path
                if path:
                    game.current_node = path[-1]
                else:
                    game.current_node = None
                    
                game.draw_frame()
                pygame.time.wait(50)
            return False

        # --- Sinh candidate moves (neighbor 4 hướng) ---
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in domains and (nx, ny) not in visited:
                if forward_check(nx, ny, path + [(x, y)]):
                    return True

        # --- Backtrack ---
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

        # Restore domain khi backtrack
        for (var, val) in pruned:
            domains[var].add(val)

        return False

    forward_check(start_x, start_y, [])

    game.is_running = False
    game.current_node = None