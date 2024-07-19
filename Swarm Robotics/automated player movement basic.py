import pygame
from random import choice

# Define constants
cols, rows = 2, 2
TILE = 100
RES = WIDTH, HEIGHT = TILE * cols, TILE * rows

# Define colors using named constants
COLOR_BACKGROUND = pygame.Color("white")
COLOR_VISITED = pygame.Color('white')
COLOR_WALL = pygame.Color("black")
COLOR_CURRENT_CELL = pygame.Color('#f70067')

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Player:
    def __init__(self,player_type,TILE):
        self.x = 5
        self.y = 5
        self.grid_x=self.x//TILE
        self.grid_y=self.y//TILE
        self.player_type = player_type
        if self.player_type == 1:
            self.icon=pygame.image.load("police.png")
            self.icon=pygame.transform.scale(self.icon,(TILE-10,TILE-10))
            self.icon_area=self.icon.get_rect()
        elif player_type == 0:
            self.icon=pygame.image.load("robber.png")
            self.icon=pygame.transform.scale(self.icon,(TILE-10,TILE-10))
            self.icon_area=self.icon.get_rect()
            
    def move(self, dx, dy,maze):
        new_x = self.x + dx
        new_y = self.y + dy
#         if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
#             self.x = new_x
#             self.y = new_y
        self.x = new_x
        self.y = new_y
        self.grid_x=self.x//TILE
        self.grid_y=self.y//TILE
            
    def draw(self, screen):
        screen.blit(self.icon,(self.x,self.y),self.icon_area)
        return screen
        

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, COLOR_CURRENT_CELL, (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, COLOR_VISITED, (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, COLOR_WALL, (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, COLOR_WALL, (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, COLOR_WALL, (x + TILE, y + TILE), (x, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, COLOR_WALL, (x, y + TILE), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze_logic():
    current_cell = grid_cells[0]
    stack = []

    while True:
        current_cell.visited = True
        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

def maze_generator(cols, rows, TILE, animate=False):
    global grid_cells, sc, clock

    RES = WIDTH, HEIGHT = TILE * cols, TILE * rows
    sc = pygame.display.set_mode(RES)
    
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

    if not animate:
        generate_maze_logic()

    running = True
    while running:
        sc.fill(COLOR_BACKGROUND)
        [cell.draw() for cell in grid_cells]
        
        if animate:
            current_cell = grid_cells[0]
            stack = []
            colors, color = [], 40

            while running and (current_cell or stack):
                current_cell.visited = True
                current_cell.draw_current_cell()
                [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 2, cell.y * TILE + 2, TILE - 4, TILE - 4), border_radius=8) for i, cell in enumerate(stack)]
                next_cell = current_cell.check_neighbors()
                if next_cell:
                    next_cell.visited = True
                    stack.append(current_cell)
                    colors.append((min(color, 255), 0, 103))
                    color += 1
                    remove_walls(current_cell, next_cell)
                    current_cell = next_cell
                elif stack:
                    current_cell = stack.pop()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False

                pygame.display.flip()
                clock.tick(10)
        else:
            ax=5
            ay=5
            grid_num=0
            previous_move="none"
            police1=Player(1,TILE)
            movable=[]
#             print(grid_cells[0].walls)
            for i in range(100):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                running = False
                if running == False:
                    break
                sc.fill(COLOR_BACKGROUND)
                [cell.draw() for cell in grid_cells]
                wall=grid_cells[grid_num].walls
#                 print(wall)
                if previous_move == "top":
                    movable=[direction for direction in wall.keys() if wall[direction]==False and direction!="bottom"]
                elif previous_move == "bottom":
                    movable=[direction for direction in wall.keys() if wall[direction]==False and direction!="top"]
                elif previous_move == "left":
                    movable=[direction for direction in wall.keys() if wall[direction]==False and direction!="right"]
                elif previous_move == "right":
                    movable=[direction for direction in wall.keys() if wall[direction]==False and direction!="left"]
                
                if len(movable)==0:
                    movable=[direction for direction in wall.keys() if wall[direction]==False]
                
                move_direction=choice(movable)
                print(move_direction)
                
                    
                if move_direction=="top":
                    police1.move(0,-30,0)
                    sc=police1.draw(sc)
                    grid_num-=16
                    previous_move=move_direction
                elif move_direction=="bottom":
                    police1.move(0,30,0)
                    grid_num+=16
                    sc=police1.draw(sc)
                    previous_move=move_direction
                elif move_direction=="left":
                    police1.move(-30,0,0)
                    sc=police1.draw(sc)
                    grid_num-=1
                    previous_move=move_direction
                elif move_direction=="right":
                    police1.move(30,0,0)
                    sc=police1.draw(sc)
                    grid_num+=1
                    previous_move=move_direction
                    
#                 print(movable)
                
#                 police1.move(30,0,0)
#                 sc=police1.draw(sc)
                ax+=TILE
                ay+=TILE
                pygame.display.update()
                pygame.time.wait(500)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
            pygame.display.flip()
    
    
    
    pygame.quit()
cols, rows = 16, 16
TILE = 30
maze_generator(cols, rows, TILE, animate=False)