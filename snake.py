import tkinter
from random import randint


window_width = 1000
window_height = 600
size = 20
map_width = window_width / size
map_height = window_height / size
max_coord_x = window_width - size
max_coord_y = window_height - size
direction = "Right"
delay = 200
lenght = 3

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
    if canvas.coords(head) == canvas.coords(apple):
        return True

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
    if event.keysym == "Right" and direction != "Left":   direction = event.keysym
    elif event.keysym == "Left" and direction != "Right": direction = event.keysym
    elif event.keysym == "Up" and direction != "Down":    direction = event.keysym
    elif event.keysym == "Down" and direction != "Up":    direction = event.keysym

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
    x1, y1, x2, y2 = canvas.coords(head)
    if direction == "Right":
        if canvas.coords(head)[0] == max_coord_x:
            canvas.move(head, -max_coord_x, 0)
        else:
            canvas.move(head, 20, 0)
    elif direction == "Left":
        if canvas.coords(head)[0] == 0:
            canvas.move(head, max_coord_x, 0)
        else:
            canvas.move(head, -20, 0)
    elif direction == "Up":
        if canvas.coords(head)[1] == 0:
            canvas.move(head, 0, max_coord_y)
        else:
            canvas.move(head, 0, -20)
    elif direction == "Down":
        if canvas.coords(head)[1] == max_coord_y:
            canvas.move(head, 0, -max_coord_y)
        else:
            canvas.move(head, 0, 20)
    move_body(x1, y1, x2, y2)
    if check_collision():
        return False
    if check_apple():
        change_coords_apple()
        add_body()
    root.after(delay, move)


root = tkinter.Tk()
root.title("Snake")
root.resizable(False, False)
root.geometry(f"{window_width}x{window_height}")

canvas = tkinter.Canvas(root, width=window_width, height=window_height, bg="#000", highlightthickness=0)
canvas.pack()
canvas.focus_set()
canvas.bind("<Key>", change_direction)

spawn_actors()
move()

root.mainloop()