import os
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
DARK_PURPLE = "#1b182b"

START_COLOR = "#69bdab"
GOAL_COLOR = "#b43f47"
WALL_COLOR = DARK_PURPLE
PATH_COLOR = "#f7d9b2"
UNKNOWN_COLOR = DARK_GRAY
VISITED_COLOR = "#cbbce9"
CURRENT_COLOR = "#e18488"
EMPTY_COLOR = WHITE
BACKTRACK_COLOR = GRAY

# --- WINDOW ---
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

BUTTON_SPACING = 8  # khoảng cách giữa các nút thuật toán
BUTTON_RADIUS = 8          # độ bo góc 

# --- NHÓM NÚT THUẬT TOÁN ---
ALG_LEFT = 60   # khoảng cách trái của nhóm thuật toán với màn hình
# NHÓM CHA
GROUP_BUTTON_WIDTH = 250 # độ rộng nút
GROUP_BUTTON_HEIGHT = 40   # độ cao nút cha
TOTAL_GROUP_HEIGHT = 6*GROUP_BUTTON_HEIGHT + 5*BUTTON_SPACING # tổng độ cao nhóm cha
# NHÓM CON
ALG_BUTTON_WIDTH = GROUP_BUTTON_WIDTH
ALG_BUTTON_HEIGHT = 60     # độ cao nút con
TOTAL_4ALG_HEIGHT = 4*ALG_BUTTON_HEIGHT +  3*BUTTON_SPACING # tổng độ cao nhóm 4 con 
PARENT_CHILD_SPACING = 30 # khoảng cách giữa nhóm cha và nhóm con

# --- MAZE ---
MAZE_OFFSET_X = ALG_LEFT + GROUP_BUTTON_WIDTH + 90 
MAZE_OFFSET_Y = 60
MAZE_SIZE = 24
CELL_SIZE = 24
MAZE_WIDTH = MAZE_HEIGHT = MAZE_SIZE * CELL_SIZE

# --- NHÓM NÚT CHỨC NĂNG ---
BUTTON_WIDTH = 85 
BUTTON_HEIGHT = 40
CONTROL_OFFSET_X = ALG_LEFT + 125
CONTROL_OFFSET_Y = MAZE_OFFSET_Y + TOTAL_GROUP_HEIGHT + PARENT_CHILD_SPACING + TOTAL_4ALG_HEIGHT + 50
CONTROL_SPACING = 10

# --- NHÓM LEGEND, STATS & HISTORY
LEGEND_HEIGHT = 185
LEGEND_STAT_HIS_X = MAZE_OFFSET_X + MAZE_WIDTH + 90
STAT_HIS_Y = MAZE_OFFSET_Y + LEGEND_HEIGHT + 10
RIGHT_SIDE_PANEL_WIDTH = 280
RIGHT_SIDE_PANEL_HEIGHT = MAZE_OFFSET_Y + TOTAL_GROUP_HEIGHT + PARENT_CHILD_SPACING + TOTAL_4ALG_HEIGHT - STAT_HIS_Y

GRADIENTS = {
    "purple_blue": ((147, 51, 234), (59, 130, 246)),
    "cyan_blue": ((6, 182, 212), (59, 130, 246)),
    "green_blue": ((74, 222, 128), (37, 99, 235)),
    "purple_pink": ((168, 85, 247), (236, 72, 153)),
    "pink_orange": ((236, 72, 153), (251, 146, 60)),
    "teal_lime": ((153, 246, 228), (217, 249, 157)),
    "red_yellow": ((254, 202, 202), (252, 165, 165), (254, 240, 138))
}

