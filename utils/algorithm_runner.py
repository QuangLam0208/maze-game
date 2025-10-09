import pygame, time

def update_game_state(game, x, y, visited_set):
    '''Cập nhật trạng thái'''
    visited_set.add((x, y))
    game.visited.add((x, y)) # cập nhật vào visited của game.py để draw_maze() (renderer.py) vẽ
    game.current_node = (x, y) # highlight node được xét
    # Update statistic
    game.stats["nodes_visited"] += 1
    game.stats["time"] = (time.time() - game.start_time) * 1000

def check_goal(game, x, y, path):
    '''Check Goal state & save path'''
    # Sử dụng custom_end nếu có và không phải None, ngược lại dùng goal mặc định
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal_x, goal_y = len(game.maze) - 1, len(game.maze[0]) - 1
    else:
        goal_x, goal_y = goal_pos
    
    if x == goal_x and y == goal_y:
        game.path = path + [(x, y)]
        game.stats["path_length"] = len(game.path)
        game.current_node = None
        game.is_running = False

        # Cập nhật thời gian
        elapsed_time = (time.time() - game.start_time) * 1000
        game.stats["time"] = elapsed_time

        # Lưu vào history
        if not hasattr(game, "history"):
            game.history = []

        game.history.insert(0, {
            "name": game.alg_name,
            "nodes": game.stats["nodes_visited"],
            "length": game.stats["path_length"],
            "time": f"{elapsed_time:.0f}ms",
            "status": "done"
        })

        if len(game.history) > 10:
            game.history.pop()

        return True
    return False

def algorithm_finished(game):
    '''Handle algorithm completion - add to history if not already added'''
    # This is called when algorithm finishes without finding path
    # Only add to history if not already added (to avoid duplicates)
    if not hasattr(game, "history"):
        game.history = []
    
    # Check if this algorithm was already added to history (success case)
    already_in_history = any(
        entry["name"] == game.alg_name 
        for entry in game.history[:3]  # Check recent entries
    )
    
    if not already_in_history:
        # Algorithm finished without finding path
        elapsed_time = (time.time() - game.start_time) * 1000
        game.stats["time"] = elapsed_time
        
        game.history.insert(0, {
            "name": game.alg_name,
            "nodes": game.stats["nodes_visited"],
            "length": 0,
            "time": f"{elapsed_time:.0f}ms",
            "status": "fail"
        })

        if len(game.history) > 10:
            game.history.pop()

def handle_frame(game, step_count, max_steps_per_frame=3, delay=80):
    if step_count >= max_steps_per_frame:
        step_count = 0
        pygame.time.wait(delay) 
        game.draw_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_running = False
                return step_count, False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Sử dụng handle_click() để xử lý click đúng cách
                game.handle_click(event.pos)
                # Kiểm tra xem game có bị dừng không
                if not game.is_running:
                    return step_count, False
        
    return step_count, True