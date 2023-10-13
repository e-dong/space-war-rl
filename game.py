"""Example file showing a circle moving on screen"""
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
RUNNING = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while RUNNING:
    # limits FPS to 60
    # DELTA_TIME is delta time in seconds since last frame, used for framerate-
    # independent physics.
    DELTA_TIME = clock.tick(60) / 1000

    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * DELTA_TIME
    if keys[pygame.K_s]:
        player_pos.y += 300 * DELTA_TIME
    if keys[pygame.K_a]:
        player_pos.x -= 300 * DELTA_TIME
    if keys[pygame.K_d]:
        player_pos.x += 300 * DELTA_TIME

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
