from random import randint
import pygame as pg
import sys

pg.time.set_timer(pg.USEREVENT, 3000)

W = 400
H = 400
WHITE = (255, 255, 255)
CARS = ('Sprites/ship24.bmp', 'Sprites/ship24.bmp', 'Sprites/ship24.bmp')
CARS_SURF = []

sc = pg.display.set_mode((W, H))

for i in range(len(CARS)):
    CARS_SURF.append(pg.image.load(CARS[i]).convert_alpha())


class Car(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))

        self.add(group)
        self.speed = randint(1, 3)

    def update(self):
        if self.rect.y < H:
            self.rect.y += self.speed
        else:
            self.kill()


cars = pg.sprite.Group()
Car(randint(1, W), CARS_SURF[randint(0, 2)], cars)

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.USEREVENT:
            Car(randint(1, W), CARS_SURF[randint(0, 2)], cars)

    sc.fill(WHITE)

    cars.draw(sc)

    pg.display.update()
    pg.time.delay(20)

    cars.update()