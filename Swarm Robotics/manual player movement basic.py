import pygame
from random import choice


# Define colors using named constants
COLOR_BACKGROUND = pygame.Color('#a6d5e2')
COLOR_VISITED = pygame.Color('white')
COLOR_WALL = pygame.Color('#1e4f5b')
COLOR_CURRENT_CELL = pygame.Color('#f70067')
DEFAULT_COLOR_HIGHLIGHT = pygame.Color('yellow')  # New color for highlighting
CURRENT_COLOR_HIGHLIGHT = pygame.Color(255,0,0)  # New color for highlighting
DETECT_COLOR_HIGHLIGHT=pygame.Color('blue')

# Image paths
POLICE_IMAGE_PATH = "police.png"
ROBBER_IMAGE_PATH = "robber.png"

pygame.init()

class Player:
    def __init__(self, player_type, TILE, cell_ran, grid_num, player_id):
        self.x = 5 + cell_ran[0] * TILE  # Starting position x
        self.y = 5 + cell_ran[1] * TILE  # Starting position y
        self.grid_x = self.x // TILE  # Grid position x
        self.grid_y = self.y // TILE  # Grid position y
        self.grid_num = grid_num  # Grid number
        self.player_type = player_type  # Player type (police or robber)
        self.player_id = player_id  # Player ID
        self.visible_cells={"top":[],
                            "bottom":[],
                            "left":[],
                            "right":[],}
        self.all_visible_cells=[]
        self.police_cell_visited=set()
        self.robber_cell_visited=set()
        
        try:
            if self.player_type == 1:
                self.icon = pygame.image.load(POLICE_IMAGE_PATH)
            elif self.player_type == 0:
                self.icon = pygame.image.load(ROBBER_IMAGE_PATH)
            self.icon = pygame.transform.scale(self.icon, (TILE - 10, TILE - 10))
            self.icon_area = self.icon.get_rect()
        except pygame.error as e:
            print(f"Error loading image: {e}")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.grid_x = self.x // TILE
        self.grid_y = self.y // TILE

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y), self.icon_area)
        return screen
    
    def update_grid_num(self, grid_num,TOP_VISIBLE_CELLS,BOTTOM_VISIBLE_CELLS,LEFT_VISIBLE_CELLS,RIGHT_VISIBLE_CELLS):
        self.grid_num = grid_num
        self.visible_cells["top"] = TOP_VISIBLE_CELLS
        self.visible_cells["bottom"] = BOTTOM_VISIBLE_CELLS
        self.visible_cells["left"] = LEFT_VISIBLE_CELLS
        self.visible_cells["right"] = RIGHT_VISIBLE_CELLS
        
        if self.player_type == 1:
            self.all_visible_cells=TOP_VISIBLE_CELLS+BOTTOM_VISIBLE_CELLS+LEFT_VISIBLE_CELLS+RIGHT_VISIBLE_CELLS
            self.police_cell_visited.add(grid_num)
#             print(self.police_cell_visited)

        if self.player_type == 0:    
            self.robber_cell_visited.add(grid_num)
            
    def top(self):
        return "top"
    def left(self):
        return "left"
    def bottom(self):
        return "bottom"
    def right(self):
        return "right"
    
    def stop(self):
        pass
        
        
        

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y  # Position of the cell
        

        
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}  # Walls of the cell

        
        self.visited = False  # Visited state of the cell

    def draw_current_cell(self, sc):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, COLOR_CURRENT_CELL, (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self, sc, color=COLOR_VISITED,x=0,y=0,wall_info=None):
        if x+y==0:
            x, y = self.x * TILE, self.y * TILE
            
            if self.visited:
                pygame.draw.rect(sc, color, (x, y, TILE, TILE))
            if self.walls['top']:
                pygame.draw.line(sc, COLOR_WALL, (x, y), (x + TILE, y), 3)
            if self.walls['right']:
                pygame.draw.line(sc, COLOR_WALL, (x + TILE, y), (x + TILE, y + TILE), 3)
            if self.walls['bottom']:
                pygame.draw.line(sc, COLOR_WALL, (x + TILE, y + TILE), (x, y + TILE), 3)
            if self.walls['left']:
                pygame.draw.line(sc, COLOR_WALL, (x, y + TILE), (x, y), 3)

            
            
            
        else:
            x, y = x * TILE, self.y * TILE
            
            if self.visited:
                pygame.draw.rect(sc, color, (x, y, TILE, TILE))
            
            movable = [d for d in wall_info.keys() if wall_info[d]]

            if "top" in movable:
                pygame.draw.line(sc, COLOR_WALL, (x, y), (x + TILE, y), 3)
            if "right" in movable:
                pygame.draw.line(sc, COLOR_WALL, (x + TILE, y), (x + TILE, y + TILE), 3)
            if "bottom" in movable:
                pygame.draw.line(sc, COLOR_WALL, (x + TILE, y + TILE), (x, y + TILE), 3)
            if "left" in movable:
                pygame.draw.line(sc, COLOR_WALL, (x, y + TILE), (x, y), 3)
        

    def check_cell(self, x, y, cols, rows, grid_cells):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, cols, rows, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
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

