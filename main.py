import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
GRAVITY = 1.62  # Ускорение свободного падения на Луне (м/с²)
THRUST = 3.0    # Сила тяги двигателя (м/с²)
SAFE_LANDING_SPEED = 2.0  # Безопасная скорость посадки (м/с)

LANDER_SCALE = 0.4
EXHAUST_SCALE = 0.9
MAN_SCALE = 0.2

LANDER_WIDTH = 0
LANDER_HEIGHT = 0

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lunar Lander")

def load_and_scale_images():
    # Загрузка изображений
    lander_img = pygame.image.load('images/lander.png')
    moon_img = pygame.image.load('images/moon.png')
    exhaust_img = pygame.image.load('images/exhaust.png')
    man_img = pygame.image.load('images/man.png')
    
    # Масштабирование изображений
    lander_img = pygame.transform.scale(lander_img, 
        (int(lander_img.get_width() * LANDER_SCALE), 
         int(lander_img.get_height() * LANDER_SCALE)))

    LANDER_WIDTH = lander_img.get_width()
    LANDER_HEIGHT = lander_img.get_height()

    exhaust_img = pygame.transform.scale(exhaust_img, 
        (int(exhaust_img.get_width() * EXHAUST_SCALE), 
         int(exhaust_img.get_height() * EXHAUST_SCALE)))
    man_img = pygame.transform.scale(man_img, 
        (int(man_img.get_width() * MAN_SCALE), 
         int(man_img.get_height() * MAN_SCALE)))
    
    explosion_img = pygame.image.load('images/explosion.png')
    explosion_img = pygame.transform.scale(explosion_img, 
        (int(LANDER_WIDTH * 1.5), int(LANDER_HEIGHT * 1.5)))
        
    return lander_img, moon_img, exhaust_img, man_img, explosion_img, LANDER_WIDTH, LANDER_HEIGHT

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
    
    if lander.y + LANDER_HEIGHT > SCREEN_HEIGHT - 270:
        if abs(lander.velocity) <= SAFE_LANDING_SPEED:
            message = "Успешная посадка!"
            lander.landed_successfully = True
            lander.landing_time = pygame.time.get_ticks()
            lander.astronaut_x = lander.x + LANDER_WIDTH//2
        else:
            message = "Крушение!"
            lander.crashed = True
            game_over = True
        message_time = pygame.time.get_ticks()
    
    return message, game_over, message_time

def draw_game(screen, lander, images, fonts, message, game_over):
    screen.fill((0, 0, 0))
    lander_img, moon_img, exhaust_img, man_img, explosion_img = images
    font, large_font = fonts
    
    # Draw moon and lander
    screen.blit(moon_img, (0, SCREEN_HEIGHT - moon_img.get_height()))
    screen.blit(lander_img, (lander.x, lander.y))
    
    # Draw exhaust
    if lander.thrust_on and not lander.crashed and not game_over:
        screen.blit(exhaust_img, (lander.x + LANDER_WIDTH//2 - exhaust_img.get_width()//2, 
                                lander.y + LANDER_HEIGHT))

    # Draw astronaut and check animation status
    if lander.landed_successfully:
        animation_finished = draw_astronaut(screen, lander, man_img, game_over)
        if animation_finished and not game_over:
            return True  # Signal to set game_over

    # Draw explosion
    if lander.crashed:
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
                            SCREEN_HEIGHT - 270 - man_img.get_height()))
        return False  # Animation not finished
    else:  # After animation
        screen.blit(man_img, (target_x, 
                            SCREEN_HEIGHT - 270 - man_img.get_height()))
        return True  # Animation finished

def draw_ui(screen, lander, font, large_font, message, game_over):
    speed_text = font.render(f"Скорость: {abs(lander.velocity):.1f} м/с", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))

    if game_over:
        text = large_font.render(message, True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 150))
        
        esc_text = font.render("ESC - выход, ПРОБЕЛ - новая игра", True, (255, 255, 255))
        screen.blit(esc_text, (SCREEN_WIDTH//2 - esc_text.get_width()//2, SCREEN_HEIGHT//2 - 30))


class LunarLander:
    def __init__(self):
        self.reset()
        self.crashed = False
        self.landed_successfully = False
        self.astronaut_x = 0
        self.landing_time = 0

    def reset(self):
        self.x = SCREEN_WIDTH // 2 - LANDER_WIDTH // 2
        self.y = 100
        self.velocity = 0
        self.thrust_on = False
        self.crashed = False
        self.landed_successfully = False
        self.astronaut_x = 0
        self.landing_time = 0

    def update(self):
        # Применяем гравитацию только если не приземлились успешно
        if not self.landed_successfully:
            self.velocity += GRAVITY * 0.1

            # Если двигатель включен, применяем силу тяги
            if self.thrust_on:
                self.velocity -= THRUST * 0.1

            # Обновляем позицию
            self.y += self.velocity

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