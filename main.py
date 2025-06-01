import pygame
import sys

from constants import *
from lunar_lander import LunarLander
from debris import Debris

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lunar Lander")

def load_and_scale_images():
    global LANDER_WIDTH, LANDER_HEIGHT, PIXELS_TO_METERS

    # Загрузка изображений
    lander_img = pygame.image.load('images/lander.png')
    moon_img = pygame.image.load('images/moon.png')
    stars_img = pygame.image.load('images/stars.png')
    exhaust_img = pygame.image.load('images/exhaust.png')
    man_img = pygame.image.load('images/man.png')
    
    # Масштабирование изображений
    lander_img = pygame.transform.scale(lander_img, 
        (int(lander_img.get_width() * LANDER_SCALE), 
         int(lander_img.get_height() * LANDER_SCALE)))

    LANDER_WIDTH = lander_img.get_width()
    LANDER_HEIGHT = lander_img.get_height()
    PIXELS_TO_METERS = REAL_LANDER_HEIGHT / LANDER_HEIGHT

    exhaust_img = pygame.transform.scale(exhaust_img, 
        (int(exhaust_img.get_width() * EXHAUST_SCALE), 
         int(exhaust_img.get_height() * EXHAUST_SCALE)))
    man_img = pygame.transform.scale(man_img, 
        (int(man_img.get_width() * MAN_SCALE), 
         int(man_img.get_height() * MAN_SCALE)))
    
    explosion_img = pygame.image.load('images/explosion.png')
    explosion_img = pygame.transform.scale(explosion_img, 
        (int(LANDER_WIDTH * 1.5), int(LANDER_HEIGHT * 1.5)))
        
    return lander_img, moon_img, stars_img, exhaust_img, man_img, explosion_img, LANDER_WIDTH, LANDER_HEIGHT

def handle_input(lander, game_over):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not game_over and not lander.landed_successfully:
        keys = pygame.key.get_pressed()
        lander.thrust_on = keys[pygame.K_UP]
        
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            return True  # Signal to restart game
    return False

def check_landing(lander, message_time):
    message = ""
    game_over = False
    
    if lander.y + LANDER_HEIGHT > SCREEN_HEIGHT - MOON_SURFACE_HEIGHT:
        if abs(lander.velocity) <= SAFE_LANDING_SPEED:
            message = "Успешная посадка!"
            lander.landed_successfully = True
            lander.landing_time = pygame.time.get_ticks()
            lander.astronaut_x = lander.x + LANDER_WIDTH//2
        else:
            message = "Крушение!"
            lander.crashed = True
            lander.crash_time = pygame.time.get_ticks()
            game_over = True
        message_time = pygame.time.get_ticks()
    
    return message, game_over, message_time

