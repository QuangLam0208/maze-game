import pygame
import sys
import time
from ui.renderer import Renderer
from algorithms.bfs import run_bfs
from algorithms.dfs import run_dfs
from algorithms.gbf import run_gbf
from algorithms.dls import run_dls
from algorithms.ucs import run_ucs
from algorithms.sa import run_simulated_annealing
from algorithms.astar import run_astar
from algorithms.beam import run_beam
from algorithms.hillclimbing import run_hill_climbing

from core.maze_generator import generate_maze, generate_beautiful_maze

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
MAZE_SIZE = 23
CELL_SIZE = 23
MAZE_WIDTH = MAZE_SIZE * CELL_SIZE
MAZE_HEIGHT = MAZE_SIZE * CELL_SIZE
MAZE_OFFSET_X = 400
MAZE_OFFSET_Y = 60

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
        
        self.history = [] #lưu lại các lần chạy
        self.alg_name = "" 
        
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
        
        # Custom Start/End nodes
        self.custom_start = (1, 1)  # Default start position  
        self.custom_end = (MAZE_SIZE-2, MAZE_SIZE-2)  # Default end position
        self.node_placement_mode = None  # None, "start", "end"

        self.maze, state = generate_maze(MAZE_SIZE)
        self._apply_state(state)

        # --- Mapping thuật toán ---
        self.algorithms = {
            "Breadth-First Search": run_bfs,
            "Depth-First Search": run_dfs,
            "Depth-Limited Search": run_dls,
            "Uniform Cost Search": run_ucs,
            "Greedy Best-First": run_gbf,
            "A* Search": run_astar,
            "Hill Climbing": run_hill_climbing,
            "Simulated Annealing": run_simulated_annealing,
            "Beam Search": run_beam
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
        # Check group buttons
        for i in range(len(self.renderer.algorithm_groups)):
            if self.renderer.get_group_button_rect(i).collidepoint(pos):
                self.selected_group = i
                self.selected_algorithm = 0
                return

        # Check algorithm buttons
        current_group = self.renderer.algorithm_groups[self.selected_group]
        for i, alg in enumerate(current_group["algorithms"]):
            if self.renderer.get_algorithm_button_rect(self.selected_group, i).collidepoint(pos):
                self.selected_algorithm = i
                return

        # Check control buttons
        actions = ["start", "stop", "reset_path", "reset", "new_maze", "beautiful_maze", "set_nodes"]

        for i, action in enumerate(actions):
            if self.renderer.get_control_button_rect(i).collidepoint(pos):
                if action == "start" and not self.is_running:
                    self.start_algorithm()
                elif action == "stop":
                    self.is_running = False
                elif action == "reset":
                    self.reset()
                elif action == "reset_path":
                    self.reset_path()
                elif action == "new_maze":
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self._apply_state(state)
                elif action == "beautiful_maze" and not self.is_running:
                    self.maze, state = generate_beautiful_maze(MAZE_SIZE)
                    self._apply_state(state)
                elif action == "set_nodes" and not self.is_running:
                    # Khi click nút, xóa các nodes hiện tại và bắt đầu đặt lại
                    if self.node_placement_mode is None:
                        # Xóa nodes hiện tại và bắt đầu mode đặt start
                        self.custom_start = None
                        self.custom_end = None
                        self.node_placement_mode = "start"
                    else:
                        # Nếu đang ở mode đặt node, thoát mode và giữ nodes đã đặt
                        self.node_placement_mode = None
                return
        
        # Check if clicking in maze area for node placement
        if (self.node_placement_mode and not self.is_running and 
            pos[0] >= MAZE_OFFSET_X and pos[0] < MAZE_OFFSET_X + MAZE_WIDTH and
            pos[1] >= MAZE_OFFSET_Y and pos[1] < MAZE_OFFSET_Y + MAZE_HEIGHT):
            
            # Convert pixel coordinates to maze grid coordinates
            col = (pos[0] - MAZE_OFFSET_X) // CELL_SIZE
            row = (pos[1] - MAZE_OFFSET_Y) // CELL_SIZE
            
            # Check if click is within maze bounds and on empty cell
            if (0 <= row < MAZE_SIZE and 0 <= col < MAZE_SIZE and 
                self.maze[row][col] == 0):  # Empty cell
                
                if self.node_placement_mode == "start":
                    self.custom_start = (row, col)
                    self.node_placement_mode = "end"  # Switch to placing end node
                elif self.node_placement_mode == "end":
                    self.custom_end = (row, col) 
                    self.node_placement_mode = None  # Done placing nodes
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
    def reset(self):
        """Reset toàn bộ maze về trắng"""
        self.maze = [[0 for _ in range(self.MAZE_SIZE)] for _ in range(self.MAZE_SIZE)]
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        

    def reset_path(self):
        """Chỉ reset path và visited, giữ nguyên maze"""
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
