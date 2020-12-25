import numpy as np
import time
    
def swap(board):
    board[64] = 1-board[64]

def print_board(board):
    rempl={0:'.',-1:'t',-2:'c',-3:'f',-4:'r',-5:'d',-6:'p',1:'T',2:'C',3:'F',4:'R',5:'D',6:'P'}
    for i in range(8):
        for j in range(8):
            print("  "+rempl[board[i*8+j]],end='')
        print("")
    print("==========================\n")

def piece_occupante(board,nx,ny):
    if nx>=0 and nx<=7 and ny>=0 and ny<=7:
        return(board[nx*8+ny])
    else:
        return 0

def get_reasonable_moves(board,x,y):
    moves=[]
    type,coul=abs(board[x*8+y]),'N' if board[x*8+y]>0 else 'B'
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
        for mon_zip in [zip([x]*8,[y]*8,range(x-1,-1,-1),[y]*abs(x)),zip([x]*8,[y]*8,range(x+1,8),[y]*abs(8-x)),zip([x]*8,[y]*8,[x]*abs(y),range(y-1,-1,-1)),zip([x]*8,[y]*8,[x]*abs(8-y),range(y+1,8))]:
            moves.extend(mon_zip)
    return moves

def get_all_reasonable_moves(board):
    moves=[]
    for x in range(8):
        for y in range(8):
            piece=board[x*8+y]
            if piece==0:
                continue
            if (piece<0) == (board[64]) :
                moves.extend(get_reasonable_moves(board,x,y))
    return moves
    
def checkcheck(board):
    lui=(-1)**(1-board[64])
    mon_roi=-4*lui
    pos_roi=board.index(mon_roi)
    x,y=pos_roi//8,pos_roi%8
    if piece_occupante(board,x+(-1)**board[64],y-1)==6*lui or piece_occupante(board,x+(-1)**board[64],y+1)==6*lui:
            return True
    for (cx,cy) in [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]:
        if piece_occupante(board,cx,cy)==4*lui:
            return True
    for (cx,cy) in [(x-2,y-1),(x-1,y-2),(x-2,y+1),(x-1,y+2),(x+1,y-2),(x+2,y-1),(x+1,y+2),(x+2,y+1)]:
        if piece_occupante(board,cx,cy)==2*lui:
            return True
    for mon_zip in [zip(range(x+1,8),range(y+1,8)),zip(range(x+1,8),range(y-1,-1,-1)),zip(range(x-1,-1,-1),range(y+1,8)),zip(range(x-1,-1,-1),range(y-1,-1,-1))]:
        for(cx,cy) in mon_zip:
            if piece_occupante(board,cx,cy)==3*lui or piece_occupante(board,cx,cy)==5*lui:
                return True
            elif piece_occupante(board,cx,cy)!=0:
                break
    for mon_zip in [zip(range(x-1,-1,-1),[y]*abs(x)),zip(range(x+1,8),[y]*abs(8-x)),zip([x]*abs(y),range(y-1,-1,-1)),zip([x]*abs(8-y),range(y+1,8))]:
        for(cx,cy) in mon_zip:
            if piece_occupante(board,cx,cy)==1*lui or piece_occupante(board,cx,cy)==5*lui:
                return True
            elif piece_occupante(board,cx,cy)!=0:
                break
    return False

def canmove(board,x,y,nx,ny):
    if (nx<0 or nx>7 or ny<0 or ny>7 or board[x*8+y]==0 or board[x*8+y]*board[nx*8+ny]>0):
        return False
    type,coul=abs(board[x*8+y]),'N' if board[x*8+y]>0 else 'B'
    lui=(-1)**(1-board[64])
    type_pioche=0
    if type==6:
        if coul=='N':
            if nx<=x or abs(ny-y)>1 or (nx-x>2 and x==1) or (nx-x>1 and x>1):
                return False
            if ny==y:
                if piece_occupante(board,nx,ny)<0:
                    return False
                if (nx-x==2 and piece_occupante(board,x+1,ny)!=0):
                    return False
            else:
                type_pioche=piece_occupante(board,nx,ny)
                if type_pioche==0 or nx-x==2:
                    return False
        else:
            if nx>=x or abs(ny-y)>1 or (x-nx>2 and x==6) or (x-nx>1 and x<6):
                return False
            if ny==y :
                if piece_occupante(board,nx,ny)>0:
                    return False
                if (x-nx==2 and piece_occupante(board,x-1,ny)!=0):
                    return False
            else:
                type_pioche=piece_occupante(board,nx,ny)
                if type_pioche==0 or x-nx==2:
                    return False
    else:
        if type==2:
            if abs(nx-x)+abs(ny-y) != 3 or nx==x or ny==y:
                return False
        else:
            if type==4:
                if (abs(nx-x)>1 or abs(ny-y)>1):
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
                if piece_occupante(board,i,j)!=0:
                    return False
        #piocher
        type_pioche=piece_occupante(board,nx,ny)
    board[nx*8+ny]=board[x*8+y]
    board[x*8+y]=0
    seraitcheck=0
    if(checkcheck(board)):
        seraitcheck=1
    board[x*8+y]=board[nx*8+ny]
    board[nx*8+ny]=0
    if type_pioche != 0:
        board[nx*8+ny]=type_pioche
    if seraitcheck:
        return False
    return True


