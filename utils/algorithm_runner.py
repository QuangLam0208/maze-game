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
            "time": f"{elapsed_time:.0f}ms"
        })

        if len(game.history) > 5:
            game.history.pop()

        return True
    return False

def handle_frame(game, step_count, max_steps_per_frame=3, delay=80):
    if step_count >= max_steps_per_frame:
            # Khi duyệt hết 4 hướng (step 0 -> 3) thì tạm dừng để tạo animation: pygame.time.wait(..) 
            step_count = 0
            pygame.time.wait(delay) 
            # Draw frame of present state (ghi đè lên frame của previous state)
            game.draw_frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return step_count, False  # Sửa: thêm step_count
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        stop_rect = pygame.Rect(110, 720, 80, 35)
                        if stop_rect.collidepoint(event.pos):
                            game.is_running = False
                            return step_count, False     
        
    return step_count, True