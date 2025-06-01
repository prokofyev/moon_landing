from constants import *

class LunarLander:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2 - LANDER_WIDTH // 2
        self.y = 100
        self.velocity = 0
        self.thrust_on = False
        self.crashed = False
        self.landed_successfully = False
        self.astronaut_x = 0
        self.landing_time = 0
        self.debris = None
        self.crash_time = 0 
        self.fuel = INITIAL_FUEL

    def update(self):
        # Применяем гравитацию только если не приземлились успешно
        if not self.landed_successfully:
            self.velocity += GRAVITY * 0.1

            # Если двигатель включен и есть топливо, применяем силу тяги
            if self.thrust_on and self.fuel > 0:
                self.velocity -= THRUST * 0.1
                self.fuel -= FUEL_CONSUMPTION_RATE * 0.1  # Уменьшаем топливо
                if self.fuel < 0:  # Проверяем, не ушло ли значение в минус
                    self.fuel = 0

            # Обновляем позицию
            self.y += self.velocity