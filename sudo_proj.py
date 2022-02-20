import pygame
import requests

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5


class SudoGenerator:

    def grid_generator(self, window):
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
                pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
            pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
            pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
        pygame.display.update()

    def sudo_init(self, window):
        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if 0 < grid[i][j] < 10:
                    value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                    window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
        pygame.display.update()

    def sudo_solver(self, window):
        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if 0 < grid_copy[i][j] < 10:
                    pygame.draw.rect(window, background_color, ((j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    if grid_original[i][j] != 0:
                        value = myfont.render(str(grid_copy[i][j]), True, original_grid_element_color)
                    elif grid_copy[i][j] == grid[i][j]:
                        value = myfont.render(str(grid_copy[i][j]), True, (0,255,0))
                    elif grid[i][j] == 0:
                        value = myfont.render(str(grid_copy[i][j]), True, (255,165,0))
                    else:
                        value = myfont.render(str(grid_copy[i][j]), True, (255, 0, 0))
                    window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
        pygame.display.update()

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
                        pygame.draw.rect(window, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        pygame.display.update()
                    if 0 < event.key - 48 < 10:  # checking for valid input
                        pygame.draw.rect(window, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))

                        value = myfont.render(str(event.key - 48), True, (0, 0, 0))
                        window.blit(value, (position[0] * 50 + 15, position[1] * 50))
                        grid[i - 1][j - 1] = event.key - 48
                        pygame.display.update()
                        return
                    return

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

    def find_empty(self, bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return i, j  # row ,col
        return False

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


if __name__ == '__main__':

    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    grid = response.json()['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

    sgen = SudoGenerator()

    # Generate Grid
    sgen.grid_generator(win)
    # Generate Initial sudoku numbers
    sgen.sudo_init(win)
    sgen.print_board(grid)
    print('------------------------------\n---------------------------\n----------------------------')

    # Get the solution
    grid_copy= [[grid_original[x][y] for y in range(len(grid_original[0]))] for x in range(len(grid_original))]
    sgen.solve(grid_copy)
    sgen.print_board(grid_copy)

    #flags
    isSolved=0

    while True:


        #Enter the numbers
        for event in pygame.event.get():
            if(isSolved == 0):
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    sgen.insert(win, (pos[0]//50, pos[1]//50))
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    sgen.sudo_solver(win)
                    isSolved =1
            if event.type == pygame.QUIT:
                pygame.quit()




