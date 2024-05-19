from tkinter import *
from PIL import Image, ImageTk
import random
import itertools 
App = Tk()
App.geometry('650x600')
App.title('Vacumm simulator')

global grid, current_position, goal_position 



def dfs_search(grid, current_position, goal_position):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)] 
    visited_nodes = [] # to keep track of visited nodes
    def dfs_helper(x, y):
        if x < 0 or x >= rows or y < 0 or y >= cols or visited[x][y] or grid[x][y] == 1:
            return None

        visited[x][y] = True
        visited_nodes.append((x, y)) # add node to visited nodes

        if (x, y) == goal_position:
            return [(x, y)]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            result = dfs_helper(new_x, new_y)
            if result:
                return [(x, y)] + result

        return None

    path = dfs_helper(current_position[0], current_position[1])
    print("Path found:", path)
    return visited_nodes, path, step # return visited nodes if no path found

def handle_start(canvas,rectangle_ids):
    global current_position
    global goal_position

    visited_nodes, path, step = dfs_search(grid, current_position, goal_position)
    for i, step in enumerate(visited_nodes):
        if i > 0:
            current_position = step
            move =  current_position[0]* len(grid) + current_position[1] 
            canvas.itemconfig(rectangle_ids[move], fill="yellow")
            App.update()  
            App.after(100)
    # step_label = Label(main_frame, text=f"Steps taken: {step}")
    # step_label.pack()    
    if not path:
        not_found = Label(main_frame, text="Solution not found")
        not_found.pack               

def draw_grid(page, number):
    global grid, current_position, goal_position
    pairs = []
    for i in range(number):
        pair = [random.randint(0, number-1), random.randint(0, number-1)]
        while pair in [[0, 0], [number-1, number-1]]:
            pair = [random.randint(0, number-1), random.randint(0, number-1)]
        pairs.append(pair)
    canvas = Canvas(page, width=400, height=400, bg="#76ABAE")
    step = 400  // number
    rectangle_ids = []
    grid = [[0 for _ in range(number)] for _ in range(number)]
    goal_position = (len(grid)-1, len(grid)-1)
    for x in range(0,400 // step , 1):
        for y in range(0, 400 // step, 1):
            obstacle = False
            for pair in pairs:  
                if(x == pair[0] and y == pair[1]):
                    rectangle_id = canvas.create_rectangle(x * step,y * step,x*step + step,y*step + step, fill="#9B3922")
                    grid[x][y] = 1
                    obstacle = True
                    break
            if(x == 0 and y == 0):
                rectangle_id = canvas.create_rectangle(x * step,y * step,x*step + step,y*step + step, fill="yellow")
                current_position = (x,y)
            elif(x == 400 // step -1  and y == 400 // step - 1):
                rectangle_id = canvas.create_rectangle(x * step,y * step,x*step + step,y*step + step, fill="blue")
            elif(obstacle == False):     
                rectangle_id =  canvas.create_rectangle(x * step,y * step,x*step + step,y*step + step)
            rectangle_ids.append(rectangle_id)         
                    
    canvas.pack()
    start_btn = Button(page,text="START", fg="#76ABAE", font=("Bold",15), border=0 ,command=lambda:handle_start(canvas, rectangle_ids))
    start_btn.pack()


def frame_4():
    frame_4 = Frame(main_frame)
    draw_grid(frame_4,4)
    frame_4.pack(pady=10)

def frame_8():
    frame_8 = Frame(main_frame)
    draw_grid(frame_8,8)
    frame_8.pack(pady=10)


def frame_16():
    frame_16 = Frame(main_frame)
    draw_grid(frame_16,16)
    frame_16.pack(pady=10)



def hide_indicator():
    button_4_indicator.config(bg ="#31363F")
    button_8_indicator.config(bg ="#31363F")
    button_16_indicator.config(bg ="#31363F")

def delete_frame():
    for frame in main_frame.winfo_children():
        frame.destroy()


def indicate(label, page):
    hide_indicator()
    label.config(bg = "#76ABAE")
    delete_frame()
    page()

side_bar = Frame(App, bg="#31363F")
side_bar.pack(side=LEFT)
side_bar.pack_propagate(False)
side_bar.configure(width=150,height=600)

select_label = Label(side_bar, text="select size", font=("Bold",15), fg="#76ABAE", bg="#31363F")
select_label.place(x=5, y= 20)

button_4 = Button(side_bar, text="4 x 4", font=("Bold",10), fg="#76ABAE", bd=0, bg="#31363F", command=lambda:indicate(button_4_indicator, frame_4))
button_4.place(x=25, y= 50)
button_4_indicator = Label(side_bar, text="",bg="#31363F")
button_4_indicator.place(x = 5, y = 45, width=5, height=30)




button_8 = Button(side_bar, text="8 x 8", font=("Bold",10), fg="#76ABAE", bd=0, bg="#31363F", command=lambda:indicate(button_8_indicator, frame_8))
button_8.place(x=25, y= 100)
button_8_indicator = Label(side_bar, text="",bg="#31363F")
button_8_indicator.place(x = 5, y = 95, width=5, height=30)





button_16 = Button(side_bar, text="16 x 16", font=("Bold",10), fg="#76ABAE", bd=0, bg="#31363F", command=lambda:indicate(button_16_indicator, frame_16))
button_16.place(x=25, y= 150)
button_16_indicator = Label(side_bar, text="",bg="#31363F")
button_16_indicator.place(x = 5, y = 145, width=5, height=30)



main_frame = Frame(App, highlightbackground='black',highlightthickness=2, bg="#222831")
main_frame.pack(side=LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=500,height=600)



App.mainloop()