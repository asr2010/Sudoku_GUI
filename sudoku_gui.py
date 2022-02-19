#setting up py game
import pygame
import requests

WIDTH = 550
background_color = (251,247,245)
original_grid_element_color = (52, 31, 151)
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def insert (win, position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                #1. tire to edit original file
                if(grid_original[i-1][j-1] != 0):
                    return
                #2. edit
                if(event.key == 48): #checking with 0
                    grid[i-1][j-1]=event.key -48
                    pygame.draw.rect(win, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                if(0 < event.key - 48 < 10 ): #checking for valid input
                    pygame.draw.rect(win, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50 + 15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return
                #3. adding the digits

def isEmpty(num):
    if(num == 0):
        return True
    return False
def isValid(position, num):
    #Row, Col and Box Checks
    for i in range(0, len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    for i in range(0,len(grid[0])):
        if(grid[i][position[1]] == num):
            return False
    x = position[0]//3*3
    y = position[1]//3*3

    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j] == num):
                return False
    return True

solved =0
def sudoku_solver(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(isEmpty(grid[i][j])):
                for k in range(1,10):
                    if isValid((i,j),k):
                        grid[i][j] = k
                        value = myfont.render(str(k), True, (0,0,0))
                        win.blit(value, (((j+1)*50 +15,(i+1)*50)))
                        pygame.display.update()
                        #pygame.time.delay(1)

                        sudoku_solver(win)
                        global solved
                        if(solved == 1):
                            return

                        grid[i][j] = 0
                        pygame.draw.rect(win, background_color, ((j+1)*50 + buffer,(i+1)*50 + buffer, 50 -2*buffer, 50 - 2*buffer))
                        pygame.display.update()
                return
    solved =1

def genSudoku(win, difficulty):
    global grid
    global grid_original
    global response

    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    if(difficulty == 1):
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
        grid = response.json()['board']
        grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if (0 < grid[i][j] < 10):
                    value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                    win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
        pygame.display.update()


def main():

    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH+100))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    mouse = pygame.mouse.get_pos()
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    myfont2 = pygame.font.SysFont('Comic Sans MS', 14)

    for i in range (0,10):
        if (i%3 == 0):
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
        pygame.draw.line(win, (0, 0, 0), (50+50*i, 50), (50+50*i,500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50+50*i), (500, 50+50*i), 2)
        pygame.draw.rect(win, (170,170,170), [WIDTH/10, WIDTH, 50,20])
        win.blit(myfont2.render('Easy', True, original_grid_element_color), (WIDTH / 10 + 5, WIDTH))
        pygame.draw.rect(win, (170, 170, 170), [WIDTH / 4.75, WIDTH, 50, 20])
        win.blit(myfont2.render('Med', True, original_grid_element_color), (WIDTH / 4.75 + 5, WIDTH))
        pygame.draw.rect(win, (170, 170, 170), [WIDTH / 3.1, WIDTH, 50, 20])
        win.blit(myfont2.render('Hard', True, original_grid_element_color), (WIDTH / 3.1 + 5, WIDTH))
        pygame.draw.rect(win, (170, 170, 170), [WIDTH/1.5, WIDTH, 50, 20])
        win.blit(myfont2.render('Solve', True, original_grid_element_color), (WIDTH / 1.5 + 5, WIDTH))
        pygame.draw.rect(win, (170, 170, 170), [WIDTH / 1.3, WIDTH, 50, 20])
        win.blit(myfont2.render('Reset', True, original_grid_element_color), (WIDTH / 1.3 + 5, WIDTH))


    pygame.display.update()





    while True:
        for event in pygame.event.get():


            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 10 <= mouse[0] <= WIDTH / 10 + 50 and WIDTH <= mouse[1] <= WIDTH + 20:
                    genSudoku(win, 1)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0] // 50, pos[1] // 50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
main()
