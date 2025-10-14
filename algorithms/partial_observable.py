from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished

def run_partial_observable_dfs(game, vision_range=1):
    """
    DFS trong môi trường chỉ nhìn thấy một phần (partial observable).
    vision_range: bán kính nhìn (số ô agent có thể quan sát).
    """

    game.alg_name = "Partial Observable"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos

    # Bản đồ đã biết (khởi tạo toàn bộ là "chưa biết")
    known_maze = [[-1 for _ in row] for row in game.maze]  # -1 = chưa biết, 0 = đường, 1 = tường
    game.known_maze = known_maze
    game.visible_cells = []  # để highlight tầm nhìn

    # Stack cho DFS
    stack = [(start_x, start_y, [])]
    visited_set = set()
    step_count = 0

    def observe(x, y):
        """Cập nhật thông tin mê cung trong tầm nhìn của agent"""
        visible = []
        for dx in range(-vision_range, vision_range + 1):
            for dy in range(-vision_range, vision_range + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]):
                    known_maze[nx][ny] = game.maze[nx][ny]
                    visible.append((nx, ny))
        game.visible_cells = visible

    # Quan sát ban đầu
    observe(start_x, start_y)

    while stack and game.is_running:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        x, y, current_path = stack.pop()
        if (x, y) in visited_set:
            continue

        # Cập nhật trạng thái
        update_game_state(game, x, y, visited_set)
        step_count += 1
        observe(x, y)  # Cập nhật kiến thức khi đứng tại (x, y)

        # Cập nhật đường đi hiện tại và node đang xét để hiển thị màu vàng
        game.path = current_path + [(x, y)]
        game.current_node = (x, y)

        # Kiểm tra goal
        if check_goal(game, x, y, current_path):
            break

        visited_set.add((x, y))

        # Thêm các node kề vào stack (chỉ thêm nếu đã "nhìn thấy" và ô là đường)
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(game.maze) and 
                0 <= new_y < len(game.maze[0]) and
                (new_x, new_y) in game.visible_cells and
                known_maze[new_x][new_y] == 0 and
                (new_x, new_y) not in visited_set):
                stack.append((new_x, new_y, current_path + [(x, y)]))

    game.is_running = False
    game.current_node = None
    if hasattr(game, "visible_cells"):
        delattr(game, "visible_cells")
    
    # Add to history if no path was found
    algorithm_finished(game)
