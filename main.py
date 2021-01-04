import pygame
import os
import sys
import time

# fail = input()
fail = 'lab+gb.png'

pygame.init()
size = width, height = 85 * 16, 50 * 16
screen = pygame.display.set_mode(size)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Program')
FPS = 1


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('imgs', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    fon = load_image('fon.jpg')
    screen.blit(pygame.transform.scale(fon, (width, height)), (0, 0))

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

class Darknes(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(darknes_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.lightrect = pygame.Rect((pos_x - 2 * tile_width, pos_y - 2 * tile_height, 5 * tile_width, 5 * tile_height))

    def update(self, x, y):
        global time
        if 0 <= self.rect.y + y < height and 0 <= self.rect.x + x < width and \
                level_map[(self.rect.y + y) // tile_height][(self.rect.x + x) // tile_width] in ('.', '@', ')', '('):
            self.rect = self.rect.move(x, y)
            # self.lightrect = pygame.Rect((x - 2 * tile_width, y - 2 * tile_height, 5 * tile_width, 5 * tile_height))
            self.lightrect = self.lightrect.move(x, y)
            if level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] == ')':
                time += 15
                remove_bonus()
                level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] = '.'
            elif level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] == '(':
                time -= 15
                remove_bonus()
                level_map[(self.rect.y) // tile_height][(self.rect.x) // tile_width] = '.'
            else:
                pass
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
# start_screen()

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

    return karta


# global level_map
# filename = "data/" + filename
# with open(filename, 'r') as mapFile:
#     level_map = [line.strip() for line in mapFile]
# max_width = max(map(len, level_map))
# return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def Show_timer(time):
    font = pygame.font.Font(None, 50)
    text = font.render(str(time), True, (255, 100, 100))
    text_x = width - 80
    text_y = 30
    screen.blit(text, (text_x, text_y))
    # pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
    #                                        text_w + 20, text_h + 20), 1)


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
            Darknes('dark', x, y)
    return new_player, x, y


level_map = load_level(fail)
player, level_x, level_y = generate_level(level_map)
run = True
win = False
time = 180
Show_timer(time)
pygame.time.set_timer(pygame.USEREVENT, 1000)
remove_dark()
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
        if key[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.USEREVENT:
            time -= 1
    clock.tick(50)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    darknes_group.draw(screen)
    player_group.draw(screen)
    Show_timer(time)
    pygame.display.flip()

terminate()
