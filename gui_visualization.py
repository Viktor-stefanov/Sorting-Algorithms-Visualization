import tkinter
import random
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sorting_algorithms.sorts import *
from info import *
from tkinter import ttk
from tkinter import font

def round_rectangle(x1, y1, x2, y2, canvas, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, kwargs, smooth=True)

def clear_screen(root):
    """ clean the whole screen? Obviously """
    for child in root.winfo_children():
        child.destroy()

def main_screen(root=None):
    """ set up the main window, it's dimensions, title, icon, etc...
        set up the header and 'choose box' widgets and display them on the screen """

    def on_start_click():
        # handle pressing the start button
        start_canvas.configure(relief="raised")
        on_start(root, sorting_alg.get(), array_size.get(), sorting_speed.get())

    # this check is made in case we want to 'redraw' the screen without actually opening a new 'tab' (another root instance)
    if root is None:
        icon = ""
        root = tkinter.Tk()
        root.option_add("*TCombobox*Listbox.font", ("Aria;", 18))
        root.title("Sorting Algorithms Visualization")
        # root.iconbitmap(icon)
        root.geometry("1400x900")
        root.configure(background="#8ecae6")
    else: # if root is passed clean the current screen before creating the 'main' screen
        clear_screen(root)
    root.bind("<Key-q>", sys.exit)
    root.bind("<Key-m>", lambda e: main_screen(root))

    header = tkinter.Label(text="Sorting Algorithms Visualization", font=("Aria;",  48, "bold"), background="#023047", fg="white")
    alg_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0)
    round_rectangle(0, 0, 425, 120, alg_canvas, radius=25, fill="#a2d2ff")
    algorithms = ("Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Bogo Sort")
    sorting_alg_label = tkinter.Label(text="Sorting algorithm:", font=("Aria;", 28), bg="#a2d2ff")
    sorting_alg = ttk.Combobox(values=algorithms, font=("Aria;", 24), state="readonly", width=20)
    sorting_alg.current(0) # set the current item to the first item
    header.pack(fill=tkinter.X)
    alg_canvas.place(x=65, y=130, w=425)
    sorting_alg_label.place(x=75, y=140)
    sorting_alg.place(x=75, y=195)

    size_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0)
    round_rectangle(0, 0, 325, 120, size_canvas, fill="#a2d2ff")
    array_size_label = tkinter.Label(text="Array size:", font=("Aria;", 28), bg="#a2d2ff")
    array_size = ttk.Combobox(values=("Small", "Average", "Big"), state="readonly", font=("Aria;", 24), width=11)
    array_size.current(0)  # set the current item to the first item
    size_canvas.place(x=540, y=130, w=425)
    array_size_label.place(x=590, y=140)
    array_size.place(x=590, y=195)

    speed_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0)
    round_rectangle(0, 0, 425, 120, speed_canvas, fill="#a2d2ff")
    sorting_speed_label = tkinter.Label(text="Sorting speed:", font=("Aria;", 28), bg="#a2d2ff")
    sorting_speed = ttk.Combobox(values=("Study", "Slow", "Fast"), state="readonly", font=("Aria;", 24), width=15)
    sorting_speed.current(0)  # set the current item to the first item
    speed_canvas.place(x=915, y=130, w=425)
    sorting_speed_label.place(x=975, y=140)
    sorting_speed.place(x=975, y=195)

    # use a canvas as a 'button' and set up event handlers for click press and release
    start_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0)
    round_rectangle(0, 0, 170, 50, start_canvas, fill="#a2d2ff")
    start_canvas.create_text(85, 25, fill="black", font=("Aria;", 20, "bold"), text="Visualize")
    start_canvas.bind("<ButtonRelease-1>", lambda e: on_start_click())
    start_canvas.place(x=1200, y=825, w=200, h=50)

    root.mainloop()

