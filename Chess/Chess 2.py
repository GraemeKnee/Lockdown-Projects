import pygame as py
import os

#global piece list
pieces = []

class piece:
    #x,y = position, c = colour
    def __init__(self,x=0,y=0,c=0):
        self.x = x
        self.y = y
        self.col = c
        self.moves = []
        self.update_moves(True)
        self.abs_path = os.path.dirname(__file__)
        self.sprite = py.image.load(os.path.join(self.abs_path,self.rel_path))

    def move(self,x,y):
        global pieces
        for q in pieces[::-1]:
            if (q.x,q.y) == (x,y):
                pieces.remove(q)
        self.x = x
        self.y = y
        self.update_moves(True)


class pawn(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_pawn.png")
        else:
            self.rel_path = os.path.join("sprite","black_pawn.png")
        super().__init__(x,y,c)


    #pawns need own move function to allow for promotion
    def move(self,x,y):
        global pieces
        for q in pieces[::-1]:
            if (q.x,q.y) == (x,y):
                pieces.remove(q)
        if (y == 7 and self.col == 0) or (y==0 and self.col == 1):
            pieces.remove(self)
            pieces.append(queen(x,y,self.col))
        self.x = x
        self.y = y

    def update_moves(self,first):
        global pieces
        if self.col == 0:
            (start,end,dir) = 1,7,1
        else:
            (start,end,dir) = 6,0,-1
        self.moves = [(self.x,self.y+dir)]
        if self.y == start:
            self.moves.append((self.x,self.y+2*dir))
        for q in pieces:
            if (q.x,q.y) == (self.x,self.y+dir):
                self.moves.remove((self.x,self.y+dir))
                if (q.x,q.y) == (self.x,self.y+2*dir) and (self.x,self.y+2*dir) in self.moves:
                    self.moves.remove((self.x,self.y+2*dir))
            elif (q.x,q.y) == (self.x+1,self.y+dir):
                self.moves.append((self.x+1,self.y+dir))
            elif (q.x,q.y) == (self.x-1,self.y+dir):
                self.moves.append((self.x-1,self.y+dir))


        if first:
            for z in self.moves:
                if check_move(self,z[0],z[1]):
                    self.moves.remove(z)


class knight(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_knight.png")
        else:
            self.rel_path = os.path.join("sprite","black_knight.png")
        super().__init__(x,y,c)
    def update_moves(self,first):
        self.moves = [(self.x-2,self.y+1),(self.x-1,self.y+2),(self.x+1,self.y+2),(self.x+2,self.y+1),(self.x+2,self.y-1),(self.x+1,self.y-2),(self.x-1,self.y-2),(self.x-2,self.y-1)]

        #remove if off the grid
        for q in self.moves[::-1]:
            if not (0<= q[0] < 8 and 0<= q[1] < 8):
                self.moves.remove(q)
            elif first:
                if check_move(self,q[0],q[1]):
                    self.moves.remove(q)




class bishop(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_bishop.png")
        else:
            self.rel_path = os.path.join("sprite","black_bishop.png")
        super().__init__(x,y,c)

    def update_moves(self,first):
        global pieces
        self.moves = []

        #generate all possible moves, 4 directions, no restrictions
        pos = [[(self.x+o*i,self.y+o*j) for o in range(1,8)] for i in [-1,1] for j in [-1,1]]
        #add directions to move until another piece is found or the edge of the board
        for dir in pos:
            end = False
            for m in dir:
                if not (0<= m[0] < 8 and 0<= m[1] < 8):
                    end = True
                else:
                    for q in pieces:
                        if (q.x,q.y) == m:
                            if q.col != self.col:
                                self.moves.append(m)
                            end = True
                            break
                if end:
                    break
                else:
                    if first:
                        if not check_move(self,m[0],m[1]):
                            self.moves.append(m)
                    else:
                        self.moves.append(m)

class rook(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_rook.png")
        else:
            self.rel_path = os.path.join("sprite","black_rook.png")
        super().__init__(x,y,c)

    def update_moves(self,first):
        global pieces
        self.moves = []
        #generate all possible moves, 4 directions, no restrictions
        pos = [[(self.x+o*i-o*i*j,self.y+o*i*j) for o in range(1,8)] for i in [-1,1] for j in [0,1]]
        #add directions to move until another piece is found or the edge of the board
        for dir in pos:
            end = False
            for m in dir:
                if not (0<= m[0] < 8 and 0<= m[1] < 8):
                    end = True
                else:
                    for q in pieces:
                        if (q.x,q.y) == m:
                            if q.col != self.col:
                                self.moves.append(m)
                            end = True
                            break
                if end:
                    break
                else:
                    if first:
                        if not check_move(self,m[0],m[1]):
                            self.moves.append(m)
                    else:
                        self.moves.append(m)

class queen(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_queen.png")
        else:
            self.rel_path = os.path.join("sprite","black_queen.png")
        super().__init__(x,y,c)

    def update_moves(self,first):
        global pieces
        self.moves = []
        #generate all possible moves, 8 directions, no restrictions
        pos = [[(self.x+o*i-o*i*j,self.y+o*i*j) for o in range(1,8)] for i in [-1,1] for j in [0,1]] + [[(self.x+o*i,self.y+o*j) for o in range(1,8)] for i in [-1,1] for j in [-1,1]]
        #add directions to move until another piece is found or the edge of the board
        for dir in pos:
            end = False
            for m in dir:
                if not (0<= m[0] < 8 and 0<= m[1] < 8):
                    end = True
                else:
                    for q in pieces:
                        if (q.x,q.y) == m:
                            if q.col != self.col:
                                self.moves.append(m)
                            end = True
                            break
                if end:
                    break
                else:
                    if first:
                        if not check_move(self,m[0],m[1]):
                            self.moves.append(m)
                    else:
                        self.moves.append(m)

class king(piece):
    def __init__(self,x=0,y=0,c=0):
        if c == 0:
            self.rel_path = os.path.join("sprite","white_king.png")
        else:
            self.rel_path = os.path.join("sprite","black_king.png")
        super().__init__(x,y,c)
    def update_moves(self,first):
        global pieces
        self.moves = [(self.x+o_x,self.y+o_y) for o_x in [-1,0,1] for o_y in [-1,0,1]]

        #remove if off the grid or ally piece or threatened by other
        for z in self.moves[::-1]:
            remove = False
            if not (0<= z[0] < 8 and 0<= z[1] < 8) :
                self.moves.remove(z)
                remove = True
            else:
                for q in pieces:
                    if q.col == self.col:
                        if (q.x,q.y) == z:
                            self.moves.remove(z)
                            remove = True
            if not remove and first:
                if check_move(self,z[0],z[1]):
                    self.moves.remove(z)



def inital_board():
    pawns = [pawn(x,1+c*5,c) for c in range(2) for x in range(8)]
    rooks = [rook(x*7,7*c,c) for c in range(2) for x in range(2)]
    knights = [knight(1+x*5,7*c,c) for c in range(2) for x in range(2)]
    bishops = [bishop(2+x*3,7*c,c) for c in range(2) for x in range(2)]
    queens = [queen(4,7*c,c) for c in range(2)]
    kings = [king(3,7*c,c) for c in range(2)]

    return [pawns+rooks+knights+bishops+queens+kings,0,-1,[]]


def check_check(colour):
    global pieces
    opp_moves = []
    k_pos = ()
    for q in pieces:
        if q.col != colour:
            opp_moves += q.moves
        elif isinstance(q,king):
            k_pos = (q.x,q.y)
    if k_pos in opp_moves:
        return True
    else:
        return False

def check_move(k, x,y):
    global pieces
    s_x = k.x
    s_y = k.y
    ind = -1
    for i in range(len(pieces))[::-1]:
        q = pieces[i]
        if (q.x,q.y) == (x,y):
            q.x =  -1
            q.y = -1
            ind = i
    k.x = x
    k.y = y
    for q in pieces:
        if q.col != k.col:
            q.update_moves(False)
    valid = check_check(k.col)
    k.x=s_x
    k.y=s_y
    if ind != -1:
        pieces[ind].x = x
        pieces[ind].y = y

    return valid


win_x = 1000
win_y = 1000

py.init()

win = py.display.set_mode((win_x,win_y))
py.display.set_caption("Chess")

run = True

clock = py.time.Clock()
FPS = 10


[pieces,player,HiLi,options] = inital_board()

for q in pieces:
    q.update_moves(True)



while run:
    clock.tick(FPS)

    #Event Manage
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        #Click detection
        elif event.type == py.MOUSEBUTTONDOWN:
            [MPosX,MPosY] = py.mouse.get_pos()
            M_x = MPosX// 100 - 1
            M_y = MPosY//100 - 1
            if 0<= M_x < 8 and 0<= M_y < 8:
                if HiLi == -1:
                    for i in range(len(pieces)):
                        q = pieces[i]
                        if q.x == M_x and q.y == M_y and q.col == player:
                            HiLi = i
                            pieces[i].update_moves(True)
                            options = pieces[i].moves
                elif (M_x,M_y) in options:
                    pieces[HiLi].move(M_x,M_y)
                    if player == 0:
                        player = 1
                    else:
                        player = 0
                    #pieces[HiLi].update_moves()
                    options = []
                    HiLi = -1
                else:
                    HiLi = -1
                    options = []
            else:
                HiLi = -1
                options = []
        elif event.type == py.KEYDOWN:
            if event.key == py.K_r:
                #reset board
                [pieces,player,HiLi,options] = inital_board()




    #Draw
    #board
    win.fill((255,255,255))
    py.draw.rect(win,(0,0,0),(90,90,820,820))
    for x in range(8):
        for y in range(8):
            if (x+y)%2 == 0:
                py.draw.rect(win,(255,255,200),(100+100*x,100+100*y,100,100))
            else:
                py.draw.rect(win,(100,100,100),(100+100*x,100+100*y,100,100))
    #Highlight
    if HiLi != -1:
        py.draw.rect(win,(100,200,100),(100+100*pieces[HiLi].x,100+100*pieces[HiLi].y,100,100))
    #Move options
    for q in options:
        py.draw.rect(win,(100,100,200),(105+100*q[0],105+100*q[1],90,90))

    #Pieces
    for q in pieces:
        if isinstance(q,king):
            if check_check(q.col):
                py.draw.rect(win,(200,100,100),(105+100*q.x,105+100*q.y,90,90))
        win.blit(q.sprite,(100+100*q.x,100+100*q.y))


    py.display.update()
