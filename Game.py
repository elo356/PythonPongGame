import pygame, sys, random
#SOUND EFFECT CREDITS: Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6104">Pixabay</a>

def save_best_score(best_score, file="pa0bestscore.txt"):
    with open(file, "w") as f:
        f.write(str(best_score))

def load_best_score(file="pa0bestscore.txt"):
    try:
        with open(file, "r") as f:
            best_score = int(f.read())
            return best_score
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, ball_hit_plyer, playing, scored

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    if start:
        ball_speed_x = 7 * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = 7 * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if not ball_hit_plyer:
            if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
                # TODO Task 2: Fix score to increase by 1
                score += 1  # Increase player score
                ball_speed_y *= -1  # Reverse ball's vertical direction
                # TODO Task 3: Increase the ball's speed by x
                ball_speed_x *= 1.06
                print("speed x test:  ",ball_speed_x)
                # If the player make a new record save it
                if load_best_score() == score-1:
                    pygame.mixer.Sound("Sounds/newrecord.mp3").play()
                ball_hit_plyer = True
    else:
        ball_hit_plyer = False

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction
        pygame.mixer.Sound("Sounds/beep.mp3").play()

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        pygame.mixer.Sound("Sounds/beep.mp3").play()

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        pygame.mixer.Sound("Sounds/gameover.mp3").play()

        # If the player make a new record save it
        if load_best_score() < score:
            save_best_score(score)
            print("NEW RECORD")
        playing = False
        restart()  # Reset the game

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally
    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score,scored
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    scored = score #save the score before resetting it
    score = 0  # Reset player score

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

#images setup
bg_image = pygame.image.load("Images/Background_space.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
bg_image.set_alpha(80) #make the trail effect

ball_image = pygame.image.load("Images/asteroid-ball.png")
ball_image = pygame.transform.scale(ball_image, (30, 30))

player_image = pygame.image.load("Images/player-img.png")
player_image = pygame.transform.scale(player_image, (100, 15))

# Colors
light_grey = (200, 200, 200)
#red = (255, 0, 0)
#bg_color = pygame.Color('grey12')
#ball_color = (0,255,0)

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, 100, 15)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Text setup
score = 0
scored = 0 #int to save the score before resetting it
basic_font = pygame.font.Font('pixelfont.ttf', 32)  # Font for displaying score
small_font = pygame.font.Font('pixelfont.ttf', 20)  # Font for displaying score

start = False  # Indicates if the game has started
playing = False # indicate if its playing
ball_hit_plyer = False

# Game Music
pygame.mixer.music.load("Sounds/bgmusic.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Elián E. Soto Ramos"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE and not playing:
                start = True  # Start the ball movement
                playing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    #screen.fill(bg_color)  # Clear screen with background color
    #pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    # TODO Task 1: Change color of the ball
    #pygame.draw.ellipse(screen, ball_color, ball)  # Draw ball

    screen.blit(bg_image, (0, 0))  # draw bg image
    screen.blit(ball_image, ball) #draw ball img
    screen.blit(player_image, player) #draw player img

    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

    best_score_text =small_font.render(f'High Score: {load_best_score()}', False, light_grey)
    screen.blit(best_score_text, (screen_width -490, 10))

    scored_txt = small_font.render(f'Scored: {scored}', False, light_grey)
    screen.blit(scored_txt, (screen_width - 120, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second