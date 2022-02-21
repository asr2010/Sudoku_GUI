'''
The submission file implements Sudoku GUI using pygame and its solver in command prompt. The class SudoGenerator has the following methods that implements all the functionalities.

Prerequisite: Install pygame and requests before running the program.

Instructions to execute:
1. To execute in developer mode: python sudo_prog.py -d.
2. To execute in normal mode: python sudo_prog.py

Developer Mode: This provides access to complete solution in the terminal and provides step by step assistance in solving the sudoku.

Features and Options:
1. Solve: Solves sudoku using backtrack algorithm.
2. Reset: Sets board to the intial step of the problem
3. Counter: Keeps track of occurences of every single digit on the grid

Methods implemented:
- grid_generator: Generate the default grid and annotations for GUI.
- sudo_init: Initializes the initial numbers of the sudoku.
- sudo_solver: Provides solution to the given sudoku using sudoku.
- insert: Allows user to enter the values in blank space
- solve: Solves the given sudoku and stores the solution.
- find_empty: Check if the given grid contains any previous value or not.
- valid: Check if the provided input is valid or not.
- print_board: Print board in command prompt.
- get_sudoku: Fetch sudoku from api using 'request'.
- reset_board: Reset playing board to starting position.
- update_stats: Keeps track of occurrences of each single digit in sudoku using Dictionary Comprehension.

This application utilized user's input from both command line and GUI.


'''

# import packages
import sys
import pygame
import requests

# global Variables
WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5


