"""Contains the main entrypoint logic"""

import pygame

from game import module_path
from game.conf import (
    CHECK_KEYS_TIME_DELAY_MS,
    MAX_FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game.player import Player


def main():
    """Entrypoint for starting up the pygame"""
    # pygame setup
    pygame.init()
    check_key_event = pygame.USEREVENT + 1
    pygame.time.set_timer(check_key_event, CHECK_KEYS_TIME_DELAY_MS)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    # Groups
    player_1 = Player(
        image_path=module_path() / "assets" / "player_1.png",
        start_pos=(screen.get_width() / 2, screen.get_height() / 2),
    )
    player_single_group = pygame.sprite.GroupSingle()
    player_single_group.add(player_1)

    running = True

    while running:
        clock.tick(MAX_FPS)
        # event loop
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            player_1.handle_events(event, check_key_event)
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw sprites to screen and update display
        player_single_group.draw(screen)
        player_single_group.update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
