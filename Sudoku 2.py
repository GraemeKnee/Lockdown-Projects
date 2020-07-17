
# coding: utf-8

# # Sudoku Solver/Generator
# ## Graeme Knee
# ## graemeknee@gmail.com
#

# In[1]:


import numpy as np
import random
import copy
import time
import pygame as py


# In[2]:


class grid:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
        self.squares_in = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
        self.squares_main = []
        self.main_update()
        self.solution = 0

    def generate_test_fail(self):
        self.squares = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for x in range(0,9)]

    def generate_test_pass(self):
        self.squares = [[4, 3, 5, 2, 6, 9, 7, 8, 1],[6, 8, 2, 5, 7, 1, 4, 9, 3],[1, 9, 7, 8, 3, 4, 5, 6, 2],[8, 2, 6, 1, 9, 5, 3, 4, 7],[3, 7, 4, 6, 8, 2, 9, 1, 5],[9, 5, 1, 7, 4, 3, 6, 2, 8],[5, 1, 9, 3, 2, 6, 8, 7, 4],[2,4,8,9,5,7,1,3,6],[7,6,3,4,1,8,2,5,9]]

    def generate_preset(self):
        self.squares = [[0,0,0,2,6,0,7,0,1],[6,8,0,0,7,0,0,9,0],[1,9,0,0,0,4,5,0,0],[8,2,0,1,0,0,0,4,0],[0,0,4,6,0,2,9,0,0],[0,5,0,0,0,3,0,2,8],[0,0,9,3,0,0,0,7,4],[0,4,0,0,5,0,0,3,6],[7,0,3,0,1,8,0,0,0]]
        self.main_update()

    def generate_seq(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
        print("Generating")
        self.solve()
        self.main_update()


    def generate_rand(self):
        N= 50
        self.squares_main = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
        print("Generating")
        self.squares_update_m()
        self.solve_rand()
        while sum(x.count(0) for x in self.squares) > 0:
            self.solve_rand()
        self.main_update()
        print("Generated, Removing")
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        random.shuffle(co_ord)
        i = 0
        while i < N:
            (x_i,y_i) = (co_ord[0][0],co_ord[0][1])
            temp = self.squares_main[y_i][x_i]
            self.squares_main[y_i][x_i] = 0
            if self.solve_count() != 1:
                self.squares_main[y_i][x_i] = temp
                random.shuffle(co_ord)
            else:
                co_ord.remove((x_i,y_i))
                i += 1

        print("Done")

    def main_update(self):
        self.squares_main = copy.deepcopy(self.squares)

    def squares_update_m(self):
        self.squares = copy.deepcopy(self.squares_main)

    def squares_update_combo(self):
        self.squares = copy.deepcopy(self.squares_main)
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        for (x,y) in co_ord:
            if self.squares_in[y][x] != 0:
                self.squares[y][x] = self.squares_in[y][x]

    def solve_out(self):
        self.squares_update_combo()
        self.solve()
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        for (x,y) in co_ord:
            if self.squares_main[y][x] != 0:
                self.squares[y][x] = 0
        return self.squares


    def solve(self):
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        self.solve_action(co_ord[1:],co_ord[0][0],co_ord[0][1])

    def solve_action(self,co_ord,x,y):
        if self.squares_main[y][x] != 0:
            if len(co_ord) == 0:
                return True
            else:
                return self.solve_action(co_ord[1:],co_ord[0][0],co_ord[0][1])
        else:
            vals = self.find_values(x,y)
            while vals != []:
                q = vals[0]
                self.squares[y][x] = q
                if len(co_ord) == 0:
                    return True
                else:
                    if self.solve_action(co_ord[1:],co_ord[0][0],co_ord[0][1]):
                        return True
                vals.remove(q)

            self.squares[y][x] = 0
            return False

    def solve_count(self):
        self.squares_update_m()
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        self.solutions = 0
        self.solve_action_count(co_ord[1:],co_ord[0][0],co_ord[0][1])
        return self.solutions

    def solve_action_count(self,co_ord,x,y):
        if self.squares[y][x] != 0:
            if len(co_ord) == 0:
                self.solutions += 1
            else:
                self.solve_action_count(co_ord[1:],co_ord[0][0],co_ord[0][1])
        else:
            vals = self.find_values(x,y)
            while vals != []:
                q = vals[0]
                self.squares[y][x] = q
                if len(co_ord) == 0:
                    self.solutions += 1
                else:
                    self.solve_action_count(co_ord[1:],co_ord[0][0],co_ord[0][1])
                vals.remove(q)
            self.squares[y][x] = 0
        return False

    def solve_rand(self):
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        self.solve_action_rand(co_ord[1:],co_ord[0][0],co_ord[0][1])

    def solve_action_rand(self,co_ord,x,y):
        if self.squares_main[y][x] != 0:
            if len(co_ord) == 0:
                return True
            else:
                return self.solve_action(co_ord[1:],co_ord[0][0],co_ord[0][1])
        else:
            vals = self.find_values(x,y)
            random.shuffle(vals)
            while vals != []:
                q = vals[0]
                self.squares[y][x] = q
                if len(co_ord) == 0:
                    return True
                else:
                    if self.solve_action_rand(co_ord[1:],co_ord[0][0],co_ord[0][1]):
                        return True
                vals.remove(q)
            self.squares[y][x] = 0
            return False



    def print_grid(self):
        for y in range(0,9):
            for x in range(0,9):
                print(self.squares_main[y][x],end='')
                if x != 8:
                    print(' ',end='')
                else:
                    print('')

    def output_grid(self):
        return self.squares_main

    def check_state(self,x,y):
        #x -= 1
        #y -= 1
        check_var = self.squares[y][x]

        if check_var == 0:
            return False

        else:
            check_row = list(self.squares[y])
            check_row.pop(x)
            check_column = list([q[x] for q in self.squares])
            check_column.pop(y)

            #identify square to check
            sq_x = (x//3)*3
            sq_y = (y//3)*3

            check_square = [self.squares[q][sq_x:sq_x+3] for q in range(sq_y,sq_y+3)]
            check_square[y-sq_y].pop(x-sq_x)
            check_square = [item for sub in check_square for item in sub]

            return not ((check_var in check_row) or (check_var in check_column) or (check_var in check_square))

    def check_state_val(self,x,y,q):
        temp = self.squares[y][x]
        self.squares[y][x] = q
        rtn = self.check_state(x,y)
        self.squares[y][x] = temp
        return rtn

    def find_values(self,x,y):
        poss_val = []
        for q in range(1,10):
            if self.check_state_val(x,y,q):
                poss_val.append(q)
        return poss_val

    def val_in(self,x,y,q):
        self.squares_in[y][x] = q
        return self.squares_in

    def check_in(self):
        self.squares_update_combo()
        co_ord = [(x, y) for x in range(9) for y in range(9)]
        in_states = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9)]

        for (x,y) in co_ord:
            in_states[y][x] = int(self.check_state(x,y))







    #def update(self, x,y,value):

#Sudoku Logic setup
MainGrid = grid()

NumList = MainGrid.output_grid()

InNumList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]

