import pygame
from pygame.draw import *
from random import randint
pygame.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

FPS = 60
time = 0
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
dx = [-3, -2, -1, 0, 1, 2, 3]
dy = dx
score = 0
balls = []
balls_num = 0
textsurface = myfont.render(str(score), False, (255, 255, 255))

def new_ball():
    chek = 0
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(50, 100)
    while chek != balls_num:
        chek = 0
        x = randint(100, 1100)
        y = randint(100, 900)
        r = randint(50, 100)
        for i in range(1,balls_num + 1):
            ro = ((balls[(i - 1) * 8] - x) ** 2 + (balls[(i - 1) * 8 + 1] - y) ** 2)**0.5
            if ro > r + balls[(i - 1) * 8 + 2]:
                chek += 1
    balls.append(x) #x
    balls.append(y) #y
    balls.append(r) #r
    balls.append(COLORS[randint(0, 5)]) #color
    balls.append(dx[randint(0, 6)])  #dx
    balls.append(dy[randint(0, 6)])  #dy
    balls.append(balls_num + 1)  #ball number
    balls.append(0)  #Time

def ball_death(num):
    for i in range(0, 8):
        balls.pop((num - 1) * 8)
    for i in range(1, balls_num):
        balls[(i - 1) * 8 + 6] = i

def ball_move(num):
    if balls[(num - 1) * 8] + balls[(num - 1) * 8 + 2] >= 1200 or balls[(num - 1) * 8] - balls[(num - 1) * 8 + 2] <= 0:
        balls[(num - 1) * 8 + 4] = -1 * balls[(num - 1) * 8 + 4]
    if balls[(num - 1) * 8 + 1] + balls[(num - 1) * 8 + 2] >= 900 or balls[(num - 1) * 8 + 1] - balls[(num - 1) * 8 + 2] <= 0:
        balls[(num - 1) * 8 + 5] = -1 * balls[(num - 1) * 8 + 5]
    for i in range(1, balls_num + 1):
        if i != num:
            ro = ((balls[(i - 1) * 8] - balls[(num - 1) * 8]) ** 2 + (balls[(i - 1) * 8 + 1] - balls[(num - 1) * 8 + 1]) ** 2)**0.5
            if ro <= balls[(num - 1) * 8 + 2] + balls[(i - 1) * 8 + 2]:
                balls[(num - 1) * 8 + 4] = dx[randint(0, 6)]
                balls[(num - 1) * 8 + 5] = dy[randint(0, 6)]
                balls[(i - 1) * 8 + 4] = dx[randint(0, 6)]
                balls[(i - 1) * 8 + 5] = dy[randint(0, 6)]
                chek = 0
                while chek != 1:
                    balls[(num - 1) * 8 + 4] = dx[randint(0, 6)]
                    balls[(num - 1) * 8 + 5] = dy[randint(0, 6)]
                    balls[(i - 1) * 8 + 4] = dx[randint(0, 6)]
                    balls[(i - 1) * 8 + 5] = dy[randint(0, 6)]
                    chek = 0
                    ro1 = ((balls[(i - 1) * 8] + balls[(i - 1) * 8 + 4] - balls[(num - 1) * 8] - balls[(num - 1) * 8 + 4]) ** 2 + (balls[(i - 1) * 8 + 1] + balls[(i - 1) * 8 + 5] - balls[(num - 1) * 8 + 1] - balls[(num - 1) * 8 + 5]) ** 2)**0.5
                    if ro1 > ro:
                        chek = 1
    balls[(num - 1) * 8] += balls[(num - 1) * 8 + 4]
    balls[(num - 1) * 8 + 1] += balls[(num - 1) * 8 + 5]
    balls[(num - 1) * 8 + 7] += 1
    circle(screen, balls[(num - 1) * 8 + 3], (balls[(num - 1) * 8], balls[(num - 1) * 8 + 1]), balls[(num - 1) * 8 + 2])

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(1, balls_num + 1):
                ro = ((balls[(i - 1) * 8] - event.pos[0]) ** 2 + (balls[(i - 1) * 8 + 1] - event.pos[1]) ** 2)**0.5
                if ro < balls[(i - 1) * 8 + 2]:
                    score += 1
                    ball_death(i)
                    balls_num -= 1
                    textsurface = myfont.render(str(score), False, (255, 255, 255))
                    break
    if time % 100 == 0:
        new_ball()
        balls_num += 1
    screen.fill(BLACK)
    for i in range(1, balls_num + 1):
        if balls[(i - 1) * 8 + 7] == 350:
            ball_death(i)
            balls_num -= 1
            break
    for i in range(1, balls_num + 1):
        ball_move(i)
    if time == 3000:
        finished = True
    screen.blit(textsurface,(100,100))
    pygame.display.update()    
    time += 1
pygame.quit()
player_name = input('inPut YouR Name*)')
file = open('records.txt', 'a')
file.write(player_name)
file.write(' : ')
file.write(str(score) + '\n')
print(score, 'попаданий в голову')
file.close()
