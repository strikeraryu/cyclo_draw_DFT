import turtle
import math
import time
import json

width = 800
height = 800
time = 0
line_col = 'white'
black = (0, 0, 0)
draw_col = "yellow"
thk = 2
drw_thk = 3

# to skip the points of the drawing (more points will increase the quality and time)
skip = 50
# magnification
mg = 1
# to move the background (i.e to draw the wave format)
move = False
# to visualize the circles
vis = False
if vis:
    skip *= 2

pen = turtle.Turtle()
pen.color('white')
pen.ht()
pen.up()
pen.speed(0)

screen = turtle.Screen()
screen.setup(width=width, height=height, startx=None, starty=None)
screen._bgcolor("black")
screen.tracer(0, 0)
screen.delay(0)

def close():
    global run
    run = False
    quit()

screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", close)


def draw_line(col, start, end, thk=1):
    pen.pensize(thk)
    pen.color(col.split())
    pen.setpos(start)
    pen.down()
    pen.setpos(end)
    pen.up()


def draw_shape_circle(col, centre, rad, thk):
    pen.pensize(thk)
    pen.color(col.split())
    pen.setpos(centre[0],centre[1]-rad)
    pen.down()
    pen.circle(rad)
    pen.up()


def draw_shape(col, crds, thk=1):
    pen.pensize(thk)
    pen.color(col)
    pen.setpos(crds[0])
    pen.down()
    for crd in crds:
        pen.setpos(crd)
    pen.up()


def DFT(points):
    circle_lst = []
    N = len(points)

    for k in range(N):
        a = 0
        b = 0
        for n in range(N):
            phi = 2*math.pi*k*n/N
            tmp_a = math.cos(phi)
            tmp_b = math.sin(phi)

            a += points[n][0]*tmp_a + points[n][1]*tmp_b
            b += -points[n][0]*tmp_b + points[n][1]*tmp_a

        a = a/N
        b = b/N
        rot = k
        rad = (a**2 + b**2)**0.5
        ang = math.atan2(b, a)
        circle_lst.append(circle_draw(rot, rad, ang))

    circle_lst.sort(key=lambda x: x.rad, reverse=True)
    return circle_lst


class circle_draw():
    def __init__(self, rot, rad, ang=0):
        self.ang = ang
        self.rad = rad
        self.rot = rot
        self.dir = 1
        self.x = 0
        self.y = 0

    def draw(self, x, y, flg=False):
        global draw_points
        self.x = (x+(math.cos(self.ang+time*self.rot)*self.rad))
        self.y = (y+(math.sin(self.ang+time*self.rot)*self.rad))
        if vis:
            try:
                draw_shape_circle("white", (x, y), self.rad, 0)
            except ValueError:
                pass
        draw_line(line_col, (x, y), (self.x, self.y), thk)
        if flg:
            if move:
                draw_line(line_col, (self.x, self.y), (200, self.y), thk)
                draw_points.append((200, self.y))
                if len(draw_points) > 300:
                    draw_points.pop(0)
            else:
                if (self.x,self.y) not in draw_points:
                    draw_points.append((self.x, self.y))


def redraw():
    global draw_points
    pen.clear()
    tmp_x, tmp_y = 0, 0

    for c in circle_lst:
        if circle_lst.index(c) == len(circle_lst)-1:
            c.draw(tmp_x, tmp_y, True)
        else:
            c.draw(tmp_x, tmp_y)
        tmp_x, tmp_y = c.x, c.y

    tmp_draw_points = []
    draw_shape(draw_col, tuple(draw_points), drw_thk)

    for crd in draw_points:
        tmp_draw_points.append((crd[0]+1, crd[1]))

    if move:
        draw_points = tmp_draw_points[:]
    screen.update()


run = True
draw_points = []
attr_lst = [(1, 100)]
with open('points.json', 'r') as f:
    file = json.load(f)
points = [(file["points"][x]['x']*mg, -file["points"][x]['y']*mg)
          for x in range(0, len(file["points"]), skip)]
#circle_lst = [circle_draw(x,y) for x,y in attr_lst]
circle_lst = DFT(points)
while run:
    time += 2*math.pi/len(points)
    redraw()
