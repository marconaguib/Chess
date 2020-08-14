import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri,pandas2ri
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import operator
import time
import csv
from random import randint

N=0

lettres=['A','B','C','D','E','F','G','H']
dic_lettres={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8}

type2num={'T':1,'C':2,'F':3,'R':4,'D':5,'P':6}

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
    def afficher(self):
        if(not self.pioch):
            a= plt.imread('C:\\Users\\Nicolas Martin\\chess\\icons\\{}_{}.png'.format(self.coul,self.type))
            plt.imshow(a,extent=(self.y-0.5,self.y+0.5,self.x-0.5,self.x+0.5))
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
    def piece_occupante2(self,nx,ny):
        if nx>=0 and nx<=7 and ny>=0 and ny<=7:
            return(self.cases[nx][ny])
        else:
            return 0
    def __init__(self):
        self.selection=-1
        self.pieces=[]
        pieces=[]
        for c in ['N','B']:
            if c=='N':
                ligne=0
            else:
                ligne=7
            pieces.append(Piece('T',c,ligne,0))
            pieces.append(Piece('C',c,ligne,1))
            pieces.append(Piece('F',c,ligne,2))
            pieces.append(Piece('R',c,ligne,3))
            pieces.append(Piece('D',c,ligne,4))
            pieces.append(Piece('F',c,ligne,5))
            pieces.append(Piece('C',c,ligne,6))
            pieces.append(Piece('T',c,ligne,7))
            for i in range(8):
                if c=='N':
                    ligne=1
                else:
                    ligne=6
                pieces.append(Piece('P',c,ligne,i))
        self.white = 0
        self.pieces=pieces
        self.cases=[[1,2,3,4,5,3,2,1],[6]*8,[0]*8,[0]*8,[0]*8,[0]*8,[-6]*8,[-1,-2,-3,-4,-5,-3,-2,-1]]
        #marco
        # for i in range(len(pieces)):
        #     if i!=3 and i!=4 and i!=0 and i!=19 and i!=17:
        #         pieces[i].pioch=1
        # self.pieces[17].move(0,6)
        # self.pieces[4].move(3,0)
        # self.pieces[0].move(0,7)
        # self.cases=[[0,0,0,4,0,0,-6,1],[0,0,0,0,0,0,0,0],[0]*8,[5,0,0,0,0,0,0,0,0],[0]*8,[0]*8,[0]*8,[0,0,0,-4,0,0,0,0]]

    def swap(self):
        self.white = 1-self.white

    def board(self):
        res=[]
        for i in np.flip(np.array(newgame.cases),0):
            res.extend(i)
        res.append((-1)**self.white)
        return res

    def get_reasonable_moves(self,p):
        moves=[]
        piece=self.pieces[self.white*16+p%16]
        type,x,y,coul=piece.type,piece.x,piece.y,piece.coul
        if type=='R':
            if x>0:
                moves.extend([(p,x-1,y-1),(p,x-1,y),(p,x-1,y+1)])
            if x<7:
                moves.extend([(p,x+1,y-1),(p,x+1,y),(p,x+1,y+1)])
            moves.extend([(p,x,y-1),(p,x,y+1)])
        elif type=='C':
            moves.extend([(p,x-2,y-1),(p,x-1,y-2),(p,x-2,y+1),(p,x-1,y+2),(p,x+1,y-2),(p,x+2,y-1),(p,x+1,y+2),(p,x+2,y+1)])
        elif type=='P':
            w=self.white
            moves.extend([(p,x+(-1)**w,y),(p,x+(-1)**w,y-1),(p,x+(-1)**w,y+1)])
            if x==1 or x==6:
                moves.append((p,x+2*(-1)**w,y))
        if type=='F' or type=='D':
            for mon_zip in [zip([p]*8,range(x+1,8),range(y+1,8)),zip([p]*8,range(x+1,8),range(y-1,-1,-1)),zip([p]*8,range(x-1,-1,-1),range(y+1,8)),zip([p]*8,range(x-1,-1,-1),range(y-1,-1,-1))]:
                moves.extend(mon_zip)
        if type=='T' or type=='D':
            for mon_zip in [zip([p]*8,range(x-1,-1,-1),[y]*abs(x)),zip([p]*8,range(x+1,8),[y]*np.abs(8-x)),zip([p]*8,[x]*abs(y),range(y-1,-1,-1)),zip([p]*8,[x]*np.abs(8-y),range(y+1,8))]:
                moves.extend(mon_zip)
        return moves

    def get_all_reasonable_moves(self):
        moves=[]
        for p in range(16):
            piece=self.pieces[self.white*16+p%16]
            if (piece.pioch):
                continue
            moves.extend(self.get_reasonable_moves(p))
        return moves

    def checkcheck2(self):
        mes_pieces=self.pieces[16*self.white:16*(self.white+1)]
        x,y = mes_pieces[3].x,mes_pieces[3].y
        lui=(-1)**(1-self.white)
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
        self.cases[nx][ny]=self.pieces[pp].numtype

    def depromouvoir_piece(self,pp,x,y):
        self.pieces[pp].depromouvoir()
        self.cases[x][y]=self.pieces[pp].numtype

    def canmove2(self,p,nx,ny):
        lui=(-1)**(1-self.white)
        ind_p=-1
        if nx<0 or nx>7 or ny<0 or ny>7:
            return (False,-1,False)
        if (self.white and self.piece_occupante2(nx,ny)<0) or (not self.white and self.piece_occupante2(nx,ny)>0):
            return (False,-1,False)
        piece=self.pieces[self.white*16+p%16]
        if (piece.pioch):
            return (False,-1,False)
        type,x,y,coul=piece.type,piece.x,piece.y,piece.coul
        if type=='P':
            if coul=='N':
                if nx<=x or abs(ny-y)>1 or (nx-x>2 and x==1) or (nx-x>1 and x>1):
                    return (False,-1,False)
                if ny==y:
                    if (self.white and self.piece_occupante2(nx,ny)>0) or (not self.white and self.piece_occupante2(nx,ny)<0):
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
                    if (self.white and self.piece_occupante2(nx,ny)>0) or (not self.white and self.piece_occupante2(nx,ny)<0):
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
        self.pieces[self.white*16+p%16].move(nx,ny)
        self.cases[nx][ny]=self.pieces[self.white*16+p%16].numtype
        self.cases[x][y]=0
        seraitcheck=0
        if(self.checkcheck2()):
            seraitcheck=1
        self.pieces[self.white*16+p%16].move(x,y)
        self.cases[nx][ny]=0
        self.cases[x][y]=self.pieces[self.white*16+p%16].numtype
        if ind_p != -1:
            self.depiocher_piece(ind_p,nx,ny)
        if seraitcheck:
            return (False,-1,False)
        pion_promu=False
        if self.pieces[p].type=='P' and (nx==7 or nx==0):
            pion_promu=True
        return (True,ind_p,pion_promu)


    def checkmate(self):
        for (p,nx,ny) in self.get_all_reasonable_moves():
            if(self.canmove2(p,nx,ny)[0]):
                return False
        return True

    def move(self,p,nx,ny):
        camarche,ind_p,pp = self.canmove2(p,nx,ny)
        if camarche:
            x,y=self.pieces[self.white*16+p%16].x,self.pieces[self.white*16+p%16].y
            self.pieces[self.white*16+p%16].move(nx,ny)
            if ind_p !=-1:
                self.piocher_piece(ind_p)
            if pp:
                self.promouvoir_piece(self.white*16+p%16,nx,ny)
            self.cases[nx][ny]=self.pieces[self.white*16+p%16].numtype
            self.cases[x][y]=0
            self.swap()
            return True
        else:
            return False

    def scoreklayer(self,p1,nx1,ny1,k):
        global N
        can,ind_p,pp=self.canmove2(p1,nx1,ny1)

        piece=self.pieces[self.white*16+p1%16]
        type,x,y,coul=piece.type,piece.x,piece.y,piece.coul
        score=0

        if pp:
            score+=100

        if ind_p != -1:
            type_p=self.pieces[ind_p].type
            dic_recompense={'P':10, 'C':40, 'F':35, 'T':50,'D':90}
            score+= dic_recompense[type_p]

        #switch
        assert(self.move(p1,nx1,ny1))
        check = self.checkcheck2()
        mate=self.checkmate()
        if check:
            score+=5
        if mate and check:
            score+=10**10
        score*=k

        if k==1:
            N+=1

        if k!=1 and not mate:
            his_best_move=(-1,-1,-1)
            his_best_score=-np.Inf
            entered=False
            for(p2,nx2,ny2) in self.get_all_reasonable_moves():
                if self.canmove2(p2,nx2,ny2)[0]:
                    entered=True
                    ce_score=self.scoreklayer(p2,nx2,ny2,k-1)
                    if ce_score > his_best_score:
                        his_best_score = ce_score
                        his_best_move=(p2,nx2,ny2)
                    if ce_score>=10**10:
                        break
            assert(entered)
            score-=his_best_score
        #undoing
        self.swap()
        self.pieces[self.white*16+p1%16].move(x,y)
        self.cases[nx1][ny1]=0
        self.cases[x][y]=self.pieces[self.white*16+p1%16].numtype
        if ind_p != -1:
            self.depiocher_piece(ind_p,nx1,ny1)
        if pp:
            self.depromouvoir_piece(self.white*16+p1%16,x,y)
        #switch back
        return score

    def afficher(self,onclick,fig,ax):
        thismanager = plt.get_current_fig_manager()
        thismanager.window.wm_iconbitmap("C:\\Users\\Nicolas Martin\\chess\\icons\\unnamed.ico")
        thismanager.window.title("Chess")
        check=self.checkcheck2()
        mate=self.checkmate()
        self.piecsel=0
        col = np.zeros((8,8))
        col[1::2,0::2]=1
        col[0::2,1::2]=1

        ax.set_aspect('equal')
        ax.set_xlim(-0.5, 7.5)
        ax.set_ylim(-0.5, 7.5)
        names=[]
        for i in range(8):
            names.append([lettres[i]]*8)
            for j in range(8):
             names[i][j]+=str(j+1)
        plt.imshow(col)
        for p in self.pieces:
            p.afficher()
        for i in range(8):
            for j in range(8):
                plt.text(i,j,names[i][j],color='black' if (i+j)%2 else 'white',alpha=0.2)
        plt.title(("White, " if self.white else "Black, ")+("Check" if check else "")+("mate!" if mate else ""))
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        if mate:
            if check:
                print(("Black" if self.white else "White")+" wins")
            else:
                print("Draw!")
        axquit = plt.axes([0.85, 0.05, 0.1, 0.075])
        bquit = Button(axquit, 'Quit')
        axres = plt.axes([0.85, 0.15, 0.1, 0.075])
        bquit = Button(axres, 'Restart')
        plt.show()
        fig.canvas.mpl_disconnect(cid)

    def letmeplay(self):
        fig,ax = plt.subplots(1)
        quitter=[]
        rejouer=[]
        def onclick(event):
            POS=(round(event.ydata), round(event.xdata))
            if piece_occupante(self.pieces[16*self.white:16*(self.white+1)],POS[0],POS[1])!=-1:
                    self.selection=piece_occupante(self.pieces,POS[0],POS[1])
                    self.piecsel=1
                    moves=self.get_reasonable_moves(self.selection)
            if self.piecsel:
                if(self.move(self.selection,int(POS[0]),int(POS[1]))):
                    plt.close()
                    self.piecesel=0
            if event.x>546 and event.x<608 and event.y >24 and event.y<58:
                quitter.append(1)
                plt.close()
            if event.x>546 and event.x<608 and event.y >73 and event.y<105:
                rejouer.append(1)
                plt.close()
        self.afficher(onclick,fig,ax)
        return (quitter,rejouer)

    def makeamove(self,mode):
        if self.checkmate():
            self.letmeplay()
            return
        if mode=='random':
            start = time.time()
            score=-np.Inf
            p_dec,nx_dec,ny_dec=-1,-1,-1
            for i in range(10000):
                p,nx,ny=randint(0,15),randint(0,7),randint(0,7)
                if self.score(p,nx,ny) > score:
                    score= self.score(p,nx,ny)
                    p_dec,nx_dec,ny_dec=p,nx,ny
            assert(self.move(p_dec,nx_dec,ny_dec))
            assert(score>-np.Inf)
            print(round(time.time() - start,3))
            return((p_dec,nx_dec,ny_dec))
        if mode=='amateur':
            score=-np.Inf
            p_dec,nx_dec,ny_dec=-1,-1,-1
            start = time.time()
            for p,nx,ny in self.get_all_reasonable_moves():
                if self.canmove2(p,nx,ny)[0]:
                    ce_score=self.scoreklayer(p,nx,ny,2)
                    if ce_score>score or (ce_score==score and randint(0,8)==4):
                         score=ce_score
                         p_dec,nx_dec,ny_dec=p,nx,ny
            assert(self.move(p_dec,nx_dec,ny_dec))
            assert(score>-np.Inf)
            return(p_dec,nx_dec,ny_dec)
        if mode=='professional':
            r = robjects.r
            numpy2ri.activate()
            pandas2ri.activate()
            state=self.board()
            f = open('state.csv', 'w')
            with f:
                writer = csv.writer(f)
                writer.writerow(state)
            f.close()
            r.source("C:\\Users\\Nicolas Martin\\chess\\predictor.R")
            f = open('response.csv', 'r')
            liste =f.readline().replace('"','').split(',')
            f.close()
            nx,ny = (7 - columns.index(liste[1])//8,columns.index(liste[1])%8)
            pieces_possibles=[]
            for x in range(8):
                for y in range(8):
                    if (abs(self.piece_occupante2(x,y))==int(liste[0])):
                        cette_piece = piece_occupante(self.pieces[16*self.white:16*(self.white+1)],x,y)
                        if self.canmove2(cette_piece,nx,ny)[0] and cette_piece!= -1:
                            pieces_possibles.append(cette_piece)
            if (len(pieces_possibles)==1):
                assert(newgame.move(pieces_possibles[0],nx,ny))
                return(pieces_possibles[0],nx,ny)
            elif(len(pieces_possibles)>1):
                score=-np.Inf
                for p in pieces_possibles:
                    ce_score=self.scoreklayer(p,nx,ny,2)
                    if ce_score>score or (ce_score==score and randint(0,8)==4):
                         score,p_dec=ce_score,p
                assert(newgame.move(p_dec,nx,ny))
                return(p_dec,nx,ny)
            else:
                #print("model failed.")
                return(self.makeamove('amateur'))

    def play(self,mode):
        while not self.checkmate():
            (quitter,rejouer)=self.letmeplay()
            if len(quitter)!=0:
                return False
            elif len(rejouer)!=0:
                self.__init__()
            if mode!='multi' and not self.checkmate():
                self.makeamove(mode)
                continue
        if self.checkmate():
            (quitter,rejouer)=self.letmeplay()
            if len(quitter)!=0:
                return False
            elif len(rejouer)!=0:
                return True
    def youplay(self):
        while not self.checkmate():
            print("black",self.makeamove('amateur'))
            if self.checkmate():
                break
            print("white",self.makeamove('professional'))
        self.letmeplay()

# replay=True
# while replay:
#     newgame=Game()
#     replay= newgame.play('professional')

newgame = Game()
newgame.youplay()
