"""Contains the main entrypoint logic"""

import pygame

from game import module_path
from game.conf import MAX_FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.ship import HumanShip


def main():
    """Entrypoint for starting up the pygame"""
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Groups
    projectile_group = pygame.sprite.Group()
    player_one = HumanShip(
        image_path=module_path() / "assets" / "player_one.png",
        start_pos=(screen.get_width() / 2, screen.get_height() / 2),
        projectile_group=projectile_group,
    )
    player_single_group = pygame.sprite.GroupSingle()
    player_single_group.add(player_one)
    # TODO: Add player 2

    running = True

    while running:
        # event loop
        for event in pygame.event.get():
            player_one.handle_events(event)
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw sprites to screen and update display
        player_single_group.draw(screen)
        # TODO: If player gets more groups, it may be good to have a
        # Player.draw_groups() function
        player_one.projectile_group.draw(screen)
        player_single_group.update()
        player_one.projectile_group.update()
        pygame.display.update()

        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
