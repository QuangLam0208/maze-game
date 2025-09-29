import pygame

# Colors (cần giữ đồng bộ với game)
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

# Maze constants để hiển thị info
MAZE_OFFSET_X = 400
MAZE_OFFSET_Y = 60

RIGHT_SIDE_PANEL_WIDTH = 180
LEGEND_HEIGHT = 210
STATS_HEIGHT = 150

class Renderer:
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        
        self.font = pygame.font.SysFont("segoeui", 20)   
        self.title_font = pygame.font.SysFont("segoeui", 28, bold=True)
        self.small_font = pygame.font.SysFont("segoeui", 16)

        # --- Kích thước nút ---
        self.GROUP_BUTTON_WIDTH = 250
        self.GROUP_BUTTON_HEIGHT = 40   # cha nhỏ hơn
        self.ALG_BUTTON_WIDTH = 250
        self.ALG_BUTTON_HEIGHT = 60     # con to hơn
        self.BUTTON_SPACING = 5
        self.BUTTON_RADIUS = 8          # độ bo góc 

        self.algorithm_groups = [
            {
                "name": "Uninformed Search",
                "color": BLUE,
                "algorithms": [
                    {"name": "Breadth-First Search", "desc": "Tìm theo chiều rộng"},
                    {"name": "Depth-First Search", "desc": "Tìm theo chiều sâu"},
                    {"name": "Depth-Limited Search", "desc": "Giới hạn độ sâu"},
                    {"name": "Uniform Cost Search", "desc": "Chi phí thấp nhất"}
                ]
            },
            {
                "name": "Informed Search",
                "color": GREEN,
                "algorithms": [
                    {"name": "A* Search", "desc": "Tối ưu với heuristic"},
                    {"name": "Greedy Best-First", "desc": "Tham lam heuristic"}
                ]
            },            
            {
                "name": "Local Search",
                "color": RED,
                "algorithms": [
                    {"name": "Hill Climbing", "desc": "Leo đồi tối ưu"},
                    {"name": "Simulated Annealing", "desc": "Mô phỏng ủ kim loại"},
                    {"name": "Beam Search", "desc": "Giới hạn node"}
                ]
            },
            {
                "name": "Complex Environment",
                "color": PURPLE,
                "algorithms": [
                    {"name": "Nondeterministic", "desc": "Hành động có nhiều kết quả"},
                    {"name": "Conformant", "desc": "Không quan sát, kế hoạch chắc chắn"},
                    {"name": "Contingency", "desc": "Kế hoạch rẽ nhánh theo quan sát"}
                ]
            },
            {
                "name": "Evolutionary Algorithms",
                "color": ORANGE,
                "algorithms": [
                    {"name": "Genetic Algorithm", "desc": "Tiến hóa tự nhiên"},
                    {"name": "Ant Colony Optimization", "desc": "Hành vi kiến"},
                    {"name": "Particle Swarm Optimization", "desc": "Đàn chim"}
                ]
            },
            {
                "name": "Machine Learning",
                "color": CYAN,
                "algorithms": [
                    {"name": "Q-Learning", "desc": "Học tăng cường"},
                    {"name": "Neural Network Path", "desc": "Mạng neural"},
                    {"name": "Random Forest Path", "desc": "Ensemble learning"}
                ]
            }
        ]

    # --- Nhóm thuật toán ---
    def draw_group_buttons(self):
        """Vẽ nhóm thuật toán thành 1 cột dọc (nút cha nhỏ hơn)"""
        start_x = 40
        start_y = MAZE_OFFSET_Y
        
        for i, group in enumerate(self.algorithm_groups):
            x = start_x
            y = start_y + i * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            button_rect = pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)
            
            # Màu button
            if self.game.selected_group == i:
                pygame.draw.rect(self.screen, group["color"], button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 3, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE
            else:
                pygame.draw.rect(self.screen, "#95a5a6", button_rect)
                pygame.draw.rect(self.screen, DARK_GRAY, button_rect, 2)
                text_color = BLACK
            
            # Vẽ tên nhóm (căn giữa theo chiều cao nhỏ hơn)
            text = self.font.render(group["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_group_button_rect(self, i):
        start_x = 40
        start_y = MAZE_OFFSET_Y
        y = start_y + i * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(start_x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

    # --- Thuật toán con ---
    def draw_algorithm_buttons(self):
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.algorithm_groups):
            return

        start_x = 40
        # đặt sau danh sách group
        start_y = (MAZE_OFFSET_Y 
                   + len(self.algorithm_groups) * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) 
                   + 40)
        spacing = self.BUTTON_SPACING
        
        current_group = self.algorithm_groups[self.game.selected_group]
        
        # Title cho nhóm được chọn
        title_text = self.font.render(
            f"Nhóm: {current_group['name']}", 
            True, current_group["color"]
        )
        self.screen.blit(title_text, (start_x, start_y - 30))
        
        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (self.ALG_BUTTON_HEIGHT + spacing)
            button_rect = pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)
            
            # Màu button
            if self.game.selected_algorithm == i:
                pygame.draw.rect(self.screen, current_group["color"], button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 3, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE
                desc_color = WHITE
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, current_group["color"], button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = current_group["color"]
                desc_color = DARK_GRAY
            
            # Vẽ tên thuật toán
            name_text = self.small_font.render(algorithm["name"], True, text_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            
            # Vẽ mô tả
            desc_text = self.small_font.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 30))

    def get_algorithm_button_rect(self, group_index, alg_index):
        start_x = 40
        start_y = (MAZE_OFFSET_Y 
                   + len(self.algorithm_groups) * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) 
                   + 40)
        y = start_y + alg_index * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

    # --- Info thuật toán hiện tại ---
    def draw_current_algorithm_info(self):
        """Hiển thị thông tin thuật toán hiện tại"""
        info_x = MAZE_OFFSET_X
        info_y = MAZE_OFFSET_Y - 45
        
        current_group = self.algorithm_groups[self.game.selected_group]
        current_alg = current_group["algorithms"][self.game.selected_algorithm]
        
        info_text = f"Đang sử dụng: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
        text = self.font.render(info_text, True, current_group["color"])
        self.screen.blit(text, (info_x, info_y))

    def draw_controls(self):
        """Vẽ các nút điều khiển"""
        button_width = 80
        button_height = 35
        start_x = 20
        start_y = 720
        spacing = 10
        
        buttons = [
            {"text": "Bắt đầu", "color": GREEN, "action": "start"},
            {"text": "Dừng", "color": RED, "action": "stop"},
            {"text": "Reset", "color": GRAY, "action": "reset"},
            {"text": "Maze mới", "color": BLUE, "action": "new_maze"}
        ]
        
        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, start_y, button_width, button_height)
            
            # Disable start button when running
            if button["action"] == "start" and self.game.is_running:
                color = GRAY
            else:
                color = button["color"]
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=self.BUTTON_RADIUS)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
            
            text = self.small_font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_control_button_rect(self, i):
        button_width = 80
        button_height = 35
        start_x = 20
        start_y = 720
        spacing = 10

        x = start_x + i * (button_width + spacing)
        return pygame.Rect(x, start_y, button_width, button_height)

    def draw_stats(self):
        """Vẽ thống kê"""
        stats_x = MAZE_OFFSET_X + self.game.MAZE_WIDTH + 20
        stats_y = MAZE_OFFSET_Y + LEGEND_HEIGHT + 20
        
        # Background
        stats_rect = pygame.Rect(stats_x, stats_y, RIGHT_SIDE_PANEL_WIDTH, STATS_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, stats_rect)
        pygame.draw.rect(self.screen, BLACK, stats_rect, 2)
        
        # Title
        title = self.font.render("Thống kê", True, BLACK)
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
            self.screen.blit(text, (stats_x + 10, stats_y + 40 + i * 22))

    def draw_legend(self):
        """Vẽ chú thích"""
        legend_x = MAZE_OFFSET_X + self.game.MAZE_WIDTH + 20
        legend_y = MAZE_OFFSET_Y
        
        legend_rect = pygame.Rect(legend_x, legend_y, RIGHT_SIDE_PANEL_WIDTH, LEGEND_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, legend_rect)
        pygame.draw.rect(self.screen, BLACK, legend_rect, 2)
        
        title = self.font.render("Chú thích", True, BLACK)
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
            y = legend_y + 40 + i * 23
            
            # Color box
            color_rect = pygame.Rect(legend_x + 15, y + 5, 15, 15)
            pygame.draw.rect(self.screen, color, color_rect)
            pygame.draw.rect(self.screen, BLACK, color_rect, 1)
            
            # Label
            label_text = self.small_font.render(label, True, BLACK)
            self.screen.blit(label_text, (legend_x + 40, y))

    def draw_maze(self):
        """Vẽ maze"""
        # Background maze
        maze_bg = pygame.Rect(MAZE_OFFSET_X - 3, MAZE_OFFSET_Y - 3, 
                            self.game.MAZE_WIDTH + 6, self.game.MAZE_HEIGHT + 6)
        pygame.draw.rect(self.screen, BLACK, maze_bg)
        
        for i in range(self.game.MAZE_SIZE):
            for j in range(self.game.MAZE_SIZE):
                x = MAZE_OFFSET_X + j * self.game.CELL_SIZE
                y = MAZE_OFFSET_Y + i * self.game.CELL_SIZE
                rect = pygame.Rect(x, y, self.game.CELL_SIZE, self.game.CELL_SIZE)
                
                # Determine cell color
                if self.game.maze[i][j] == 1:  # Wall
                    color = BLACK
                elif i == 0 and j == 0:  # Start
                    color = GREEN
                elif i == self.game.MAZE_SIZE - 1 and j == self.game.MAZE_SIZE - 1:  # Goal
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

    def draw_all(self):
        """Vẽ tất cả các thành phần giao diện"""
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats()
        self.draw_current_algorithm_info()
        self.draw_maze()
        self.draw_legend()