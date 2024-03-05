import pygame
import pygame_menu
import subprocess
import pickle

pygame.init()
surface = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Моя Первая Игра")
sound_effect = pygame.mixer.Sound('blipSelect.wav')
def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    subprocess.Popen(["python", "main.py"])
    sound_effect.play()
    pass

def new_game():
    player_rect = pygame.Rect(0,0,0,0)
    mask=[1,1]
    data = {
        'rect': player_rect,
        'mask': mask,
        'count': 0
    }
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)
    subprocess.Popen(["python", "main.py"])
    sound_effect.play()
    pass

menu = pygame_menu.Menu('Добро пожаловать', 400, 300,
                       theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add.text_input('Имя: ', default='Аркакий?')
menu.add.button('Продолжить', start_the_game)
menu.add.button('Начать новую игру', new_game)
menu.add.button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(surface)