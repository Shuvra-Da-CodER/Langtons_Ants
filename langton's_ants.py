import pygame
import random

pygame.init()

#Writing the constants in the game

FPS=25 # frames per second
GRID_SIZE=100 # size of the grid
CELL_SIZE= 10 # size of each cell in px
WIDTH=GRID_SIZE*CELL_SIZE # width of the grid and the screen
HEIGHT=GRID_SIZE*CELL_SIZE # height of the grid and the screen
BLACK=(0,0,0) 
GRID_COLOR=(255,229,186) # color of the grid
ANT1_COLOR= (255,0,0) # color of the first ant [RED]
ANT2_COLOR=(0,0,255) # color of the second ant [BLUE]
SELF_PROB=0.8 # probability of the ant's forward movement afer getting its own pheromone
CROSS_PROB=0.2 #This is the probability of the ant's forward movement after getting the pheromone of the other ant
MAX_PHEROMONE_AGE=5 # max age of the pheromone


class Grid:
    def __init__(self,size):
        self.size=size
        i,j=0,0
        self.grid=[[GRID_COLOR for i in range(size)] for j in range(size)]
        i,j=0,0
        self.pheromones=[[None for i in range(size)] for i in range(size)]  #This nested list will contain the id of the ants
        i,j=0,0
        self.pheromone_ages=[[0 for i in range(size)] for i in range(size)]

    def flip_color(self,x,y):
        if self.grid[x][y]==GRID_COLOR:
            self.grid[x][y]=BLACK
        else:
            self.grid[x][y]=GRID_COLOR
    
    def set_pheromone(self,x,y,ant_id):
        self.pheromones[x][y]=ant_id
        self.pheromone_ages[x][y]=0
    
    def get_pheromone(self, x,y):
        return self.pheromones[x][y]
    
    def update_pheromones(self):
        for i in range (GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.pheromones[i][j] is not None:
                    self.pheromone_ages[i][j]+=1
                    print("Pheromone age at ",i,j," is ",self.pheromone_ages[i][j])
                    if self.pheromone_ages[i][j]>MAX_PHEROMONE_AGE:
                        self.pheromones[i][j]=None
                        self.pheromone_ages[i][j]=0

    
class Ant:
    def __init__(self,x,y,direction,ant_id,color):
        self.x=x
        self.y=y
        self.direction=direction
        self.ant_id=ant_id
        self.color=color
    
    def move(self,grid):
        x=self.x
        y=self.y
        pheromone= grid.get_pheromone(x,y)
        #This block gets executed if there is pheromone present in that grid cell
        if pheromone==self.ant_id:
            if random.random()<=SELF_PROB:   #checking if prob is less than 80%
                self.move_forward(grid)       #moving straight
                return
        elif (pheromone is not None):
            if random.random()<=CROSS_PROB:
                self.move_forward(grid)
                return
        
        #If there is no pheromone present in the grid cell
        if grid.grid[x][y]==GRID_COLOR:
            self.direction=(self.direction+1)%4
        else:
            self.direction=(self.direction-1)%4
        
        grid.flip_color(x,y)    #colour of the visited cell is changed
        grid.set_pheromone(x,y,self.ant_id)      #pheromone is set in the cell; if the ant is A, then A is set in the cell
        self.move_forward(grid)  #moving forward

    def move_forward(self,grid):
        if self.direction==0:    #moving up 
            self.x=(self.x-1)%GRID_SIZE          #the value of row decreases, eg. from row 3 to row 2
        elif self.direction==1:  #moving right
            self.y=(self.y+1)%GRID_SIZE          #the value of column increases, eg. from column 3 to column 4
        elif self.direction==2:  #moving down
            self.x=(self.x+1)%GRID_SIZE          #the value of row increases, eg. from row 3 to row 4
        else:                    #moving left
            self.y=(self.y-1)%GRID_SIZE          #the value of column decreases, eg. from column 3 to column 2
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.y*CELL_SIZE,self.x*CELL_SIZE,CELL_SIZE,CELL_SIZE))


def main():
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()
    pygame.display.set_caption("Langton's Ants")
    grid= Grid(GRID_SIZE)       #creating an instance of Grid class
    ant1=Ant(GRID_SIZE//2,GRID_SIZE//2,0,'A',ANT1_COLOR)    #creating an instance of Ant class
    ant2=Ant(GRID_SIZE//2-10,GRID_SIZE//2+10,2,'B',ANT2_COLOR)  #creating another instance of Ant class
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        
        ant1.move(grid)
        ant2.move(grid)
        
        #Updating the pheromone's life cycle
        grid.update_pheromones()
        

        #Drawing the grid with borders
        screen.fill(GRID_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color=grid.grid[i][j]
                pygame.draw.rect(screen,color,(j*CELL_SIZE,i*CELL_SIZE,CELL_SIZE,CELL_SIZE))           #drawing the cells
                pygame.draw.rect(screen,(255,255,255),(j*CELL_SIZE,i*CELL_SIZE,CELL_SIZE,CELL_SIZE),1)    #drawing the white borders of the cells
        
        #Drawing the ants
        ant1.draw(screen)
        ant2.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__=="__main__":
    main()