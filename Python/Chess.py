import numpy as np
from random import randint

class Game():        
    def __init__(self,white=1,cases=[[1,2,3,4,5,3,2,1],[6]*8,[0]*8,[0]*8,[0]*8,[0]*8,[-6]*8,[-1,-2,-3,-4,-5,-3,-2,-1]]):
        self.cases=cases
        for i in range(8):
            for j in range(8):
                val = self.cases[i][j]
                if val==0:
                    continue
                c = 'B' if (val<0) else 'N'
        self.white = white
        self.rois=[(0,3),(7,3)]
    
    def track_rois(self,x,y):
        if(self.cases[x][y]==4):
            self.rois[0]=x,y
        if(self.cases[x][y]==-4):
            self.rois[1]=x,y
        
    def swap(self):
        self.white = 1-self.white

    def print_board(self):
        print(str(np.asarray(self.cases)).replace('0','.').replace('-1',' t').replace('-2',' c').replace('-3',' f').replace('-4',' r').replace('-5',' d').replace('-6',' p').replace('1','T').replace('2','C').replace('3','F').replace('4','R').replace('5','D').replace('6','P'))
        print('\n')
    
    def piece_occupante(self,nx,ny):
        if nx>=0 and nx<=7 and ny>=0 and ny<=7:
            return(self.cases[nx][ny])
        else:
            return 0

    def get_reasonable_moves(self,x,y):
        moves=[]
        type,coul=abs(self.cases[x][y]),'N' if self.cases[x][y]>0 else 'B'
        if type==4:
            if x>0:
                moves.extend([(x,y,x-1,y-1),(x,y,x-1,y),(x,y,x-1,y+1)])
            if x<7:
                moves.extend([(x,y,x+1,y-1),(x,y,x+1,y),(x,y,x+1,y+1)])
            moves.extend([(x,y,x,y-1),(x,y,x,y+1)])
        elif type==2:
            moves.extend([(x,y,x-2,y-1),(x,y,x-1,y-2),(x,y,x-2,y+1),(x,y,x-1,y+2),(x,y,x+1,y-2),(x,y,x+2,y-1),(x,y,x+1,y+2),(x,y,x+2,y+1)])
        elif type==6:
            w=1 if coul=='B' else 0
            moves.extend([(x,y,x+(-1)**w,y),(x,y,x+(-1)**w,y-1),(x,y,x+(-1)**w,y+1)])
            if x==1 or x==6:
                moves.append((x,y,x+2*(-1)**w,y))
        if type==3 or type==5:
            for mon_zip in [zip([x]*8,[y]*8,range(x+1,8),range(y+1,8)),zip([x]*8,[y]*8,range(x+1,8),range(y-1,-1,-1)),zip([x]*8,[y]*8,range(x-1,-1,-1),range(y+1,8)),zip([x]*8,[y]*8,range(x-1,-1,-1),range(y-1,-1,-1))]:
                moves.extend(mon_zip)
        if type==1 or type==5:
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
        x,y=self.rois[self.white]
        if self.piece_occupante(x+(-1)**self.white,y-1)==6*lui or self.piece_occupante(x+(-1)**self.white,y+1)==6*lui:
                return True
        for (cx,cy) in [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]:
            if self.piece_occupante(cx,cy)==4*lui:
                return True
        for (cx,cy) in [(x-2,y-1),(x-1,y-2),(x-2,y+1),(x-1,y+2),(x+1,y-2),(x+2,y-1),(x+1,y+2),(x+2,y+1)]:
            if self.piece_occupante(cx,cy)==2*lui:
                return True
        for mon_zip in [zip(range(x+1,8),range(y+1,8)),zip(range(x+1,8),range(y-1,-1,-1)),zip(range(x-1,-1,-1),range(y+1,8)),zip(range(x-1,-1,-1),range(y-1,-1,-1))]:
            for(cx,cy) in mon_zip:
                if self.piece_occupante(cx,cy)==3*lui or self.piece_occupante(cx,cy)==5*lui:
                    return True
                elif self.piece_occupante(cx,cy)!=0:
                    break
        for mon_zip in [zip(range(x-1,-1,-1),[y]*abs(x)),zip(range(x+1,8),[y]*np.abs(8-x)),zip([x]*abs(y),range(y-1,-1,-1)),zip([x]*np.abs(8-y),range(y+1,8))]:
            for(cx,cy) in mon_zip:
                if self.piece_occupante(cx,cy)==1*lui or self.piece_occupante(cx,cy)==5*lui:
                    return True
                elif self.piece_occupante(cx,cy)!=0:
                    break
        return False

    def canmove(self,x,y,nx,ny):
        if (nx<0 or nx>7 or ny<0 or ny>7 or self.cases[x][y]==0 or self.cases[x][y]*self.cases[nx][ny]>0):
            return False
        type,coul=abs(self.cases[x][y]),'N' if self.cases[x][y]>0 else 'B'
        lui=(-1)**(1-self.white)
        type_pioche=0
        if type==6:
            if coul=='N':
                if nx<=x or abs(ny-y)>1 or (nx-x>2 and x==1) or (nx-x>1 and x>1):
                    return False
                if ny==y:
                    if self.piece_occupante(nx,ny)<0:
                        return False
                    if (nx-x==2 and self.piece_occupante(x+1,ny)!=0):
                        return False
                else:
                    type_pioche=self.piece_occupante(nx,ny)
                    if type_pioche==0 or nx-x==2:
                        return False
            else:
                if nx>=x or abs(ny-y)>1 or (x-nx>2 and x==6) or (x-nx>1 and x<6):
                    return False
                if ny==y :
                    if self.piece_occupante(nx,ny)>0:
                        return False
                    if (x-nx==2 and self.piece_occupante(x-1,ny)!=0):
                        return False
                else:
                    type_pioche=self.piece_occupante(nx,ny)
                    if type_pioche==0 or x-nx==2:
                        return False
        else:
            if type==2:
                if np.abs(nx-x)+np.abs(ny-y) != 3 or nx==x or ny==y:
                    return False
            else:
                if type==4:
                    if (np.abs(nx-x)>1 or np.abs(ny-y)>1):
                        return False
                if type==3:
                    if abs(nx - x) != abs(ny -y):
                        return False
                if type==1:
                    if nx!=x and ny!=y:
                        return False
                if type==5:
                    if (abs(nx - x) != abs(ny -y)) and nx!=x and ny!=y:
                        return False
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
                    if self.piece_occupante(i,j)!=0:
                        return False
            #piocher
            type_pioche=self.piece_occupante(nx,ny)
        self.cases[nx][ny]=self.cases[x][y]
        self.cases[x][y]=0
        self.track_rois(nx,ny)
        seraitcheck=0
        if(self.checkcheck()):
            seraitcheck=1
        self.cases[x][y]=self.cases[nx][ny]
        self.cases[nx][ny]=0
        self.track_rois(x,y)
        if type_pioche != 0:
            self.cases[nx][ny]=type_pioche
        if seraitcheck:
            return False
        return True


    def checkmate(self):
        for (x,y,nx,ny) in self.get_all_reasonable_moves():
            if(self.canmove(x,y,nx,ny)):
                return False
        return True

    def move(self,x,y,nx,ny):
        self.cases[nx][ny]=self.cases[x][y]
        self.cases[x][y]=0
        if (abs(self.cases[nx][ny])==6 and (nx==7 or nx==0)):
            self.cases[nx][ny]= 5 if self.cases[nx][ny]==6 else -5
        self.track_rois(nx,ny)
        self.swap()        

    def scoreklayer(self,x,y,nx1,ny1,k,largeur):
        type_pioche,pp = self.cases[nx1][ny1],(abs(self.cases[x][y])==6 and (nx1==7 or nx1==0))
        score=0
        if pp:
            score+=100
        if type_pioche != 0:
            dic_recompense={6:10, 2:40, 3:35, 1:50,5:90}
            score+= dic_recompense[abs(type_pioche)]
        
        assert(self.canmove(x,y,nx1,ny1))
        self.move(x,y,nx1,ny1)
        check = self.checkcheck()
        mate=self.checkmate()
        if check:
            score+=5
        if mate and check:
            score+=10**10
        score*=k

        if k!=1 and not mate:
            reasonable_moves=self.get_all_reasonable_moves()
            np.random.shuffle(reasonable_moves)
            moves=[]
            scores=[]
            for(x2,y2,nx2,ny2) in reasonable_moves:
                if self.canmove(x2,y2,nx2,ny2):
                    moves.append((x2,y2,nx2,ny2))
                    scores.append(self.scoreklayer(x2,y2,nx2,ny2,1,largeur))
            
            best_moves=[moves[i] for i in np.argsort(scores)[-largeur:]]
            best_scores=[]
            for(x2,y2,nx2,ny2) in best_moves:
                best_scores.append(self.scoreklayer(x2,y2,nx2,ny2,k-1,largeur))
            score-=np.max(best_scores)
            
        #undoing
        self.swap()
        self.cases[x][y]=self.cases[nx1][ny1]
        self.cases[nx1][ny1]=type_pioche
        if pp:
            self.cases[x][y]= 6 if self.cases[x][y]==5 else -6
        self.track_rois(x,y)
        #switch back
        return score


    def makeamove(self,level,width):
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
        
        reasonable_moves=self.get_all_reasonable_moves()
        np.random.shuffle(reasonable_moves)
        moves=[]
        scores=[]
        for(x2,y2,nx2,ny2) in reasonable_moves:
            if self.canmove(x2,y2,nx2,ny2):
                moves.append((x2,y2,nx2,ny2))
                scores.append(self.scoreklayer(x2,y2,nx2,ny2,level,width))
        x,y,nx,ny=moves[np.argmax(scores)]
        assert(self.canmove(x,y,nx,ny))
        self.move(x,y,nx,ny)
        return True

cases=[[0,0,0,4,0,0,0,0],[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*7+[-6],[0,0,0,-4,0,0,0,0]]
newgame=Game(1,cases)
still_can_play = True
while still_can_play:
    newgame.print_board()
    still_can_play = newgame.makeamove(3,10)
    if not still_can_play:
        break
    newgame.print_board()
    still_can_play = newgame.makeamove(2,10)
    
