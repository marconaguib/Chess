import tkinter as tk

def newGame():
    window.destroy()
    newWindow = tk.Tk()
    newWindow.title("Chess")
    newWindow.iconbitmap("C:\\Users\\Nicolas Martin\\interf\\unnamed.ico")
    newWindow.geometry("1050x730+450+50")

    frame= tk.Frame(master=newWindow, bg="black")
    frame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

    board_face = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\Chess_Board.png")
    button_face_1 = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\new_game.png")
    board = tk.Label(master=frame,image=board_face, borderwidth=1)
    button_1 = tk.Button(master=frame,image=button_face_1)
    board.photo = board_face
    button_1.photo = button_face_1
    board.pack(side=tk.LEFT)
    button_1.pack(side=tk.RIGHT)


window = tk.Tk()
window.title("Chess")
window.iconbitmap("C:\\Users\\Nicolas Martin\\interf\\unnamed.ico")
window.geometry("500x700+1000+50")

frame= tk.Frame(master=window, bg="black")
frame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

background_face = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\bg.png")
greeting_face = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\greeting.png")
button_face_1 = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\new_game.png")
button_face_2 = tk.PhotoImage(file="C:\\Users\\Nicolas Martin\\interf\\settings.png")

background = tk.Label(master=frame,image=background_face, borderwidth=0)
greeting = tk.Label(master=frame,image=greeting_face, borderwidth=0)
button_1 = tk.Button(master=frame,image=button_face_1,command=newGame)
button_2 = tk.Button(master=frame,image=button_face_2)
greeting.pack(side=tk.TOP)
button_2.pack(side=tk.BOTTOM)
button_1.pack(side=tk.BOTTOM)
background.pack(side=tk.BOTTOM)

window.mainloop()
