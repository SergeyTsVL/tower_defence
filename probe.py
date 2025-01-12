import pygame
import sys

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Курсор над областью")

# Определение области для проверки
check_area = pygame.Rect(100, 100, 200, 200)

# Цикл игрового процесса
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if check_area.collidepoint(mouse_pos):
                if event.buttons[0]:  # Левая кнопка мыши
                    print("Курсор над областью и нажата левая кнопка")
                elif event.buttons == 1:  # Буква '4' на клавиатуре
                    print("Курсор над областью и нажата буква '4'sfddgbsf")

        # Дополнительный обработчик для проверки нажатия кнопки 4
        keys = pygame.key.get_pressed()
        if keys[pygame.K_4] and check_area.collidepoint(pygame.mouse.get_pos()):
            print("Курсор над областью и нажата буква '4'")

    # Очистка экрана
    screen.fill((255, 255, 255))

    # Рисование области для проверки
    pygame.draw.rect(screen, (200, 200, 200), check_area)

    # Обновление дисплея
    pygame.display.flip()

    # Установка лимита кадров
    pygame.time.Clock().tick(60)

# Завершение работы Pygame
pygame.quit()
sys.exit()