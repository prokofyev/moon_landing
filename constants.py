# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
GRAVITY = 1.62  # Ускорение свободного падения на Луне (м/с²)
THRUST = 3.0    # Сила тяги двигателя (м/с²)
SAFE_LANDING_SPEED = 2.0  # Безопасная скорость посадки (м/с)

LANDER_SCALE = 0.4
EXHAUST_SCALE = 0.9
MAN_SCALE = 0.2

LANDER_WIDTH = 1
LANDER_HEIGHT = 1

MOON_SURFACE_HEIGHT = 250  # Высота поверхности луны от нижнего края экрана
MIN_SCREEN_Y = 100  # минимальное расстояние от верха экрана в пикселях

REAL_LANDER_HEIGHT = 5.0  # Реальная высота ракеты в метрах
PIXELS_TO_METERS = REAL_LANDER_HEIGHT / LANDER_HEIGHT  # Коэффициент для конвертации пикселей в метры

INITIAL_FUEL = 100.0  # Начальное количество топлива
FUEL_CONSUMPTION_RATE = 5  # Расход топлива в секунду
FUEL_BAR_WIDTH = 200  # Ширина полоски топлива
FUEL_BAR_HEIGHT = 20  # Высота полоски топлива