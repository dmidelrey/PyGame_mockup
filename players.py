import pygame
# Функция загрузки изображений
def load_images(image_paths, size):
    images = []
    for image_path in image_paths:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, size)
        images.append(image)
    return images

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pygame.Surface((size_x, size_y))
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
        self.count = 0
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
