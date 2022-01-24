import os
import sys
import random
import pygame
import sqlite3
import database


def print_text(text, x, y):
    font_color = (255, 255, 255)
    font_type = pygame.font.SysFont('Consolas', 30)
    text2 = font_type.render(text, True, font_color)
    screen.blit(text2, (x, y))


class Button:
    def __init__(self, width, height, color1=(69, 22, 28), color2=(50, 10, 24)):
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2

    def draw(self, x, y, text, action=None, window=None, l=None):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        if x < pos[0] < x + self.width and y < pos[1] < y + self.height:
            pygame.draw.rect(screen, self.color2, (x, y, self.width, self.height))
            if pressed[0] == 1:
                if window is not None:
                    close_window = True
                if action is not None:
                    if l == 1:
                        action(1)
                    if l == 2:
                        action(2)
                    if l == 3:
                        action(3)
                    else:
                        action()
        else:
            pygame.draw.rect(screen, self.color1, (x, y, self.width, self.height))

        print_text(text, x + 10, y + 10)


def menu(a=None):
    menu = load_image('meanwhile.jpg')
    start_btn = Button(200, 50)
    exit_btn = Button(200, 50)
    running = True
    menu = pygame.transform.smoothscale(menu, screen.get_size())
    Pause = False
    vol = 1.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if event.type == pygame.QUIT:
                running = False
        screen.blit(menu, (0, 0))
        start_btn.draw(400, 20, 'Start game', choose_game)
        exit_btn.draw(400, 80, 'Exit game', exit)
        pygame.display.flip()


