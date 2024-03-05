import pygame
import os
import players
import pickle

# Измененные параметры
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
pygame.display.set_caption("Моя Первая Игра")

running = True

player_images = ['sprites/sprite2.png']
left_anim = ['sprites/sprite8.png', 'sprites/sprite9.png', 'sprites/sprite10.png', 'sprites/sprite11.png']
up_anim = ['sprites/sprite4.png', 'sprites/sprite5.png', 'sprites/sprite6.png', 'sprites/sprite7.png']
down_anim = ['sprites/sprite1.png', 'sprites/sprite2.png', 'sprites/sprite3.png']

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)

player = players.Player(data['rect'].x, data['rect'].y, (327 // 4, 428 // 4), player_images, left_anim, up_anim, down_anim)
player.count = data['count']
mask=data['mask']

all_obs = pygame.sprite.Group()
if mask[0]:
    obstacle = players.Obstacle(200, 100, 100, 50)
    all_obs.add(obstacle)
if mask[1]:
    obstacle_1 = players.Obstacle(250, 150, 100, 50)
    all_obs.add(obstacle_1)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, all_obs)

# Настройка шрифта
font = pygame.font.SysFont(None, 36)  # Выбор системного шрифта размером 36

# Создание текстовой строки
text = font.render(str(player.count), True, (0, 255, 255))  # Создаем текстовое изображение

# Получение прямоугольника, описывающего текст
text_rect = text.get_rect()
text_rect.bottomright = (width - 10, height - 10)  # Устанавливаем координаты правого нижнего угла

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data={
                'rect':player.rect,
                'mask':mask,
                'count':player.count
            }
            with open('data.pickle', 'wb') as f:
                pickle.dump(data, f)
            running = False

    pressed = pygame.key.get_pressed()
    # Копируем текущее состояние rect игрока
    player_rect = player.rect.copy()

    # Обновляем позицию игрока
    player.move(pressed)

    # Проверяем столкновение с препятствием
    collisions = pygame.sprite.spritecollide(player, all_obs, False)
    if collisions:
        for obstacle in collisions:
            obstacle.kill()
            all_sprites.remove(obstacle)
            all_obs.remove(obstacle)
            player.count=player.count+1

    if player.count == 2:
        player.count = 0
        player.rect.x = 0
        player.rect.y = 0
        mask = [1,1]

    window.fill((255, 255, 255))

    all_sprites.update()
    all_sprites.draw(window)

    text = font.render(str(player.count), True, (0, 255, 255))  # Создаем текстовое изображение
    # Вывод текста на экран
    window.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
