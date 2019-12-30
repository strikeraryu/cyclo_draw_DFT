import turtle
import math
import json

width = 800
height = 800
line_col = "white"
draw_col = "yellow"
black = (0, 0, 0)
thk = 2
draw_thk = 3
skip = 75
time = 0
draw_pnts = False
vis = False
if vis:
    skip *= 2

pen = turtle.Turtle()
pen.color('white')
pen.ht()
pen.up()

screen = turtle.Screen()
screen.setup(width=width,height=height,startx=None,starty=None)
screen._bgcolor("black")
screen.tracer(False)

def close():
    global run
    run = False
    quit()

screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", close)

def draw_line(col,start,end,thk=1):
    pen.pensize(thk)
    pen.color(col.split())
    pen.setpos(start)
    pen.down()
    pen.setpos(end)
    pen.up()

def draw_shape_circle(col,centre,rad,thk):
    pen.pensize(thk)
    pen.color(col.split())
    pen.setpos(centre[0],centre[1]-rad)
    pen.down()
    pen.circle(rad)
    pen.up()

def draw_shape(col,crds,thk=1):
    pen.pensize(thk)
    pen.color(col)
    pen.setpos(crds[0])
    pen.down()
    for crd in crds:
        pen.setpos(crd)
    pen.up()



def DFT(points, flg=False):
    circle_lst = []
    N = len(points)

    for k in range(N):
        a = 0
        b = 0
        for n in range(N):
            phi = 2*math.pi*k*n/N
            a += points[n]*math.cos(phi)
            b -= points[n]*math.sin(phi)

        a = a/N
        b = b/N
        rot = k
        rad = (a**2 + b**2)**0.5
        ang = math.atan2(b, a)
        if flg:
            ang += 90
        circle_lst.append(circle_draw(rot, rad, ang))

    circle_lst.sort(key = lambda x: x.rad, reverse = True)
    return circle_lst


class circle_draw():
    def __init__(self, rot, rad, ang=0):
        self.ang = ang
        self.rad = rad
        self.rot = rot
        self.dir = 1
        self.x = 0
        self.y = 0

    def draw(self, x, y):
        self.x = (x+(math.cos(self.rot*time + self.ang)*self.rad))
        self.y = (y+(math.sin(self.rot*time  + self.ang)*self.rad))
        draw_line(line_col, (x, y), (self.x, self.y), thk)
        if vis:
            try:
                draw_shape_circle(line_col,((x),(y)),(self.rad),1)
            except ValueError:
                pass



def redraw():
    global draw_points
    pen.clear()

    tmp_x, tmp_y = 200,300
    for c in circle_lst_x:
        if circle_lst_x.index(c) == len(circle_lst_x)-1:
            c.draw(tmp_x, tmp_y)
            x_axis_x,x_axis_y = c.x,c.y
            draw_points_x.append(c.x)
        else:
            c.draw(tmp_x, tmp_y)
        tmp_x, tmp_y = c.x, c.y

    tmp_x, tmp_y = -300,-100
    for c in circle_lst_y:
        if circle_lst_y.index(c) == len(circle_lst_y)-1:
            c.draw(tmp_x, tmp_y)
            y_axis_x,y_axis_y = c.x,c.y
            draw_points_y.append(c.y)
        else:
            c.draw(tmp_x, tmp_y)
        tmp_x, tmp_y = c.x, c.y

    draw_points = [(x, y) for x, y in zip(draw_points_x, draw_points_y)]

    draw_shape( draw_col, tuple(draw_points), draw_thk)
    draw_line(line_col,(x_axis_x,x_axis_y),(draw_points_x[-1],draw_points_y[-1]),thk)
    draw_line(line_col,(y_axis_x,y_axis_y),(draw_points_x[-1],draw_points_y[-1]),thk)

    screen.update()


run = True
draw_points_x = []
draw_points_y = []
attr_lst = [(1, 100)]
with open('points.json', 'r') as f:
    file = json.load(f)
points_x = [file["points"][x]['x'] for x in range(0,len(file["points"]),skip)]
points_y = [-file["points"][x]['y'] for x in range(0,len(file["points"]),skip)]
# circle_lst = [circle_draw(x,y) for x,y in attr_lst]
# points_x = [math.cos(math.radians(x))*100 for  x in range(0,360,3)]
# points_y = [math.sin(math.radians(y))*100 for  y in range(0,360,3)]
circle_lst_x = DFT(points_x)
circle_lst_y = DFT(points_y, True)

while run:
    time += 2*math.pi/len(points_x)
    redraw()
quit()