def results():
    background = pygame.image.load('beach.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    running = True
    res = database.get_all_results()
    back_to_menu_btn = Button(100, 50, (255, 127, 73), (255, 117, 56))
    vol = 1.0
    Pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if event.type == pygame.QUIT or close_window:
                running = False

        screen.blit(background, (0, 0))
        counter = 10
        back_to_menu_btn.draw(800, 500, 'Back', choose_game, True)
        for elem in res:
            text3 = f'your score: {elem[1]} (for level {elem[0]})'
            font = pygame.font.SysFont('Consolas', 20)
            screen.blit(font.render(text3, True, (0, 0, 0)), (10, counter))
            counter += 30
        pygame.display.flip()


def choose_game(a=None):
    global close_window
    close_window = False
    background = pygame.image.load('beach.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    running = True
    level1_btn = Button(150, 150, (119, 221, 119), (80, 200, 120))
    level2_btn = Button(150, 150, (119, 221, 119), (80, 200, 120))
    level3_btn = Button(150, 150, (119, 221, 119), (80, 200, 120))
    back_to_menu_btn = Button(200, 50, (255, 160, 0), (237, 145, 33))
    results_table = Button(240, 50, (255, 160, 0), (237, 145, 33))
    Pause = False
    vol = 1.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if event.type == pygame.QUIT or close_window:
                running = False
        screen.blit(background, (0, 0))
        level1_btn.draw(150, 300, 'Level 1', start_game, l=1)
        level2_btn.draw(400, 300, 'Level 2', start_game, l=2)
        level3_btn.draw(650, 300, 'Level 3', start_game, l=3)
        results_table.draw(360, 540, 'Results table', results)
        back_to_menu_btn.draw(380, 600, 'Go to menu', menu, True)
        pygame.display.update()


def play(level):
    global returning
    level = level

    class Cup(pygame.sprite.Sprite):
        image = load_image('cup.png')
        image = pygame.transform.scale(image, (40, 40))
        image = pygame.transform.flip(image, True, False)

        def __init__(self, group):
            super().__init__(group)
            self.cup_image = Cup.image
            self.rect = self.cup_image.get_rect()
            self.mask = pygame.mask.from_surface(self.cup_image)
            self.rect.x = 90
            self.rect.y = 530
            self.speedx = 0
            self.flag = 'left'

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_DOWN]:
                if self.flag == 'left':
                    Cup.image = pygame.transform.flip(Cup.image, True, False)
                    self.rect.x += 100
                    self.flag = 'right'
            if keystate[pygame.K_UP]:
                if self.flag == 'right':
                    Cup.image = pygame.transform.flip(Cup.image, True, False)
                    self.rect.x -= 100
                    self.flag = 'left'
            self.rect.x += self.speedx
            if self.rect.right > width - 140 and self.flag == 'left':
                self.rect.right = width - 140
            if self.rect.right > width - 40 and self.flag == 'right':
                self.rect.right = width - 40
            if self.rect.left < 40 and self.flag == 'left':
                self.rect.left = 40
            if self.rect.left < 140 and self.flag == 'right':
                self.rect.left = 140

    class Rednote(pygame.sprite.Sprite):
        image = load_image("rednote.png")
        image = pygame.transform.scale(image, (50, 50))

        def __init__(self, group, y):
            super().__init__(group)
            self.image = Rednote.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = random.randint(15, width - 15)
            self.rect.y = 0
            self.collide = False
            self.score = 0

        def update(self, *args, level):
            self.level = level
            if level == 1:
                self.rect = self.rect.move(0, 2)
            if level == 2:
                self.rect = self.rect.move(0, 3)
            if level == 3:
                self.rect = self.rect.move(0, 5)
            if self.rect.bottom > height:
                self.kill()
            if pygame.sprite.collide_mask(self, cup):
                self.collide = True
            else:
                self.collide = False
            if self.collide:
                Notes.catches += 15
                self.kill()

    class Gorillaz(pygame.sprite.Sprite):
        image = load_image('gorillaz.png')
        image = pygame.transform.scale(image, (220, 300))

        def __init__(self, group):
            super().__init__(group)
            self.guitar_image = Gorillaz.image
            self.rect = self.guitar_image.get_rect()
            self.mask = pygame.mask.from_surface(self.guitar_image)
            self.rect.x = 50
            self.rect.y = 450
            self.speedx = 0
            self.flag = 'left'

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_DOWN]:
                if self.flag == 'left':
                    Gorillaz.image = pygame.transform.flip(Gorillaz.image, True, False)
                    self.flag = 'right'
            if keystate[pygame.K_UP]:
                if self.flag == 'right':
                    Gorillaz.image = pygame.transform.flip(Gorillaz.image, True, False)
                    self.flag = 'left'
            self.rect.x += self.speedx
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.left < 0:
                self.rect.left = 0

    class Notes(pygame.sprite.Sprite):
        image = load_image("notes.png")
        image = pygame.transform.scale(image, (50, 50))
        image_boom = load_image("boom.png")
        image_boom = pygame.transform.scale(image_boom, (50, 50))
        catches = 0

        def __init__(self, group, y):
            super().__init__(group)
            self.image = Notes.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = random.randint(15, width - 15)
            self.rect.y = y
            self.collide = False
            self.score = 0
            self.bomb = False

        def update(self, *args, level):
            self.level = level
            if level == 1:
                self.rect = self.rect.move(0, 1)
            if level == 2:
                self.rect = self.rect.move(0, 2)
            if level == 3:
                self.rect = self.rect.move(0, 3)
            if self.rect.bottom > height:
                self.kill()
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image = self.image_boom
                self.bomb = True
            if pygame.sprite.collide_mask(self, cup):
                self.collide = True
            else:
                self.collide = False
            if self.collide and self.bomb:
                Notes.catches += 10
                self.kill()
            if self.collide:
                Notes.catches += 1
                self.kill()

    all_sprites = pygame.sprite.Group()
    notes = pygame.sprite.Group()
    one_sprite = pygame.sprite.Group()
    background = pygame.image.load('beach.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    gorillaz = Gorillaz(one_sprite)
    cup = Cup(one_sprite)
    for _ in range(20):
        m = Notes(all_sprites, random.randrange(height))
        notes.add(m)
    running = True
    fps = 60
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    font = pygame.font.SysFont("Consolas", 20)
    time = 20
    t = random.randrange(time)
    vol = 1.0
    Pause = False
    GamePause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_p and not GamePause:
                    GamePause = True

                elif event.key == pygame.K_p and GamePause:
                    GamePause = False
                elif event.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not GamePause:
                    for bomb in all_sprites:
                        all_sprites.update(event, level=level)
            if event.type == MYEVENTTYPE:
                if not GamePause:
                    m = Notes(all_sprites, 0)
                    notes.add(m)
                    time -= 1
            if time == t:
                rednote = Rednote(all_sprites, 0)
            if time == 0:
                game_over(level)
                running = False
        if not GamePause:
            one_sprite.update()
        screen.blit(background, (0, 0))
        clock.tick(fps)
        all_sprites.draw(screen)
        one_sprite.draw(screen)
        if not GamePause:
            all_sprites.update(level=level)
        if GamePause:
            text3 = f'press "p" to continue'
            font = pygame.font.SysFont('Consolas', 80)
            screen.blit(font.render(text3, True, (0, 0, 0)), (50, 300))
        text = f'score:{str(Notes.catches)}'
        text2 = f'time:{str(time)}'
        text3 = f'ur best score: {database.get_result(level)}'
        font = pygame.font.SysFont('Consolas', 20)
        screen.blit(font.render(text3, True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(text2, True, (0, 0, 0)), (900, 30))
        screen.blit(font.render(text, True, (0, 0, 0)), (900, 10))
        returning = Notes.catches
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_game(level):
    background = pygame.image.load('beach.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    global counter, text
    counter, text = 10, '10'.center(16)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 100)
    skip_btn = Button(100, 50, (255, 63, 5), (209, 49, 0))
    flPause = False
    vol = 1.0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif e.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif e.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if e.type == pygame.USEREVENT:
                counter -= 1
                if counter > 0:
                    text = str(counter).center(17)
                elif counter == 0:
                    text = "GO".center(16)
                else:
                    break
            if e.type == pygame.QUIT:
                break
        else:
            screen.blit(background, (0, 0))
            skip_btn.draw(450, 500, 'Skip', play, True, l=level)
            screen.blit(font.render(text, True, (0, 0, 0)), (25, 48))
            pygame.display.flip()
            clock.tick(60)
            continue
        break
    play(level)


def game_over(level):
    level = level
    end = load_image('gameover.jpg')
    running = True
    close_window = False
    end = pygame.transform.smoothscale(end, screen.get_size())
    gotomenu_btn = Button(200, 50)
    score = returning
    database.insert_into(level, returning)
    vol = 1.0
    Pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_MINUS:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_PLUS:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
            if event.type == pygame.QUIT or close_window:
                running = False
        screen.blit(end, (0, 0))
        gotomenu_btn.draw(400, 500, 'Exit', menu, True)

        font = pygame.font.SysFont('Consolas', 100)
        screen.blit(font.render(str(score), True, (0, 0, 0)), (660, 300))
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("{x}.mp3".format(x=random.randint(0, 6)))
    pygame.mixer.music.play()
    for i in range(7):
        pygame.mixer.music.queue("{i}.mp3".format(i=i))
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)
    clock = pygame.time.Clock()
    pygame.display.flip()
    menu()
    pygame.quit()