def draw_game(screen, lander, images, fonts, message, game_over):
    screen.fill((0, 0, 0))
    lander_img, moon_img, stars_img, exhaust_img, man_img, explosion_img = images
    font, large_font = fonts

    screen.blit(stars_img, (0, 0))
    
    # Определяем, нужно ли начать уменьшение размера ракеты
    if lander.y < MIN_SCREEN_Y:
        # Масштаб уменьшается пропорционально превышению границы
        min_scale = 0.01
        height_meters = get_height_meters(lander.y)
        scale = max(min_scale, get_height_meters(MIN_SCREEN_Y) / height_meters)
        # Фиксируем позицию ракеты на экране
        display_y = MIN_SCREEN_Y
    else:
        scale = 1.0
        display_y = lander.y

    scaled_moon = pygame.transform.scale(moon_img, 
        (int(moon_img.get_width() * scale), int(moon_img.get_height() * scale)))

    # Вычисляем позицию для центрального изображения луны
    moon_width = scaled_moon.get_width()
    center_x = (SCREEN_WIDTH - scaled_moon.get_width()) // 2
    moon_y = SCREEN_HEIGHT - scaled_moon.get_height()

    # Отрисовываем центральное изображение
    screen.blit(scaled_moon, (center_x, moon_y))

    # Добавляем копии слева от центра, пока не заполним экран
    left_x = center_x - moon_width
    while left_x >= -moon_width + 1:  # +1 пиксель для перекрытия
        screen.blit(scaled_moon, (left_x, moon_y))
        left_x -= moon_width
    
    # Добавляем копии справа от центра, пока не заполним экран
    right_x = center_x + moon_width
    while right_x <= SCREEN_WIDTH:
        screen.blit(scaled_moon, (right_x, moon_y))
        right_x += moon_width

    # Draw lander or debris
    if lander.crashed:
        if lander.debris is None:
            lander.debris = Debris(lander_img, lander.x, lander.y, lander.velocity)
        lander.debris.update()
        lander.debris.draw(screen)
    else:
        # Масштабируем изображение ракеты
        scaled_lander = pygame.transform.scale(lander_img, 
            (int(LANDER_WIDTH * scale), int(LANDER_HEIGHT * scale)))
        # Корректируем позицию по горизонтали, чтобы ракета оставалась по центру
        x_offset = (LANDER_WIDTH - scaled_lander.get_width()) // 2
        screen.blit(scaled_lander, (lander.x + x_offset, display_y))
        
        if lander.thrust_on and not lander.landed_successfully:
            # Масштабируем выхлоп соответственно
            scaled_exhaust = pygame.transform.scale(exhaust_img,
                (int(exhaust_img.get_width() * scale),
                 int(exhaust_img.get_height() * scale)))
            # Вычисляем центр ракеты с учетом масштаба
            lander_center_x = lander.x + x_offset + scaled_lander.get_width() // 2
            
            # Позиционируем выхлоп по центру ракеты
            exhaust_x = lander_center_x - scaled_exhaust.get_width() // 2
            exhaust_y = display_y + scaled_lander.get_height()
            
            screen.blit(scaled_exhaust, (exhaust_x, exhaust_y))
    
     # Draw astronaut and check animation status
    if lander.landed_successfully:
        animation_finished = draw_astronaut(screen, lander, man_img, game_over)
        if animation_finished and not game_over:
            return True  # Signal to set game_over

    # Draw explosion
    if lander.crashed:
        current_time = pygame.time.get_ticks()
        # Показываем взрыв только в течение 500 мс после крушения
        if current_time - lander.crash_time < 50:
            explosion_x = lander.x + LANDER_WIDTH//2 - explosion_img.get_width()//2
            explosion_y = lander.y + LANDER_HEIGHT//2 - explosion_img.get_height()//2
            screen.blit(explosion_img, (explosion_x, explosion_y))

    # Draw UI
    draw_ui(screen, lander, font, large_font, message, game_over)

def draw_astronaut(screen, lander, man_img, game_over):
    current_time = pygame.time.get_ticks()
    target_x = lander.x - LANDER_WIDTH
    
    if current_time - lander.landing_time < 1000:  # During animation
        progress = (current_time - lander.landing_time) / 1000.0
        start_x = lander.x + LANDER_WIDTH//2
        lander.astronaut_x = start_x + (target_x - start_x) * progress
        screen.blit(man_img, (int(lander.astronaut_x), 
                            SCREEN_HEIGHT - MOON_SURFACE_HEIGHT - man_img.get_height()))
        return False  # Animation not finished
    else:  # After animation
        screen.blit(man_img, (target_x, 
                            SCREEN_HEIGHT - MOON_SURFACE_HEIGHT - man_img.get_height()))
        return True  # Animation finished

def get_height_meters(y):
    height_pixels = max(0, SCREEN_HEIGHT - MOON_SURFACE_HEIGHT - (y + LANDER_HEIGHT))
    height_meters = height_pixels * PIXELS_TO_METERS
    return height_meters

def draw_ui(screen, lander, font, large_font, message, game_over):
    # Отображение скорости
    speed_text = font.render(f"Скорость: {abs(lander.velocity):.1f} м/с", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))

    # Отображение высоты (расстояние от поверхности луны до нижней части ракеты)
    height_meters = get_height_meters(lander.y + LANDER_HEIGHT)
    height_text = font.render(f"Высота: {height_meters:.1f} м", True, (255, 255, 255))
    screen.blit(height_text, (10, 40))

    if game_over:
        text = large_font.render(message, True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 150))
        
        esc_text = font.render("ESC - выход, ПРОБЕЛ - новая игра", True, (255, 255, 255))
        screen.blit(esc_text, (SCREEN_WIDTH//2 - esc_text.get_width()//2, SCREEN_HEIGHT//2 - 30))

def main():
    clock = pygame.time.Clock()
    lander = LunarLander()
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 120)
    game_over = False
    message = ""
    message_time = 0
    
    images = load_and_scale_images()
    global LANDER_WIDTH, LANDER_HEIGHT
    *images, LANDER_WIDTH, LANDER_HEIGHT = images
    fonts = (font, large_font)

    while True:
        should_restart = handle_input(lander, game_over)
        
        if not game_over and not lander.landed_successfully:
            lander.update()
            message, game_over, message_time = check_landing(lander, message_time)

        should_end_game = draw_game(screen, lander, images, fonts, message, game_over)
        if should_end_game:
            game_over = True
            message_time = pygame.time.get_ticks()
        
        if game_over and should_restart:
            game_over = False
            lander.reset()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()