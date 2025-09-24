import math, random
from utils.algorithm_runner import update_game_state, check_goal, handle_frame
from .heuristic import DEFAULT_HEURISTIC

def run_simulated_annealing(game, initial_temp=1000, cooling_rate=0.99, heuristic=DEFAULT_HEURISTIC):
    start = game.start
    goal = game.end

    # current_state = (cell, path, cost)
    current = (start, [start], heuristic(start, goal))
    temperature = initial_temp
    step_count = 0

    while game.is_running and temperature > 1:
        step_count, ok = handle_frame(game, step_count)
        if not ok:
            return

        (x, y), path, cost = current
        update_game_state(game, x, y, game.visited)

        if check_goal(game, x, y, path):
            return

        # Sinh neighbors
        neighbors = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and game.maze[nx][ny] == 0:
                new_cell = (nx, ny)
                neighbors.append((new_cell, path + [new_cell], heuristic(new_cell, goal)))

        if not neighbors:
            break

        # Tìm neighbor tốt nhất
        best_neighbor = min(neighbors, key=lambda n: n[2])

        if best_neighbor[2] < cost:
            # Nếu tốt hơn → nhận ngay
            current = best_neighbor
        else:
            # Ngược lại → random 1 neighbor
            random_neighbor = random.choice(neighbors)
            delta = random_neighbor[2] - cost
            if random.random() < math.exp(-delta / temperature):
                current = random_neighbor

        temperature *= cooling_rate

    # kết thúc
    game.is_running = False
    game.current_node = None
