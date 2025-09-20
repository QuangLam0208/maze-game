import pygame
import sys
import time
from ui.renderer import Renderer
from algorithms.bfs import run_bfs
from algorithms.dfs import run_dfs
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

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Pathfinding - 6 Groups Algorithm Selection")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20)
        self.title_font = pygame.font.SysFont('arial', 28)
        self.small_font = pygame.font.SysFont('arial', 16)
        
        # Add maze dimensions as instance attributes
        self.MAZE_SIZE = MAZE_SIZE
        self.MAZE_WIDTH = MAZE_WIDTH
        self.MAZE_HEIGHT = MAZE_HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.MAZE_OFFSET_X = MAZE_OFFSET_X
        self.MAZE_OFFSET_Y = MAZE_OFFSET_Y
        
        self.renderer = Renderer(self.screen, self)
        
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

        # --- Mapping thuật toán ---
        self.algorithms = {
            "Breadth-First Search (BFS)": run_bfs,
            "Depth-First Search (DFS)": run_dfs,
            # "Uniform Cost Search": run_ucs,
            # "A* Search": run_astar,
            # "Greedy Best-First": run_greedy,
            # "Dijkstra's Algorithm": run_dijkstra,
            # ... thêm các thuật toán khác
        }

    # --- Event Handling & Algorithms ---
    def _apply_state(self, state):
        """Áp dụng trạng thái cho mê cung"""
        self.start = state.get('start', (0, 0))
        self.end = state.get('end', (MAZE_SIZE-1, MAZE_SIZE-1))
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}

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

    def get_current_algorithm_name(self):
        """Lấy tên thuật toán đang chọn"""
        group = self.renderer.algorithm_groups[self.selected_group]
        alg = group["algorithms"][self.selected_algorithm]
        return alg["name"]

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

        alg_name = self.get_current_algorithm_name()
        if alg_name in self.algorithms:
            self.algorithms[alg_name](self)
        else:
            print(f"⚠ Thuật toán {alg_name} chưa được cài đặt!")
            self.is_running = False

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
