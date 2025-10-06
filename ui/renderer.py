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
        
        self.font = pygame.font.SysFont("segoeui", 20)   
        self.title_font = pygame.font.SysFont("segoeui", 28, bold=True)
        self.small_font = pygame.font.SysFont("segoeui", 16)

        # --- Kích thước nút ---
        self.GROUP_BUTTON_WIDTH = 170
        self.GROUP_BUTTON_HEIGHT = 38   # cha nhỏ hơn
        self.ALG_BUTTON_WIDTH = 250
        self.ALG_BUTTON_HEIGHT = 60     # con to hơn
        self.BUTTON_SPACING = 5
        self.BUTTON_RADIUS = 8          # độ bo góc 

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
                    {"name": "Nondeterministic", "desc": "Tìm kiếm với cấu trúc AND-OR"},
                    {"name": "Unobservable Search", "desc": "Không quan sát"},
                    {"name": "Partial Observable", "desc": "Nhìn thấy một phần"}
                ]
            },
            {
                "name": "Constraint Satisfied Problem",
                "gradient": "teal_lime",
                "text_color": BLACK,
                "algorithms": [
                    {"name": "Backtracking", "desc": "Thử và sai, quay lui khi vi phạm"},
                    {"name": "Forward Checking", "desc": "Cắt tỉa miền giá trị sau mỗi gán"},
                    {"name": "Arc Consistency Algorithm 3", "desc": "Thuật toán duy trì tính nhất quán"}
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
        """Vẽ 6 nhóm thuật toán chia thành 3 hàng 2 cột, thu nhỏ gọn"""
        cols = 2
        spacing_x = 12   # khoảng cách giữa 2 cột
        spacing_y = 8    # khoảng cách giữa 2 hàng
        start_x = 30     # dịch trái (cách mép trái màn hình)
        start_y = MAZE_OFFSET_Y   # cách trên 1 chút

        # Thu nhỏ group button
        self.GROUP_BUTTON_WIDTH = 170
        self.GROUP_BUTTON_HEIGHT = 38

        for i, group in enumerate(self.algorithm_groups):
            row = i // cols
            col = i % cols
            x = start_x + col * (self.GROUP_BUTTON_WIDTH + spacing_x)
            y = start_y + row * (self.GROUP_BUTTON_HEIGHT + spacing_y)
            button_rect = pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

            gradient_key = group.get("gradient", "purple_blue")
            colors = GRADIENTS[gradient_key]

            if self.game.selected_group == i:
                if len(colors) == 2:
                    Renderer.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1],
                                                vertical=False, border_radius=self.BUTTON_RADIUS)
                else:
                    Renderer.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], colors[2],
                                                vertical=False, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = group.get("text_color", WHITE)
            else:
                c1, c2 = GRADIENTS["purple_blue"]
                Renderer.draw_gradient_rect(self.screen, button_rect, c1, c2,
                                            vertical=False, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE

            text = self.font.render(group["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_group_button_rect(self, i):
        """Vị trí đúng của group thứ i (phải khớp với draw_group_buttons)"""
        cols = 2
        spacing_x = 12
        spacing_y = 8
        start_x = 30
        start_y = MAZE_OFFSET_Y 

        row = i // cols
        col = i % cols
        x = start_x + col * (self.GROUP_BUTTON_WIDTH + spacing_x)
        y = start_y + row * (self.GROUP_BUTTON_HEIGHT + spacing_y)

        return pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

    # --- Thuật toán con ---
    def draw_algorithm_buttons(self):
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.algorithm_groups):
            return
        cols = 2
        rows = (len(self.algorithm_groups) + cols - 1) // cols  # số hàng thực tế
        start_x = 40
        start_y = (MAZE_OFFSET_Y 
                + rows * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
                + 40)  # cách 1 chút dưới nhóm 6 thuật toán
        spacing = self.BUTTON_SPACING

        
        current_group = self.algorithm_groups[self.game.selected_group]

        # Lấy gradient của group
        gradient_key = current_group.get("gradient", "purple_blue")
        colors = GRADIENTS[gradient_key]
        main_color = colors[0]   # màu text / viền chính

        # Title cho nhóm được chọn
        title_text = self.font.render(
            f"Nhóm: {current_group['name']}", 
            True, (147, 51, 234)
        )
        self.screen.blit(title_text, (start_x, start_y - 30))
        
        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (self.ALG_BUTTON_HEIGHT + spacing)
            button_rect = pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

            if self.game.selected_algorithm == i:
                # --- chọn: vẽ gradient full ---
                if len(colors) == 2:
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1],
                                                vertical=False,
                                                border_radius=self.BUTTON_RADIUS)
                else:
                    Renderer.draw_gradient_rect(self.screen, button_rect,
                                                colors[0], colors[1], colors[2],
                                                vertical=False,
                                                border_radius=self.BUTTON_RADIUS)

                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = current_group.get("text_color", WHITE)  # chữ theo group
                desc_color = current_group.get("text_color", WHITE)
            else:
                # --- chưa chọn: viền gradient, nền trắng ---
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, main_color, button_rect, 1, border_radius=self.BUTTON_RADIUS)

                # chữ tím xanh cố định
                c1, c2 = GRADIENTS["purple_blue"]
                text_color = c1
                desc_color = c2
            
            # Vẽ tên thuật toán
            name_text = self.small_font.render(algorithm["name"], True, text_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            
            # Vẽ mô tả
            desc_text = self.small_font.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 30))

    def get_algorithm_button_rect(self, group_index, alg_index):
        """Vị trí chính xác của thuật toán con"""
        cols = 2
        rows = (len(self.algorithm_groups) + cols - 1) // cols  # = 3 hàng (vì 6 nhóm)
        start_x = 40
        start_y = (MAZE_OFFSET_Y 
                + rows * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
                + 40)  # đồng bộ với draw_algorithm_buttons
        spacing = self.BUTTON_SPACING
        y = start_y + alg_index * (self.ALG_BUTTON_HEIGHT + spacing)
        return pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

    # --- Info thuật toán hiện tại ---
    def draw_current_algorithm_info(self):
        """Hiển thị thông tin thuật toán hiện tại"""
        info_x = MAZE_OFFSET_X
        info_y = MAZE_OFFSET_Y - 45
        
        current_group = self.algorithm_groups[self.game.selected_group]
        current_alg = current_group["algorithms"][self.game.selected_algorithm]

        # Lấy gradient màu của group
        gradient_key = current_group.get("gradient", "purple_blue")
        colors = GRADIENTS[gradient_key]
        main_color = (147, 51, 234)

        info_text = f"Đang sử dụng: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
        text = self.font.render(info_text, True, main_color)
        self.screen.blit(text, (info_x, info_y))

    def draw_controls(self):
        button_width = 100
        button_height = 40
        cols = 3
        spacing_x = 10
        spacing_y = 10

        start_x = 40

        group_rows = 3
        max_algorithms = 4

        start_y = (
            MAZE_OFFSET_Y
            + group_rows * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            + 40
            + max_algorithms * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
            + 20
        )

        buttons = [
            {"text": "Bắt đầu", "color": GREEN, "action": "start"},
            {"text": "Dừng", "color": RED, "action": "stop"},
            {"text": "Reset Path", "color": GRAY, "action": "reset_path"},
            {"text": "Reset", "color": DARK_GRAY, "action": "reset"},
            {"text": "Maze mới", "color": BLUE, "action": "new_maze"},
            {"text": "Maze Đẹp", "color": PURPLE, "action": "beautiful_maze"},
            {"text": "Start/End", "color": (255, 140, 0), "action": "set_nodes"},
            {"text": "Wall Node", "color": ORANGE, "action": "set_wall"},
            {"text": "Thống kê", "color": CYAN, "action": "statistics"},
        ]

        for i, button in enumerate(buttons):
            row = i // cols
            col = i % cols
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)

            color = GRAY if (button["action"] == "start" and self.game.is_running) else button["color"]

            pygame.draw.rect(self.screen, color, button_rect, border_radius=self.BUTTON_RADIUS)

            border_width = 3 if (
                (button["action"] == "set_nodes" and self.game.node_placement_mode in ("start", "end"))
                or (button["action"] == "set_wall" and self.game.node_placement_mode == "wall")
            ) else 1
            pygame.draw.rect(self.screen, BLACK, button_rect, border_width, border_radius=self.BUTTON_RADIUS)

            text = self.small_font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        # Nút QUIT 
        quit_width = 3 * button_width + 2 * spacing_x  # 3 nút + 2 khoảng cách
        quit_height = button_height
        quit_x = start_x
        quit_y = start_y + 3 * (button_height + spacing_y)  # Dưới 3 hàng nút
        quit_rect = pygame.Rect(quit_x, quit_y, quit_width, quit_height)
        
        pygame.draw.rect(self.screen, (220, 20, 60), quit_rect, border_radius=self.BUTTON_RADIUS)  # Crimson Red
        pygame.draw.rect(self.screen, BLACK, quit_rect, 1, border_radius=self.BUTTON_RADIUS)
        
        quit_text = self.font.render("QUIT", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.screen.blit(quit_text, quit_text_rect)
    
    def get_control_button_rect(self, i):
        """Trả về vị trí (Rect) của nút điều khiển thứ i"""
        button_width = 100
        button_height = 40
        cols = 3
        spacing_x = 10
        spacing_y = 10

        start_x = 40

        group_rows = 3
        max_algorithms = 4

        start_y = (
            MAZE_OFFSET_Y
            + group_rows * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            + 40
            + max_algorithms * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
            + 20
        )

        # Nếu là nút Quit (index 9)
        if i == 9:
            quit_width = 3 * button_width + 2 * spacing_x
            quit_x = start_x
            quit_y = start_y + 3 * (button_height + spacing_y)
            return pygame.Rect(quit_x, quit_y, quit_width, button_height)
        
        # Các nút khác
        row = i // cols
        col = i % cols
        x = start_x + col * (button_width + spacing_x)
        y = start_y + row * (button_height + spacing_y)

        return pygame.Rect(x, y, button_width, button_height)



    def draw_stats_and_history(self):
            """Vẽ bảng thống kê & history kết hợp"""
            # Vị trí bên phải maze
            stats_x = MAZE_OFFSET_X + self.game.MAZE_WIDTH + 20
            stats_y = MAZE_OFFSET_Y + 220  # Dưới legend
            
            # Background - Tăng chiều cao để chứa cả stats và history
            stats_rect = pygame.Rect(stats_x, stats_y, 300, 380)
            pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect)
            pygame.draw.rect(self.screen, BLACK, stats_rect, 2)
            
            # STATS HIỆN TẠI 
            title = self.font.render("Lần chạy hiện tại", True, BLACK)
            self.screen.blit(title, (stats_x + 10, stats_y + 10))
            
            # Current stats
            stats_info = [
                f"Nodes đã thăm: {self.game.stats['nodes_visited']}",
                f"Độ dài đường đi: {self.game.stats['path_length']}",
                f"Thời gian: {self.game.stats['time']:.0f}ms",
                f"Trạng thái: {'Đang chạy' if self.game.is_running else 'Dừng'}"
            ]
            
            for i, info in enumerate(stats_info):
                text = self.small_font.render(info, True, BLACK)
                self.screen.blit(text, (stats_x + 10, stats_y + 40 + i * 20))
            
            # Đường phân cách
            pygame.draw.line(self.screen, DARK_GRAY, 
                            (stats_x + 10, stats_y + 130), 
                            (stats_x + 240, stats_y + 130), 2)
            
            #HISTORY
            history_title = self.font.render("Lịch sử", True, BLACK)
            self.screen.blit(history_title, (stats_x + 10, stats_y + 140))
            
            if not self.game.history:
                no_data = self.small_font.render("Chưa có dữ liệu", True, GRAY)
                self.screen.blit(no_data, (stats_x + 10, stats_y + 170))
            else:
                offset_y = 170
                for i, entry in enumerate(self.game.history):
                    # Màu xen kẽ
                    color = BLACK if i % 2 == 0 else DARK_GRAY
                    
                    # Tên thuật toán
                    name_text = self.small_font.render(f"#{i+1}. {entry['name']}", True, color)
                    self.screen.blit(name_text, (stats_x + 10, stats_y + offset_y))
                    
                    # Thông tin chi tiết
                    info_text = self.small_font.render(
                        f"Nodes:{entry['nodes']}    Len:{entry['length']}    Time:{entry['time']}", 
                        True, color
                    )
                    self.screen.blit(info_text, (stats_x + 10, stats_y + offset_y + 16))
                    
                    offset_y += 38

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

        # Dùng known_maze nếu có, ngược lại dùng maze đầy đủ
        maze = getattr(self.game, "known_maze", self.game.maze)
        
        for i in range(self.game.MAZE_SIZE):
            for j in range(self.game.MAZE_SIZE):
                x = MAZE_OFFSET_X + j * self.game.CELL_SIZE
                y = MAZE_OFFSET_Y + i * self.game.CELL_SIZE
                rect = pygame.Rect(x, y, self.game.CELL_SIZE, self.game.CELL_SIZE)
                
                cell = maze[i][j]

                # Determine cell color
                if cell == -1:  # Chưa biết
                    color = GRAY
                elif cell == 1:  # Wall
                    color = BLACK
                elif (hasattr(self.game, 'custom_start') and self.game.custom_start is not None and 
                      (i, j) == self.game.custom_start):  # Custom Start
                    color = GREEN
                elif (hasattr(self.game, 'custom_end') and self.game.custom_end is not None and 
                      (i, j) == self.game.custom_end):  # Custom End
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

        # Highlight tầm nhìn nếu có
        if hasattr(self.game, "visible_cells"):
            for (i, j) in self.game.visible_cells:
                x = MAZE_OFFSET_X + j * self.game.CELL_SIZE
                y = MAZE_OFFSET_Y + i * self.game.CELL_SIZE
                rect = pygame.Rect(x, y, self.game.CELL_SIZE, self.game.CELL_SIZE)
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 2)  # viền xanh

    def draw_all(self):
        """Vẽ tất cả các thành phần giao diện"""
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats_and_history()
        self.draw_current_algorithm_info()
        self.draw_maze()
        self.draw_legend()
