import pygame
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((920, 680))

# Title and Icon
pygame.display.set_caption("SpaceRevengers")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player revenger
playerImg = pygame.image.load('revenger.png')
playerX = 450
playerY = 550


def player(x, y):
    screen.blit(playerImg, (x, y))


# Alien

alienImg = pygame.image.load('alien.png')
aleinY = []
aleinX = []
aleinX_change = []
no_of_alien = 5
for i in range(no_of_alien):
    aleinY.append(random.randint(0, 50))
    aleinX.append(random.randint(0, 856))
    aleinX_change.append(0.1)


def alein(x, y):
    screen.blit(alienImg, (x, y))


# Bullet


bulletX = 0
bulletY = 550
bullet_state = "Ready"
bulletImg = pygame.image.load('light-bolt.png')


def bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def Collision(aleinX, aleinY, bulletX, bulletY):
    if (-30 <= (aleinX - bulletX) <= 30) and (-30 <= (aleinY - bulletY) <= 30):
        return True
    else:
        return False


def main():
    global bullet_state, bulletY, bulletX, playerX, playerY, aleinX, aleinY, aleinX_change, no_of_alien
    background = pygame.image.load('background.jpg')
    mixer.music.load('background.wav')
    mixer.music.play(-1)
    playerX_change = 0
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    endfont = pygame.font.Font('freesansbold.ttf', 64)
    running = True
    while running:
        screen.blit(background, (0, 0))
        # Keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerX_change += 0.5
                if event.key == pygame.K_LEFT:
                    playerX_change -= 0.5
                if event.key == pygame.K_DOWN:
                    playerX_change = 0
                # Triggering Bullet
                if event.key == pygame.K_SPACE and bullet_state == "Ready":
                    mixer.Sound('laser.wav').play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.2
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.2
        # Revenger movement
        if playerX <= 0 and playerX_change < 0:
            playerX_change = 0.2
        elif playerX >= 856 and playerX_change > 0:
            playerX_change = -0.2
        playerX += playerX_change
        player(playerX, playerY)
        # Alien movement
        for i in range(no_of_alien):
            if aleinX[i] <= 0:
                aleinX_change[i] = 0.3
                aleinY[i] += 30
            elif aleinX[i] >= 856:
                aleinX_change[i] = -0.3
                aleinY[i] += 30
            aleinX[i] += aleinX_change[i]
            alein(aleinX[i], aleinY[i])
            if aleinY[i] > 520:
                for j in range(no_of_alien):
                    aleinY[j] = 720
                game_end_text = endfont.render('GAME OVER', True, (255, 255, 255))
                screen.blit(game_end_text, (300, 280))
            # Collision
            aleindeath = Collision(aleinX[i], aleinY[i], bulletX, bulletY)
            if aleindeath:
                mixer.Sound('explosion.wav').play()
                bulletY = 550
                bullet_state = "Ready"
                score += 1
                aleinY[i] = random.randint(0, 50)
                aleinX[i] = random.randint(0, 856)
        if bullet_state == "Fire":
            if bulletY <= 0:
                bulletY = 550
                bullet_state = "Ready"
            else:
                bulletY -= 1.5
                bullet(bulletX, bulletY)
        score_text = font.render(f'Score : {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.update()


if __name__ == '__main__':
    main()
