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
MAZE_OFFSET_Y = 100


class Renderer:
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 16)

    # --- Nhóm thuật toán ---
    def draw_group_buttons(self):
        """Vẽ 6 nhóm thuật toán ở góc trên trái (2x3)"""
        button_width = 120
        button_height = 50
        start_x = 20
        start_y = 20
        spacing = 10
        
        for i, group in enumerate(self.game.algorithm_groups):
            # Tính vị trí button (2 cột, 3 hàng)
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # Màu button
            if self.game.selected_group == i:
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

    # --- Thuật toán con ---
    def draw_algorithm_buttons(self):
        """Vẽ 3 thuật toán con ở góc dưới trái"""
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.game.algorithm_groups):
            return
        
        button_width = 250
        button_height = 60
        start_x = 20
        start_y = 420
        spacing = 5
        
        current_group = self.game.algorithm_groups[self.game.selected_group]
        
        # Title cho nhóm được chọn
        title_text = self.font.render(
            f"Nhóm: {current_group['name'].replace(chr(10), ' ')}", 
            True, current_group["color"]
        )
        self.screen.blit(title_text, (start_x, start_y - 30))
        
        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect(start_x, y, button_width, button_height)
            
            # Màu button
            if self.game.selected_algorithm == i:
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

    # --- Info thuật toán hiện tại ---
    def draw_current_algorithm_info(self):
        """Hiển thị thông tin thuật toán hiện tại"""
        info_x = MAZE_OFFSET_X
        info_y = MAZE_OFFSET_Y - 40
        
        current_group = self.game.algorithm_groups[self.game.selected_group]
        current_alg = current_group["algorithms"][self.game.selected_algorithm]
        
        info_text = f"Đang sử dụng: {current_alg['name']} ({current_group['name'].replace(chr(10), ' ')})"
        text = self.font.render(info_text, True, current_group["color"])
        self.screen.blit(text, (info_x, info_y))