def on_start(root, alg, size, speed):
    """ helper function to clean the screen and build the graph, array, set speed, etc... before graphing of the algorithm """
    clear_screen(root)
    # check the function name e.g. (bogo_sort) with the current algorithm's name and if they match you assign the function to the algorithm variable
    algorithm = [sort for sort in (bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort, bogo_sort) if sort.__name__.replace("_", " ") == alg.lower()][0]
    array_size = 25 if size == "Small" else 100 if size == "Average" else 200
    sort_speed = speed if speed == "Study" else 500 if speed == "Slow" else 1
    # initialize an array of size - array_size with random numbers from 1 to the size of the array and get the iterator object of the sorting alg chosen
    arr = random.sample(range(1, array_size+1), array_size)
    generator = algorithm(arr)

    fig, ax, canvas, str_var = graph_layout(root, array_size, alg)
    start_visualization(generator, alg, sort_speed, fig, ax, canvas, str_var)

def graph_layout(root, array_size, alg):
    """ layout of the APP while the graph is being visualized. Returns the ax object for later use in the bar chart """
    # create the figure, axes etc... (set up the graph)
    fig = plt.Figure(figsize=(15, 8), dpi=100, facecolor="#8ecae6")
    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(axis="x", colors="white") # change the tick colors to white on both the x and the y axis
    ax.tick_params(axis="y", colors="white")
    # create the embedded canvas object and an operation counter
    canvas = FigureCanvasTkAgg(fig, master=root)
    string_var = tkinter.StringVar()
    string_var.set(f"Operations: 0")
    op_counter = tkinter.Label(root, textvariable=string_var, font=("Aria;", 18, "bold"), bg="#8ecae6", fg="#a2d2ff")
    # create a 'header' using a canvas for the round edges...
    header_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0, height=110)
    round_rectangle(0, 0, 1200, 60, header_canvas, fill="#a2d2ff")
    header = tkinter.Label(root, text=f"{alg.capitalize()} performed on an array of {array_size} elements", font=("Aria;", 28, "bold"), bg="#a2d2ff")
    # use a canvas as a menu button
    menu_canvas = tkinter.Canvas(root, bg="#8ecae6", highlightthickness=0)
    round_rectangle(0, 0, 170, 50, menu_canvas, fill="#a2d2ff")
    menu_canvas.create_text(85, 25, fill="black", font=("Aria;", 20, "bold"), text="Menu")
    menu_canvas.bind("<ButtonRelease-1>", lambda e: main_screen(root))
    # put everything on the screen
    header_canvas.pack(fill=tkinter.BOTH, padx=(100, 0), pady=(60, 0))
    menu_canvas.place(x=1200, y=825, w=200, h=50)
    canvas.get_tk_widget().place(x=-67, y=60)
    header.place(x=120, y=69)
    op_counter.place(x=120, y=820)

    return fig, ax, canvas, string_var

def start_visualization(generator, alg_name, sort_speed, fig, ax, canvas, str_var):
    """ method does the actual graphing of the sorting algorithm """
    operations = 0
    def simple_frame(frames):
        """ function is called every time a frame is being visualized
            change the position of the bars according to the current 'yield' from the sorting algorithm
            difference between simple & complex is in the unpacking of the 'frames' values (bubble, insertion, selection - 3 items, all other 4, merge 5)"""
        nonlocal operations
        arr, left, right = frames
        for index, bar in enumerate(bars):
            bar.set_height(arr[index])
            bar.set_color("paleturquoise")
            if index in (left, right):
                bar.set_color("r")
            bar.set_edgecolor((0, 0, 0))
        operations += 1
        str_var.set(f"Operations: {operations}")
        fig.canvas.draw()
        canvas.flush_events()

    # def complex_frame(frames):
    #     nonlocal operations
    #     arr, left, right


    # get the first iteration of the sorting algorithm to create a bars object (which we manipulate in the visualize_frame function above
    array, left_item, right_item = next(generator)
    bars = ax.bar(sorted(array), array)
    # create the animation. frames argument takes a generator and passes it's yield statements as arguments to visualize_frame. That is why we unpack 3 things in the function: arr, left, right = frames
    if sort_speed != "Study":
        ani = animation.FuncAnimation(
            fig,
            simple_frame,
            frames=generator,
            interval=sort_speed,
            repeat=False
        )
        ani._start() # start the animation


if __name__ == "__main__":
    main_screen()