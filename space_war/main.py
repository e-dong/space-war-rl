"""Contains the main entrypoint logic"""
import asyncio
from pathlib import Path

import pygame

from space_war import __path__
from space_war.sim.conf import (
    CHECK_KEYS_TIME_DELAY_MS,
    MAX_FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from space_war.sim.player import HumanPlayer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# create custom event to check user input
check_key_event = pygame.USEREVENT + 1
pygame.time.set_timer(check_key_event, CHECK_KEYS_TIME_DELAY_MS)

clock = pygame.time.Clock()


player_surf = pygame.image.load(
    Path(__path__[0], "sim", "assets", "player_one.png")
).convert_alpha()


async def main():
    """Entrypoint for starting up the pygame"""

    # Groups
    player_one = HumanPlayer(
        surf=player_surf,
        start_pos=(screen.get_width() / 2, screen.get_height() / 2),
    )
    player_single_group = pygame.sprite.GroupSingle()
    player_single_group.add(player_one)

    running = True

    while running:
        # event loop
        for event in pygame.event.get():
            player_one.handle_events(event, check_key_event)
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw sprites to screen and update display
        player_single_group.draw(screen)
        player_single_group.update()

        pygame.display.update()
        await asyncio.sleep(0)

        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    # This is the program entry point:
    asyncio.run(main())
