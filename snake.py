import pygame
import random
import math

pygame.init()

# Colors
black = (0, 0, 0)
pink = (255, 182, 193)
white = (255, 255, 255)  
red = (255, 0, 0)         
dark_green = (0, 100, 0)     


# Screen configuration
width, height = 500, 500
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("SNAKE GAME")
font = pygame.font.Font("font/PixelifySans-Bold.ttf", 25)
small_font = pygame.font.Font("font/PixelifySans-Bold.ttf", 15)

# Load and scale assets
head_img = pygame.image.load("assets/head.png").convert_alpha()
head_img = pygame.transform.scale(head_img, (40, 40))

head_mouth_open_img = pygame.image.load("assets/head_mouth_open.png").convert_alpha()
head_mouth_open_img = pygame.transform.scale(head_mouth_open_img, (40, 40))

body_img = pygame.image.load("assets/body.png").convert_alpha()
body_img = pygame.transform.scale(body_img, (40, 40))

curve_ur = pygame.image.load("assets/curve_ur.png").convert_alpha()
curve_ur = pygame.transform.scale(curve_ur, (40, 40))

curve_ul = pygame.image.load("assets/curve_ul.png").convert_alpha()
curve_ul = pygame.transform.scale(curve_ul, (40, 40))

curve_dr = pygame.image.load("assets/curve_dr.png").convert_alpha()
curve_dr = pygame.transform.scale(curve_dr, (40, 40))

curve_dl = pygame.image.load("assets/curve_dl.png").convert_alpha()
curve_dl = pygame.transform.scale(curve_dl, (40, 40))

tail_img = pygame.image.load("assets/tail.png").convert_alpha()
tail_img = pygame.transform.scale(tail_img, (40, 40))

fox_img = pygame.image.load("assets/fox.png").convert_alpha()
fox_img = pygame.transform.scale(fox_img, (40, 40))

