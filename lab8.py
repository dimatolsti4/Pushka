from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

g = 2

k = 0.8 # eating coefficiention

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 75

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.vy += g

        if self.x + self.vx + self.r > 800 or self.x + self.vx < self.r:
            self.vx *= -(1 - k)**0.5
            self.vy *= (1 - k)**0.5
        if self.y + self.vy + self.r > 600 or self.y + self.vy < self.r:
            self.vy *= -(1 - k)**0.5
            self.vx *= (1 - k)**0.5
        
        self.x += self.vx
        self.y += self.vy

        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def hittest(self, obj):
        if dist(self, obj) <= self.r + obj.r:
            return True
        return False
    def death(self):
        self.live -= 1

class gun():
    def __init__(self):
        self.f2_power = 5
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        
        global balls, bullet

        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan2((event.y-new_ball.y) , (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
                self.an = math.atan2((event.y-450), (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.vx = 0
        self.vy = 0
        
        self.points = 0
        self.live = 1

        self.id = canv.create_oval(0,0,0,0)
        self.id_points = canv.create_text(30,30,text = self.points,font = '28')
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(550, 740)
        y = self.y = rnd(50, 350)
        r = self.r = rnd(2, 50)

        self.vx = rnd(1, 3)
        self.vy = rnd(1, 3)
        
        color = self.color
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def move(self):
        if self.x + self.vx + self.r > 800 or self.x + self.vx < self.r + 400:
            self.vx *= -1
        if self.y + self.vy + self.r > 400 or self.y + self.vy < self.r:
            self.vy *= -1
            
        self.x += self.vx
        self.y += self.vy
        self.r = rnd(2, 50)
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)


def dist(o1, o2):
    return ((o1.x - o2.x) ** 2 + (o1.y - o2.y) ** 2) ** 0.5

screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []

def new_game(event=''):
    targets = [target(), target()]
    global gun, screen1, balls, bullet

    for t in targets:
        t.new_target()
        t.live = 1

    bullet = 0
    balls = []

    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03

    while targets or balls:
        for t in targets:
            t.move()
        
        for b in balls:
            b.move()
            b.death()
            if b.live == 0:
                balls.remove(b)
                canv.delete(b.id)
            for t in targets:
                
                if b.hittest(t):
                    t.live = 0
                    t.hit()
                    targets.remove(t)
        
        if not targets:
            canv.bind('<Button-1>', '')
            canv.bind('<ButtonRelease-1>', '')
            canv.itemconfig(screen1, text='Вы попали VGOLOVU за ' + str(bullet) + ' выстрелов')

        canv.update()

        time.sleep(0.03)

        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)

new_game()
