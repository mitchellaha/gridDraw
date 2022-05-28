# a tkinter pixel drawing program
import tkinter as tk
from tkinter import filedialog as fd
import json

# create a window
root = tk.Tk()
root.title("Pixel Drawing")
root.geometry("555x555")

grid_dimensions = 25
canvas_width = 501
canvas_height = 501
grid_size = 20

# create a canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, scrollregion=(0, 0, canvas_width, canvas_height), bg="white")
canvas.pack()

# make the drawing grid of the grid_dimensions
for i in range(grid_size):
    for j in range(grid_size):
        canvas.create_rectangle(i*grid_dimensions, j*grid_dimensions, (i+1)*grid_dimensions, (j+1)*grid_dimensions, fill="white")


# ? Color Palette Bar
# create a toolbar for picking the current color
colorBar = tk.Frame(root)
colorBar.pack(side=tk.BOTTOM, fill=tk.X)
current_color = "black"

# Function to change the current color
def change_color(new_color):
    global current_color
    current_color = new_color

# create a color picker button for each color
for color in ["red", "orange", "yellow", "green", "blue", "purple", "black", "white"]:
    # create a button
    button = tk.Button(colorBar, text=color, width=3, command=lambda c=color: change_color(c), highlightbackground=color)
    # pack the button
    button.pack(side=tk.LEFT)


# ? Toolbar
toolBar = tk.Frame(root)
toolBar.pack(side=tk.BOTTOM, fill=tk.X)

# create a toolbar for clearing the canvas
def clear_canvas():
    canvas.delete("all")
    for i in range(grid_size):
        for j in range(grid_size):
            canvas.create_rectangle(i*grid_dimensions, j*grid_dimensions, (i+1)*grid_dimensions, (j+1)*grid_dimensions, fill="white")

# create a toolbar item for saving and loading the canvas to json
def save_canvas():
    # get the canvas as a list of lists
    canvas_list = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            rectangle = canvas.find_closest(i*grid_dimensions, j*grid_dimensions)
            row.append(canvas.itemcget(rectangle, "fill"))
        canvas_list.append(row)

    files = [('JSON', '*.json')]
    file = fd.asksaveasfile(filetypes = files, defaultextension = files)
    if file is not None:
        # save the canvas to a json file
        with open(file.name, "w") as f:
            json.dump(canvas_list, f)

def load_canvas():
    filename = fd.askopenfilename()
    if filename:
        with open(filename, "r") as f:
            canvas_list = json.load(f)
        for i in range(grid_size):
            for j in range(grid_size):
                canvas.itemconfig(canvas.find_closest(i*grid_dimensions, j*grid_dimensions), fill=canvas_list[i][j])


clearButton = tk.Button(toolBar, text="Clear", command=clear_canvas)
clearButton.pack(side=tk.LEFT)

saveButton = tk.Button(toolBar, text="Save", command=save_canvas)
saveButton.pack(side=tk.LEFT)

loadButton = tk.Button(toolBar, text="Load", command=load_canvas)
loadButton.pack(side=tk.LEFT)



# on click of the canvas rectangle, change the selected rectangle to the current color
def on_click(event):
    # get the x and y coordinates of the mouse click
    x = event.x
    y = event.y
    # get the rectangle that was clicked
    rectangle = canvas.find_closest(x, y)
    # change the color of the rectangle to black
    canvas.itemconfig(rectangle, fill=current_color)

# bind the mouse click to the on_click function
canvas.bind('<Button-1>', on_click)
canvas.bind('<B1-Motion>', on_click)


# run the program
root.mainloop()