def generate_maze_logic(grid_cells, cols, rows, loop_percent):
    current_cell = grid_cells[0]
    stack = []

    while True:
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(cols, rows, grid_cells)
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break
    
    add_loops(grid_cells, cols, rows, loop_percent)

def add_loops(grid_cells, cols, rows, loop_percent):
    num_cells = cols * rows
    num_loops = int((loop_percent / 100) * num_cells)
    
    for _ in range(num_loops):
        while True:
            cell = choice(grid_cells)
            direction = choice(['top', 'right', 'bottom', 'left'])
            
            if direction == 'top' and cell.y > 0:
                neighbor = cell.check_cell(cell.x, cell.y - 1, cols, rows, grid_cells)
                if neighbor and cell.walls['top'] and neighbor.walls['bottom']:
                    cell.walls['top'] = False
                    neighbor.walls['bottom'] = False
                    break
            elif direction == 'right' and cell.x < cols - 1:
                neighbor = cell.check_cell(cell.x + 1, cell.y, cols, rows, grid_cells)
                if neighbor and cell.walls['right'] and neighbor.walls['left']:
                    cell.walls['right'] = False
                    neighbor.walls['left'] = False
                    break
            elif direction == 'bottom' and cell.y < rows - 1:
                neighbor = cell.check_cell(cell.x, cell.y + 1, cols, rows, grid_cells)
                if neighbor and cell.walls['bottom'] and neighbor.walls['top']:
                    cell.walls['bottom'] = False
                    neighbor.walls['top'] = False
                    break
            elif direction == 'left' and cell.x > 0:
                neighbor = cell.check_cell(cell.x - 1, cell.y, cols, rows, grid_cells)
                if neighbor and cell.walls['left'] and neighbor.walls['right']:
                    cell.walls['left'] = False
                    neighbor.walls['right'] = False
                    break
                    
def ran_dom(cols, rows, grid_cells):
    cell_nums = [i for i in range(cols * rows)]
    cell_num = choice(cell_nums)
    cell = grid_cells[cell_num]
    return ([cell.x, cell.y], cell_num)
def get_direction(event):
    direction_keys = {
        pygame.K_w: "top",
        pygame.K_a: "left",
        pygame.K_s: "bottom",
        pygame.K_d: "right",
        pygame.K_1: "0",
        pygame.K_2: "1",
        pygame.K_3: "2",
        pygame.K_4: "3",
        pygame.K_5: "4",
        pygame.K_6: "5",
        pygame.K_7: "6",
        pygame.K_8: "7",
        pygame.K_9: "8",
        pygame.K_0: "9"
    }
    if event.type == pygame.KEYDOWN:
        return direction_keys.get(event.key, "none")



def manual_movement(player, direction, grid_cells, tile, player_number,maze_desc):
    TOP_VISIBLE_CELLS=[]
    BOTTOM_VISIBLE_CELLS=[]
    LEFT_VISIBLE_CELLS=[]
    RIGHT_VISIBLE_CELLS=[]
        
    cols, rows, TILE = maze_desc  # Unpack the list into cols, rows, and TILE
    grid_num = player.grid_num
    wall = grid_cells[grid_num].walls
    movable = [d for d in wall.keys() if not wall[d]]
    COLOR_HIGHLIGHT = DEFAULT_COLOR_HIGHLIGHT
    if player.player_id == player_number:
        COLOR_HIGHLIGHT = CURRENT_COLOR_HIGHLIGHT
        if direction == "top" and direction in movable:
            player.move(0, -tile)
            grid_num -= cols
        elif direction == "bottom" and direction in movable:
            player.move(0, tile)
            grid_num += cols
        elif direction == "left" and direction in movable:
            player.move(-tile, 0)
            grid_num -= 1
        elif direction == "right" and direction in movable:
            player.move(tile, 0)
            grid_num += 1
            

    for direction in movable:
        start_y = grid_num // cols

        for y in range(start_y, -1, -1):
            cell = grid_cells[grid_num - (start_y - y) * cols]
