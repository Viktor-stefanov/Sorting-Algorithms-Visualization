import pygame
import sorting_algorithms.sorts as sorts
from random import randint, shuffle
import sys

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (204, 25, 42)
GREEN = (51, 229, 51)
BLUE = (51, 185, 229)

def setup():
    global s_height
    sort_type = input('-!- Pick a sorting algorithm - (b)ubblesort, (s)electionsort, (i)nsertionsort, (m)ergesort, (q)uicksort: ')
    N = input('-!- Choose the array size (small, medium, large): ')

    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    s_width, s_height = pygame.display.get_surface().get_size()
    pygame.display.set_caption('Visualizing Sort Algorithms')

    return s_width, s_height, win, sort_type, N

def array_setup(s_width, N):
    global padding, array_width
    padding = s_width // 125

    max_awidth = int(s_width - padding * 2)
    if N in 'small':
        N = max_awidth // 15
        print(N)
        fps = 10
    elif N in 'medium':
        N = max_awidth // 6
        print(N)
        fps = 30
    elif N in 'large':
        N = max_awidth // 2
        fps = 80
    array_width = int(max_awidth / N)

    highest_number = s_height - 30
    array = [randint(1, highest_number) for _ in range(int(N))]

    return array, fps

def update_graph(win, arr, redEls=None, blueEls=None, greenEls=None, ts=None, last=False):
    global fps

    win.fill(BLACK)
    if ts:
        for i, line in enumerate(ts, start=1):
            win.blit(line, (50, 50 * i))
        arr.sort()

    for i in range(len(arr)):
        color = WHITE
        if isinstance(redEls, tuple):
            if i in redEls:
                color = RED
        else:
            if i == redEls or sorted == True:
                color = RED
        if isinstance(greenEls, tuple):
            if i in greenEls:
                color = GREEN
        else:
            if i == greenEls:
                color = GREEN
        if i == blueEls:
            color = BLUE

        if last == True:
            color = GREEN
            if array_width == 2: # if we are sorting a large array increase the rate at which the green sorted bars appear, so it doesn't look very slow
                clock.tick(0)
            else:
                clock.tick(120)
            pygame.display.update()

        pygame.draw.rect(win, color, (padding + array_width * i, s_height - 5 - arr[i], array_width - 1, arr[i]))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit(), sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if fps > 1500:
                    fps = 1500
                fps += fps * 1.05
            if event.button == 5:
                fps -= fps / 1.05
                if fps < 10:
                    fps = 10

    clock.tick(fps)

def sort(win, arr, sort_type):
    if sort_type == 'quicksort' or sort_type.startswith('q'):
        start = 0
        end = len(arr) - 1
        array_generator = sorts.quicksort(arr, start, end)
        for array, red, green in array_generator:
            update_graph(win, array, redEls=red, greenEls=green)
        update_graph(win, array, last=True)
    elif sort_type == 'mergesort' or sort_type.startswith('m'):
        start = 0
        end = len(arr) - 1
        array_generator = sorts.mergesort(arr, start, end)
        for array, red, blue, green in array_generator:
            update_graph(win, array, redEls=red, blueEls=blue, greenEls=green)
        update_graph(win, array, last=True)
    else:
        if sort_type == 'bubblesort' or sort_type.startswith('b'):
            sort_type = sorts.bubblesort
        elif sort_type == 'selectionsort' or sort_type.startswith('s'):
            sort_type = sorts.selectionsort
        elif sort_type == 'insertionsort' or sort_type.startswith('i'):
            sort_type = sorts.insertionsort

        array_generator = sort_type(arr)
        for array, bigger, smaller in array_generator:
            update_graph(win, array, redEls=smaller, greenEls=bigger)
        update_graph(win, array, last=True)

    return True, array

def main():
    global clock, fps

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 25)

    s_width, s_height, win, sort_type, N = setup()
    array, fps = array_setup(s_width, N)

    finished = False
    pygame.event.clear()
    while True:
        multi_line_text = [font.render('Spacebar - shuffle & sort', False, (255, 255, 255)), font.render('Scroll up / down - speed up / slow down', False, (255, 255, 255))]
        if finished:
            multi_line_text.append(font.render('r - sort a new shuffled array', False, (255, 255, 255)))
        update_graph(win, array, ts=multi_line_text)

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()
        # check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit(), sys.exit()
            if event.key == pygame.K_SPACE and finished != True:
                shuffle(array)
                finished, array = sort(win, array, sort_type)
            if event.key == pygame.K_r and finished == True:
                shuffle(array)
                sort(win, array, sort_type)

if __name__ == '__main__':
    main()