def checkmate(board):
    for (x,y,nx,ny) in get_all_reasonable_moves(board):
        if(canmove(board,x,y,nx,ny)):
            return False
    return True

def move(board,x,y,nx,ny):
    board[nx*8+ny]=board[x*8+y]
    board[x*8+y]=0
    if (abs(board[nx*8+ny])==6 and (nx==7 or nx==0)):
        board[nx*8+ny]= 5 if board[nx*8+ny]==6 else -5
    board[64] = 1-board[64]     

def scoreklayer(board,x,y,nx1,ny1,k,largeur):
    type_pioche,pp = board[nx1*8+ny1],(abs(board[x*8+y])==6 and (nx1==7 or nx1==0))
    score=0
    if pp:
        score+=100
    if type_pioche != 0:
        dic_recompense={6:10, 2:40, 3:35, 1:50,5:90}
        score+= dic_recompense[abs(type_pioche)]
    
    assert(canmove(board,x,y,nx1,ny1))
    move(board,x,y,nx1,ny1)
    check = checkcheck(board)
    mate=checkmate(board)
    if check:
        score+=5
    if mate and check:
        score+=10**10
    score*=k

    if k!=1 and not mate:
        reasonable_moves=get_all_reasonable_moves(board)
        np.random.shuffle(reasonable_moves)
        moves=[]
        scores=[]
        for(x2,y2,nx2,ny2) in reasonable_moves:
            if canmove(board,x2,y2,nx2,ny2):
                moves.append((x2,y2,nx2,ny2))
                scores.append(scoreklayer(board,x2,y2,nx2,ny2,1,largeur))
        
        best_moves=[moves[i] for i in np.argsort(scores)[-largeur:]]
        best_scores=[]
        for(x2,y2,nx2,ny2) in best_moves:
            best_scores.append(scoreklayer(board,x2,y2,nx2,ny2,k-1,largeur))
        score-=np.max(best_scores)
        
    #undoing
    board[64] = 1-board[64]
    board[x*8+y]=board[nx1*8+ny1]
    board[nx1*8+ny1]=type_pioche
    if pp:
        board[x*8+y]= 6 if board[x*8+y]==5 else -6
    #switch back
    return score


def makeamove(board,level,width):
    if checkmate(board):
        if checkcheck(board):
            if board[64] :
                print("Checkmate, black wins.")
            else:
                print("Checkmate, white wins.")
            return False
        if board[64] :
            print("Draw, white cannot move.")
        else:
            print("Draw, black cannot move.")
        return False
    
    reasonable_moves=get_all_reasonable_moves(board)
    np.random.shuffle(reasonable_moves)
    moves=[]
    scores=[]
    for(x2,y2,nx2,ny2) in reasonable_moves:
        if canmove(board,x2,y2,nx2,ny2):
            moves.append((x2,y2,nx2,ny2))
            scores.append(scoreklayer(board,x2,y2,nx2,ny2,level,width))
    x,y,nx,ny=moves[np.argmax(scores)]
    assert(canmove(board,x,y,nx,ny))
    move(board,x,y,nx,ny)
    return True

board=[1,2,3,4,5,3,2,1]+[6]*8+[0]*32+[-6]*8+[-1,-2,-3,-4,-5,-3,-2,-1]+[1]
still_can_play = True
while still_can_play:
    print_board(board)
    start=time.time()
    still_can_play = makeamove(board,3,100)
    end=time.time()
    print(end-start)
    if not still_can_play:
        break
    print_board(board)
    still_can_play = makeamove(board,2,10)
    