SolList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]

run = True

py.init()

clock = py.time.Clock()
FPS = 60

#SquareSize
SqrSz = 80

#Grid Display Size (GDS)
GDS = SqrSz*9

win = py.display.set_mode((GDS+200,GDS+200))

py.display.set_caption("Sudoku")

#Initalise Highlight
HiLi = [-1,-1]

#Render text Numbers
font = py.font.Font(None,SqrSz)
NumText = [font.render(str(i+1),1,(0,0,0)) for i in range(9)]
InText = [font.render(str(i+1),1,(0,0,255)) for i in range(9)]
SolText = [font.render(str(i+1),1,(0,100,0)) for i in range(9)]

while run:
    clock.tick(FPS)

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        #click detection
        elif event.type == py.MOUSEBUTTONDOWN:
            [MPosX,MPosY] = py.mouse.get_pos()
            MPosX -= 100
            MPosY -= 100
            if 0 < MPosX < GDS and 0 < MPosY < GDS:
                #If square already highlighted, deselect
                if HiLi == [MPosX//SqrSz, MPosY//SqrSz] or NumList[MPosY//SqrSz][MPosX//SqrSz] != 0:
                    HiLi = [-1,-1]
                #determine square clicked on to be highlighted "HiLi"
                else:
                    HiLi = [MPosX//SqrSz, MPosY//SqrSz]
            else:
                HiLi = [-1,-1]

        elif event.type == py.KEYDOWN:
            if event.key == py.K_r:
                InNumList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
                SolList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
                MainGrid.generate_rand()
                NumList = MainGrid.output_grid()
            elif event.key == py.K_c:
                #clear user inputs
                InNumList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
                SolList = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(0,9)]
            elif event.key == py.K_s:
                print("solve")
                SolList = MainGrid.solve_out()
            elif HiLi != [-1,-1]:
                Q = -1
                if event.key == py.K_1 or event.key == py.K_KP1:
                    Q = 1
                elif event.key == py.K_2 or event.key == py.K_KP2:
                    Q = 2
                elif event.key == py.K_3 or event.key == py.K_KP3:
                    Q = 3
                elif event.key == py.K_4 or event.key == py.K_KP4:
                    Q = 4
                elif event.key == py.K_5 or event.key == py.K_KP5:
                    Q = 5
                elif event.key == py.K_6 or event.key == py.K_KP6:
                    Q = 6
                elif event.key == py.K_7 or event.key == py.K_KP7:
                    Q = 7
                elif event.key == py.K_8 or event.key == py.K_KP8:
                    Q = 8
                elif event.key == py.K_9 or event.key == py.K_KP9:
                    Q = 9
                elif event.key == py.K_0 or event.key == py.K_KP0 or event.key == py.K_BACKSPACE or event.key == py.K_DELETE:
                    Q = 0
                if Q != -1:
                    InNumList = MainGrid.val_in(HiLi[0],HiLi[1],Q)





    #white Background
    win.fill((255,255,255))

    #Draw Square Highlight
    if HiLi != [-1,-1]:
        py.draw.rect(win, (200,100,100),(100+HiLi[0]*SqrSz,100+HiLi[1]*SqrSz,SqrSz,SqrSz))
    #Draw grid lines
    #Thick
    for i in range(4):
        #Horizontal
        py.draw.rect(win, (0,0,0),(100+i*GDS/3,100,5,GDS))
        #Vertical
        py.draw.rect(win, (0,0,0),(100,100+i*GDS/3,GDS,5))
    #Thin
    for i in range(10):
        if i not in (0,3,6,9):
            #Horizontal
            py.draw.rect(win, (0,0,0),(100+i*GDS/9,100,2,GDS))
            #Vertical
            py.draw.rect(win, (0,0,0),(100,100+i*GDS/9,GDS,2))

    #Draw Numbers
    for y in range(9):
        for x in range(9):
            Q = NumList[y][x]
            if Q != 0:
                win.blit(NumText[Q-1],(100+SqrSz*(x+.35),100+SqrSz*(y+.2)))
    #Draw Input Numbers
    for y in range(9):
        for x in range(9):
            Q = InNumList[y][x]
            if Q != 0:
                win.blit(InText[Q-1],(100+SqrSz*(x+.35),100+SqrSz*(y+.2)))
    #Draw Solution Numbers
    for y in range(9):
        for x in range(9):
            if InNumList[y][x] == 0:
                Q = SolList[y][x]
                if Q != 0:
                    win.blit(SolText[Q-1],(100+SqrSz*(x+.35),100+SqrSz*(y+.2)))





    py.display.update()

quit()





# In[3]:


#Create sudoku grid object
#MainGrid = grid()
#Generate a new random sudoku layout
#MainGrid.generate_rand()
#Print out the grid
#MainGrid.print_grid()
#print()

#Show how many solutions the grid has (check that it is one)
#MainGrid.solve_count()
#print(MainGrid.solution)
#Solve the grid
#MainGrid.solve()
#print the solution
#MainGrid.print_grid()