apple_img = pygame.image.load("assets/apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (40, 40))

python_img = pygame.image.load("assets/python.png").convert_alpha()
python_img = pygame.transform.scale(python_img, (40, 40))

body_food_img = pygame.image.load("assets/body_food.png").convert_alpha()
body_food_img = pygame.transform.scale(body_food_img, (40, 40))

fondo_img = pygame.image.load("assets/fondo.png").convert_alpha()
fondo_img = pygame.transform.scale(fondo_img, (width, height))

# Some game settings
block_size = 20
snake_speed = 4


# draw_snake draws the snake on screen with proper orientation:
# straight segments, curved segments based on direction changes,
# tail rotation, head rotation and change mood when eating
def draw_snake(snake_pos, snake_direction, last_food_coord, food_position):
    for i in range(1, len(snake_pos) - 1):
        prev = snake_pos[i - 1]
        curr = snake_pos[i]
        next_ = snake_pos[i + 1]
        
        # Direction vectors between segments
        dir1 = (curr[0] - prev[0], curr[1] - prev[1])
        dir2 = (next_[0] - curr[0], next_[1] - curr[1])
        
        # Block code to determinate if segment is a curve or straight
        if dir1 != dir2:
            if dir1 == (0, -block_size) and dir2 == (block_size, 0) or dir2 == (0, block_size) and dir1 == (-block_size, 0):
                img = curve_dr
            elif dir1 == (0, -block_size) and dir2 == (-block_size, 0) or dir2 == (0, block_size) and dir1 == (block_size, 0):
                img = curve_dl
            elif dir1 == (0, block_size) and dir2 == (-block_size, 0) or dir2 == (0, -block_size) and dir1 == (block_size, 0):
                img = curve_ul
            elif dir1 == (0, block_size) and dir2 == (block_size, 0) or dir2 == (0, -block_size) and dir1 == (-block_size, 0):
                img = curve_ur
            else:
                img = body_img
        # Rotate straight segment
        else:
            angle = math.degrees(math.atan2(-dir2[1], dir2[0])) + 90
            # Change in the snake´s body image when it eats
            if curr in last_food_coord:
                img = pygame.transform.rotate(body_food_img, angle)
            else:
                img = pygame.transform.rotate(body_img, angle)

        rect = img.get_rect(center=curr)
        screen.blit(img, rect)
    # Draw tail
    if len(snake_pos) >= 2:
        tail_dir = (snake_pos[0][0] - snake_pos[1][0], snake_pos[0][1] - snake_pos[1][1])
        tail_angle = math.degrees(math.atan2(-tail_dir[1], tail_dir[0])) + 90
        rotated_tail = pygame.transform.rotate(tail_img, tail_angle)
        tail_rect = rotated_tail.get_rect(center=snake_pos[0])
        screen.blit(rotated_tail, tail_rect)
    # Draw head
    head = snake_pos[-1]
    if tuple(head) == food_position: 
        head_final_img = head_mouth_open_img
    else:
        head_final_img = head_img
    angle = math.degrees(math.atan2(-snake_direction[1], snake_direction[0])) + 90
    rotated_head = pygame.transform.rotate(head_final_img, angle)
    head_rect = rotated_head.get_rect(center=head)
    screen.blit(rotated_head, head_rect.topleft)

# show_score displays the current score centered at the top 
# of the screen
def show_score(score):
    value = font.render(f"Score: {score}", False, black)
    rect = value.get_rect(center=(width // 2, 45))
    screen.blit(value, rect)

def game_menu():
    menu_running = True
    while menu_running:
        
        screen.fill(black)
        title_font = pygame.font.Font("font/PixelifySans-Bold.ttf", 35)
        # Tittle
        title_text = title_font.render("Snake Invasion: Fox Survival", True, red)
        title_rect = title_text.get_rect(center=(width // 2, height // 3))

        # Start button
        start_text = font.render("Press SPACE to Start or Q to Quit", True, white)
        start_rect = start_text.get_rect(center=(width // 2, height // 2 + 20))

        # Instructions
        inst1 = small_font.render("PROTECT YOUR HEAD FROM THE FIRE AND FOXES", True, white)
        inst2 = small_font.render("WIN THE GAME SURVIVING 10 FOXES", True, white)

        inst1_rect = inst1.get_rect(center=(width // 2, height // 2 + 60))
        inst2_rect = inst2.get_rect(center=(width // 2, height // 2 + 85))
        
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(inst1, inst1_rect)
        screen.blit(inst2, inst2_rect)
        
        # Decoration
        screen.blit(head_mouth_open_img, (width // 2 - 20, height // 2 - 50))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False #Exit the menu and enter the game.
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    # Necessary variables
    last_food_coord = []
    game_over = False
    game_close = False
    snake_direction = [1, 0]

    start_x = (width // 2) - ((width // 2) % block_size)
    start_y = (height // 2) - ((height // 2) % block_size)

    x = start_x
    y = start_y
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1
    score = 0
    margin = 40

    foxes = []  # list of actives foxes
    max_foxes = 11
    next_fox_score = 10  # amount of point to spawn the first fox


    # random_position generates a random position aligned to the 
    # grid within the playable area respecting margins
    def random_position(exclude=None):
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)
        while True:
            rx = round(random.randrange(margin, width - margin - block_size) / block_size) * block_size
            ry = round(random.randrange(margin, height - margin - block_size) / block_size) * block_size
            pos = (rx, ry)
            if pos not in exclude:
                return pos

    # spawn_fox determines a different position for the new enemy (fox) than that of the snake
    def spawn_fox(avoid_positions):
        pos = random_position(avoid_positions)
        dx_fox = random.choice([-block_size, block_size])
        return {'x': pos[0], 'y': pos[1], 'dx': dx_fox}

    food_x, food_y = random_position(set())  # calculates initial food position
    is_special = random.choice([False, False, False, True])

    clock = pygame.time.Clock()

    while not game_over:
        screen.blit(fondo_img, (0, 0))
        if len(foxes) >= max_foxes:
            game_close = True
            
            
        # Game Over screen
        while game_close:
            title_font = pygame.font.Font("font/PixelifySans-Bold.ttf", 50)
            if len(foxes) >= max_foxes:
                screen.fill(dark_green)

                line1 = title_font.render("¡GAME COMPLETED!", True, white)
                rect1 = line1.get_rect(center=(width // 2, height // 2 - 60))

                line2= font.render("You were able to dodge and survive", True, white)
                rect2 = line2.get_rect(center=(width // 2, height // 2 - 20))
                line3= font.render("the 10 foxes", True, white)
                rect3 = line3.get_rect(center=(width // 2, height // 2 + 20))

                line4= font.render("Press Q to Quit or P to Play Again", True, white)
                rect4 = line4.get_rect(center=(width // 2, height // 2 + 70))

                screen.blit(line1, rect1)
                screen.blit(line2, rect2)
                screen.blit(line3, rect3)
                screen.blit(line4, rect4)
            else:
                screen.fill(red)

                line1 = title_font.render("¡GAME OVER!", True, white)
                rect1 = line1.get_rect(center=(width // 2, height // 2 - 20))

                line2= font.render("Press Q to Quit or P to Play Again", True, white)
                rect2 = line2.get_rect(center=(width // 2, height // 2 + 20))

                screen.blit(line1, rect1)
                screen.blit(line2, rect2)

            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        return

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake_direction = [-1, 0]
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake_direction = [1, 0]
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake_direction = [0, -1]
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake_direction = [0, 1]
                    dy = block_size
                    dx = 0

        # Update snake position
        x += dx
        y += dy

        # foxes movement handling
        for f in foxes:
            f['x'] += f['dx']
            if f['x'] >= width - margin or f['x'] < margin:
                f['dx'] *= -1

        # wall collision
        if x >= width - margin or x < margin or y >= height - margin or y < margin:
            game_close = True

        # Render food
        if is_special:
            screen.blit(python_img, python_img.get_rect(center=(food_x, food_y)).topleft)
        else:
            screen.blit(apple_img, apple_img.get_rect(center=(food_x, food_y)).topleft)

        # render foxes
        for f in foxes:
            screen.blit(fox_img, fox_img.get_rect(center=(f['x'], f['y'])).topleft)

        # Detect collision snake -> fox
        for f in foxes:
            if int(x) == f['x'] and int(y) == f['y']:
                game_close = True

        # update snake
        head = [x, y]
        snake_list.append(head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # snake collision
        for segment in snake_list[:-1]:
            if segment == head:
                game_close = True

        # Draw snake
        draw_snake(snake_list, snake_direction, last_food_coord, (food_x, food_y))
        show_score(score)
        pygame.display.update()

        # food collision
        if x == food_x and y == food_y:
            if is_special:
                score += 5
                snake_length += 5
                for i in range(5):
                    if len(snake_list) >= i + 1:
                        last_food_coord.append(snake_list[-(i + 1)])
            else:
                score += 1
                snake_length += 1
                last_food_coord.append(snake_list[-1])

            food_x, food_y = random_position(set([(food_x, food_y)]))
            is_special = random.choice([False, False, False, False, False, True])

        last_food_coord = [coord for coord in last_food_coord if coord in snake_list]

        # spawn foxes logic
        if score >= next_fox_score:
            # Build a set of positions to avoid (existing snake, food, and foxes)
            avoid = set((tuple(pos) for pos in snake_list))
            avoid.add((food_x, food_y))
            for f in foxes:
                avoid.add((f['x'], f['y']))

            new_fox = spawn_fox(avoid)
            foxes.append(new_fox)
            next_fox_score += 10 # next amount of points

        clock.tick(snake_speed)

    pygame.quit()
    quit()


while True:
    game_menu() 
    game_loop()  