# class SudoGenerator
class SudoGenerator:
    # Generate the default grid and annotations for GUI.
    def grid_generator(self, window):
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
                pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
            pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
            pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
        pygame.draw.rect(window, (0, 255, 0), (60, 510, 100, 30))
        myfont2 = pygame.font.SysFont('Comic Sans MS', 20)
        value = myfont2.render('Solve', True, (0, 0, 0))
        window.blit(value, (80,510))
        pygame.draw.rect(window, (255, 0, 0), (190, 510, 100, 30))
        value = myfont2.render('Reset', True, (0, 0, 0))
        window.blit(value, (215, 510))
        pygame.display.update()

    # Initializes the initial numbers of the sudoku.
    def sudo_init(self, window):
        for i in range(0, len(grid_original[0])):
            for j in range(0, len(grid_original[0])):
                pygame.draw.rect(
                    window,
                    background_color,
                    ((j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer)
                )
                if 0 < grid_original[i][j] < 10:
                    value = myfont.render(str(grid_original[i][j]), True, original_grid_element_color)
                    window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
        pygame.display.update()

    # Provides solution to the given sudoku using sudoku.
    def sudo_solver(self, window):
        pygame.draw.rect(win, background_color, (10, 510, 540, 30))
        myfont3 = pygame.font.SysFont('Comic Sans MS', 20)
        value = myfont3.render('Red: Invalid;    Green: Correct;    Orange: Expected', True, (0, 0, 0))
        window.blit(value, (35, 510))

        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if 0 < grid_copy[i][j] < 10:
                    pygame.draw.rect(
                        window,
                        background_color,
                        ((j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer)
                    )
                    if grid_original[i][j] != 0:
                        value = myfont.render(str(grid_copy[i][j]), True, original_grid_element_color)
                    elif grid_copy[i][j] == grid[i][j]:
                        value = myfont.render(str(grid_copy[i][j]), True, (0, 255, 0))
                    elif grid[i][j] == 0:
                        value = myfont.render(str(grid_copy[i][j]), True, (255, 165, 0))
                    elif grid_copy[i][j] != grid[i][j]:
                        value = myfont.render(str(grid_copy[i][j]), True, (255, 0, 0))
                    window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

        pygame.display.update()

    # Allows user to enter the values in blank space.
    def insert(self, window, position):
        i, j = position[1], position[0]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # 1. tire to edit original file
                    if grid_original[i - 1][j - 1] != 0:
                        return
                    # 2. edit
                    if event.key == 48:  # checking with 0
                        grid[i - 1][j - 1] = event.key - 48
                        pygame.draw.rect(
                            window,
                            background_color,
                            (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer)
                        )
                        pygame.display.update()
                    if 0 < event.key - 48 < 10:  # checking for valid input
                        pygame.draw.rect(window, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        font_color = (0, 0, 0)
                        if dev:
                            if str(grid_copy[i-1][j-1]) == str(event.key - 48):
                                print('\nValid Input')
                                font_color = (0, 255, 0)
                            else:
                                print('\nInvalid Input')
                                font_color = (255, 0, 0)

                        value = myfont.render(str(event.key - 48), True, font_color)
                        window.blit(value, (position[0] * 50 + 15, position[1] * 50))
                        grid[i - 1][j - 1] = event.key - 48
                        pygame.display.update()
                        return
                    return

    # Solves the given sudoku using the back-track algorithm and stores the solution
    def solve(self, bo):

        find = self.find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(bo, i, (row, col)):
                bo[row][col] = i

                if self.solve(bo):
                    return True

                bo[row][col] = 0
        return False

    # Check if the given grid contains any previous value or not.
    def find_empty(self, bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return i, j  # row ,col
        return False

    # Check if the provided input is valid or not.
    def valid(self, bo, num, pos):
        # check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False
        # Check Column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check Box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False
        return True

    # Print board in command prompt.
    def print_board(self, bo):

        for i in range(len(bo)):
            if i % 3 == 0 and i != 0:
                print("-----------------------")

            for j in range(len(bo[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(bo[i][j])
                else:
                    print(str(bo[i][j]) + " ", end="")

    # Fetch sudoku from api using 'request'.
    def get_sudoku(self, level):
        if level == 1:
            request_str = "https://sugoku.herokuapp.com/board?difficulty=easy"
        elif level == 2:
            request_str = "https://sugoku.herokuapp.com/board?difficulty=medium"
        else:
            request_str = "https://sugoku.herokuapp.com/board?difficulty=hard"

        # try-execute to handle failure of API endpoints
        try:
            res = requests.get(request_str)
            if res.text == '{"board":[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]}\n':
                raise ConnectionError
        except ConnectionError:
            res = 0

        return res

    # Reset playing board to starting position.
    def reset_board(self, win):
        sgen.sudo_init(win)
        global grid
        grid = [[grid_original[x][y] for y in range(len(grid_original[0]))] for x in range(len(grid_original))]
        pygame.draw.rect(win, background_color, (10, 10, 540, 30))
        pygame.display.update()
        # print(grid)

    # Update the counter keeping the track of occurrences of each single digit in sudoku.
    def update_stats(self, window):
        # Generation of occurrence tracker using dictionary comprehension.
        d = {n: sum(x.count(n) for x in grid) for n in range(1, 10)}
        if dev:
            print(d)
        myfont2 = pygame.font.SysFont('Comic Sans MS', 20)
        pygame.draw.rect(window, background_color,(120,10 ,420 ,30 ))
        value = myfont2.render('Counter:   '+str(d), True, (0, 0, 0))
        window.blit(value, (15, 10))
        pygame.display.update()


# 1. python module __main__
if __name__ == '__main__':

    dev = False
    try:
        if sys.argv[1] == '-d':
            dev = True
            print('\nWelcome to dev mode!\n')
    except IndexError:
        dev = False

    pygame.init()
    win = pygame.display.set_mode((WIDTH , WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    sgen = SudoGenerator()

    response = sgen.get_sudoku(1)
    if response == 0:
        grid = [
            [0, 0, 0, 9, 0, 0, 0, 0, 2],
            [0, 0, 0, 4, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 5, 0, 0, 9, 0, 7, 0],
            [3, 0, 6, 7, 0, 0, 5, 0, 0],
            [7, 0, 0, 0, 6, 5, 0, 0, 0],
            [0, 3, 2, 0, 0, 1, 8, 5, 7],
            [5, 6, 1, 0, 7, 0, 9, 0, 3],
            [9, 8, 7, 5, 2, 0, 0, 1, 6]
        ]
    else:
        grid = response.json()['board']

    # store original copy of the sudoku board for future comparisons
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

    # Generate Grid
    sgen.grid_generator(win)
    # Generate Initial sudoku numbers
    sgen.sudo_init(win)
    if dev:
        print("Problem: ")
        sgen.print_board(grid)
        print('------------------------------\n------------------------------')

    # Get the solution
    grid_copy= [[grid_original[x][y] for y in range(len(grid_original[0]))] for x in range(len(grid_original))]
    sgen.solve(grid_copy)
    if dev:
        print('Solution:')
        sgen.print_board(grid_copy)

    # flags
    isSolved=0

    while True:
        # Enter the numbers
        for event in pygame.event.get():
            if isSolved == 0:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 60 <= pos[0] <= 160 and 510 <= pos[1] <= 540:
                        sgen.sudo_solver(win)
                        isSolved = 1
                    elif 190 <= pos[0] <= 290 and 510 <= pos[1] <= 540:
                        sgen.reset_board(win)
                    else:
                        sgen.insert(win, (pos[0]//50, pos[1]//50))
                        sgen.update_stats(win)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    sgen.sudo_solver(win)
                    isSolved = 1
            if event.type == pygame.QUIT:
                pygame.quit()




