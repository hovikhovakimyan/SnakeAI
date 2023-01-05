import pygame
import random
import asyncio
from hamiltonian import Hamiltonian
from dropdown import DropDown

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLOR_INACTIVE = (128,128,128)
COLOR_ACTIVE = (105,105,105)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (100, 150, 255)

# Initialize Pygame
pygame.init()

#screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

async def main():
    X, Y = 30, 30
    BLOCK_SIZE = 30
    WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
    ARENASIZE = WIDTH*HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set the window title
    pygame.display.set_caption("SnakeAI")

    # Set the frame rate
    clock = pygame.time.Clock()
    frame_rate = 100
    list1 = DropDown(
        [WHITE, COLOR_ACTIVE],
        [WHITE, COLOR_LIST_ACTIVE],
        screen.get_width()//2-100, (screen.get_height()//12)*1, 200, 60, 
        pygame.font.SysFont(None, 30), 
        "Select Grid Size", ["20x20", "30x30","40x40"])
    list2 = DropDown(
        [WHITE, COLOR_ACTIVE],
        [WHITE, COLOR_LIST_ACTIVE],
        screen.get_width()//2-100, (screen.get_height()//12)*4, 200, 60, 
        pygame.font.SysFont(None, 30), 
        "Select Block Size", ["20", "25","30","35"])
    list3 = DropDown(
        [WHITE, COLOR_ACTIVE],
        [WHITE, COLOR_LIST_ACTIVE],
        screen.get_width()//2-100, (screen.get_height()//12)*7, 200, 60, 
        pygame.font.SysFont(None, 30), 
        "Select Speed", ["25","50", "100","200"])


    def tourDist(x,y):
        if x<y:
            return y-x-1
        return y-x-1+(WIDTH*HEIGHT)

    def setTours():
        for i in range(0,len(cycle)-1):
            tour[cycle[i]] = i

    def check_collision(pos):
        if len(snake_position) > 0 and (pos[0] < 0 or pos[0] > (X*BLOCK_SIZE)-BLOCK_SIZE or pos[1] < 0 or pos[1] > (X*BLOCK_SIZE)-BLOCK_SIZE):
            return True
        if pos in snake_position[1:]:
            return True
        return False

    def convertToSnakePos(pos):
        return (pos[0]*BLOCK_SIZE,pos[1]*BLOCK_SIZE)

    def convertToPathPos(pos):
        return (pos[0]//BLOCK_SIZE,pos[1]//BLOCK_SIZE)

    def draw_cycle(points):
        font = pygame.font.Font('freesansbold.ttf', 10)
        prev = points[0]

        for point in points:
            pygame.draw.line(screen, RED, [point[0] * BLOCK_SIZE + BLOCK_SIZE//2, point[1] * BLOCK_SIZE + BLOCK_SIZE//2], [prev[0] * BLOCK_SIZE + BLOCK_SIZE//2, prev[1] * BLOCK_SIZE + BLOCK_SIZE//2], 4)
            prev = point
        # for i in range(0,len(cycle)):
        #     text = font.render(f'{i}', True, WHITE, BLACK)
        #     textRect = text.get_rect()
        #     textRect.center=(cycle[i][0] * BLOCK_SIZE + BLOCK_SIZE//2, cycle[i][1] * BLOCK_SIZE + BLOCK_SIZE//2)
        #     screen.blit(text,textRect)
        #     prev = cycle[i]
        pygame.display.update()

    def draw_start():
        font = pygame.font.SysFont('Roboto', 48)
        text = font.render("Start", True, BLACK)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 10*9 - text_rect.height / 2
        start_button = pygame.Rect(screen.get_width()//2-75, (screen.get_width()//10*9)-30, 150, 60)

        pygame.draw.rect(screen, WHITE, start_button)
        screen.blit(text, [text_x, text_y])
        return start_button

    def getNextPosition(pos):
        tourNumber = tour[pos]
        distanceToFood = tourDist(tourNumber,tour[convertToPathPos(food_position)])
        distanceToTail = tourDist(tourNumber,tour[convertToPathPos(snake_position[len(snake_position)-1])])
        cuttingAmountAvailable = distanceToTail-2
        emptySquares = (HEIGHT*WIDTH) - len(snake_position)-2

        if emptySquares<ARENASIZE//2:
            cuttingAmountAvailable=0
        elif distanceToFood<distanceToTail:
            cuttingAmountAvailable -= 1
            if((distanceToTail-distanceToFood)*4 > emptySquares):
                cuttingAmountAvailable-=10
        
        cuttingAmountDesired = distanceToFood
        if cuttingAmountDesired<cuttingAmountAvailable:
            cuttingAmountAvailable=cuttingAmountDesired
        if cuttingAmountAvailable<0:
            cuttingAmountAvailable=0

        canGoRight = not check_collision(convertToSnakePos((pos[0]+1,pos[1])))
        canGoLeft = not check_collision(convertToSnakePos((pos[0]-1,pos[1])))
        canGoDown = not check_collision(convertToSnakePos((pos[0],pos[1]-1)))
        canGoUp = not check_collision(convertToSnakePos((pos[0],pos[1]+1)))
        bestDist = -1
        bestNext = pos
        
        if canGoRight:
            dist = tourDist(tourNumber, tour[(pos[0]+1,pos[1])])
            if dist<= cuttingAmountAvailable and dist>bestDist:
                bestNext = (pos[0]+1,pos[1])
                bestDist = dist
        if canGoLeft:
            dist = tourDist(tourNumber, tour[(pos[0]-1,pos[1])])
            if dist<= cuttingAmountAvailable and dist>bestDist:
                bestNext = (pos[0]-1,pos[1])
                bestDist = dist
        if canGoDown:
            dist = tourDist(tourNumber, tour[(pos[0],pos[1]-1)])
            if dist<= cuttingAmountAvailable and dist>bestDist:
                bestNext = (pos[0],pos[1]-1)
                bestDist = dist
        if canGoUp:
            dist = tourDist(tourNumber, tour[(pos[0],pos[1]+1)])
            if dist<= cuttingAmountAvailable and dist>bestDist:
                bestNext = (pos[0],pos[1]+1)
                bestDist = dist
        if bestDist >= 0:
            return bestNext
        else:
            bestNext = cycle.index(pos)
            return cycle[bestNext+1]

    #Initialize snake and food
    snake_position = [(220, 200), (200, 200)]
    food_position = (random.randint(0, X-1) * BLOCK_SIZE, random.randint(0, Y-1) * BLOCK_SIZE)
    #initialize booleans
    food_spawn = True
    game_over=False
    gamestart = False
    startClicked = False
    #Outer While Loop
    while 1:
        #Main Menu Loop
        while not gamestart:
            startClicked = False
            clock.tick(frame_rate)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    exit()
            selected_option1 = list1.update(event_list)
            if selected_option1 >= 0:
                list1.main = list1.options[selected_option1]
                grid = list1.main.split('x')
                X = int(grid[0])
                Y = int(grid[1])
            selected_option2 = list2.update(event_list)
            if selected_option2 >= 0:
                list2.main = list2.options[selected_option2]
                BLOCK_SIZE = int(list2.main)
            selected_option3 = list3.update(event_list)
            if selected_option3 >= 0:
                list3.main = list3.options[selected_option3]
                frame_rate = int(list3.main)

            screen.fill(BLACK)        
            list1.draw(screen)
            list2.draw(screen)
            list3.draw(screen)
            start_button = draw_start()
            pygame.display.flip()
            await asyncio.sleep(0)

            if pygame.mouse.get_pressed()[0]==1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    startClicked = True

            if startClicked:
                gamestart = True
                #update dimmensions
                WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
                ARENASIZE = WIDTH*HEIGHT
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                #create hamiltonian cycle
                ham = Hamiltonian(X,Y)
                nodes = ham.create_nodes()
                edges = ham.create_edges()
                final_edges = ham.prims_algoritm(edges)
                points, cycle = ham.hamiltonian_cycle(nodes, final_edges)
                #set tour numbers
                tour = {}
                setTours()
                #initialize snake and food
                snake_position = [(220, 200), (200, 200)]
                food_position = (random.randint(0, X-1) * BLOCK_SIZE, random.randint(0, Y-1) * BLOCK_SIZE)
                await asyncio.sleep(0)
        # Game loop
        while gamestart:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if not game_over:
                currentpos = convertToPathPos(snake_position[0])
                snake_position.insert(0,convertToSnakePos(getNextPosition(currentpos)))

            # Check if the snake has eaten the food
            if snake_position[0] == food_position:
                food_spawn = False
            else:
                snake_position.pop()

            # Spawn new food
            if not food_spawn and len(snake_position)<X*Y:
                inSnake = True
                #Make sure the food isn't inside snake
                while(inSnake):
                    food_position = (random.randint(0, X-1) * BLOCK_SIZE, random.randint(0, Y-1) * BLOCK_SIZE)
                    inSnake=False
                    for pos in snake_position:
                        if food_position==pos:
                            inSnake=True
                            break
                food_spawn = True

            #draw_cycle(cycle) (commented out debugging code)

            screen.fill(BLACK)
            #draw snake with green head
            pygame.draw.rect(screen, GREEN, pygame.Rect(snake_position[0][0], snake_position[0][1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            for pos in snake_position[1:]:
                pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            #draw food
            pygame.draw.rect(screen, RED, pygame.Rect(
                    food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))
            # Check if the snake has collided with the walls or itself
            game_over=check_collision(snake_position[0])
            #if game is over display main menu and restart button
            if game_over:
                if len(snake_position)>=400:
                    pygame.draw.rect(screen, GREEN, pygame.Rect(
                    food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))
                #restart button
                font = pygame.font.SysFont('Roboto', 30)
                text = font.render("Restart", True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = (screen.get_height()//5)*2 - text_rect.height/2
                restart_button = pygame.Rect(screen.get_width()//2-100, ((screen.get_height()//5)*2)-30, 200, 60)
                if pygame.mouse.get_pressed()[0]==1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        game_over=False
                        snake_position = [(220, 200), (200, 200)]
                pygame.draw.rect(screen, BLACK, restart_button)
                screen.blit(text, [text_x, text_y])


                #Main Menu Button
                font = pygame.font.SysFont('Roboto', 30)
                text = font.render("Main Menu", True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height()//2 - text_rect.height / 2
                main_menu = pygame.Rect(screen.get_width()//2-100, screen.get_height()//2-30, 200, 60)
                if pygame.mouse.get_pressed()[0]==1:
                    mouse_pos = pygame.mouse.get_pos()
                    if main_menu.collidepoint(mouse_pos):
                        X=30
                        Y=30
                        BLOCK_SIZE=30
                        WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
                        ARENASIZE = WIDTH*HEIGHT
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        gamestart=False
                        game_over=False
                        list1.main = "Select Grid Size" 
                        list2.main = "Select Block Size"
                        list3.main = "Select Speed"
                        snake_position = [(220, 200), (200, 200)]
                pygame.draw.rect(screen, BLACK, main_menu)
                screen.blit(text, [text_x, text_y])

            #update clock and display
            pygame.display.update()
            clock.tick(frame_rate)
            await asyncio.sleep(0)
            
asyncio.run( main() )
    