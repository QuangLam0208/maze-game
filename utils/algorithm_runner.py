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
    if x == len(game.maze) - 1 and y == len(game.maze[0]) - 1:
        game.path = path + [(x, y)]
        game.stats["path_length"] = len(game.path)
        game.current_node = None
        game.is_running = False
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
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        stop_rect = pygame.Rect(110, 720, 80, 35)
                        if stop_rect.collidepoint(event.pos):
                            game.is_running = False
                            return step_count, False     
        
    return step_count, True