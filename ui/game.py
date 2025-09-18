import pygame
import sys
import time
import random
from collections import deque

from algorithms.bfs import run_bfs
from ui.renderer import Renderer

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
MAZE_SIZE = 25
CELL_SIZE = 20
MAZE_WIDTH = MAZE_SIZE * CELL_SIZE
MAZE_HEIGHT = MAZE_SIZE * CELL_SIZE
MAZE_OFFSET_X = 400
MAZE_OFFSET_Y = 100

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


class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Pathfinding - 6 Groups Algorithm Selection")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 16)
        
        # Initialize renderer
        self.renderer = Renderer(self.screen, self)

        # Algorithm groups
        self.algorithm_groups = [
            {
                "name": "Uninformed\nSearch",
                "color": BLUE,
                "algorithms": [
                    {"name": "Breadth-First Search (BFS)", "desc": "Tìm theo chiều rộng"},
                    {"name": "Depth-First Search (DFS)", "desc": "Tìm theo chiều sâu"},
                    {"name": "Uniform Cost Search", "desc": "Chi phí đồng đều"}
                ]
            },
            {
                "name": "Informed\nSearch",
                "color": GREEN,
                "algorithms": [
                    {"name": "A* Search", "desc": "Tối ưu với heuristic"},
                    {"name": "Greedy Best-First", "desc": "Tham lam heuristic"},
                    {"name": "Bidirectional Search", "desc": "Tìm hai chiều"}
                ]
            },
            {
                "name": "Dynamic\nProgramming",
                "color": PURPLE,
                "algorithms": [
                    {"name": "Dijkstra's Algorithm", "desc": "Đường ngắn nhất"},
                    {"name": "Floyd-Warshall", "desc": "Mọi cặp điểm"},
                    {"name": "Bellman-Ford", "desc": "Trọng số âm"}
                ]
            },
            {
                "name": "Heuristic\nMethods",
                "color": RED,
                "algorithms": [
                    {"name": "Hill Climbing", "desc": "Leo đồi tối ưu"},
                    {"name": "Simulated Annealing", "desc": "Mô phỏng ủ kim loại"},
                    {"name": "Beam Search", "desc": "Giới hạn node"}
                ]
            },
            {
                "name": "Evolutionary\nAlgorithms",
                "color": ORANGE,
                "algorithms": [
                    {"name": "Genetic Algorithm", "desc": "Tiến hóa tự nhiên"},
                    {"name": "Ant Colony Optimization", "desc": "Hành vi kiến"},
                    {"name": "Particle Swarm Optimization", "desc": "Đàn chim"}
                ]
            },
            {
                "name": "Machine\nLearning",
                "color": CYAN,
                "algorithms": [
                    {"name": "Q-Learning", "desc": "Học tăng cường"},
                    {"name": "Neural Network Path", "desc": "Mạng neural"},
                    {"name": "Random Forest Path", "desc": "Ensemble learning"}
                ]
            }
        ]

        # Game state
        self.selected_group = 0
        self.selected_algorithm = 0
        self.maze = []
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self.start_time = 0

        self.generate_maze()


    # Có thể tách ra file riêng ??? .core/maze_generator.py
    def generate_maze(self):
        """Tạo maze ngẫu nhiên"""
        self.maze = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

        # Tạo tường ngẫu nhiên
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                if random.random() < 0.3 and not (i == 0 and j == 0) and not (i == MAZE_SIZE-1 and j == MAZE_SIZE-1):
                    self.maze[i][j] = 1  # Tường

        self.reset_pathfinding()


    # Có thể tách ra file riêng ??? .core/path_finding.py
    def reset_pathfinding(self):
        """Reset trạng thái tìm đường"""
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}


    # render: 6 nhóm thuật toán -> đưa hàm này vào trong ui/renderer.py, rồi gọi ở đây
    def draw_group_buttons(self):
        """Vẽ 6 nhóm thuật toán ở góc trên trái (2x3)"""
        button_width = 120
        button_height = 50
        start_x = 20
        start_y = 20
        spacing = 10
        
        for i, group in enumerate(self.algorithm_groups):
            # Tính vị trí button (2 cột, 3 hàng)
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            
            # Vẽ button
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # Màu button
            if self.selected_group == i:
                pygame.draw.rect(self.screen, group["color"], button_rect)
                pygame.draw.rect(self.screen, BLACK, button_rect, 3)
                text_color = WHITE
            else:
                pygame.draw.rect(self.screen, LIGHT_GRAY, button_rect)
                pygame.draw.rect(self.screen, DARK_GRAY, button_rect, 2)
                text_color = BLACK
            
            # Vẽ text (có thể có 2 dòng)
            lines = group["name"].split('\n')
            for j, line in enumerate(lines):
                text = self.font.render(line, True, text_color)
                text_rect = text.get_rect()
                text_x = x + (button_width - text_rect.width) // 2
                text_y = y + (button_height - len(lines) * 20) // 2 + j * 20
                self.screen.blit(text, (text_x, text_y))
    
    # render: 3 thuật toán con mỗi nhóm -> đưa hàm này vào trong ui/renderer.py, rồi gọi ở đây
    def draw_algorithm_buttons(self):
        """Vẽ 3 thuật toán con ở góc dưới trái"""
        if self.selected_group < 0 or self.selected_group >= len(self.algorithm_groups):
            return
        
        button_width = 250
        button_height = 60
        start_x = 20
        start_y = 420  # Dưới các button nhóm
        spacing = 5
        
        current_group = self.algorithm_groups[self.selected_group]
        
        # Title cho nhóm được chọn
        title_text = self.font.render(f"Nhóm: {current_group['name'].replace(chr(10), ' ')}", True, current_group["color"])
        self.screen.blit(title_text, (start_x, start_y - 30))
        
        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect(start_x, y, button_width, button_height)
            
            # Màu button
            if self.selected_algorithm == i:
                pygame.draw.rect(self.screen, current_group["color"], button_rect)
                pygame.draw.rect(self.screen, BLACK, button_rect, 3)
                text_color = WHITE
                desc_color = WHITE
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect)
                pygame.draw.rect(self.screen, current_group["color"], button_rect, 2)
                text_color = current_group["color"]
                desc_color = DARK_GRAY
            
            # Vẽ tên thuật toán
            name_text = self.small_font.render(algorithm["name"], True, text_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            
            # Vẽ mô tả
            desc_text = self.small_font.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 25))
    
    #render: 3 thuật toán con mỗi nhóm -> đưa hàm này vào trong ui/renderer.py, rồi gọi ở đây
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
            if button["action"] == "start" and self.is_running:
                color = GRAY
            else:
                color = button["color"]
            
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            text = self.small_font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
    
    # render








    # --- Event Handling & Algorithms ---
    def handle_click(self, pos):
        """Xử lý click chuột"""
        # Check group buttons (2x3 grid)
        button_width = 120
        button_height = 50
        start_x = 20
        start_y = 20
        spacing = 10
        
        for i in range(6):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                self.selected_group = i
                self.selected_algorithm = 0  # Reset algorithm selection
                return
        
        # Check algorithm buttons
        button_width = 250
        button_height = 60
        start_x = 20
        start_y = 420
        spacing = 5
        
        for i in range(3):
            y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect(start_x, y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                self.selected_algorithm = i
                return
        
        # Check control buttons
        button_width = 80
        button_height = 35
        start_x = 20
        start_y = 720
        spacing = 10
        
        actions = ["start", "stop", "reset", "new_maze"]
        
        for i, action in enumerate(actions):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, start_y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                if action == "start" and not self.is_running:
                    self.start_algorithm()
                elif action == "stop":
                    self.is_running = False
                elif action == "reset":
                    self.reset_pathfinding()
                elif action == "new_maze":
                    self.generate_maze()
                return

    def start_algorithm(self):
        """Bắt đầu chạy thuật toán"""
        if self.is_running:
            return

        self.is_running = True
        self.visited = set()
        self.path = []
        self.current_node = (0, 0)
        self.start_time = time.time()
        self.stats["nodes_visited"] = 0

        # Demo: run BFS
        run_bfs(self)

    def draw_frame(self):
        """Vẽ một frame hoàn chỉnh"""
        self.screen.fill(WHITE)
        
        # Draw all UI elements
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.renderer.draw_all()
        
        pygame.display.flip()

    def run(self):
        """Vòng lặp chính"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            self.draw_frame()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
