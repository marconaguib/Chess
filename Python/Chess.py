import numpy as np
from random import randint

lettres=['A','B','C','D','E','F','G','H']
dic_lettres={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8}

type2num={'T':1,'C':2,'F':3,'R':4,'D':5,'P':6}
num2type=['T','C','F','R','D','P']


columns=["a8","b8","c8","d8","e8","f8","g8","h8",
        "a7","b7","c7","d7","e7","f7","g7","h7",
        "a6","b6","c6","d6","e6","f6","g6","h6",
        "a5","b5","c5","d5","e5","f5","g5","h5",
        "a4","b4","c4","d4","e4","f4","g4","h4",
        "a3","b3","c3","d3","e3","f3","g3","h3",
        "a2","b2","c2","d2","e2","f2","g2","h2",
        "a1","b1","c1","d1","e1","f1","g1","h1"]

class Piece():
    def __init__(self, type,coul,x,y):
        self.coul=coul
        self.type = type
        self.x=x
        self.y=y
        self.pioch=0
        if coul=='N':
            self.numtype= type2num[type]
        else:
            self.numtype= -1*type2num[type]
    def move(self,nx,ny):
        self.x=nx
        self.y=ny
        self.nom_position = lettres[self.y]+str(self.x+1)
    def piocher(self):
        self.pioch=1
    def depiocher(self):
        self.pioch=0
    def promouvoir(self):
        self.type='D'
        if self.coul=='N':
            self.numtype=5
        else:
            self.numtype=-5
    def depromouvoir(self):
        self.type='P'
        if self.coul=='N':
            self.numtype=6
        else:
            self.numtype=-6

def piece_occupante(liste,nx,ny):
    for p,i in enumerate(liste):
        if i.pioch==0 and (i.x,i.y)==(nx,ny):
            return(p)
    return(-1)

