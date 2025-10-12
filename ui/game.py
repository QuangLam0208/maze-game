import pygame
import sys
import time
import os
from datetime import datetime
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
from algorithms.unobservable import run_unobservable_dfs
from algorithms.and_or_search import run_and_or_search
from algorithms.partial_observable import run_partial_observable_dfs
from algorithms.forward_checking import run_forward_checking
from algorithms.AC3 import run_ac3_csp
from algorithms.backtracking import run_backtracking
from algorithms.minimax import run_minimax

from core.maze_generator import generate_maze, generate_beautiful_maze

# Colors
WHITE = (255, 255, 255)

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = None
        background_path = "assets/pics/bg-maze-game.png"  # đường dẫn đến ảnh
        if os.path.exists(background_path):
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
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
            "Minimax (Player vs Monster)": run_minimax,
            "Arc Consistency 3": run_ac3_csp

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
                    self.reset_player_monster()  # Reset Player và Monster positions
                
                self.selected_group = i
                self.selected_algorithm = -1  # Không auto-chọn thuật toán nào
                return

        # Check algorithm buttons
        current_group = self.renderer.algorithm_groups[self.selected_group]
        for i, alg in enumerate(current_group["algorithms"]):
            if self.renderer.get_algorithm_button_rect(self.selected_group, i).collidepoint(pos):
                # Reset Player và Monster khi chọn thuật toán khác
                if self.selected_algorithm != i:
                    self.reset_player_monster()
                    
                self.selected_algorithm = i
                # Nếu đã chạy tất cả thuật toán trong nhóm, highlight kết quả thuật toán này
                if self.group_results:
                    self.selected_result_algorithm = alg["name"]
                    self.highlight_algorithm_result(alg["name"])
                return

        # Check control buttons
        actions = ["start", "stop", "reset_path", "reset", "new_maze", "beautiful_maze", "set_nodes", "set_wall","statistics", "group_statistics"]

        for i, action in enumerate(actions):
            if self.renderer.get_control_button_rect(i).collidepoint(pos):
                # --- Ưu tiên xử lý STOP trước ---
                if action == "stop":
                    if self.is_running:
                        self.is_running = False
                    self.renderer.button_states["stop"] = "flash"
                    pygame.time.set_timer(pygame.USEREVENT + 1, 200, loops=1)
                    return

                # --- Nếu đang chạy thì chỉ cho STOP, các nút khác bị vô hiệu ---
                if self.is_running:
                    return

                # --- Logic nhấn nút ---
                if action == "start" and not self.is_running:
                    # Nếu đang bật wall thì tắt
                    if self.node_placement_mode == "wall":
                        self.node_placement_mode = None
                        self.renderer.button_states["set_wall"] = "normal"

                    # Đổi màu nút sang active (tím-xanh)
                    self.renderer.button_states["start"] = "active"

                    # Vẽ lại ngay để hiển thị thay đổi
                    self.draw_frame()
                    pygame.display.flip()
                    pygame.time.wait(100)  # cho 0.1 giây để update UI

                    # Gọi thuật toán (tự set is_running bên trong)
                    self.start_algorithm()

                    # Khi chạy xong → trở lại đỏ-vàng
                    self.renderer.button_states["start"] = "normal"

                elif action == "reset":
                    self.reset()
                    self.default_start_end_node()
                    self.renderer.button_states["reset"] = "flash"

                elif action == "reset_path":
                    self.reset_path()
                    self.renderer.button_states["reset_path"] = "flash"

                elif action == "new_maze":
                    self.maze, state = generate_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()
                    self.reset_path()  # Reset path khi tạo maze mới
                    self.reset_player_monster()  # Reset Player và Monster positions
                    self.renderer.button_states["new_maze"] = "flash"
                elif action == "beautiful_maze" and not self.is_running:
                    self.maze, state = generate_beautiful_maze(MAZE_SIZE)
                    self.clear_history()
                    self._apply_state(state)
                    self.default_start_end_node()
                    self.reset_path()  # Reset path khi tạo beautiful maze
                    self.reset_player_monster()  # Reset Player và Monster positions
                    self.renderer.button_states["beautiful_maze"] = "flash"
                elif action == "set_nodes" and not self.is_running:
                    self.reset_path()
                    # bật/tắt chế độ đặt node
                    if self.node_placement_mode in ("start", "end"):
                        self.node_placement_mode = None
                        self.renderer.button_states["set_nodes"] = "normal"
                    else:
                        self.custom_start = None
                        self.custom_end = None
                        self.node_placement_mode = "start"
                        self.renderer.button_states["set_nodes"] = "active"

                elif action == "set_wall":
                    self.reset_path()
                    if self.node_placement_mode == "wall":
                        self.node_placement_mode = None
                        self.renderer.button_states["set_wall"] = "normal"
                    else:
                        self.node_placement_mode = "wall"
                        self.renderer.button_states["set_wall"] = "active"

                elif action == "statistics":
                    self.show_statistics()
                    self.renderer.button_states["statistics"] = "flash"

                elif action == "group_statistics": # Xử lý nút mới
                    self.show_group_statistics()
                    self.renderer.button_states["group_statistics"] = "flash"

                # --- Hiệu ứng flash tạm thời ---
                if self.renderer.button_states[action] == "flash":
                    pygame.time.set_timer(pygame.USEREVENT + 1, 200, loops=1)

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
                        self.renderer.button_states["set_nodes"] = "normal"
                elif self.node_placement_mode == "wall":
                    # Không cho phép thay đổi điểm start/end
                    if clicked_node != self.custom_start and clicked_node != self.custom_end:
                        # Chuyển đổi giữa tường và đường đi (1 và 0)
                        self.maze[row][col] = 1 - self.maze[row][col]
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
            print("Cần đặt đủ cả Start và End nodes trước khi chạy thuật toán!")
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

    def run_all_algorithms_in_group(self):
        """Chạy tất cả thuật toán trong nhóm được chọn"""
        print("Đang chạy tất cả thuật toán trong nhóm...")
        
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
            print(f"Đang chạy: {alg_name}")
            
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
                print(f"Thuật toán {alg_name} chưa được implement")
                
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
        
        print("Đã chạy xong tất cả thuật toán trong nhóm!")
        print("Nhấn vào thuật toán con để xem kết quả của nó")

    def highlight_algorithm_result(self, algorithm_name):
        """Highlight kết quả của một thuật toán cụ thể"""
        if algorithm_name in self.group_results:
            result = self.group_results[algorithm_name]
            self.path = result['path']
            self.visited = result['visited']
            self.stats = result['stats']
            print(f"Đang hiển thị kết quả của {algorithm_name}: {len(self.path)} nodes trong path")

    def draw_frame(self):
        """Vẽ một frame hoàn chỉnh"""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
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
                elif event.type == pygame.USEREVENT + 1:
                    # Reset các nút flash về normal
                    for k, v in self.renderer.button_states.items():
                        if v == "flash":
                            self.renderer.button_states[k] = "normal"

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
        
        # Reset Player và Monster positions
        self.reset_player_monster()
        
        self.clear_history()

        # remove partial-observable artifacts so renderer will draw full maze
        if hasattr(self, "known_maze"):
            delattr(self, "known_maze")
        if hasattr(self, "visible_cells"):
            delattr(self, "visible_cells")
            
    def reset_player_monster(self):
        """Reset vị trí Player và Monster khi đổi maze hoặc thuật toán"""
        if hasattr(self, 'player_pos'):
            delattr(self, 'player_pos')
        if hasattr(self, 'monster_pos'):
            delattr(self, 'monster_pos')
            
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
        
        # Reset Player và Monster positions
        self.reset_player_monster()
        
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
        
        # BỔ SUNG: Rút gọn tên thuật toán cho hiển thị trên trục X
        short_algos = []
        for name in algos:
            if 'Breadth-First' in name: short_algos.append('BFS')
            elif 'Depth-First' in name: short_algos.append('DFS')
            elif 'Depth-Limited' in name: short_algos.append('DLS')
            elif 'Uniform Cost' in name: short_algos.append('UCS')
            elif 'A*' in name: short_algos.append('A*')
            elif 'Greedy Best' in name: short_algos.append('GBFS')
            elif 'Simulated Annealing' in name: short_algos.append('SA')
            elif 'Hill Climbing' in name: short_algos.append('HC')
            elif 'Arc Consistency' in name: short_algos.append('AC3')
            elif 'Forward Checking' in name: short_algos.append('FC')
            elif 'Nondeterministic' in name: short_algos.append('AND-OR')
            elif 'Unobservable Search' in name: short_algos.append('Unobs')
            elif 'Partial Observable' in name: short_algos.append('P-Obs')
            elif 'Backtracking' in name: short_algos.append('BT')
            elif len(name) > 10: short_algos.append(name.replace(' ', '\n')) # Xuống dòng nếu quá dài
            else: short_algos.append(name)

        nodes = [d["nodes"] for d in data]
        
        # Xử lý time an toàn hơn
        times = []
        for d in data:
            time_str = str(d["time"]).replace("ms", "").strip()
            try:
                times.append(float(time_str))
            except ValueError:
                times.append(0)
        
        fig = plt.figure(figsize=(12, 5))

        # Biểu đồ Nodes
        ax1 = plt.subplot(1, 2, 1)
        bars1 = ax1.bar(short_algos, nodes, color="skyblue", edgecolor='navy', alpha=0.7)
        ax1.set_title("Nodes đã thăm", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Số lượng nodes")
        ax1.grid(axis='y', alpha=0.3)
        ax1.tick_params(axis='x', rotation=0) # Giữ nhãn nằm ngang
        
        # Thêm giá trị lên cột
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}',
                     ha='center', va='bottom', fontsize=9)

        # Biểu đồ Time
        ax2 = plt.subplot(1, 2, 2)
        bars2 = ax2.bar(short_algos, times, color="salmon", edgecolor='darkred', alpha=0.7)
        ax2.set_title("Thời gian thực thi", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Thời gian (ms)")
        ax2.grid(axis='y', alpha=0.3)
        ax2.tick_params(axis='x', rotation=0) # Giữ nhãn nằm ngang
        
        # Thêm giá trị lên cột
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1f}',
                     ha='center', va='bottom', fontsize=9)

        plt.suptitle("Thống kê So sánh Thuật toán", 
                     fontsize=14, fontweight='bold')
        
        # Bổ sung: Điều chỉnh lề dưới để nhãn không bị chồng lấn/cắt
        plt.subplots_adjust(bottom=0.25)
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

    def get_alg_group_name(self, alg_name):
        """Tìm tên nhóm của thuật toán, bao gồm cả trường hợp tên bị viết tắt/lưu không chính xác."""
        name_map = {
            "GBF": "Greedy Best-First", 
            "AC-3": "Arc Consistency Algorithm 3", 
            "Unobservable": "Unobservable Search",
            "AND-OR Search": "Nondeterministic",
            "SA": "Simulated Annealing",                   
            "Beam": "Beam Search",                         
        }
        alg_name_to_check = name_map.get(alg_name, alg_name)

        for group in self.renderer.algorithm_groups:
            for alg in group["algorithms"]:
                if alg["name"] == alg_name_to_check:
                    return group["name"]
        
        return "Khác" 
    
    def show_group_statistics(self):
        if not self.history:
            print("Chưa có dữ liệu lịch sử để thống kê theo nhóm!")
            return

        # 1. Gom các kết quả lịch sử theo nhóm và tìm kết quả tốt nhất (Nodes visited ít nhất)
        best_in_group = {}
        
        # Chỉ xem xét các thuật toán tìm được path (length != 0)
        valid_history = [d for d in self.history if d.get("length", 0) != 0]

        if not valid_history:
            print("Không có thuật toán nào tìm được đích để thống kê theo nhóm!")
            return

        for entry in valid_history:
            alg_name = entry["name"]
            group_name = self.get_alg_group_name(alg_name)
            
            if group_name not in best_in_group or entry["nodes"] < best_in_group[group_name]["nodes"]:
                best_in_group[group_name] = entry
        
        # 2. Chuẩn bị dữ liệu cho đồ thị
        data = list(best_in_group.values())
        
        # Loại bỏ nhóm "Coming Soon" và sắp xếp theo tên nhóm
        data = [d for d in data if self.get_alg_group_name(d['name']) != "Coming Soon"]
        data.sort(key=lambda x: self.get_alg_group_name(x['name']))

        # Rút gọn tên nhóm cho hiển thị trên trục X
        group_names_long = [self.get_alg_group_name(d["name"]) for d in data]
        short_group_names = []
        for name in group_names_long:
            if name == "Uninformed Search": short_group_names.append("Uninf. Search")
            elif name == "Informed Search": short_group_names.append("Inf. Search")
            elif name == "Local Search": short_group_names.append("Local Search")
            elif name == "Complex Environment": short_group_names.append("Complex Env.")
            elif name == "Constraint Satisfied": short_group_names.append("CSP")
            else: short_group_names.append(name)
            
        nodes = [d["nodes"] for d in data]
        
        # Xử lý time an toàn hơn
        times = []
        for d in data:
            time_str = str(d["time"]).replace("ms", "").strip()
            try:
                times.append(float(time_str))
            except ValueError:
                times.append(0)

        # 3. Vẽ đồ thị (giống show_statistics nhưng đổi tiêu đề và label)
        fig = plt.figure(figsize=(12, 5))

        # Biểu đồ Nodes
        ax1 = plt.subplot(1, 2, 1)
        bars1 = ax1.bar(short_group_names, nodes, color="skyblue", edgecolor='navy', alpha=0.7)
        ax1.set_title("Nodes đã thăm (Thuật toán tốt nhất mỗi nhóm)", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Số lượng nodes")
        ax1.set_xlabel("Nhóm Thuật toán")
        ax1.grid(axis='y', alpha=0.3)
        ax1.tick_params(axis='x', rotation=0) # Giữ nhãn nằm ngang
        
        # Thêm giá trị lên cột (Tên thuật toán + Giá trị)
        for bar, d in zip(bars1, data):
            height = bar.get_height()
            # Lấy tên rút gọn của thuật toán cho hiển thị trên bar
            display_name = d["name"].split(' ')[0] # Thường là tên viết tắt/ngắn gọn đầu tiên
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{display_name}\n{int(height)}',
                     ha='center', va='bottom', fontsize=8)


        # Biểu đồ Time
        ax2 = plt.subplot(1, 2, 2)
        bars2 = ax2.bar(short_group_names, times, color="salmon", edgecolor='darkred', alpha=0.7)
        ax2.set_title("Thời gian thực thi (Thuật toán tốt nhất mỗi nhóm)", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Thời gian (ms)")
        ax2.set_xlabel("Nhóm Thuật toán")
        ax2.grid(axis='y', alpha=0.3)
        ax2.tick_params(axis='x', rotation=0) # Giữ nhãn nằm ngang
        
        # Thêm giá trị lên cột (Tên thuật toán + Giá trị)
        for bar, d in zip(bars2, data):
            height = bar.get_height()
            display_name = d["name"].split(' ')[0]
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                     f'{display_name}\n{height:.1f}',
                     ha='center', va='bottom', fontsize=8)


        plt.suptitle("Thống kê So sánh Thuật toán Tốt nhất theo Nhóm", 
                     fontsize=14, fontweight='bold')
        
        # Bổ sung: Điều chỉnh lề dưới để nhãn không bị chồng lấn/cắt
        plt.subplots_adjust(bottom=0.25) 
        plt.tight_layout()
        
        # Lưu ra file
        stats_dir = "assets/pics/statics"
        os.makedirs(stats_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(stats_dir, f"group_statistics_{timestamp}.png")
        
        plt.savefig(stats_file, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Mở file bằng trình xem ảnh mặc định
        if os.name == 'nt':  # Windows
            os.startfile(stats_file)