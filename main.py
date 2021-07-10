import pygame
import random
import math
from pygame import mixer

pygame.init()

# Icons, Display, Screen, Background Image, Caption creation
running = True
icon = pygame.image.load("icons/icon.png")
background = pygame.image.load("background/background.png")
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")

# Importing the player
spaceship = pygame.image.load("models/player.png")
spaceship_x = 608
spaceship_y = 630

# Player movement variables
spaceship_x_move = 0
# Player movement speed
spaceship_x_move_speed = 6

# Player creation function
def player():
    screen.blit(spaceship, (spaceship_x, spaceship_y))

# Creating Empty lists for the Spawner loop
enemy = []
enemy_x = []
enemy_y = []
enemy_x_move = []
enemy_y_move = []

# Number of enemies to be randomized
spawn_rate = 6

# Creating the Spawner loop
for i in range(spawn_rate):
    # Randomizing the Enemies before importing
    enemy_list = ["models/enemy_1.png","models/enemy_2.png","models/enemy_3.png"]
    enemy_randomized = random.choice(enemy_list)

    # Importing the enemy
    enemy.append(pygame.image.load(enemy_randomized))
    enemy_x.append(random.randint(0, 1216))
    enemy_y.append(random.randint(30, 100))

    # Enemy Movement Variables
    enemy_x_move.append(3)
    enemy_y_move.append(20)
    
# Enemy movement speed
enemy_x_move_speed = 3

# Enemy Creation Function
def enemy_random():
    screen.blit(enemy[i], (enemy_x[i], enemy_y[i]))

# Importing the Bullet
bullet = pygame.image.load("models/missile.png")
bullet_x = spaceship_x + 16
bullet_y = spaceship_y
# Creating the bullet state
fired = False

# Bullet movement variable
bullet_y_move = -10

# Crating the Bullet function
def bullet_fired():
    global fired
    fired = True
    screen.blit(bullet, (bullet_x, bullet_y))
    
# Creating the Collision function using √((x_2-x_1)²+(y_2-y_1)²) formula
def collision_function(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    if distance <= 28:
        return True
    else:
        return False
    
# Creating the Scoring System
score_value = 0
font = pygame.font.Font("fonts/font.ttf", 33)

# Axis of the Score
score_x = 10
score_y = 5

# Creating the Scoring Function
def score_function():
    score = font.render("Score : " + str(score_value), True, (235, 225, 52))
    if score_value >= 100:
        high_score_function()
    screen.blit(score, (score_x, score_y))
    
# Creating the Game over system
over = pygame.font.Font("fonts/font.ttf", 150)

# Axis of the Game Over font
game_over_x = 310
game_over_y = 240

# Creating the Game Over Function
def game_over_function():
    game_over = over.render("Game Over", True, (235, 225, 52))
    screen.blit(game_over, (game_over_x, game_over_y))
    
# Adding the High Score system
high_score_font = pygame.font.Font("fonts/font.ttf", 15)

# Axis of the High Score
high_score_x = 10
high_score_y = 47

# Creating the High Score Function
def high_score_function():
    high_score = high_score_font.render("High Score !!!", True, (0, 255, 204))
    screen.blit(high_score, (high_score_x, high_score_y))
    
# Adding the Background Music
mixer.music.load("sound/background_music.wav")
mixer.music.play(-1)

# Creating the main loop
while running:
    # Creating the event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Setting up the movement keys
        if event.type == pygame.KEYDOWN:
            # Setting up the Player movement keys
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                spaceship_x_move = spaceship_x_move_speed
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                spaceship_x_move = -spaceship_x_move_speed
        # Setting up the Bullet firing keys
            if event.key == pygame.K_SPACE:
                if fired == False:
                    # Adding the Bullet Sound
                    bullet_sound = mixer.Sound("sound/fire.wav")
                    bullet_sound.play()
                    bullet_x = spaceship_x + 16
                    bullet_fired()

        # Finishing up the movement keys
        if event.type == pygame.KEYUP:
            spaceship_x_move = 0

    # Filling the screen with RGB color 
    screen.fill((0, 0, 70))
    # Adding the Background Image on the screen
    screen.blit(background, (0, 0))
    
    # Player movement loop
    spaceship_x += spaceship_x_move

    # Player movement boundaries
    if spaceship_x >= 1216:
        spaceship_x = 1216
    if spaceship_x <= 0:
        spaceship_x = 0
    
    # Creating Movement loop for Every spawned enemy
    for i in range(spawn_rate):
        # Creating the Game Over loop
        if enemy_y[i] > 580:
            if enemy_x[i] >= spaceship_x:
                for j in range(spawn_rate):
                    enemy_y[j] = 2000
                    spaceship_y = 2000
                game_over_function()
                # Removing the Background Music
                mixer.music.unload()
                break
        
        # Enemy movement loop
        enemy_x[i] += enemy_x_move[i]
        
        # Enemy movement Boundaries
        if enemy_x[i] >= 1216:
            enemy_x_move[i] = -enemy_x_move_speed
            enemy_y[i] += enemy_y_move[i]
        if enemy_x[i] <= 0:
            enemy_x_move[i] = enemy_x_move_speed
            enemy_y[i] += enemy_y_move[i]
    
        # Importing the Collision function
        collision = collision_function(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision == True:
            bullet_y = spaceship_y
            fired = False
            # Adding the Explosion sound Effect
            boom = mixer.Sound("sound/boom.wav")
            boom.play()
            score_value += 1
            enemy_x[i] = random.randint(0, 1216)
            enemy_y[i] = random.randint(30, 100)
    
        # Calling the Enemy on screen
        enemy_random()
        
    # Calling the Bullet on the screen
    if fired == True:
        bullet_fired()
        bullet_y += bullet_y_move
        # Creating the reload loop
        if bullet_y <= -32:
            bullet_y = spaceship_y
            fired = False
            
    # Calling The player on screen
    player()
    
    # Calling the Scoring function on the Screen
    score_function()
    
    # Updating the screen continuously
    pygame.display.update()