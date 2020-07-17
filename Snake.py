
import math
import random
import pygame as py

#Window size
win_x = 1000
win_y = 800


#Initalise and window
py.init()
win = py.display.set_mode((win_x,win_y))
py.display.set_caption("Snake")
run = True

#Clock
clock = py.time.Clock()
FPS = 10

#Create Grid
sqr_sz = 50
len_x = math.floor(win_x/sqr_sz)
len_y = math.floor(win_y/sqr_sz)

co_ord = [(x,y) for x in range(len_x) for y in range(len_y)]

#Inital Snake
snk = [(3,3),(2,3),(1,3)]
#snake direction: 0:up, 1:right, 2:down 3:left
sn_dir = 1

food = random.choice(co_ord)
while food in snk:
    food = random.choice(co_ord)
Game_over = False

font = py.font.Font(None,72)
g_o_text = font.render("YOU DIED", True, (180,0,0))


# Game loop'
while run:
    clock.tick(FPS)

    #Event Manage
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

        #Snake Direction
        if event.type == py.KEYDOWN:
            if Game_over:
                if event.key == py.K_r:
                    snk = [(3,3),(2,3),(1,3)]
                    sn_dir = 1
                    food = random.choice(co_ord)
                    while food in snk:
                        food = random.choice(co_ord)
                    Game_over = False
            else:
                if event.key == py.K_w:
                    if sn_dir != 2:
                        sn_dir = 0
                elif event.key == py.K_d:
                    if sn_dir != 3:
                        sn_dir = 1
                elif event.key == py.K_s:
                    if sn_dir != 0:
                        sn_dir = 2
                elif event.key == py.K_a:
                    if sn_dir != 1:
                        sn_dir = 3

    #Move snake
    #Get next square
    (h_x,h_y) = snk[0]
    if sn_dir == 0:
        nx = (h_x,h_y-1)
    elif sn_dir == 1:
        nx = (h_x+1,h_y)
    elif sn_dir == 2:
        nx = (h_x,h_y+1)
    else:
        nx = (h_x-1,h_y)
    #Check next square (in grid and not a snake // food)
    if nx in snk or not 0 <= nx[0] <= len_x-1 or not 0 <= nx[1] <= len_y-1:
        Game_over = True

    elif nx == food:
        snk = [nx] + snk
        while food in snk:
            food = random.choice(co_ord)

    #Move snake
    else:
        snk = [nx] + snk[:-1]

    win.fill((0,0,0))
    #Object Draw
    for (x,y) in snk:
        py.draw.rect(win,(255,0,0),(x*sqr_sz,y*sqr_sz,sqr_sz,sqr_sz))

    py.draw.rect(win,(0,255,0),(food[0]*sqr_sz,food[1]*sqr_sz,sqr_sz,sqr_sz))
    if Game_over:
        py.draw.rect(win,(50,50,50),(0,win_y/2-50,win_x,100))
        win.blit(g_o_text,(win_x/2-100,win_y/2-20))


    py.display.update()

quit()
