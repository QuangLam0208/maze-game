import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
CYAN = (0, 200, 200)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

# Constants
MAZE_SIZE = 25
CELL_SIZE = 20
MAZE_WIDTH = MAZE_SIZE * CELL_SIZE
MAZE_HEIGHT = MAZE_SIZE * CELL_SIZE
MAZE_OFFSET_X = 400
MAZE_OFFSET_Y = 100

class Renderer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 16)

    def draw_stats(self):
        """Vẽ thống kê"""
        stats_x = 20
        stats_y = 250
        
        # Background
        stats_rect = pygame.Rect(stats_x, stats_y, 250, 120)
        pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect)
        pygame.draw.rect(self.screen, BLACK, stats_rect, 2)
        
        # Title
        title = self.font.render("📊 Thống kê", True, BLACK)
        self.screen.blit(title, (stats_x + 10, stats_y + 10))
        
        # Stats info
        stats_info = [
            f"Nodes đã thăm: {self.game.stats['nodes_visited']}",
            f"Độ dài đường đi: {self.game.stats['path_length']}",
            f"Thời gian: {self.game.stats['time']:.0f}ms",
            f"Trạng thái: {'Đang chạy' if self.game.is_running else 'Dừng'}"
        ]
        
        for i, info in enumerate(stats_info):
            text = self.small_font.render(info, True, BLACK)
            self.screen.blit(text, (stats_x + 10, stats_y + 35 + i * 18))

    def draw_current_algorithm_info(self):
        """Hiển thị thông tin thuật toán hiện tại"""
        info_x = MAZE_OFFSET_X
        info_y = MAZE_OFFSET_Y - 40
        
        current_group = self.game.algorithm_groups[self.game.selected_group]
        current_alg = current_group["algorithms"][self.game.selected_algorithm]
        
        info_text = f"Đang sử dụng: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
        text = self.font.render(info_text, True, current_group["color"])
        self.screen.blit(text, (info_x, info_y))

    def draw_maze(self):
        """Vẽ maze"""
        # Background maze
        maze_bg = pygame.Rect(MAZE_OFFSET_X - 5, MAZE_OFFSET_Y - 5, MAZE_WIDTH + 10, MAZE_HEIGHT + 10)
        pygame.draw.rect(self.screen, BLACK, maze_bg)
        
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                x = MAZE_OFFSET_X + j * CELL_SIZE
                y = MAZE_OFFSET_Y + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Determine cell color
                if self.game.maze[i][j] == 1:  # Wall
                    color = BLACK
                elif i == 0 and j == 0:  # Start
                    color = GREEN
                elif i == MAZE_SIZE - 1 and j == MAZE_SIZE - 1:  # Goal
                    color = RED
                elif self.game.current_node and self.game.current_node == (i, j):  # Current node
                    color = PINK
                elif (i, j) in self.game.path:  # Path
                    color = YELLOW
                elif (i, j) in self.game.visited:  # Visited
                    color = LIGHT_BLUE
                else:  # Empty
                    color = WHITE
                
                pygame.draw.rect(self.screen, color, rect)
                if color != BLACK:  # Don't draw border on walls
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)

    def draw_legend(self):
        """Vẽ chú thích"""
        legend_x = MAZE_OFFSET_X + MAZE_WIDTH + 20
        legend_y = MAZE_OFFSET_Y
        
        legend_rect = pygame.Rect(legend_x, legend_y, 180, 200)
        pygame.draw.rect(self.screen, WHITE, legend_rect)
        pygame.draw.rect(self.screen, BLACK, legend_rect, 2)
        
        title = self.font.render("🔍 Chú thích", True, BLACK)
        self.screen.blit(title, (legend_x + 10, legend_y + 10))
        
        legend_items = [
            ("Start", GREEN),
            ("Goal", RED),
            ("Tường", BLACK),
            ("Đã thăm", LIGHT_BLUE),
            ("Đường đi", YELLOW),
            ("Hiện tại", PINK),
            ("Trống", WHITE)
        ]
        
        for i, (label, color) in enumerate(legend_items):
            y = legend_y + 40 + i * 22
            
            # Color box
            color_rect = pygame.Rect(legend_x + 15, y, 15, 15)
            pygame.draw.rect(self.screen, color, color_rect)
            pygame.draw.rect(self.screen, BLACK, color_rect, 1)
            
            # Label
            label_text = self.small_font.render(label, True, BLACK)
            self.screen.blit(label_text, (legend_x + 40, y + 2))

    def draw_all(self):
        """Vẽ tất cả các thành phần UI"""
        self.draw_stats()
        self.draw_current_algorithm_info()
        self.draw_maze()
        self.draw_legend()