import tkinter
from random import randint


window_width = 1000
window_height = 600
delay = 200

def default():
    global lenght
    global current_direction
    global direction
    lenght = 6
    current_direction = "Right"
    direction = current_direction

def forget_play():
    map_size_label.place_forget()
    small.place_forget()
    normal.place_forget()
    big.place_forget()
    play_button.place_forget()

def forget_gameover():
    gameover_label.place_forget()
    gameover_button_to_menu.place_forget()
    gameover_button_again.place_forget()

def menu(x=0):
    if x: forget_gameover()
    map_size_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.25)
    small.place(anchor=tkinter.W, relx=0.45, rely=0.35)
    normal.place(anchor=tkinter.W, relx=0.45, rely=0.45)
    big.place(anchor=tkinter.W, relx=0.45, rely=0.55)
    play_button.place(anchor=tkinter.CENTER, relx=0.5, rely=0.7)

def again():
    forget_gameover()
    start()

def gameover():
    canvas.delete("all")
    canvas.pack_forget()
    gameover_label["text"] = f"Your score is {lenght}"
    gameover_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.40)
    gameover_button_to_menu.place(anchor=tkinter.CENTER, relx=0.3, rely=0.6)
    gameover_button_again.place(anchor=tkinter.CENTER, relx=0.7, rely=0.6)

def play():
    global size
    global map_width
    global map_height
    global max_coord_x
    global max_coord_y
    size = square_size.get()
    map_width = window_width / size
    map_height = window_height / size
    max_coord_x = window_width - size
    max_coord_y = window_height - size
    forget_play()
    start()

def start():
    default()
    canvas.pack()
    canvas.focus_set()
    canvas.bind("<Key>", change_direction)
    spawn_actors()
    move()

def add_body():
    x1, y1, x2, y2 = canvas.coords(body[-1])
    body.append(canvas.create_rectangle(x1, y1, x2, y2, fill="#00EE00"))

def random_coords():
    x1, y1 = randint(0, map_width - 1) * size, randint(0, map_height - 1) * size
    x2 = x1 + size
    y2 = y1 + size
    return x1, y1, x2, y2

def change_coords_apple():
    x1, y1, x2, y2 = random_coords()
    canvas.coords(apple, x1, y1, x2, y2)

def check_apple():
    global lenght
    if canvas.coords(head) == canvas.coords(apple):
        lenght += 1
        return True
    return False

def check_collision():
    for i in body:
        if canvas.coords(head) == canvas.coords(i):
            return True
    return False

def move_body(x1, y1, x2, y2):
    for i in body:
        x11, y11, x21, y21 = canvas.coords(i)
        canvas.coords(i, x1, y1, x2, y2)
        x1, y1, x2, y2 = x11, y11, x21, y21

def change_direction(event):
    global direction
    if event.keysym == "Right" and current_direction != "Left" and current_direction != "Right":  direction = event.keysym
    elif event.keysym == "Left" and current_direction != "Right" and current_direction != "Left": direction = event.keysym
    elif event.keysym == "Up" and current_direction != "Down" and current_direction != "Up":      direction = event.keysym
    elif event.keysym == "Down" and current_direction != "Up" and current_direction != "Down":    direction = event.keysym

def spawn_actors():
    global head
    global body
    global apple
    head = canvas.create_rectangle(0, 0, size, size, fill="#00EE00")
    body = []
    x1, x2 = canvas.coords(head)[0] - size, canvas.coords(head)[2] - size
    for i in range(lenght - 1):
        body.append(canvas.create_rectangle(x1, 0, x2, size, fill="#00EE00"))
        x1 -= size
        x2 -= size
    x1, y1, x2, y2 = random_coords()
    apple = canvas.create_rectangle(x1, y1, x2, y2, fill="#EE0000")

def move():
    global current_direction
    x1, y1, x2, y2 = canvas.coords(head)
    if direction == "Right":
        if canvas.coords(head)[0] == max_coord_x:
            canvas.move(head, -max_coord_x, 0)
        else:
            canvas.move(head, size, 0)
    elif direction == "Left":
        if canvas.coords(head)[0] == 0:
            canvas.move(head, max_coord_x, 0)
        else:
            canvas.move(head, -size, 0)
    elif direction == "Up":
        if canvas.coords(head)[1] == 0:
            canvas.move(head, 0, max_coord_y)
        else:
            canvas.move(head, 0, -size)
    elif direction == "Down":
        if canvas.coords(head)[1] == max_coord_y:
            canvas.move(head, 0, -max_coord_y)
        else:
            canvas.move(head, 0, size)
    move_body(x1, y1, x2, y2)
    current_direction = direction
    if check_collision():
        gameover()
        return False
    if check_apple():
        change_coords_apple()
        add_body()
    root.after(delay, move)


root = tkinter.Tk()
root.title("Snake")
root.resizable(False, False)
root.geometry(f"{window_width}x{window_height}")
root["bg"] = "#000"

map_size_label = tkinter.Label(root, text="Select size of map: ", font="Arial 28 bold", fg="#62d2a2", bg="#000")

square_size = tkinter.IntVar()
square_size.set(25)

small = tkinter.Radiobutton(root, text='small', font="Arial 22 bold", variable=square_size, value=50, fg="#fff", bg="#000", activebackground="#000", activeforeground="#fff", selectcolor="#222222")
normal = tkinter.Radiobutton(root, text='normal', font="Arial 22 bold", variable=square_size, value=25, fg="#fff", bg="#000", activebackground="#000", activeforeground="#fff", selectcolor="#222222")
big = tkinter.Radiobutton(root, text='big', font="Arial 22 bold", variable=square_size, value=20, fg="#fff", bg="#000", activebackground="#000", activeforeground="#fff", selectcolor="#222222")

play_button = tkinter.Button(root, text="Play", font="Arial 22 bold", padx="40", command=play, fg="#62d2a2", bg="#222222", relief=tkinter.RIDGE)

menu()

canvas = tkinter.Canvas(root, width=window_width, height=window_height, bg="#000", highlightthickness=0)

gameover_label = tkinter.Label(font="Arial 28 bold", fg="#62d2a2", bg="#000")
gameover_button_to_menu = tkinter.Button(root, text="Menu", font="Arial 22 bold", padx="40", command=lambda x = 1: menu(x), fg="#62d2a2", bg="#222222", relief=tkinter.RIDGE)
gameover_button_again = tkinter.Button(root, text="Again", font="Arial 22 bold", padx="40", command=again, fg="#62d2a2", bg="#222222", relief=tkinter.RIDGE)

root.mainloop()