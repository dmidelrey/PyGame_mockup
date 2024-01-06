import pygame
import os

# Функция загрузки изображений
def load_images(image_paths, size):
    images = []
    for image_path in image_paths:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, size)
        images.append(image)
    return images

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, images, left_anim, up_anim, down_anim):
        super().__init__()

        self.images = load_images(images, size)
        self.left_anim = load_images(left_anim, size)
        self.up_anim = load_images(up_anim, size)
        self.down_anim = load_images(down_anim, size)
        self.right_anim = [pygame.transform.flip(image, True, False) for image in self.left_anim]

        self.orientation = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        animations = {
            0: self.images,
            1: self.up_anim,
            2: self.right_anim,
            3: self.left_anim,
            4: self.down_anim
        }

        self.index = (self.index + 1) % len(animations[self.orientation])
        self.image = animations[self.orientation][self.index]

    def move(self, keys):
        direction_mapping = {
            pygame.K_UP: (0, -5, 1),
            pygame.K_DOWN: (0, 5, 4),
            pygame.K_LEFT: (-5, 0, 3),
            pygame.K_RIGHT: (5, 0, 2)
        }

        for key, (dx, dy, orientation) in direction_mapping.items():
            if keys[key]:
                self.rect.x += dx
                self.rect.y += dy
                self.orientation = orientation

        if not any(keys):
            self.orientation = 0

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

player = Player(30, 30, (327 // 4, 428 // 4), player_images, left_anim, up_anim, down_anim)
obstacle = Obstacle(200, 100)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, obstacle)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    # Копируем текущее состояние rect игрока
    player_rect = player.rect.copy()

    # Обновляем позицию игрока
    player.move(pressed)

    # Проверяем столкновение с препятствием
    if pygame.sprite.spritecollide(player, [obstacle], False):
        # Восстанавливаем старую позицию rect
        player.rect = player_rect

    window.fill((255, 255, 255))

    all_sprites.update()
    all_sprites.draw(window)


    pygame.display.flip()
    clock.tick(10)

pygame.quit()
