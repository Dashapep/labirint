import pygame
import os
import sys
import time
import random

pygame.init()
size = width, height = 85 * 16, 50 * 16
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Program')
FPS = 1


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('imgs', name)  # папка с картинками
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():  # загрузка главной заставки
    w, h = pygame.display.get_surface().get_size()
    fon = load_image('заставка.png')
    screen.blit(fon, (w // 2 - 400, h // 2 - 400))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def between_screen():  # закгрузка переходной заставки между уровнями
    screen.fill((0, 0, 0))
    w, h = pygame.display.get_surface().get_size()
    fon = load_image('серединная_заставка.png')
    font = pygame.font.Font(None, 40)
    screen.blit(fon, (w // 2 - 400, h // 2 - 400))
    text = font.render("Вы прошли " + str(yroven) + " уровень", True, (100, 255, 100))
    screen.blit(text, (w // 2 - 400 + 100, h // 2 - 400 + 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def looser_screen():  # загрузка заставки в случае проигрыша
    screen.fill((0, 0, 0))
    w, h = pygame.display.get_surface().get_size()
    fon = load_image('проигрышная_заставка.png')
    font = pygame.font.Font(None, 40)
    screen.blit(fon, (w // 2 - 400, h // 2 - 400))
    text = font.render("Вы не прошли " + str(yroven) + " уровень", True, (100, 255, 100))
    screen.blit(text, (w // 2 - 400 + 100, h // 2 - 400 + 250))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def winner_screen():  # загрузка заставки в случае выигрыша
    screen.fill((0, 0, 0))
    w, h = pygame.display.get_surface().get_size()
    fon = load_image('победная_заставка.png')
    font = pygame.font.Font(None, 40)
    screen.blit(fon, (w // 2 - 400, h // 2 - 400))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'), 'good': load_image('good.png'),
               'bad': load_image('bad.png'), 'dark': load_image('dark.png')}
player_image = load_image('dog.png', -1)

tile_width = tile_height = 16


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Darknes(pygame.sprite.Sprite):  # подключение темноты в лабиринте
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(darknes_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.lightrect = pygame.Rect((pos_x - 1 * tile_width, pos_y - 1 * tile_height, 5 * tile_width, 5 * tile_height))
        self.x = pos_x
        self.y = pos_y

    def update(self, x, y):
        global time
        global vremya
        dx = x // tile_width
        dy = y // tile_height
        if 0 <= self.rect.y + y < height and 0 <= self.rect.x + x < width and \
                level_map[(self.rect.y + y) // tile_height][(self.rect.x + x) // tile_width] in ('.', '@', ')', '('):
            self.rect = self.rect.move(x, y)
            self.lightrect = self.lightrect.move(x, y)  # светлое пространство вокруг героя
            if level_map[(self.rect.y) // tile_height][
                (self.rect.x) // tile_width] == ')':  # если герой наступил на зеленый бонус
                time += 15  # таймер увеличивается на 15 секунд
                remove_bonus()
                level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] = '.'  # бонус удаляется с карты
            elif level_map[(self.rect.y) // tile_height][
                (self.rect.x) // tile_width] == '(':  # если герой наступил на красный бонус
                time -= 15  # таймер уменьшается на 15 секунд
                remove_bonus()
                level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] = '.'  # бонус удаляется с карты
            else:
                pass
            self.x += dx
            self.y += dy
            remove_dark()


def remove_bonus():
    for bonus_elem in tiles_group:
        if player.rect.collidepoint(bonus_elem.rect.center):
            x = bonus_elem.rect.x // 16
            y = bonus_elem.rect.y // 16
            bonus_elem.kill()
            Tile('empty', x, y)


def remove_dark():
    for dark_elem in darknes_group:
        if player.lightrect.collidepoint(dark_elem.rect.center):
            dark_elem.kill()


clock = pygame.time.Clock()
start_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
darknes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_level(filename):
    global level_map
    from PIL import Image
    fullname = os.path.join('imgs', filename)
    a = Image.open(fullname)
    sh, d = a.size
    count_good = 10  # количество зеленых бонусов
    count_bad = 10  # количество красных бонусов
    karta = []
    for y in range(5, d, 14):
        stroka = []
        for x in range(5, sh, 14):
            pix_coord = (x, y)
            try:
                r, g, b, alf = a.getpixel(pix_coord)
            except:
                r, b, g, alf = 0, 0, 0, 0
            if r == 0 and g == 0 and b == 0:
                stroka += '#'
            elif r > 100 and b < 100 and g < 100:
                stroka += '@'
            elif g > 150 and b < 100 and r < 100:
                stroka += ')'
            elif b > 200 and g < 100 and r < 100:
                stroka += '('
            else:
                stroka += '.'
        karta.append(stroka)
    shir_kart = len(karta[0])
    dlin_kart = len(karta)
    while count_bad > 0:  # рандомное выставление 10 красных бонусов на карте
        x = random.randint(1, shir_kart - 2)
        y = random.randint(1, dlin_kart - 2)
        if karta[y][x] == '.':
            karta[y][x] = '('
            count_bad -= 1
    while count_good > 0:  # рандомное выставление 10 зеленых бонусов на карте
        x = random.randint(1, shir_kart - 2)
        y = random.randint(1, dlin_kart - 2)
        if karta[y][x] == '.':
            karta[y][x] = ')'
            count_good -= 1

    return karta


def Show_timer(time):  # показ в левом верхнем углу  сколько прошло, осталось и номер уровня
    font = pygame.font.Font(None, 30)
    text = font.render(str(time), True, (255, 100, 100))
    tvremya = font.render(str(vremya), True, (100, 255, 100))
    textvremya = font.render('Прошло: ', True, (100, 255, 100))
    texttime = font.render('Осталось: ', True, (255, 100, 100))
    yrov = font.render('Уровень ' + str(yroven) + ' / 6', True, (100, 100, 255))
    text_x = width - 80
    text_y = 20
    screen.blit(text, (text_x, text_y))
    screen.blit(texttime, (text_x - 100, text_y))
    screen.blit(tvremya, (text_x, text_y + 30))
    screen.blit(textvremya, (text_x - 100, text_y + 30))
    screen.blit(yrov, (text_x - 100, text_y + 60))

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == ')':
                Tile('good', x, y)
            elif level[y][x] == '(':
                Tile('bad', x, y)
            if not (x < 1 or y < 1 or x >= len(level[y]) - 1 or y >= len(level) - 1):
                Darknes('dark', x, y)
    return new_player, x, y


spisok = ['lab1.png', 'lab2.png', 'lab3.png', 'lab4.png', 'lab5.png',
          'lab6.png']  # задается список доступных лабиринтов
random.shuffle(spisok)  # перемешивается
yroven = 0
for fail in spisok:
    level_map = load_level(fail)
    player, level_x, level_y = generate_level(level_map)
    run = True
    win = False
    time = 240
    vremya = 0
    Show_timer(time)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    remove_dark()
    yroven += 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                player.update(0, tile_height)
            if key[pygame.K_UP]:
                player.update(0, -tile_height)
            if key[pygame.K_LEFT]:
                player.update(-tile_width, 0)
            if key[pygame.K_RIGHT]:
                player.update(tile_width, 0)
            if key[pygame.K_ESCAPE]:  # при нажатии esc игра заканчивается с проигрышем
                run = False
            if key[pygame.K_F10]:  # при нажатии ctrl + F10 весь лабирит становится светлым
                for dark_elem in darknes_group:
                    dark_elem.kill()
            if key[pygame.K_F11]:  # при нажатии ctrl + F11 игра заканчивается с победой
                win = True
                run = False
                break
            if event.type == pygame.USEREVENT:
                time -= 1
                if time <= 0:
                    run = False
                vremya += 1
            if player.y >= level_y or player.x >= level_x:
                run = False
                win = True
        clock.tick(50)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        darknes_group.draw(screen)
        player_group.draw(screen)
        Show_timer(time)
        pygame.display.flip()

    level_map = []
    player.kill()
    if not win:
        looser_screen()
        break
    else:
        between_screen()
if win:
    winner_screen()
terminate()
