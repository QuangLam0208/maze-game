import pygame
import time

def run_dls(game):
    """Chạy Depth-Limited Search"""

    limit = game.MAZE_SIZE * game.MAZE_SIZE
    path = Recursive_DLS(game, 0, 0, [], limit)
    if path is not None:
        game.path = path
        game.stats["path_length"] = len(path)
    game.is_running = False
    game.current_node = None


def Recursive_DLS(game, x, y, current_path, limit):
    """
    Đệ quy DLS:
    - x, y: node hiện tại
    - current_path: ds các ô đã đi
    - limit: số bước còn lại
    """

    # Vẽ frame + highlight
    game.current_node = (x, y)
    game.visited.add((x, y))
    game.stats["nodes_visited"] += 1
    game.stats["time"] = (time.time() - game.start_time) * 1000
    game.draw_frame()

    # Xử lý sự kiện stop game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.is_running = False
            return None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                stop_rect = pygame.Rect(20 + 90, 720, 80, 35)
                if stop_rect.collidepoint(event.pos):
                    game.is_running = False
                    return None

    pygame.time.wait(80)  # animation

    # Nếu tới Goal
    if x == len(game.maze) - 1 and y == len(game.maze[0]) - 1:
        return current_path + [(x, y)]

    # Hết giới hạn độ sâu
    if limit == 0:
        return None

    # Duyệt 4 hướng
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and #không ra ngoài biên của mê cung.
            game.maze[nx][ny] == 0 and (nx, ny) not in game.visited): #ô trống và chưa đi qua trước đó

            result = Recursive_DLS(game, nx, ny, current_path + [(x, y)], limit - 1) #Gọi đệ quy thử đi tiếp từ ô (nx, ny)
            if result is not None:
                return result

    # Nếu không tìm thấy
    return None
