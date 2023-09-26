import pygame

'''
Path finder based on the A-star algorithm
Finds shortest path and creates arrows throughout maze
'''

# Path class that stores information about individual cells
class path():
    def __init__(self, x, y, parent, f_value, h_value) -> None:
        self.x = x
        self.y = y
        self.parent = parent
        self.f_value = f_value
        self.h_value = h_value
# Wall class
class wall():
    def __init__(self) -> None:
        pass

# Functions to calculate h_value and f_value
def h_value(x, y, end):
    return abs(end[0] - x) + abs(end[1] - y)
def f_value(x, y, end):
    h_value(x,y,end)

mymaze2 = []
# Take in input and create 2D list which represents the maze, find start and end
with open("maze.txt", "r") as file:
    mymaze1 = file.readlines()
for a in mymaze1:
    mymaze2.append(a.replace('\n', ''))
    

number = 11
maze = []
for a in range(len(mymaze2)):
    maze.append(list(mymaze2[a]))
start = []
end = []
for a in range(number):
    if maze[a][0] == 'p':
        start.append(0)
        start.append(a)
    if maze[a][len(maze[a])-1] == 'p':
        end.append(len(maze[a])-1)
        end.append(a)

# Create a 2D list of path and wall objects
new_maze = [[] for y in range(number)]  
for a in range(number):
    for b in range(len(maze[a])):
        if maze[a][b] == '#':
            item = wall()
            new_maze[a].append(item)
        else:
            item = path(b, a, [], 0, h_value(b, a, end))
            new_maze[a].append(item)

# ---Main A-star algorithm---
open = []
closed = []
open.append(new_maze[start[1]][start[0]])
current = open[0]
while True:
    current = open[0]
    for a in range(len(open)):
        if open[a].f_value < current.f_value:
            current = open[a]
    open.remove(current)
    closed.append(current)
    if current.x == end[0] and current.y == end[1]:
        end_x = current.x
        end_y = current.y
        break
    else:
        if current.y - 1 >= 0:
            top = new_maze[current.y - 1][current.x]
            if (type(top) != wall) and top not in closed:
                if top.f_value > current.f_value + 1 or top not in closed or top.f_value == 0:
                    top.f_value = h_value(top.x, top.y, end) + current.f_value - current.h_value + 1
                    top.parent.append(current.x)
                    top.parent.append(current.y)
                    if top not in open:
                        open.append(top)
        if current.y + 1 < number:
            bot = new_maze[current.y + 1][current.x]
            if (type(bot) != wall) and bot not in closed:
                if (bot.f_value > current.f_value + 1) or (bot not in closed) or (bot.f_value == 0):
                    bot.f_value = h_value(bot.x, bot.y, end) + current.f_value - current.h_value + 1
                    bot.parent.append(current.x)
                    bot.parent.append(current.y)
                    if bot not in open:
                        open.append(bot)
                
        if current.x + 1 < len(maze[0]):
            right = new_maze[current.y][current.x + 1]
            if (type(right) != wall) and right not in closed:
                if (right.f_value > current.f_value + 1) or (right not in closed) or (right.f_value == 0):
                    right.f_value = h_value(right.x, right.y, end) + current.f_value - current.h_value + 1
                    right.parent.append(current.x)
                    right.parent.append(current.y)
                    if right not in open:
                        open.append(right)

        if current.x - 1 >= 0:
            left = new_maze[current.y][current.x - 1]
            if (type(left) != wall) and left not in closed:
                if (left.f_value > current.f_value + 1) or (left not in closed) or (left.f_value == 0):
                    left.f_value = h_value(left.x, left.y, end) + current.f_value - current.h_value + 1
                    left.parent.append(current.x)
                    left.parent.append(current.y)
                    if left not in open:
                        open.append(left)
final_list = []
# Create arrows throughout original input using the parents of paths
counter = 1
while True:
    counter += 1
    cur_maze = new_maze[end_y][end_x]
    final_list.append(cur_maze)
    if end_y > cur_maze.parent[1]:
        maze[cur_maze.parent[1]][cur_maze.parent[0]] = 'v'
    elif end_y < cur_maze.parent[1]:
        maze[cur_maze.parent[1]][cur_maze.parent[0]] = '^'
    elif end_x < cur_maze.parent[0]: 
        maze[cur_maze.parent[1]][cur_maze.parent[0]] = '<'
    else:
        maze[cur_maze.parent[1]][cur_maze.parent[0]] = '>'     
    end_y = cur_maze.parent[1]
    end_x = cur_maze.parent[0]
    if start[0] == end_x and start[1] == end_y:
        maze[end_y][end_x] = '>'
        maze[end[1]][end[0]] = '>'
        break

# Print out the orignal maze with arrows
print()
for a in range(number):
    for b in range(len(maze[0])):
        print(maze[a][b], end = '')
    print()
print(f"The length of the minimum path = {counter}")




pygame.init()
screen_height = 880
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Maze")

def grid():
    for a in range(0, screen_width, 80):
        for b in range(0, screen_height, 80):
            if type(new_maze[b//80][a//80]) == wall: 
                pygame.draw.rect(screen, (133, 133, 133), (1+a, 1+b, 78, 78))
            elif type(new_maze[b//80][a//80]) == path:
                pygame.draw.rect(screen, (255, 255, 255), (1+a, 1+b, 78, 78))
def solve(listf, startx, starty):
    pygame.draw.rect(screen, (0, 0, 255), (startx*80+1, starty*80+1, 78, 78))
    for a in listf[::-1]:
        pygame.time.wait(200)
        pygame.draw.rect(screen, (0, 255, 0), (a.x*80+1, a.y*80+1, 78, 78))
        pygame.display.update()
    
def solve_keep(listf, startx, starty):
    pygame.draw.rect(screen, (0, 0, 255), (startx*80+1, starty*80+1, 78, 78))
    for a in listf[::-1]:
        pygame.draw.rect(screen, (0, 255, 0), (a.x*80+1, a.y*80+1, 78, 78))
finished = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    grid()
    if finished != True:
        solve(final_list, start[0], start[1])
        finished = True
    solve_keep(final_list, start[0], start[1])
    pygame.display.update()