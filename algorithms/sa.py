import math, random
from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished
from .heuristic import DEFAULT_HEURISTIC

def run_simulated_annealing(game, initial_temp=1000, cooling_rate=0.99, heuristic=DEFAULT_HEURISTIC):

    game.alg_name = "SA"

    # Sử dụng custom start và end nếu có
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    start = start_pos
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal = (len(game.maze)-1, len(game.maze[0])-1)
    else:
        goal = goal_pos

    # current_state = (cell, path, cost)
    current = (start, [start], heuristic(start, goal))
    temperature = initial_temp
    step_count = 0
    visited_set = set()

    while game.is_running and temperature > 1:
        result = handle_frame(game, step_count)
        if result is None:
            return
        step_count, ok = result
        if not ok:
            return

        (x, y), path, cost = current

        # Nếu đã thăm rồi → bỏ qua
        if (x, y) in visited_set:
            print(f"[Step {step_count}] Already visited {x, y}, stopping.")
            game.is_running = False
            break

        visited_set.add((x, y))
        update_game_state(game, x, y, visited_set)
        
        # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
        game.path = path
        
        step_count += 1
        print(f"[Step {step_count}] At {x, y}, cost={cost:.2f}, temp={temperature:.2f}")

        if check_goal(game, x, y, path):
            break

        # Sinh neighbors (chỉ lấy ô chưa thăm)
        neighbors = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(game.maze) and 
                0 <= ny < len(game.maze[0]) and 
                game.maze[nx][ny] == 0 and 
                (nx, ny) not in visited_set
            ):
                new_cell = (nx, ny)
                neighbors.append((new_cell, path + [new_cell], heuristic(new_cell, goal)))
                game.stats["nodes_expanded"] += 1

        # Nếu hết đường → dừng luôn
        if not neighbors:
            print(f"[Step {step_count}] Dead end at {x, y}, stopping.")
            game.is_running = False
            break

        # Chọn neighbor
        best_neighbor = min(neighbors, key=lambda n: n[2])
        if best_neighbor[2] < cost:
            current = best_neighbor
        else:
            random_neighbor = random.choice(neighbors)
            delta = random_neighbor[2] - cost
            if random.random() < math.exp(-delta / temperature):
                current = random_neighbor

        temperature *= cooling_rate

    game.is_running = False
    game.current_node = None
    
    # Add to history if no path was found
    algorithm_finished(game)