#             cell.draw(sc, color=COLOR_HIGHLIGHT)
            TOP_VISIBLE_CELLS.append(grid_num - (start_y - y) * cols)
            if cell.walls['top']:
                break

        for y in range(start_y, rows):
            cell = grid_cells[grid_num + (y - start_y) * cols]
#             cell.draw(sc, color=COLOR_HIGHLIGHT)
            BOTTOM_VISIBLE_CELLS.append(grid_num + (y - start_y) * cols)

            if cell.walls['bottom']:
                break

        start_x = grid_num % cols

        for x in range(start_x, -1, -1):
            cell = grid_cells[grid_num - (start_x - x)]
#             cell.draw(sc, color=COLOR_HIGHLIGHT)
            LEFT_VISIBLE_CELLS.append(grid_num - (start_x - x))
            if cell.walls['left']:
                break

        for x in range(start_x, cols):
            cell = grid_cells[grid_num + (x - start_x)]
#             cell.draw(sc, color=COLOR_HIGHLIGHT)
            RIGHT_VISIBLE_CELLS.append(grid_num + (x - start_x))
            if cell.walls['right']:
                break
        
        player.update_grid_num(grid_num,TOP_VISIBLE_CELLS,BOTTOM_VISIBLE_CELLS,LEFT_VISIBLE_CELLS,RIGHT_VISIBLE_CELLS)
    return grid_num



def maze_generator(maze_desc, num_of_players):
    cols, rows, TILE, loop_percent = maze_desc  # Unpack the list into cols, rows, and TILE
    maze_desc = cols, rows, TILE
    global grid_cells, sc, clock
    RES = WIDTH, HEIGHT = TILE * (cols * 2+1), TILE * rows
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    
    running = True #condition for loop to exist and terminate
    
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]# making col*row cell objects
    generate_maze_logic(grid_cells, cols, rows, loop_percent)# make the maze

    
    player_number = 0 #index of moving player set to first/0th player
    player_ids = [str(i) for i in range(len(num_of_players))]  # List of all the players as strings
    players= [Player(player_type, TILE, *ran_dom(cols, rows, grid_cells), ids) for ids, player_type in enumerate(num_of_players)]  # List of all player objects



    visited_cells=set()
    police_visible_cells=set()
    while running:
        current_police_visible_cells=set()
        sc.fill(COLOR_BACKGROUND)
        for x in range(0,cols*rows):
            [grid_cells[x].draw(sc,x=(x%cols)+cols+1,wall_info=grid_cells[x].walls)]
        
        
        
#         [cell.draw(sc) for cell in grid_cells]
        
        [grid_cells[cell].draw(sc) for cell in visited_cells]
        
        key_press = "none"
        for player1 in players:
            
            
            
            for cell in player1.all_visible_cells:
                visited_cells.add(cell)
                
            
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                key_press = get_direction(event)
                if key_press:
                    break

            if key_press in player_ids:
                player_number = int(key_press)
            grid_num = manual_movement(player1, key_press, grid_cells, TILE, player_number,maze_desc)
            
            for player1 in players:
                if player1.player_id != player_number:
                    [grid_cells[cell].draw(sc,color=DEFAULT_COLOR_HIGHLIGHT) for cell in player1.all_visible_cells]
                    
                    
            for player1 in players:
                if player1.player_id == player_number:
                    selected_player_visible_cells=player1.all_visible_cells
                    [grid_cells[cell].draw(sc,color=CURRENT_COLOR_HIGHLIGHT) for cell in player1.all_visible_cells]
#                     sc.blit(player1.icon, (player1.x, player1.y), player1.icon_area)
                if player1.player_type==1:
                    for cel in player1.all_visible_cells:
                        police_visible_cells.add(cel)
                        current_police_visible_cells.add(cel)
                    
            for player1 in players:
#                 if player1.player_id != player_number:
                if player1.grid_num in current_police_visible_cells:
                    grid_cells[player1.grid_num].draw(sc, color=DETECT_COLOR_HIGHLIGHT)
                    sc.blit(player1.icon, (player1.x, player1.y), player1.icon_area)
        
            
            
        for player1 in players:
            
            if player1.player_type==1:
                sc.blit(player1.icon, (player1.x, player1.y), player1.icon_area)
            
            sc.blit(player1.icon, (player1.x+(cols+1)*TILE, player1.y), player1.icon_area)
        if not running:
                break

        pygame.display.update()
        pygame.time.wait(50)
    pygame.quit()


    
    
# Parameters for the maze
cols, rows = 5, 5  # Larger grid size for better testing
TILE = 50  # Tile size
loop_percent = 20
maze_desc =[cols,rows,TILE,loop_percent]
players = [1,0,1]
maze_generator(maze_desc, players)  # Start the maze generator with 3 players