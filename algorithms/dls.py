from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished


def run_dls(game):
    """Chạy Depth-Limited Search"""

    game.alg_name = "Depth-Limited Search"

    # Sử dụng custom_start nếu có và không phải None, ngược lại dùng (0, 0)
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos

    limit = game.MAZE_SIZE * game.MAZE_SIZE
    path = Recursive_DLS(game, start_x, start_y, [], set(), limit, 0)
    if path is not None:
        game.path = path
        game.stats["path_length"] = len(path)
    game.is_running = False
    game.current_node = None
    
    # Add to history if no path was found
    algorithm_finished(game)


def Recursive_DLS(game, x, y, current_path, visited_set, limit, step_count):
    """
    Đệ quy DLS:
    - x, y: node hiện tại
    - current_path: ds các ô đã đi
    - visited_set: để tránh lặp
    - limit: số bước còn lại
    - step_count: dùng cho handle_frame
    """
    if not game.is_running:
            return None
        
    # animation & sự kiện   
    result = handle_frame(game, step_count)
    if result is None:
        return None
    step_count, ok = result
    if not ok:
        return None

    # cập nhật trạng thái node hiện tại
    update_game_state(game, x, y, visited_set)
    
    # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
    game.path = current_path + [(x, y)]

    # Nếu tới Goal
    if check_goal(game, x, y, current_path):
        return current_path + [(x, y)]

    # Hết giới hạn độ sâu
    if limit == 0:
        return None

    # Duyệt 4 hướng
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and #không ra ngoài biên của mê cung.
            game.maze[nx][ny] == 0 and (nx, ny) not in visited_set): #ô trống và chưa đi qua trước đó

            result = Recursive_DLS(game, nx, ny, current_path + [(x, y)], visited_set, limit - 1, step_count + 1) #Gọi đệ quy thử đi tiếp từ ô (nx, ny)
            if result is not None:
                return result

    # Nếu không tìm thấy
    return None
