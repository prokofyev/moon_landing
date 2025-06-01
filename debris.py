import pygame
import random

from constants import *

class Debris:
    def __init__(self, image, x, y, velocity):
        # Разделяем изображение на 9 частей
        self.pieces = []
        width = image.get_width() // 3
        height = image.get_height() // 3
        
        # Используем скорость падения для расчёта разлёта обломков
        velocity_factor = abs(velocity) / SAFE_LANDING_SPEED * 0.1
        
        for row in range(3):
            for col in range(3):
                # Создаем поверхность для части
                piece = pygame.Surface((width, height))
                # Копируем часть изображения
                piece.blit(image, (0, 0), 
                          (col * width, row * height, width, height))
                # Делаем черный цвет прозрачным
                piece.set_colorkey((0, 0, 0))
                
                # Начальная позиция и скорость для каждой части
                # Увеличиваем разброс скоростей в зависимости от скорости падения
                self.pieces.append({
                    'surface': piece,
                    'x': x + col * width,
                    'y': y + row * height,
                    'dx': random.uniform(-5, 5) * velocity_factor,
                    'dy': random.uniform(-10, -5) * velocity_factor,
                    'angle': 0,
                    'rotation_speed': random.uniform(-10, 10) * velocity_factor
                })
        
        self.start_time = pygame.time.get_ticks()
        
    def update(self):
        for piece in self.pieces:
            if not self.is_settled():
                # Применяем гравитацию
                piece['dy'] += GRAVITY * 0.1
                
                # Обновляем позицию
                piece['x'] += piece['dx']
                piece['y'] += piece['dy']
                
                # Вращаем часть
                piece['angle'] += piece['rotation_speed']
                
                # Отскок от поверхности
                if piece['y'] > SCREEN_HEIGHT - MOON_SURFACE_HEIGHT:
                    piece['y'] = SCREEN_HEIGHT - MOON_SURFACE_HEIGHT
                    piece['dy'] *= -0.5  # Уменьшаем энергию при отскоке
                    piece['dx'] *= 0.8   # Трение
                    piece['rotation_speed'] *= 0.8  # Замедляем вращение при ударе
                    if random.random() < 0.1:  # 10% шанс на трение
                        piece['rotation_speed'] *= -1
            else:
                # Если обломки остановились, прекращаем вращение
                piece['rotation_speed'] = 0
                
    def draw(self, screen):
        for piece in self.pieces:
            # Вращаем изображение
            rotated = pygame.transform.rotate(piece['surface'], piece['angle'])
            # Получаем новый прямоугольник после вращения
            rect = rotated.get_rect(center=(piece['x'] + piece['surface'].get_width()//2,
                                          piece['y'] + piece['surface'].get_height()//2))
            screen.blit(rotated, rect)
            
    def is_settled(self):
        # Проверяем, все ли части практически остановились
        for piece in self.pieces:
            if abs(piece['dy']) > 0.1 or abs(piece['dx']) > 0.1:
                return False
        return True