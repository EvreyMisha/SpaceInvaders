import pygame
import pygame_menu
import random
import sys


class Bullet(pygame.sprite.Sprite):
    def __init__(self, xy, im, group):
        pygame.sprite.Sprite.__init__(self)
        random.choice(lasersound).play()
        self.xy = xy
        self.im = im
        self.add(group)
        self.rect = pygame.Rect(*xy, 5, 50)

    def move(self):
        speed = 10
        self.xy[1] -= speed
        self.rect = pygame.Rect(*self.xy, 5, 39)

    def render(self):
        win.blit(self.im, self.xy)

    def delete(self):
        if pygame.sprite.spritecollideany(self, rects):
            self.kill()
        if self.xy[1] < 0:
            self.kill()

    def update(self):
        self.delete()
        self.move()
        self.render()


class EnemyBullet(Bullet):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        random.choice(lasersound).play()
        self.xy = xy
        self.im = red_bullet[0]
        self.im.set_colorkey((0, 0, 0))
        self.add(enemy_bullets)
        self.rect = pygame.Rect(*xy, 5, 50)

    def move(self):
        speed = 10
        self.xy[1] += speed
        self.rect = pygame.Rect(*self.xy, 5, 39)

    def delete(self):
        if pygame.sprite.spritecollideany(self, ships):
            if player.shield > 0:
                player.shield -= 5
            else:
                player.hp -= 5
            self.kill()
        if self.xy[1] > 700:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 50
        self.max_shield = 50
        self.hp = 50
        self.frags = 0

        self.level = 0
        self.x = 0
        self.y = 600
        self.kd = 5
        self.shipSp = pygame.image.load('Sprites/ship24.bmp')  # 88 / 68
        self.ship_rect = self.shipSp.get_rect(bottomright=(100, 700))
        self.rect = self.shipSp.get_rect()
        self.shipSp.set_colorkey((0, 0, 0))
        player_bullet.set_colorkey((0, 0, 0))
        self.add(group)
        self.text = pygame.font.Font(None, 36)
        self.text_surface = self.text.render('Hello Привет', True, (180, 0, 0))

    def move(self):
        keys = pygame.key.get_pressed()
        move = ((keys[pygame.K_LEFT] or keys[pygame.K_a]), (keys[pygame.K_RIGHT] or keys[pygame.K_d]),
                (keys[pygame.K_UP] or keys[pygame.K_w]), (keys[pygame.K_DOWN] or keys[pygame.K_s]))

        if move[0] and self.x > 0:
            self.x -= 5
        if move[1] and self.x < 1000 - 88:
            self.x += 5
        if move[2]:
            self.y -= 5
        if move[3]:
            self.y += 5

        self.rect = pygame.Rect(self.x - 20, self.y, 88, 68)

        if keys[pygame.K_SPACE] and self.kd == 0:
            if self.level == 0:
                Bullet([self.x + 22, self.y], player_bullet, bullets)
            elif self.level == 1:
                Bullet([self.x - 5, self.y], player_bullet, bullets)
                Bullet([self.x + 50, self.y], player_bullet, bullets)
            elif self.level == 2:
                Bullet([self.x - 5, self.y], player_bullet, bullets)
                Bullet([self.x + 50, self.y], player_bullet, bullets)
                Bullet([self.x - 10, self.y], player_bullet, bullets)
                Bullet([self.x + 55, self.y], player_bullet, bullets)
            self.kd = 10
        if self.kd:
            self.kd -= 1

    def render(self):
        win.blit(self.shipSp, (self.x, self.y))
        pygame.draw.rect(win, (50, 255, 255), (0, 0, int(self.shield) * 5, 20))
        pygame.draw.rect(win, (190, 0, 0), (0, 20, self.hp * 5, 20))
        win.blit(self.text_surface, (50, 150))

    def upgrade(self):
        if self.frags == 10:
            self.level = 1
        elif self.frags == 20:
            self.level = 2

    def update(self):
        self.text_surface = self.text.render(str(self.frags), True, (180, 0, 0))
        if self.shield < self.max_shield:
            self.shield += 0.01
        self.move()
        self.render()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        r = random.randint(0, 2)
        self.enemySp = pygame.transform.scale(enemy_sprites[r],  (90, 70))
        self.enemySp_hit = pygame.transform.scale(enemy_sprites_hit[r],  (90, 70))
        self.enemySp.set_colorkey((0, 0, 0))
        self.enemySp_hit.set_colorkey((0, 0, 0))

        self.rect = self.enemySp.get_rect()
        self.is_hit = 0

        self.add(group)
        self.color = (0, 0, 0)
        self.hp = 10
        self.target = [random.randint(0, 1000), random.randint(0, 400)]

    def move_to_target(self):
        if self.x < self.target[0]:
            self.x += 1
        elif self.x > self.target[1]:
            self.x -= 1

        if self.y < self.target[1]:
            self.y += 1
        elif self.y > self.target[1]:
            self.y -= 1

        self.rect = pygame.Rect(self.x - 10, self.y, 100, 50)
        if self.x == self.target[0] and self.y == self.target[1]:
            self.target = [random.randint(0, 1000), random.randint(0, 400)]

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets):
            self.is_hit = 5
            self.color = (255, 255, 0)
            self.hp -= 1
            if self.hp < 0:
                self.kill()
                player.frags += 1
                player.upgrade()

        if not random.randint(0, 100):
            EnemyBullet([self.x + 20, self.y + 30])

        #Рисовка врагов
        if self.is_hit:
            win.blit(self.enemySp_hit, (self.x, self.y))
            self.is_hit -= 1
        else:
            win.blit(self.enemySp, (self.x, self.y))
        self.move_to_target()


pygame.init()
win = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Space")


player_bullet = pygame.image.load('Sprites/bullet.bmp')  # 88 / 68
red_bullet = [pygame.image.load('Sprites/red_bullet.bmp')]
enemy_sprites = [pygame.image.load('Sprites/enemy/' + str(i) + '.bmp') for i in range(1, 4)]
enemy_sprites_hit = [pygame.image.load('Sprites/enemy/' + str(i) + 'hit.bmp') for i in range(1, 4)]

lasersound = []
for i in range(5):
    lasersound.append(pygame.mixer.Sound('Sounds/laserSmall_00' + str(i) + '.ogg'))
    lasersound[i].set_volume(0.01)

obj = []
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
ships = pygame.sprite.Group()
player = Player(ships)

rects = pygame.sprite.Group()
Alien(100, 100, rects)
Alien(200, 200, rects)
Alien(300, 300, rects)


def gameloop():
    run = True
    while run:
        pygame.time.delay(10)

        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                sys.exit()
        if not run:
            break
        win.fill((0, 0, 0))
        if not random.randint(-50,50):
            Alien(300, 300, rects)
        ships.update()
        rects.update()
        bullets.update()
        enemy_bullets.update()
        pygame.display.update()


class Menu:
    def __init__(self):
        menu = pygame_menu.Menu(300, 400, 'Welcome', theme=pygame_menu.themes.THEME_DARK)
        menu.add_text_input('Name :', default='John Doe')
        menu.add_button('Play', gameloop)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu = menu
        menu.mainloop(win)
        pygame.quit()

    def set_difficulty(Difficulty):
        print(Difficulty)

Menu()