class Game():        
    def __init__(self,cases=[[1,2,3,4,5,3,2,1],[6]*8,[0]*8,[0]*8,[0]*8,[0]*8,[-6]*8,[-1,-2,-3,-4,-5,-3,-2,-1]]):
        self.cases=cases
        self.pieces=[]
        for i in range(8):
            for j in range(8):
                val = self.cases[i][j]
                if val==0:
                    continue
                c = 'B' if (val<0) else 'N'
                self.pieces.append(Piece(num2type[abs(val)-1],c,i,j))
        self.white = 1
        
    def swap(self):
        self.white = 1-self.white

    def print_board(self):
        print(str(np.asarray(self.cases)).replace('0','.').replace('-1',' t').replace('-2',' c').replace('-3',' f').replace('-4',' r').replace('-5',' d').replace('-6',' p').replace('1','T').replace('2','C').replace('3','F').replace('4','R').replace('5','D').replace('6','P'))
        print('\n')
    
    def piece_occupante2(self,nx,ny):
        if nx>=0 and nx<=7 and ny>=0 and ny<=7:
            return(self.cases[nx][ny])
        else:
            return 0

    def get_reasonable_moves(self,x,y):
        moves=[]
        type=num2type[abs(self.cases[x][y])-1]
        type,coul=num2type[abs(self.cases[x][y])-1],'N' if self.cases[x][y]>0 else 'B'
        if type=='R':
            if x>0:
                moves.extend([(x,y,x-1,y-1),(x,y,x-1,y),(x,y,x-1,y+1)])
            if x<7:
                moves.extend([(x,y,x+1,y-1),(x,y,x+1,y),(x,y,x+1,y+1)])
            moves.extend([(x,y,x,y-1),(x,y,x,y+1)])
        elif type=='C':
            moves.extend([(x,y,x-2,y-1),(x,y,x-1,y-2),(x,y,x-2,y+1),(x,y,x-1,y+2),(x,y,x+1,y-2),(x,y,x+2,y-1),(x,y,x+1,y+2),(x,y,x+2,y+1)])
        elif type=='P':
            w=1 if coul=='B' else 0
            moves.extend([(x,y,x+(-1)**w,y),(x,y,x+(-1)**w,y-1),(x,y,x+(-1)**w,y+1)])
            if x==1 or x==6:
                moves.append((x,y,x+2*(-1)**w,y))
        if type=='F' or type=='D':
            for mon_zip in [zip([x]*8,[y]*8,range(x+1,8),range(y+1,8)),zip([x]*8,[y]*8,range(x+1,8),range(y-1,-1,-1)),zip([x]*8,[y]*8,range(x-1,-1,-1),range(y+1,8)),zip([x]*8,[y]*8,range(x-1,-1,-1),range(y-1,-1,-1))]:
                moves.extend(mon_zip)
        if type=='T' or type=='D':
            for mon_zip in [zip([x]*8,[y]*8,range(x-1,-1,-1),[y]*abs(x)),zip([x]*8,[y]*8,range(x+1,8),[y]*np.abs(8-x)),zip([x]*8,[y]*8,[x]*abs(y),range(y-1,-1,-1)),zip([x]*8,[y]*8,[x]*np.abs(8-y),range(y+1,8))]:
                moves.extend(mon_zip)
        return moves

    def get_all_reasonable_moves(self):
        moves=[]
        for x in range(8):
            for y in range(8):
                piece=self.cases[x][y]
                if piece==0:
                    continue
                if (piece<0) == (self.white) :
                    moves.extend(self.get_reasonable_moves(x,y))
        return moves
        
    def checkcheck(self):
        lui=(-1)**(1-self.white)
        mon_roi=-4*lui
        for i in range(8):
            for j in range(8):
                if self.cases[i][j]==mon_roi:
                    x,y=i,j
                    break
            else:
                continue
            break
        if self.piece_occupante2(x+(-1)**self.white,y-1)==6*lui or self.piece_occupante2(x+(-1)**self.white,y+1)==6*lui:
                return True
        for (cx,cy) in [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]:
            if self.piece_occupante2(cx,cy)==4*lui:
                return True
        for (cx,cy) in [(x-2,y-1),(x-1,y-2),(x-2,y+1),(x-1,y+2),(x+1,y-2),(x+2,y-1),(x+1,y+2),(x+2,y+1)]:
            if self.piece_occupante2(cx,cy)==2*lui:
                return True
        for mon_zip in [zip(range(x+1,8),range(y+1,8)),zip(range(x+1,8),range(y-1,-1,-1)),zip(range(x-1,-1,-1),range(y+1,8)),zip(range(x-1,-1,-1),range(y-1,-1,-1))]:
            for(cx,cy) in mon_zip:
                if self.piece_occupante2(cx,cy)==3*lui or self.piece_occupante2(cx,cy)==5*lui:
                    return True
                elif self.piece_occupante2(cx,cy)!=0:
                    break
        for mon_zip in [zip(range(x-1,-1,-1),[y]*abs(x)),zip(range(x+1,8),[y]*np.abs(8-x)),zip([x]*abs(y),range(y-1,-1,-1)),zip([x]*np.abs(8-y),range(y+1,8))]:
            for(cx,cy) in mon_zip:
                if self.piece_occupante2(cx,cy)==1*lui or self.piece_occupante2(cx,cy)==5*lui:
                    return True
                elif self.piece_occupante2(cx,cy)!=0:
                    break
        return False

    def piocher_piece(self,ind_p):
        self.pieces[ind_p].piocher()

    def depiocher_piece(self,ind_p,nx,ny):
        self.pieces[ind_p].depiocher()
        self.cases[nx][ny]=self.pieces[ind_p].numtype

    def promouvoir_piece(self,pp,nx,ny):
        self.pieces[pp].promouvoir()
        self.cases[nx][ny]= 5 if self.pieces[pp].coul=='N' else -5

    def depromouvoir_piece(self,pp,x,y):
        self.pieces[pp].depromouvoir()
        self.cases[x][y]= 6 if self.pieces[pp].coul=='N' else -6

    def canmove(self,x,y,nx,ny):
        if (self.cases[x][y]==0):
            return (False,-1,False)
        type,coul=num2type[abs(self.cases[x][y])-1],'N' if self.cases[x][y]>0 else 'B'
        lui=(-1)**(1-self.white)
        ind_p=-1
        if nx<0 or nx>7 or ny<0 or ny>7:
            return (False,-1,False)
        if (self.white and self.piece_occupante2(nx,ny)<0) or (not self.white and self.piece_occupante2(nx,ny)>0):
            return (False,-1,False)
        if type=='P':
            if coul=='N':
                if nx<=x or abs(ny-y)>1 or (nx-x>2 and x==1) or (nx-x>1 and x>1):
                    return (False,-1,False)
                if ny==y:
                    if self.piece_occupante2(nx,ny)<0:
                        return (False,-1,False)
                    if (nx-x==2 and self.piece_occupante2(x+1,ny)!=0):
                        return (False,-1,False)
                else:
                    ### change pas
                    ind_p=piece_occupante(self.pieces,nx,ny)
                    if ind_p==-1 or nx-x==2:
                        return (False,-1,False)
                    self.piocher_piece(ind_p)
            else:
                if nx>=x or abs(ny-y)>1 or (x-nx>2 and x==6) or (x-nx>1 and x<6):
                    return (False,-1,False)
                if ny==y :
                    if self.piece_occupante2(nx,ny)>0:
                        return (False,-1,False)
                    if (x-nx==2 and self.piece_occupante2(x-1,ny)!=0):
                        return (False,-1,False)
                else:
                    ind_p=piece_occupante(self.pieces,nx,ny)
                    if ind_p==-1 or x-nx==2:
                        return (False,-1,False)
                    self.piocher_piece(ind_p)
        else:
            if type=='C':
                if np.abs(nx-x)+np.abs(ny-y) != 3 or nx==x or ny==y:
                    return (False,-1,False)
            else:
                if type=='R':
                    if (np.abs(nx-x)>1 or np.abs(ny-y)>1):
                        return (False,-1,False)
                if type=='F':
                    if abs(nx - x) != abs(ny -y):
                        return (False,-1,False)
                if type=='T':
                    if nx!=x and ny!=y:
                        return (False,-1,False)
                if type=='D':
                    if (abs(nx - x) != abs(ny -y)) and nx!=x and ny!=y:
                        return (False,-1,False)
                #rien sur le chemin
                if nx>x:
                    range_x=range(x,nx,1)
                elif nx<x:
                    range_x=range(x,nx,-1)
                else:
                    range_x=[x]*abs(ny-y)
                if ny>y:
                    range_y=range(y,ny,1)
                elif ny<y:
                    range_y=range(y,ny,-1)
                else:
                    range_y=[y]*abs(nx-x)
                for (i,j) in zip(range_x,range_y):
                    if((i,j)==(x,y)):
                        continue
                    if self.piece_occupante2(i,j)!=0:
                        return (False,-1,False)
            #piocher
            ind_p=piece_occupante(self.pieces,nx,ny)
            if ind_p!=-1:
                self.piocher_piece(ind_p)
        self.cases[nx][ny]=self.cases[x][y]
        self.cases[x][y]=0
        seraitcheck=0
        if(self.checkcheck()):
            seraitcheck=1
        self.cases[x][y]=self.cases[nx][ny]
        self.cases[nx][ny]=0
        if ind_p != -1:
            self.depiocher_piece(ind_p,nx,ny)
        if seraitcheck:
            return (False,-1,False)
        pion_promu=False
        if type=='P' and (nx==7 or nx==0):
            pion_promu=True
        return (True,ind_p,pion_promu)


    def checkmate(self):
        for (x,y,nx,ny) in self.get_all_reasonable_moves():
            if(self.canmove(x,y,nx,ny)[0]):
                return False
        return True

    def move(self,x,y,nx,ny):
        camarche,ind_p,pp = self.canmove(x,y,nx,ny)
        if camarche:
            p=piece_occupante(self.pieces,x,y)
            self.pieces[p].move(nx,ny)
            if ind_p !=-1:
                self.piocher_piece(ind_p)
            self.cases[nx][ny]=self.cases[x][y]
            self.cases[x][y]=0
            if pp:
                self.promouvoir_piece(p,nx,ny)
            self.swap()
            return True
        else:
            return False

    def scoreklayer(self,x,y,nx1,ny1,k):
        can,ind_p,pp=self.canmove(x,y,nx1,ny1)
        
        type,coul=num2type[abs(self.cases[x][y])-1],'N' if self.cases[x][y]>0 else 'B'
        score=0

        if pp:
            score+=100

        if ind_p != -1:
            type_p=self.pieces[ind_p].type
            dic_recompense={'P':10, 'C':40, 'F':35, 'T':50,'D':90}
            score+= dic_recompense[type_p]

        assert(self.move(x,y,nx1,ny1))
        check = self.checkcheck()
        mate=self.checkmate()
        if check:
            score+=5
        if mate and check:
            score+=10**10
        score*=k

        if k!=1 and not mate:
            his_best_move=(-1,-1,-1)
            his_best_score=-np.Inf
            for(x2,y2,nx2,ny2) in self.get_all_reasonable_moves():
                if self.canmove(x2,y2,nx2,ny2)[0]:
                    ce_score=self.scoreklayer(x2,y2,nx2,ny2,k-1)
                    if ce_score > his_best_score:
                        his_best_score = ce_score
                        his_best_move=(x2,y2,nx2,ny2)
                    if ce_score>=10**10:
                        break
            score-=his_best_score
        #undoing
        self.swap()
        p1=piece_occupante(self.pieces,nx1,ny1)
        piece=self.pieces[p1]
        self.pieces[p1].move(x,y)
        self.cases[nx1][ny1]=0
        self.cases[x][y]=self.pieces[p1].numtype
        if ind_p != -1:
            self.depiocher_piece(ind_p,nx1,ny1)
        if pp:
            self.depromouvoir_piece(p1,x,y)
        #switch back
        return score


    def makeamove(self,level):
        if self.checkmate():
            if self.checkcheck():
                if self.white :
                    print("Checkmate, black wins.")
                else:
                    print("Checkmate, white wins.")
                return False
            if self.white :
                print("Draw, white cannot move.")
            else:
                print("Draw, black cannot move.")
            return False
        score=-np.Inf
        p_dec,nx_dec,ny_dec=-1,-1,-1
        for x,y,nx,ny in self.get_all_reasonable_moves():
            if self.canmove(x,y,nx,ny)[0]:
                ce_score=self.scoreklayer(x,y,nx,ny,level)
                if ce_score>score or (ce_score==score and randint(0,6)==0):
                     score=ce_score
                     x_dec,y_dec,nx_dec,ny_dec=x,y,nx,ny
        assert(self.move(x_dec,y_dec,nx_dec,ny_dec))
        assert(score>-np.Inf)
        return(True)

cases=[[0,0,0,4,0,0,0,0],[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*7+[-6],[0,0,0,-4,0,0,0,0]]
# cases = [[0,0,0,4,0,0,-6,1],[0]*8,[0]*8,[5,0,0,0,0,0,0,0],[0]*8,[0]*8,[0]*8,[0,0,0,-4,0,0,0,0]]
newgame=Game()
still_can_play = True
while still_can_play:
    newgame.print_board()
    still_can_play = newgame.makeamove(2)
    if not still_can_play:
        break
    newgame.print_board()
    still_can_play = newgame.makeamove(1)
    
