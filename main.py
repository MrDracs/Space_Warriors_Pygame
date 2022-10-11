import pygame
import random
import math
import sys
from pygame import mixer

pygame.init()
life = 'alive'
# Images loading
iconImg = pygame.image.load("data/Icon.png")
Backgrond = pygame.image.load("data/bg11.png")
Backgrond = pygame.transform.scale(Backgrond, (800, 600))

playerImg = pygame.image.load("data/player.png")
bulletImg = pygame.image.load("data/bullet.png")

# setting up screen and frame rate by specifying ticks using clock
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
mixer.music.load("data/Bit Style.wav")
mixer.music.play(-1)

# title and icon for game
pygame.display.set_caption("data/Space Warrior")
pygame.display.set_icon(iconImg)

# score
score_value = 0
font = pygame.font.Font("data/SCORE.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over text
over_font = pygame.font.Font("data/OVER.ttf", 62)
over_textX = 150
over_textY = 200

# exit text
ded_font = pygame.font.Font('data/OVER.ttf', 25)
ded_fontX = 240
ded_fontY = 300

def game_over_text(x, y, x1, y1):
    game_over = over_font.render("GAME OVER", True, (255, 255, 255))
    ded = ded_font.render("Press 'X' to Exit", True, (255, 255, 0))
    screen.blit(game_over, (x, y))
    screen.blit(ded, (x1, y1))
    mixer.music.stop()
    game_over = mixer.Sound("data/Game Over.wav")
    game_over.play(1)

# credit text
credit_font = pygame.font.Font('data/SCORE.ttf', 12)
credit_fontX = 620
credit_fontY = 570

def credit_text(x, y):
    credit = credit_font.render("Made By : Rohit Kushwaha", True, (255, 255, 255))
    screen.blit(credit, (x, y))




# player positions and function
playerX = 368
playerY = 500
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# player positions and function
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 14, y))


# enemy positions and function
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

number_of_enemies = 7
for i in range(number_of_enemies):
    enemyImage = pygame.image.load("data/enemy2.png")
    enemyImage = pygame.transform.flip(enemyImage, False, True)
    enemyImg.append(enemyImage)
    enemyX.append(random.randrange(10, 725))
    enemyY.append(random.randrange(10, 200))
    enemyX_change.append(8)
    enemyY_change.append(15)


# enemy function
def enemy(x, y):
    screen.blit(enemyImage, (x, y))


# collision function
def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + math.pow(EnemyY - BulletY, 2))
    if distance < 29:
        explode = mixer.Sound("data/explode.wav")
        explode.play()
        return True
    else:
        return False


# Game Loop
running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(Backgrond, (0, 0))

    # Getting the events that are happening
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # check if Key is pressed, if yes, then execute accordingly
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_LEFT:
                playerX_change += -5
            if events.key == pygame.K_RIGHT:
                playerX_change += 5
            if events.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("data/pew pew.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
            if events.key == pygame.K_x and life == 'lolded':
                running = False

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                playerX_change = 0

    # bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # setting up functions of player
    playerX += playerX_change
    player(playerX, playerY)
    # Restricting player movement
    if playerX <= 0:
        playerX = 0

    if playerX >= 730:
        playerX = 730

    # game over text

    for i in range(number_of_enemies):
        if enemyY[i] >= 450:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
                game_over_text(over_textX, over_textY, ded_fontX, ded_fontY)
                life = 'lolded'

            break

        # enemy movement mechaning
        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i], enemyY[i])

        # Restricting enemy movement
        if enemyX[i] <= 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randrange(10, 725)
            enemyY[i] = random.randrange(10, 200)

    show_score(textX, textY)
    credit_text(credit_fontX, credit_fontY)
    pygame.display.update()
    clock.tick(120)
