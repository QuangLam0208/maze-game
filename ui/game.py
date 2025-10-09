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
from ui.renderer import MAZE_SIZE, CELL_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y, MAZE_HEIGHT, MAZE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
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
from algorithms.partial_observable import run_partial_observable_dfs
from algorithms.forward_checking import run_forward_checking
from algorithms.AC3 import run_ac3_csp
from algorithms.backtracking import run_backtracking

from core.maze_generator import generate_maze, generate_beautiful_maze

# Colors
WHITE = (255, 255, 255)

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Pathfinding")
        self.clock = pygame.time.Clock()
        
        self.history = [] #lưu lại các lần chạy
        self.alg_name = "" 
        
        # Add maze dimensions as instance attributes
        self.MAZE_SIZE = MAZE_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.MAZE_OFFSET_X = MAZE_OFFSET_X
        self.MAZE_OFFSET_Y = MAZE_OFFSET_Y
        
        self.renderer = Renderer(self.screen, self)
        
        # Game state
        self.selected_group = 0
        self.selected_algorithm = -1  # Không chọn thuật toán nào ban đầu
        self.maze = []
        self.visited = set()
        self.path = []
        self.current_node = None
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self.start_time = 0
        self.backtracked_nodes = set()  # Lưu các node đã backtrack
        
        # Lưu kết quả chạy tất cả thuật toán trong nhóm
        self.group_results = {}  # {algorithm_name: {path: [...], stats: {...}}}
        self.selected_result_algorithm = None  # Thuật toán được chọn để highlight
        
        # Custom Start/End nodes
        self.custom_start = (0, 0)  # Default start position
        self.custom_end = (MAZE_SIZE-1, MAZE_SIZE-1)  # Default end position
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
            "Beam Search": run_beam,
            "Unobservable Search": run_unobservable_dfs,
            "Nondeterministic": run_and_or_search,
            "Partial Observable": run_partial_observable_dfs,
            "Backtracking": run_backtracking,
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
        self.backtracked_nodes = set()

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
                # If switching to a different group, reset path and group results
                if self.selected_group != i:
                    self.reset_path()  # Reset current path display
                    self.group_results = {}  # Clear previous group results
                    self.selected_result_algorithm = None  # Clear result selection
                
                self.selected_group = i
                self.selected_algorithm = -1  # Không auto-chọn thuật toán nào
                return

        # Check algorithm buttons
        current_group = self.renderer.algorithm_groups[self.selected_group]
        for i, alg in enumerate(current_group["algorithms"]):
            if self.renderer.get_algorithm_button_rect(self.selected_group, i).collidepoint(pos):
                self.selected_algorithm = i
                # Nếu đã chạy tất cả thuật toán trong nhóm, highlight kết quả thuật toán này
                if self.group_results:
                    self.selected_result_algorithm = alg["name"]
                    self.highlight_algorithm_result(alg["name"])
                return

        # Check control buttons
        actions = ["start", "stop", "reset_path", "reset", "new_maze", "beautiful_maze", "set_nodes", "set_wall", "statistics", "quit"]

        for i, action in enumerate(actions):
            if self.renderer.get_control_button_rect(i).collidepoint(pos):
                #  Nếu đang chạy, chỉ cho phép nút DỪNG 
                if self.is_running:
                    if action == "stop":
                        self.is_running = False
                    # Các nút khác bị vô hiệu
                    return
                if action == "start" and not self.is_running:
                    if self.node_placement_mode == "wall":
                        self.node_placement_mode = None
                    self.start_algorithm()
                elif action == "stop":
                    self.is_running = False
                elif action == "reset":
                    self.reset()
                    self.default_start_end_node()  # Đặt lại start/end nodes về default
                elif action == "reset_path":
                    self.reset_path()
                elif action == "new_maze":
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()  # Đặt lại start/end nodes về default
                elif action == "beautiful_maze" and not self.is_running:
                    self.maze, state = generate_beautiful_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()  # Đặt lại start/end nodes về default
                elif action == "set_nodes" and not self.is_running:
                    # Reset path khi bắt đầu đặt nodes
                    self.reset_path()
                    # Khi click nút, xóa các nodes hiện tại và bắt đầu đặt lại
                    if self.node_placement_mode is None:
                        # Xóa nodes hiện tại và bắt đầu mode đặt start
                        self.custom_start = None
                        self.custom_end = None
                        self.node_placement_mode = "start"
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
        if self.selected_algorithm == -1:
            return None
        group = self.renderer.algorithm_groups[self.selected_group]
        alg = group["algorithms"][self.selected_algorithm]
        return alg["name"]

    def start_algorithm(self):
        if self.is_running:
            return
        
        # --- Dọn dẹp trạng thái partial observable còn sót ---
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")

        # Kiểm tra xem cả start và end nodes đã được đặt chưa
        if not hasattr(self, 'custom_start') or not hasattr(self, 'custom_end') or \
           self.custom_start is None or self.custom_end is None:
            print("⚠ Cần đặt đủ cả Start và End nodes trước khi chạy thuật toán!")
            return

        # Nếu chưa chọn thuật toán con, chạy tất cả thuật toán trong nhóm
        if self.selected_algorithm == -1:
            self.run_all_algorithms_in_group()
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
            # Algorithm completion (success/failure) is now handled by algorithm_runner.py
        else:
            print(f"⚠ Thuật toán {alg_name} chưa được cài đặt!")
            self.is_running = False

    def run_all_algorithms_in_group(self):
        """Chạy tất cả thuật toán trong nhóm được chọn"""
        print("🔄 Đang chạy tất cả thuật toán trong nhóm...")
        
        # Reset kết quả cũ
        self.group_results = {}
        self.selected_result_algorithm = None
        
        # Prepare history for group execution
        if not hasattr(self, "history"):
            self.history = []
        
        current_group = self.renderer.algorithm_groups[self.selected_group]
        total_algorithms = len(current_group["algorithms"])
        completed = 0
        
        for i, alg_info in enumerate(current_group["algorithms"]):
            alg_name = alg_info["name"]
            print(f"📊 Đang chạy: {alg_name}")
            
            # Reset trạng thái cho mỗi thuật toán
            self.visited = set()
            self.path = []
            self.current_node = None
            self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
            self.start_time = time.time()
            self.alg_name = alg_name
            
            # Chạy thuật toán nếu có
            if alg_name in self.algorithms:
                # Tạm thời set is_running = True để thuật toán chạy
                self.is_running = True
                
                try:
                    self.algorithms[alg_name](self)
                    
                    # Lưu kết quả
                    elapsed_time = (time.time() - self.start_time) * 1000
                    found_goal = len(self.path) > 0
                    
                    self.group_results[alg_name] = {
                        'path': list(self.path),  # Copy path
                        'visited': set(self.visited),  # Copy visited
                        'stats': {
                            'nodes_visited': self.stats["nodes_visited"],
                            'path_length': len(self.path),
                            'time': elapsed_time,
                            'found_goal': found_goal
                        }
                    }
                    
                    # Note: History is already handled by algorithm_runner.py
                    
                except Exception as e:
                    print(f" Lỗi khi chạy {alg_name}: {e}")
                    self.group_results[alg_name] = {
                        'path': [],
                        'visited': set(),
                        'stats': {
                            'nodes_visited': 0,
                            'path_length': 0,
                            'time': 0,
                            'found_goal': False
                        }
                    }
                    
                    # Add to history only for errors not caught by algorithm_runner
                    if not hasattr(self, "history"):
                        self.history = []
                    
                    self.history.insert(0, {
                        "name": alg_name,
                        "nodes": 0,
                        "length": 0,
                        "time": "0ms",
                        "status": "fail"
                    })
            else:
                print(f"⚠ Thuật toán {alg_name} chưa được implement")
                
            completed += 1
            print(f" Hoàn thành {completed}/{total_algorithms}")
        
        # Kết thúc
        self.is_running = False
        self.current_node = None
        self.visited = set()
        self.path = []
        
        # Trim history to keep only last 10 entries
        if hasattr(self, "history") and len(self.history) > 10:
            self.history = self.history[:10]
        
        print("🎉 Đã chạy xong tất cả thuật toán trong nhóm!")
        print("💡 Nhấn vào thuật toán con để xem kết quả của nó")

    def highlight_algorithm_result(self, algorithm_name):
        """Highlight kết quả của một thuật toán cụ thể"""
        if algorithm_name in self.group_results:
            result = self.group_results[algorithm_name]
            self.path = result['path']
            self.visited = result['visited']
            self.stats = result['stats']
            print(f"🔍 Đang hiển thị kết quả của {algorithm_name}: {len(self.path)} nodes trong path")

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
        self.backtracked_nodes = set()
        
        # Clear group results
        self.group_results = {}
        self.selected_result_algorithm = None
        
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
        self.backtracked_nodes = set()
        
        # Clear group results
        self.group_results = {}
        self.selected_result_algorithm = None
        # Nếu trước đó đang dùng partial-observable, xóa known_maze / visible_cells
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")
        
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
        data = [d for d in data if d.get("length", 0) != 0]
        if not data:
            print("Không có thuật toán nào tìm được đích để thống kê!")
            return

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
