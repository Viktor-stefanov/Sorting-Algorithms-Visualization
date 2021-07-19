import tkinter
import random
import sys
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sorting_algorithms.sorts import *
from tkinter import ttk
from info import sorts


def round_rectangle(x1, y1, x2, y2, canvas, radius=25, **kwargs):
    """ create a round rectangle with the create_polygon method of the canvas tkinter object. P.S. Tkinter sucks! """
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

class Visualization:
    def __init__(self):
        """ set up the main window, it's dimensions, title, icon, etc... """
        icon = ""
        self.root = tkinter.Tk()
        self.root.option_add("*TCombobox*Listbox.font", ("Aria;", 18))
        self.root.title("Sorting Algorithms Visualization")
        # self.root.iconbitmap(icon)
        self.root.geometry("1400x900")
        self.root.configure(background="#8ecae6")
        self.root.bind("<Key-q>", sys.exit)
        self.root.bind("<Key-m>", lambda e: self.main_screen())
        # initialize variables
        self.combobox_v = None  # tkinter.StringVar() to inform us when the user has selected an algorithm from the combobox
        self.alg_information = None  # the short description which shows when you select an algorithm in the combobox
        self.sorting_alg = None  # which algorithm has been chosen
        self.array_size = None  # the size of the to be sorted array
        self.sorting_speed = None  # the speed of the animation
        self.graph_canvas = None  # FigureCanvasTkAgg
        self.operation_var = None  # operation counter StringVar()
        self.operations = 0  # operations counter for the graph

        self.main_screen()

    def main_screen(self):
        """ create the 'main menu' layout and draw it on the screen"""
        self.operations = 0
        def on_start_click():
            # when the user clicks the start button activate the on_start function to continue
            self.on_start()

        def alg_selected(index, value, op):
            # show a brief description when a sorting alg has been selected from the combobox
            information = [sort for sort in sorts if self.combobox_v.get().lower() in sort.lower()][
                0]  # if eg 'Bubble Sort' is in the sort description then choose that one. There are no duplicates of let's say 2 'Bubble Sort' in 2 descriptions
            self.alg_information.config(text=information)

        clear_screen(self.root) # clean the screen from other layouts

        header = tkinter.Label(text="Sorting Algorithms Visualization", font=("Aria;",  48, "bold"), background="#023047", fg="white")
        alg_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0)
        round_rectangle(0, 0, 425, 120, alg_canvas, radius=25, fill="#a2d2ff")
        algorithms = ("Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Bogo Sort", "Heap Sort")
        self.combobox_v = tkinter.StringVar()
        self.combobox_v.trace("w", alg_selected)
        sorting_alg_label = tkinter.Label(self.root, text="Sorting algorithm:", font=("Aria;", 28), bg="#a2d2ff")
        self.sorting_alg = ttk.Combobox(self.root, values=algorithms, textvar=self.combobox_v, font=("Aria;", 24), state="readonly", width=16)
        header.pack(fill=tkinter.X)
        alg_canvas.place(x=65, y=130, w=425)
        sorting_alg_label.place(x=126, y=140)
        self.sorting_alg.place(x=120, y=195)

        information_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0, width=2000, height=1000)
        round_rectangle(0, 0, 1255, 380, information_canvas, radius=25, fill="#a2d2ff")
        self.alg_information = tkinter.Label(information_canvas, text="", font=("Aria;", 28), wraplength=1240, justify="left", bg="#a2d2ff")
        information_canvas.place(x=75, y=325)
        self.alg_information.place(x=15, y=15)
        self.sorting_alg.current(0)  # set the algorithm combobox default to bubble sort. This will also trigger the alg_selected function since we are tracing the self.combobox_v StringVar() and will put the description of bubblesort on the screen

        size_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0, height=150)
        round_rectangle(0, 0, 325, 120, size_canvas, fill="#a2d2ff")
        array_size_label = tkinter.Label(text="Array size:", font=("Aria;", 28), bg="#a2d2ff")
        self.array_size = ttk.Combobox(values=("Miniature", "Small", "Average", "Big"), state="readonly", font=("Aria;", 24), width=10)
        self.array_size.current(0)  # set the current item to the first item
        size_canvas.place(x=540, y=130, w=425)
        array_size_label.place(x=615, y=140)
        self.array_size.place(x=600, y=195)

        speed_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0, height=180)
        round_rectangle(0, 0, 425, 120, speed_canvas, fill="#a2d2ff")
        sorting_speed_label = tkinter.Label(text="Animation speed:", font=("Aria;", 28), bg="#a2d2ff")
        self.sorting_speed = ttk.Combobox(values=("Study", "Slow", "Fast"), state="readonly", font=("Aria;", 24), width=15)
        self.sorting_speed.current(0)  # set the current item to the first item
        speed_canvas.place(x=915, y=130, w=425)
        sorting_speed_label.place(x=975, y=140)
        self.sorting_speed.place(x=970, y=195)

        # use a canvas as a 'button' and set up event handlers for click press and release
        start_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0)
        round_rectangle(0, 0, 170, 50, start_canvas, fill="#a2d2ff")
        start_canvas.create_text(85, 25, fill="black", font=("Aria;", 20, "bold"), text="Visualize")
        start_canvas.bind("<ButtonRelease-1>", lambda e: on_start_click())
        start_canvas.place(x=1200, y=825, w=200, h=50)

        self.root.mainloop()

    def on_start(self):
        """ helper function to clean the screen and build the graph, array, sort speed, etc... before graphing the algorithm """
        alg_name = self.sorting_alg.get()
        size = self.array_size.get()
        speed = self.sorting_speed.get()
        clear_screen(self.root)
        # check the function name e.g. (bogo_sort) with the current algorithm's name and if they match you assign the function to the algorithm variable
        self.sorting_alg = [sort for sort in (bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort, bogo_sort, heap_sort)
                            if sort.__name__.replace("_", " ") == alg_name.lower()][0]
        self.array_size = 10 if size == "Miniature" else 25 if size == "Small" else 100 if size == "Average" else 200
        self.sorting_speed = speed if speed == "Study" else 500 if speed == "Slow" else 1
        if self.sorting_alg == bogo_sort:
            self.array_size = 5 if size == "Miniature" else 6 if size == "Small" else 8 if size == "Average" else 10
        # initialize an array of size self.array_size with random numbers from 1 to the size of the array and get the generator object of the sorting alg chosen
        arr = random.sample(range(1, self.array_size+1), self.array_size)
        if alg_name in ("Quick Sort", "Merge Sort"):
            generator = self.sorting_alg(arr, 0, len(arr)-1)
        else:
            generator = self.sorting_alg(arr)

        fig, ax = self.graph_layout(alg_name)
        self.start_visualization(generator, arr, fig, ax)

    def graph_layout(self, alg_name):
        """ create the layout of the app displayed while the graph will be visualized """
        # create the figure, axes etc... (set up the graph)
        fig = plt.Figure(figsize=(15, 8), dpi=100, facecolor="#8ecae6")
        ax = fig.add_subplot(1, 1, 1)
        ax.tick_params(axis="x", colors="white") # change the tick colors to white on both the x and the y axis
        ax.tick_params(axis="y", colors="white")
        # create the embedded canvas object and an operation counter
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.operation_var = tkinter.StringVar()
        self.operation_var.set(f"Operations: 0")
        op_counter = tkinter.Label(self.root, textvariable=self.operation_var, font=("Aria;", 18, "bold"), bg="#8ecae6")
        # create a 'header' using a canvas for the round edges...
        header_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0, height=90)
        round_rectangle(0, 0, 1100, 60, header_canvas, fill="#a2d2ff")
        header = tkinter.Label(self.root, text=f"{alg_name.capitalize()} performed on an array of {self.array_size} elements", font=("Aria;", 28, "bold"), bg="#a2d2ff", justify="center", width=47)
        # use a canvas as a menu button
        menu_canvas = tkinter.Canvas(self.root, bg="#8ecae6", highlightthickness=0)
        round_rectangle(0, 0, 170, 50, menu_canvas, fill="#a2d2ff")
        menu_canvas.create_text(85, 25, fill="black", font=("Aria;", 20, "bold"), text="Menu")
        menu_canvas.bind("<ButtonRelease-1>", lambda e: self.main_screen())
        # put everything on the screen
        header_canvas.pack(fill=tkinter.BOTH, padx=(150, 0), pady=(60, 0))
        header.place(x=155, y=68)
        menu_canvas.place(x=1200, y=825, w=200, h=50)
        self.graph_canvas.get_tk_widget().place(x=-67, y=60)
        op_counter.place(x=120, y=820)

        return fig, ax

    def start_visualization(self, generator, array, fig, ax):
        """ method does the actual graphing of the sorting algorithm """
        def study_frame(event):
            try:
                next_frame = next(generator)
                display_frame(next_frame, study=True)
            except StopIteration:
                pass
                # call self.finished_visualization(). And create it ofc

        def display_frame(frame, study=False):
            """ display individual frame from the animation. Set the height of the bars, their colors and update the operations counter """
            arr, low, mid, high = frame  # again tkinter stuff...
            for index, bar in enumerate(bars):
                bar.set_height(arr[index])
                bar.set_color("paleturquoise")
                if index == high:
                    bar.set_color("r")
                elif index == low:
                    bar.set_color("g")
                if index in mid:
                    bar.set_color("#000000")
                bar.set_edgecolor((0, 0, 0))
            self.operations += 1
            self.operation_var.set(f"Operations: {self.operations}")
            if study is True:
                fig.canvas.draw()

        bars = ax.bar(sorted(array), array)

        # create the animation. frames argument takes a generator and passes it's yield statements as arguments to visualize_frame. That is why we unpack 3 things in the function: arr, left, right = frames
        if self.sorting_speed != "Study":
            ani = animation.FuncAnimation(
                fig,
                display_frame,
                frames=generator,
                interval=self.sorting_speed,
                repeat=False,
            )
            ani._start()  # start the animation
        else:  # if the user chose the 'study" sorting speed show frames only when the user presses the mouse
            self.root.bind("<ButtonPress>", study_frame)


if __name__ == "__main__":
    app = Visualization()