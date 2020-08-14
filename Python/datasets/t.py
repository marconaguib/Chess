import chess.pgn
import csv

cases=["a8","b8","c8","d8","e8","f8","g8","h8",
        "a7","b7","c7","d7","e7","f7","g7","h7",
        "a6","b6","c6","d6","e6","f6","g6","h6",
        "a5","b5","c5","d5","e5","f5","g5","h5",
        "a4","b4","c4","d4","e4","f4","g4","h4",
        "a3","b3","c3","d3","e3","f3","g3","h3",
        "a2","b2","c2","d2","e2","f2","g2","h2",
        "a1","b1","c1","d1","e1","f1","g1","h1"]

boards = []
moves = []
tours=[]

pgn = open("C:\\Users\\Nicolas Martin\\chess\\datasets\\B02.pgn")
rep={'\n':' ','.':'0','r':'-1','n':'-2','b':'-3','q':'-5','k':'-4','p':'-6','R':'1','N':'2','B':'3','Q':'5','K':'4','P':'6'}

for i in range(3355):
    game=chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
        s= str(board).replace('\n',' ')
        for i,j in rep.items():
            s=s.replace(i,j)
        board_list=s.split()
        move_str=str(move)
        tour=-1 if int(board_list[cases.index(move_str[0:2])])<0 else 1

        boards.append(board_list)
        moves.append(move_str)
        tours.append(tour)
        board.push(move)

pgn = open("C:\\Users\\Nicolas Martin\\chess\\datasets\\C15.pgn")
rep={'\n':' ','.':'0','r':'-1','n':'-2','b':'-3','q':'-5','k':'-4','p':'-6','R':'1','N':'2','B':'3','Q':'5','K':'4','P':'6'}

for i in range(3188):
    game=chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
        s= str(board).replace('\n',' ')
        for i,j in rep.items():
            s=s.replace(i,j)
        board_list=s.split()
        move_str=str(move)
        tour=-1 if int(board_list[cases.index(move_str[0:2])])<0 else 1

        boards.append(board_list)
        moves.append(move_str)
        tours.append(tour)
        board.push(move)
#
# pgn = open("C:\\Users\\Nicolas Martin\\chess\\Karpov.pgn")
# rep={'\n':' ','.':'0','r':'-1','n':'-2','b':'-3','q':'-5','k':'-4','p':'-6','R':'1','N':'2','B':'3','Q':'5','K':'4','P':'6'}
#
# for i in range(530):
#     game=chess.pgn.read_game(pgn)
#     board = game.board()
#     for move in game.mainline_moves():
#         s= str(board).replace('\n',' ')
#         for i,j in rep.items():
#             s=s.replace(i,j)
#         board_list=s.split()
#         move_str=str(move)
#         tour=-1 if int(board_list[cases.index(move_str[0:2])])<0 else 1
#
#         boards.append(board_list)
#         moves.append(move_str)
#         tours.append(tour)
#         board.push(move)
#
# pgn = open("C:\\Users\\Nicolas Martin\\chess\\Kasparov.pgn")
# rep={'\n':' ','.':'0','r':'-1','n':'-2','b':'-3','q':'-5','k':'-4','p':'-6','R':'1','N':'2','B':'3','Q':'5','K':'4','P':'6'}
#
# for i in range(548):
#     game=chess.pgn.read_game(pgn)
#     board = game.board()
#     for move in game.mainline_moves():
#         s= str(board).replace('\n',' ')
#         for i,j in rep.items():
#             s=s.replace(i,j)
#         board_list=s.split()
#         move_str=str(move)
#         tour=-1 if int(board_list[cases.index(move_str[0:2])])<0 else 1
#
#         boards.append(board_list)
#         moves.append(move_str)
#         tours.append(tour)
#         board.push(move)
#
# pgn = open("C:\\Users\\Nicolas Martin\\chess\\Kosteniuk.pgn")
# rep={'\n':' ','.':'0','r':'-1','n':'-2','b':'-3','q':'-5','k':'-4','p':'-6','R':'1','N':'2','B':'3','Q':'5','K':'4','P':'6'}
#
# for i in range(469):
#     game=chess.pgn.read_game(pgn)
#     board = game.board()
#     for move in game.mainline_moves():
#         s= str(board).replace('\n',' ')
#         for i,j in rep.items():
#             s=s.replace(i,j)
#         board_list=s.split()
#         move_str=str(move)
#         tour=-1 if int(board_list[cases.index(move_str[0:2])])<0 else 1
#
#         boards.append(board_list)
#         moves.append(move_str)
#         tours.append(tour)
#         board.push(move)
#
#

f = open('C:\\Users\\Nicolas Martin\\chess\\moves.csv', 'a+')
with f:
    writer=csv.writer(f)
    for i in range(len(boards)):
        writer.writerow(boards[i]+[tours[i],moves[i]])

f.close()
