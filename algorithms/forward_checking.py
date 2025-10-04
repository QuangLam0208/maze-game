from utils.algorithm_runner import update_game_state, check_goal, handle_frame
import pygame

def run_forward_checking(game):
    """
    Forward Checking (CSP style):
    - Mỗi bước đi coi như gán giá trị cho biến.
    - Sau khi gán, cập nhật miền giá trị của biến còn lại.
    - Nếu miền rỗng -> backtrack.
    """

    game.alg_name = "Forward Checking (CSP)"

    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start_x, start_y = start_pos
    goal_pos = getattr(game, 'custom_end', (len(game.maze)-1, len(game.maze[0])-1))

    # Domain = tất cả cell hợp lệ
    domain = {(i, j) for i in range(len(game.maze))
                        for j in range(len(game.maze[0])) if game.maze[i][j] == 0}

    visited = set()
    step_count = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def forward_check(x, y, path):
        nonlocal step_count

        if not game.is_running:
            return False

        # Frame update
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return False

        # Gán giá trị cho biến hiện tại
        update_game_state(game, x, y, visited)
        game.draw_frame()
        pygame.time.wait(80)

        # Check goal
        if check_goal(game, x, y, path):
            return True

        visited.add((x, y))

        # Forward checking: tính miền còn lại của biến kế
        possible_moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in domain and (nx, ny) not in visited:
                # Kiểm tra miền của (nx,ny): còn ít nhất 1 neighbor khả thi sau nó?
                future = [
                    (nx + ddx, ny + ddy)
                    for ddx, ddy in directions
                    if (nx + ddx, ny + ddy) in domain and (nx + ddx, ny + ddy) not in visited
                ]
                if future:  # còn miền hợp lệ
                    possible_moves.append((nx, ny))

        # Thử gán cho từng biến kế tiếp
        for (nx, ny) in possible_moves:
            if forward_check(nx, ny, path + [(x, y)]):
                return True

        # Nếu không thành công -> backtrack
        visited.remove((x, y))
        if (x, y) in game.visited:
            game.visited.remove((x, y))  # node quay lại trắng
            game.draw_frame()

        return False

    forward_check(start_x, start_y, [])

    game.is_running = False
    game.current_node = None
