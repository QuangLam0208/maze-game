import pygame
import sys
import time
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
from algorithms.Unobservable import run_unobservable_dfs
from algorithms.and_or_search import run_and_or_search
from algorithms.partial_observable import run_partial_observable_dfs, run_partial_observable_bfs
from algorithms.forward_checking import run_forward_checking
from algorithms.AC3 import run_ac3_csp

from PIL import Image, ImageDraw, ImageFont

from core.maze_generator import generate_maze, generate_beautiful_maze

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
MAZE_SIZE = 25
CELL_SIZE = 25
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
        self.custom_start = (0, 0)  # Default start position
        self.custom_end = (MAZE_SIZE-1, MAZE_SIZE-1)  # Default end position
        self.node_placement_mode = None  # None, "start", "end", "wall"

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
            "Beam Search": run_beam,
            "Unobservable Search": run_unobservable_dfs,
            "Nondeterministic": run_and_or_search,
            "Partial Observable": run_partial_observable_dfs,
            "Forward Checking": run_forward_checking,
            "Arc Consistency Algorithm 3": run_ac3_csp,
            # ... thêm các thuật toán khác
        }

    # --- Event Handling & Algorithms ---
    def default_start_end_node(self):
        """Đặt lại start và end node về vị trí mặc định"""
        # Xóa nodes hiện tại nếu có
        self.custom_start = (0, 0)  # Default start position
        self.custom_end = (MAZE_SIZE-1, MAZE_SIZE-1)  # Default end position
        self.node_placement_mode = None  # Tắt mode đặt node
    
    def _apply_state(self, state):
        """Áp dụng trạng thái cho mê cung"""
        self.start = state.get('start', (0, 0))
        self.end = state.get('end', (MAZE_SIZE-1, MAZE_SIZE-1))
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}

        # Nếu trước đó đang dùng partial-observable, xóa known_maze / visible_cells
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")

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
        actions = ["start", "stop", "reset_path", "reset", "new_maze", "beautiful_maze", "set_nodes", "set_wall", "statistics", "quit"]

        for i, action in enumerate(actions):
            if self.renderer.get_control_button_rect(i).collidepoint(pos):
                if action == "start" and not self.is_running:
                    self.start_algorithm()
                elif action == "stop":
                    self.is_running = False
                elif action == "reset":
                    self.reset()
                    self.default_start_end_node()
                elif action == "reset_path":
                    self.reset_path()
                elif action == "new_maze":
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()
                elif action == "beautiful_maze" and not self.is_running:
                    self.maze, state = generate_beautiful_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()
                elif action == "set_nodes" and not self.is_running:
                    self.reset_path()
                    if self.node_placement_mode in ("start", "end"):
                        self.node_placement_mode = None
                    else:
                        self.custom_start = None
                        self.custom_end = None
                        self.node_placement_mode = "start"
                elif action == "set_wall" and not self.is_running:
                    self.reset_path()
                    if self.node_placement_mode == "wall":
                        self.node_placement_mode = None
                    else:
                        self.node_placement_mode = "wall"
                elif action == "statistics":
                    self.show_statistics()
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
                return
        
        # Check if clicking in maze area for node placement
        if (self.node_placement_mode and not self.is_running and 
            pos[0] >= MAZE_OFFSET_X and pos[0] < MAZE_OFFSET_X + MAZE_WIDTH and
            pos[1] >= MAZE_OFFSET_Y and pos[1] < MAZE_OFFSET_Y + MAZE_HEIGHT):
            
            # Convert pixel coordinates to maze grid coordinates
            col = (pos[0] - MAZE_OFFSET_X) // CELL_SIZE
            row = (pos[1] - MAZE_OFFSET_Y) // CELL_SIZE
            
            clicked_node = (row, col)

            if 0 <= row < MAZE_SIZE and 0 <= col < MAZE_SIZE:
                if self.node_placement_mode == "start":
                    if self.maze[row][col] == 0:
                        self.custom_start = clicked_node
                        self.node_placement_mode = "end"
                elif self.node_placement_mode == "end":
                    if self.maze[row][col] == 0 and clicked_node != self.custom_start:
                        self.custom_end = clicked_node
                        self.node_placement_mode = None
                elif self.node_placement_mode == "wall":
                    # Không cho phép thay đổi điểm start/end
                    if clicked_node != self.custom_start and clicked_node != self.custom_end:
                        # Chuyển đổi giữa tường và đường đi (1 và 0)
                        self.maze[row][col] = 1 - self.maze[row][col]
                return


    def get_current_algorithm_name(self):
        """Lấy tên thuật toán đang chọn"""
        group = self.renderer.algorithm_groups[self.selected_group]
        alg = group["algorithms"][self.selected_algorithm]
        return alg["name"]

    def start_algorithm(self):
        if self.is_running:
            return

        # Kiểm tra xem cả start và end nodes đã được đặt chưa
        if not hasattr(self, 'custom_start') or not hasattr(self, 'custom_end') or \
           self.custom_start is None or self.custom_end is None:
            print("⚠ Cần đặt đủ cả Start và End nodes trước khi chạy thuật toán!")
            return

        self.is_running = True
        self.visited = set()
        self.path = []
        self.current_node = (0, 0)
        self.start_time = time.time()
        self.stats["nodes_visited"] = 0

        alg_name = self.get_current_algorithm_name()
        self.alg_name = alg_name   # nhớ lưu tên thuật toán
        if alg_name in self.algorithms:
            self.algorithms[alg_name](self)

            # ⬇Sau khi thuật toán chạy xong mà không tìm thấy đích
            if not self.path:  
                self.is_running = False
                elapsed_time = (time.time() - self.start_time) * 1000
                self.stats["time"] = elapsed_time

                if not hasattr(self, "history"):
                    self.history = []

                self.history.insert(0, {
                    "name": self.alg_name,
                    "nodes": self.stats["nodes_visited"],
                    "length": 0,
                    "time": f"{elapsed_time:.0f}ms",
                    "status": "Not Found"
                })

                if len(self.history) > 5:
                    self.history.pop()
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
        
        self.clear_history()

        # remove partial-observable artifacts so renderer will draw full maze
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")
            
    def reset_path(self):
        """Chỉ reset path và visited, giữ nguyên maze"""
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        
    def clear_history(self):
        """Xóa toàn bộ dữ liệu đã lưu trong history"""
        self.history = []
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")
            
    def show_statistics(self):
        if not self.history:
            print("Chưa có dữ liệu để thống kê!")
            return

        # Giữ kết quả mới nhất cho từng thuật toán
        unique = {}
        for entry in reversed(self.history):
            unique[entry["name"]] = entry
        data = list(unique.values())

        # Sắp xếp theo tên để đồ thị ổn định
        data.sort(key=lambda x: x["name"])

        algos = [d["name"] for d in data]
        nodes = [d["nodes"] for d in data]
        
        # Xử lý time an toàn hơn
        times = []
        for d in data:
            time_str = str(d["time"]).replace("ms", "").strip()
            try:
                times.append(float(time_str))
            except ValueError:
                times.append(0)

        # Sử dụng backend Agg để không tạo cửa sổ tương tác
        
        fig = plt.figure(figsize=(12, 5))

        # Biểu đồ Nodes
        ax1 = plt.subplot(1, 2, 1)
        bars1 = ax1.bar(algos, nodes, color="skyblue", edgecolor='navy', alpha=0.7)
        ax1.set_title("Nodes đã thăm", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Số lượng nodes")
        ax1.grid(axis='y', alpha=0.3)
        ax1.tick_params(axis='x', rotation=0)
        
        # Thêm giá trị lên cột
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)

        # Biểu đồ Time
        ax2 = plt.subplot(1, 2, 2)
        bars2 = ax2.bar(algos, times, color="salmon", edgecolor='darkred', alpha=0.7)
        ax2.set_title("Thời gian thực thi", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Thời gian (ms)")
        ax2.grid(axis='y', alpha=0.3)
        ax2.tick_params(axis='x', rotation=0)
        
        # Thêm giá trị lên cột
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)

        plt.suptitle("Thống kê So sánh Thuật toán", 
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Tạo thư mục nếu chưa có
        stats_dir = "assets/pics/statics"
        os.makedirs(stats_dir, exist_ok=True)
        
        # Lưu ra file với timestamp để không ghi đè
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(stats_dir, f"statistics_{timestamp}.png")
        
        plt.savefig(stats_file, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Mở file bằng trình xem ảnh mặc định
        if os.name == 'nt':  # Windows
            os.startfile(stats_file)