class Renderer:
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        
        # --- Load custom fonts ---
        lost_path = os.path.join("assets", "fonts", "LostVietnam-Regular.otf")
        josefin_path = os.path.join("assets", "fonts", "JosefinSans-SemiBold.ttf")

        self.lostvn_font = pygame.font.Font(lost_path, 22)   # font cho nhóm cha
        self.big_josef = pygame.font.Font(josefin_path, 18)  # font cho nhóm con
        self.small_josef = pygame.font.Font(josefin_path, 14)  # mô tả nhỏ hơn

        self.algorithm_groups = [
            {
                "name": "Uninformed Search",
                "gradient": "cyan_blue",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Breadth-First Search", "desc": "Tìm theo chiều rộng"},
                    {"name": "Depth-First Search", "desc": "Tìm theo chiều sâu"},
                    {"name": "Depth-Limited Search", "desc": "Giới hạn độ sâu"},
                    {"name": "Uniform Cost Search", "desc": "Chi phí thấp nhất"}
                ]
            },
            {
                "name": "Informed Search",
                "gradient": "green_blue",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "A* Search", "desc": "Tối ưu với heuristic"},
                    {"name": "Greedy Best-First", "desc": "Tham lam heuristic"}
                ]
            },            
            {
                "name": "Local Search",
                "gradient": "purple_pink",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Hill Climbing", "desc": "Leo đồi tối ưu"},
                    {"name": "Simulated Annealing", "desc": "Mô phỏng ủ kim loại"},
                    {"name": "Beam Search", "desc": "Giới hạn node"}
                ]
            },
            {
                "name": "Complex Environment",
                "gradient": "pink_orange",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Nondeterministic", "desc": "Cấu trúc AND-OR"},
                    {"name": "Unobservable Search", "desc": "Không quan sát"},
                    {"name": "Partial Observable", "desc": "Nhìn thấy một phần"}
                ]
            },
            {
                "name": "Constraint Satisfied",
                "gradient": "teal_lime",
                "text_color": BLACK,
                "algorithms": [
                    {"name": "Backtracking", "desc": "Thử và sai, quay lui khi vi phạm"},
                    {"name": "Forward Checking", "desc": "Cắt tỉa miền giá trị sau mỗi gán"},
                    {"name": "Arc Consistency 3", "desc": "Duy trì tính nhất quán"}
                ]
            },
            {
                "name": "Coming Soon",
                "gradient": "red_yellow",
                "text_color": BLACK,
                "algorithms": [
                    {"name": "", "desc": ""},
                    {"name": "", "desc": ""},
                    {"name": "", "desc": ""}
                ]
            }
        ]

        self.button_states = {
            "start": "normal",
            "stop": "normal",
            "reset_path": "normal",
            "reset": "normal",
            "new_maze": "normal",
            "beautiful_maze": "normal",
            "set_nodes": "normal",
            "set_wall": "normal",
            "statistics": "normal",
            "group_statistics": "normal"
        }

    def draw_gradient_rect(surface, rect, color1, color2, color3=None, vertical=True, border_radius=0):
        """
        Vẽ gradient (2 hoặc 3 màu) với bo góc.
        """
        x, y, w, h = rect

        # --- Tạo surface tạm để chứa gradient ---
        temp_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        # --- Vẽ gradient lên temp_surface ---
        if color3 is None:
            steps = h if vertical else w
            for i in range(steps):
                ratio = i / steps
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                if vertical:
                    pygame.draw.line(temp_surface, (r, g, b), (0, i), (w, i))
                else:
                    pygame.draw.line(temp_surface, (r, g, b), (i, 0), (i, h))
        else:
            steps = h if vertical else w
            mid = steps // 2
            for i in range(steps):
                if i < mid:
                    ratio = i / mid
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                else:
                    ratio = (i - mid) / (steps - mid)
                    r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
                    g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
                    b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
                if vertical:
                    pygame.draw.line(temp_surface, (r, g, b), (0, i), (w, i))
                else:
                    pygame.draw.line(temp_surface, (r, g, b), (i, 0), (i, h))

        # --- Tạo mask bo góc ---
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=border_radius)
        temp_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # --- Vẽ lên surface chính ---
        surface.blit(temp_surface, (x, y))

    # --- Nhóm thuật toán ---
    def draw_group_buttons(self):
        """Vẽ nhóm thuật toán thành 1 cột dọc (nút cha nhỏ hơn)"""
        start_x = ALG_LEFT
        start_y = MAZE_OFFSET_Y
        
        for i, group in enumerate(self.algorithm_groups):
            x = start_x
            y = start_y + i * (GROUP_BUTTON_HEIGHT + BUTTON_SPACING)
            button_rect = pygame.Rect(x, y, GROUP_BUTTON_WIDTH, GROUP_BUTTON_HEIGHT)
            
            colors = GRADIENTS["purple_blue"]

            if self.game.selected_group == i:
                if len(colors) == 2:
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1],
                                                vertical=False,
                                                border_radius=BUTTON_RADIUS)
                else:  # 3 màu
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1], colors[2],
                                                vertical=False,
                                                border_radius=BUTTON_RADIUS)
                # viền
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=BUTTON_RADIUS)
                text_color = WHITE
            else:
                c1, c2, c3 = GRADIENTS["red_yellow"]
                Renderer.draw_gradient_rect(self.screen, button_rect,
                                            c1, c2, c3,
                                            vertical=False,
                                            border_radius=BUTTON_RADIUS)
                text_color = "#2e2f4b"

            text = self.lostvn_font.render(group["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            text_rect.y -= 2
            self.screen.blit(text, text_rect)

    def get_group_button_rect(self, i):
        start_x = ALG_LEFT
        start_y = MAZE_OFFSET_Y
        y = start_y + i * (GROUP_BUTTON_HEIGHT + BUTTON_SPACING)
        return pygame.Rect(start_x, y, GROUP_BUTTON_WIDTH, GROUP_BUTTON_HEIGHT)

    # --- Thuật toán con ---
    def draw_algorithm_buttons(self):
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.algorithm_groups):
            return

        start_x = ALG_LEFT
        start_y = (MAZE_OFFSET_Y + TOTAL_GROUP_HEIGHT + PARENT_CHILD_SPACING)
        spacing = BUTTON_SPACING
        
        current_group = self.algorithm_groups[self.game.selected_group]

        # Lấy gradient của group
        colors = GRADIENTS["purple_pink"]
        main_color = colors[0]   # màu text / viền chính
        
        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (ALG_BUTTON_HEIGHT + spacing)
            button_rect = pygame.Rect(start_x, y, ALG_BUTTON_WIDTH, ALG_BUTTON_HEIGHT)

            if self.game.selected_algorithm == i:
                if len(colors) == 2:
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1],
                                                vertical=False,
                                                border_radius=BUTTON_RADIUS)
                else:
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1], colors[2],
                                                vertical=False,
                                                border_radius=BUTTON_RADIUS)

                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=BUTTON_RADIUS)
                text_color = current_group.get("text_color", WHITE)  # chữ theo group
                desc_color = current_group.get("text_color", WHITE)
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=BUTTON_RADIUS)

                # chữ tím xanh cố định
                c1, c2 = GRADIENTS["purple_blue"]
                text_color = c1
                desc_color = c2
            
            # Vẽ tên thuật toán
            name_text = self.big_josef.render(algorithm["name"], True, text_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            
            # Vẽ mô tả
            desc_text = self.small_josef.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 30))

    def get_algorithm_button_rect(self, group_index, alg_index):
        start_x = ALG_LEFT
        start_y = (MAZE_OFFSET_Y 
                   + len(self.algorithm_groups) * (GROUP_BUTTON_HEIGHT + BUTTON_SPACING) 
                   + PARENT_CHILD_SPACING)
        y = start_y + alg_index * (ALG_BUTTON_HEIGHT + BUTTON_SPACING)
        return pygame.Rect(start_x, y, ALG_BUTTON_WIDTH, ALG_BUTTON_HEIGHT)

    # --- Info thuật toán hiện tại ---
    def draw_current_algorithm_info(self):
        """Hiển thị thông tin thuật toán hiện tại"""
        info_x = MAZE_OFFSET_X
        info_y = MAZE_OFFSET_Y - 45
        
        current_group = self.algorithm_groups[self.game.selected_group]
        
        # Lấy gradient màu của group
        gradient_key = current_group.get("gradient", "purple_blue")
        colors = GRADIENTS[gradient_key]
        main_color = (147, 51, 234)

        if self.game.selected_algorithm == -1:
            # Chưa chọn thuật toán con
            if self.game.group_results:
                info_text = f"Nhóm: {current_group['name']} - Đã chạy tất cả thuật toán (Nhấn thuật toán con để xem kết quả)"
            else:
                info_text = f"Nhóm: {current_group['name']} - Nhấn Run để chạy tất cả thuật toán"
        else:
            # Đã chọn thuật toán con
            current_alg = current_group["algorithms"][self.game.selected_algorithm]
            if self.game.selected_result_algorithm:
                info_text = f"Đang hiển thị: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
            else:
                info_text = f"Đang sử dụng: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
        text = self.big_josef.render(info_text, True, main_color)
        self.screen.blit(text, (info_x, info_y))        

    def draw_controls(self):
        """Vẽ các nút điều khiển với gradient và hiệu ứng nhấn"""
        buttons = [
            {"text": "Run", "action": "start"},
            {"text": "Stop", "action": "stop"},
            {"text": "Reset", "action": "reset_path"},
            {"text": "Empty", "action": "reset"},
            {"text": "Graph", "action": "new_maze"},
            {"text": "Maze", "action": "beautiful_maze"},
            {"text": "Start/End", "action": "set_nodes"},
            {"text": "Wall", "action": "set_wall"},
            {"text": "Statistic", "action": "statistics"},
            {"text": "Group Stat", "action": "group_statistics"}
        ]

        # --- Cấu hình layout ---
        first_row_count = 6
        button_width, button_height = BUTTON_WIDTH, BUTTON_HEIGHT
        spacing = CONTROL_SPACING

        maze_center_x = MAZE_OFFSET_X + MAZE_WIDTH // 2
        total_row1_width = first_row_count * button_width + (first_row_count - 1) * spacing
        start_x_row1 = maze_center_x - total_row1_width // 2
        start_y_row1 = CONTROL_OFFSET_Y

        total_row2_width = (len(buttons) - first_row_count) * button_width + (len(buttons) - first_row_count - 1) * spacing
        start_x_row2 = maze_center_x - total_row2_width // 2
        start_y_row2 = start_y_row1 + button_height + spacing + 5

        # --- Gradient preset ---
        red_yellow = GRADIENTS["red_yellow"]
        purple_blue = GRADIENTS["purple_blue"]

        for i, button in enumerate(buttons):
            if i < first_row_count:
                x = start_x_row1 + i * (button_width + spacing)
                y = start_y_row1
            else:
                j = i - first_row_count
                x = start_x_row2 + j * (button_width + spacing)
                y = start_y_row2

            rect = pygame.Rect(x, y, button_width, button_height)
            state = self.button_states.get(button["action"], "normal")

            # --- Xác định gradient và màu chữ ---
            if state == "active":
                c1, c2 = purple_blue
                text_color = WHITE
            elif state == "flash":
                c1, c2 = purple_blue
                text_color = WHITE
            else:
                c1, c2, c3 = red_yellow
                text_color = BLACK

            # Nút Run bị khóa khi đang chạy
            if button["action"] == "start" and self.game.is_running:
                c1, c2, c3 = red_yellow
                text_color = GRAY

            # Vẽ gradient
            if "c3" in locals():
                Renderer.draw_gradient_rect(self.screen, rect, c1, c2, c3, vertical=False, border_radius=BUTTON_RADIUS)
            else:
                Renderer.draw_gradient_rect(self.screen, rect, c1, c2, vertical=False, border_radius=BUTTON_RADIUS)

            # Viền
            border_col = BLACK
            pygame.draw.rect(self.screen, border_col, rect, 1, border_radius=BUTTON_RADIUS)

            # Text
            text = self.small_josef.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def get_control_button_rect(self, i):
        """Trả về vị trí nút thứ i (2 hàng: 6 nút trên, 4 nút dưới)"""
        button_width = BUTTON_WIDTH
        button_height = BUTTON_HEIGHT
        spacing = CONTROL_SPACING
        first_row_count = 6

        maze_center_x = MAZE_OFFSET_X + MAZE_WIDTH // 2

        # Hàng 1
        total_row1_width = first_row_count * button_width + (first_row_count - 1) * spacing
        start_x_row1 = maze_center_x - total_row1_width // 2
        start_y_row1 = CONTROL_OFFSET_Y

        # Hàng 2
        total_row2_width = (10 - first_row_count) * button_width + (10 - first_row_count - 1) * spacing
        start_x_row2 = maze_center_x - total_row2_width // 2
        start_y_row2 = start_y_row1 + button_height + spacing + 5

        # Tính rect cho nút i
        if i < first_row_count:
            x = start_x_row1 + i * (button_width + spacing)
            y = start_y_row1
        else:
            j = i - first_row_count
            x = start_x_row2 + j * (button_width + spacing)
            y = start_y_row2

        return pygame.Rect(x, y, button_width, button_height)
    
    def draw_legend(self):
        """Vẽ chú thích"""
        legend_x = LEGEND_STAT_HIS_X
        legend_y = MAZE_OFFSET_Y
        
        legend_rect = pygame.Rect(legend_x, legend_y, RIGHT_SIDE_PANEL_WIDTH, LEGEND_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, legend_rect)
        pygame.draw.rect(self.screen, BLACK, legend_rect, 2)
        
        title = self.lostvn_font.render("LEGEND", True, "#2e2f4b")
        self.screen.blit(title, (legend_x + 10, legend_y + 10))
        
        legend_items = [
            ("Start", START_COLOR),
            ("Goal", GOAL_COLOR),
            ("Wall", WALL_COLOR),
            ("Visited", VISITED_COLOR),
            ("Path", PATH_COLOR),
            ("Current", CURRENT_COLOR),
            ("Unknown", UNKNOWN_COLOR),
            ("Backtrack", BACKTRACK_COLOR),
            ("Empty", EMPTY_COLOR)
        ]
        
        for i, (label, color) in enumerate(legend_items):
            # Tính vị trí hàng và cột
            col = i % 2  # 0 hoặc 1
            row = i // 2

            # Khoảng cách giữa các cột và hàng
            col_spacing = 100
            row_spacing = 25

            # Gốc trên bên trái của bảng legend
            x = legend_x + 15 + col * col_spacing
            y = legend_y + 45 + row * row_spacing

            # Ô màu
            color_rect = pygame.Rect(x, y + 5, 15, 15)
            pygame.draw.rect(self.screen, color, color_rect)
            pygame.draw.rect(self.screen, BLACK, color_rect, 1)

            # Nhãn
            label_text = self.small_josef.render(label, True, BLACK)
            self.screen.blit(label_text, (x + 25, y + 5))

    def draw_stats_and_history(self):
            """Vẽ bảng thống kê & history kết hợp"""
            # Vị trí bên phải maze
            stats_x = LEGEND_STAT_HIS_X
            stats_y = STAT_HIS_Y
            
            # Background - Tăng chiều cao để chứa cả stats và history
            stats_rect = pygame.Rect(stats_x, stats_y, RIGHT_SIDE_PANEL_WIDTH, RIGHT_SIDE_PANEL_HEIGHT)
            pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect)
            pygame.draw.rect(self.screen, BLACK, stats_rect, 2)
            
            # STATS HIỆN TẠI 
            title = self.lostvn_font.render("CURRENT RUNNING", True, "#2e2f4b")
            self.screen.blit(title, (stats_x + 10, stats_y + 10))
            
            # Current stats
            stats_info = [
                f"Nodes visited : {self.game.stats['nodes_visited']}",
                f"Path length : {self.game.stats['path_length']}",
                f"Time : {self.game.stats['time']:.0f}ms",
                f"Status : {'Running' if self.game.is_running else 'Stop'}"
            ]
            
            for i, info in enumerate(stats_info):
                text = self.small_josef.render(info, True, BLACK)
                self.screen.blit(text, (stats_x + 15, stats_y + 45 + i * 20))
            
            # Đường phân cách
            pygame.draw.line(self.screen, DARK_GRAY, 
                            (stats_x + 10, stats_y + 130), 
                            (stats_x + 260, stats_y + 130), 2)
            
            #HISTORY
            history_title = self.lostvn_font.render("HISTORY", True, "#2e2f4b")
            self.screen.blit(history_title, (stats_x + 10, stats_y + 140))
            
            if not self.game.history:
                no_data = self.small_josef.render("No data", True, GRAY)
                self.screen.blit(no_data, (stats_x + 15, stats_y + 180))
            else:
                offset_y = 180
                recent_history = self.game.history[:5]

                for i, entry in enumerate(recent_history):
                    # Càng cũ thì càng nhạt
                    fade = min(40 + i * 25, 120)  # càng cao càng nhạt
                    color = (fade, fade, fade) if i > 0 else (10, 10, 10)
                    
                    # Tên thuật toán với status
                    status_text = entry.get('status', 'unknown')
                    name_text = self.small_josef.render(f"#{i+1}. {entry['name']} ({status_text})", True, color)
                    self.screen.blit(name_text, (stats_x + 15, stats_y + offset_y))

                    # Hiển thị thông tin chi tiết
                    info_text = self.small_josef.render(
                        f"Nodes: {entry['nodes']}   Len: {entry['length']}   Time: {entry['time']}",
                        True, color
                    )
                    self.screen.blit(info_text, (stats_x + 35, stats_y + offset_y + 16))

                    offset_y += 38

    def draw_maze(self):
        """Vẽ maze"""
        # Background maze
        maze_bg = pygame.Rect(MAZE_OFFSET_X - 3, MAZE_OFFSET_Y - 3, 
                            MAZE_WIDTH + 6, MAZE_HEIGHT + 6)
        pygame.draw.rect(self.screen, BLACK, maze_bg)

        # Dùng known_maze nếu có, ngược lại dùng maze đầy đủ
        maze = getattr(self.game, "known_maze", self.game.maze)
        
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                x = MAZE_OFFSET_X + j * CELL_SIZE
                y = MAZE_OFFSET_Y + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                cell = maze[i][j]

                # Determine cell color
                if cell == -1:  # Chưa biết
                    color = UNKNOWN_COLOR
                elif cell == 1:  # Wall
                    color = WALL_COLOR
                elif (hasattr(self.game, 'custom_start') and self.game.custom_start is not None and 
                      (i, j) == self.game.custom_start):  # Custom Start
                    color = START_COLOR
                elif (hasattr(self.game, 'custom_end') and self.game.custom_end is not None and 
                      (i, j) == self.game.custom_end):  # Custom End
                    color = GOAL_COLOR
                elif self.game.current_node and self.game.current_node == (i, j):  # Current node
                    color = CURRENT_COLOR
                elif (i, j) in self.game.path:  # Path
                    color = PATH_COLOR
                elif (i, j) in getattr(self.game, 'backtracked_nodes', set()):  # Backtracked nodes (màu xám nhạt)
                    color = BACKTRACK_COLOR
                elif (i, j) in self.game.visited:  # Visited (màu xanh nhạt)
                    color = VISITED_COLOR
                else:  # Empty
                    color = WHITE
                
                pygame.draw.rect(self.screen, color, rect)
                if color != WALL_COLOR: 
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

        # Highlight path của thuật toán được chọn nếu có
        if (hasattr(self.game, 'selected_result_algorithm') and 
            self.game.selected_result_algorithm and 
            self.game.selected_result_algorithm in self.game.group_results):
            
            result_path = self.game.group_results[self.game.selected_result_algorithm]['path']
            for i, j in result_path:
                x = MAZE_OFFSET_X + j * CELL_SIZE
                y = MAZE_OFFSET_Y + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                # Vẽ viền dày màu đỏ để highlight
                pygame.draw.rect(self.screen, RED, rect, 3)

        # Highlight tầm nhìn nếu có
        if hasattr(self.game, "visible_cells"):
            for (i, j) in self.game.visible_cells:
                x = MAZE_OFFSET_X + j * CELL_SIZE
                y = MAZE_OFFSET_Y + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 2)  # viền xanh

    def draw_all(self):
        """Vẽ tất cả các thành phần giao diện"""
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats_and_history()
        self.draw_maze()
        self.draw_legend()
