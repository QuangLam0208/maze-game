import os
import pygame
import sys

pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 950, 534
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game - Title Screen")

# Font chữ
font = pygame.font.Font(os.path.join("assets", "fonts", "MightySouly-lxggD.ttf"), 30)

# Màu sắc
WHITE = (255, 255, 255)

# Load background
background = pygame.image.load(os.path.join("assets", "pics", "maze-bg.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def draw_text(text, font, color, surface, x, y, is_center=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if is_center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def title_screen():
    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))  # vẽ ảnh nền

        # Vẽ nút
        start_button = draw_text("START", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 20)
        exit_button = draw_text("QUIT", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 80)

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Start Game!")
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    title_screen()
