import pygame
import sorting_algorithms.sorts as sorts
from random import randint, shuffle
import copy
import sys

pygame.init()

BLACK = (0, 0, 0)
HOVERED = (192, 253, 251)
WHITE = (255, 255, 255)
RED = (204, 25, 42)
GREEN = (51, 229, 51)
BLUE = (41, 41, 255)

def setup():
    global cell_width, cell_height
    # set up the main surface, give it a caption and extract it's width and height..
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Visualizing Sort Algorithms')
    s_width, s_height = pygame.display.get_surface().get_size()
    # find out how much would 1 quadrant of the screen be and then create the sections list
    # which will multiply the x, y coordinates by the corresponding value, to draw the rectangles in the corresponding section of the screen
    cell_width = s_width // 3
    cell_height = s_height // 2
    sections = ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1))
    return win, sections

def array_setup(sections, size):
    global arr_width, padding

    highest_number = cell_height - 10
    padding = 20
    max_awidth = cell_width - padding

    if size == 3:
        N = int(max_awidth / 10)
    elif size == 4:
        N = int(max_awidth // 8)
    else:
        N = int(max_awidth / 5)
    arr_width = int(max_awidth / N)

    array = [randint(1, highest_number) for _ in range(N)]
    shuffle(array)

    return array

def blit_text(win, speedC=None, sizeC=None, hovered=None):
    ''' function to blit the menu text on the screen and at the proper coordinates
        not flexible for different resolutions as for now'''
    win.blit(font.render('spacebar - shuffle & sort', False, WHITE), (cell_height, cell_height // 6))

    # create a colors list, so you can give the picked index the green color
    colors = [WHITE] * 6
    if hovered is not None:
        colors[hovered] = HOVERED
    if speedC is not None:
        colors[speedC] = GREEN
    if sizeC is not None:
        colors[sizeC] = GREEN

    # create a list of the font render objects and blit them on the screen with their corresponding positions
    speed_text = [font.render('Choose sorting speed:', False, WHITE), font.render('slow', False, colors[0]), font.render('normal', False, colors[1]), font.render('fast', False, colors[2])]
    position = (cell_width // 5, cell_width // 2)
    win.blit(speed_text[0], (position[0], position[1]))
    speed_s = win.blit(speed_text[1], (position[0], int(position[1] * 1.5)))
    speed_n = win.blit(speed_text[2], (position[0], position[1] * 2))
    speed_f = win.blit(speed_text[3], (position[0], int(position[1] * 2.5)))

    size_text = [font.render('Choose array size:', False, WHITE), font.render('small', False, colors[3]), font.render('medium', False, colors[4]),  font.render('large', False, colors[5])]
    position = (cell_width * 1.9 , cell_width // 2)
    win.blit(size_text[0], (position[0], position[1]))
    size_s = win.blit(size_text[1], (position[0], int(position[1] * 1.5)))
    size_m = win.blit(size_text[2], (position[0], position[1] * 2))
    size_l = win.blit(size_text[3], (position[0], int(position[1] * 2.5)))

    # return a list of the speed - indexes 0-2, and size 3-5
    return (speed_s, speed_n, speed_f, size_s, size_m, size_l)

def update_bars(win, arr, pos=None, redEls=None, blueEls=None, greenEls=None, finished=False, bogo=False):
    ''' function to update the sort graphs on the screen '''
    global fps, arr_width

    n = len(arr)
    # loop trough the element's indexes, so to make the coloured elements unique - opposite to by value becasue the array is random and there might be 2 items with the same value
    for i in range(n):
        color = WHITE
        # all the isinstance(x, tuple) checks, check if there are more than 1 elements to be painted(insertion sort)
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
        # no need to check for a tuple of blueEls, because we never have more than 1 blue element :)
        if i == blueEls:
            color = BLUE
        # check if the array has finished sorting or not
        if finished == True:
            color = GREEN
            clock.tick(0)

        a_width = arr_width
        # create special elements width for the BOGO SORT!!!
        if bogo == True:
            a_width = int(cell_width - 15) // len(arr)

        # just some tinkering with the padding of the sections
        offset = 0
        if pos[0] == 0:
            offset = padding
        if pos[0] == 1:
            offset = padding // 2
        pygame.draw.rect(win, color, (offset + a_width * i + (cell_width * pos[0]), cell_height - arr[i] + (cell_height * pos[1]), a_width-1, arr[i]))

    clock.tick(fps)

def sort(win, arr, sections):
    # start, end variables for merge and quicksort
    start = 0
    end = len(arr) - 1
    # set up the array generators
    marr = copy.deepcopy(arr)
    ms_gen = sorts.mergesort(marr, start, end)
    barr = copy.deepcopy(arr)
    bs_gen = sorts.bubblesort(barr)
    qarr = copy.deepcopy(arr)
    qs_gen = sorts.quicksort(qarr, start, end)
    sarr = copy.deepcopy(arr)
    ss_gen = sorts.selectionsort(sarr)
    iarr = copy.deepcopy(arr)
    is_gen = sorts.insertionsort(iarr)
    # bogo sort is special case :D
    bsArray = [randint(1, cell_height - 10) for n in range(6)]
    shuffle(bsArray)
    bogos_gen = sorts.bogosort(bsArray)
    # create a dictionary, so to know how many elements to except (merge and quicksort yield 4, while all others except bogo 3, and bogo only 1)
    generators = {bs_gen: 'b', ss_gen: 's', is_gen: 'i', ms_gen: 'm', qs_gen: 'q', bogos_gen: 'bogo'}
    breakCounter = 0 # break counter increments on generator depletion, if breakCounter == len(generators): break; self-explanatory
    while True:
        win.fill(BLACK)
        # enumerate the loop, so to get the approriate section. i.e index = 3, section[3] = (2, 0) = top right section...
        for index, (gen, sort_type) in enumerate(generators.items()):
            try:
                if sort_type == 'm':
                    array, red, blue, green = next(gen)
                    update_bars(win, array, pos=sections[index], redEls=red, blueEls=blue, greenEls=green)
                elif sort_type == 'bogo':
                    array = next(gen)
                    update_bars(win, array, pos=sections[index], bogo=True)
                elif sort_type in ('b', 's', 'i', 'q'):
                    array, red, green = next(gen)
                    update_bars(win, array, pos=sections[index], redEls=red, greenEls=green)
                # if a sort has finished run the update_bars function with 'finished' attribute set to True
                if sort_type == 'finished':
                    # check if the array is bogo, to return a sorted bogo array :DD
                    if gen != 'bogo':
                        update_bars(win, sorted(arr), pos=sections[index], finished=True)
                    else:
                        update_bars(win, sorted(bsArray), pos=sections[index], finished=True)
            # on generator depletion, set it's sort_type to finished and increment breakCounter variable
            except StopIteration:
                generators[gen] = 'finished'
                breakCounter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(), sys.exit()
        if breakCounter == len(generators):
            break

        pygame.display.update()

    return True

def main():
    global clock, fps, font

    # create a clock object to set the fps
    clock = pygame.time.Clock()
    # create font object, and speedColor and sizeColor variables which hold the index of the chosen size/speed in the menu
    font = pygame.font.SysFont('Comic Sans MS', 60)
    speedC, sizeC, hover = None, None, None
    # get the main surface and the sections list from the setup function
    win, sections = setup()
    finished = False
    while True:
        win.fill(BLACK)
        rects = blit_text(win, speedC, sizeC, hover) # get the list of speed and size

        # check the event queue for exit buttons, space - the start sort button and left mouse click to check wheter one of the boxes has been selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            # check for key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(), sys.exit()
                if event.key == pygame.K_SPACE and None not in (speedC, sizeC): # the None not in part is to check wheter both speed and size has been selected therefore None is not a part of them
                    array = array_setup(sections, size=sizeC) # set up the array
                    # set the speed according to the chosen one
                    if speedC == 0:
                        fps = 30
                    elif speedC == 1:
                        fps = 100
                    elif speedC == 2:
                        fps = 300

                    sort(win, array, sections=sections)
            hover = [rect.collidepoint(pygame.mouse.get_pos()) for rect in rects]
            if 1 in hover:
                hover = hover.index(1)
            else:
                hover = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # event button 1 == left click
                for index, rect in enumerate(rects):
                    # widen the text's rect width, so the click is not stricly restricted to the text visual
                    rect.x -= 60
                    rect.w += 140
                    click = rect.collidepoint(pygame.mouse.get_pos())

                    if click == 1:
                        if index < 3: # if the enumeration index is less than 3, then one of the speed boxes has been chosen, either one of the size ones
                            speedC = index
                        else:
                            sizeC = index


        pygame.display.update()


if __name__ == '__main__':
    main()