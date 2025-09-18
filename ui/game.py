import pygame
import sys
import time
import random
from collections import deque
from ui.renderer import Renderer


from algorithms.bfs import run_bfs
from core.maze_generator import generate_maze

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
        
        self.renderer = Renderer(self.screen, self)


        # Algorithm groups: cái này add vào chung với hàm render 6 nhóm thuật toán ui/renderer.py
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

        self.maze, state = generate_maze(MAZE_SIZE)
        self._apply_state(state)

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
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self._apply_state(state)
                elif action == "new_maze":
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self._apply_state(state)
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
        
        # Draw all UI elements using renderer
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
