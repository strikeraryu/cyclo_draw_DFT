import pygame as pg
import json
import math

width = 800
height = 800
white = (255, 255, 255)
black = (0, 0, 0)

win = pg.display.set_mode((width, height))
pg.display.set_caption("cyclo draw")
clock = pg.time.Clock()

points = []
run = True
click = False
while run:
    for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pg.MOUSEBUTTONUP:
            click = False

    if click:
        points.append({'x': pos[0]-width/2, 'y':pos[1]-height/2})
        pg.draw.circle(win, white, pos, 1)

    pg.display.update()


with open("points.json", 'w') as f:
    tmp = {"points": points}
    json.dump(tmp, f)
quit()
