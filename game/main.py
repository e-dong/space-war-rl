"""Contains the main entrypoint logic"""

import pygame

from game import module_path
from game.conf import MAX_FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.ship import HumanShip

# TODO: Refactor collision logic in main


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
        start_pos=(
            screen.get_width() / 4,
            screen.get_height() / 4,
        ),
        start_ang=0,
        projectile_group=projectile_group,
    )
    player_two = HumanShip(
        image_path=module_path() / "assets" / "player_one.png",
        start_pos=(
            screen.get_width() - screen.get_width() / 4,
            screen.get_height() - screen.get_height() / 4,
        ),
        start_ang=180,
        projectile_group=projectile_group,
    )
    player_one_group = pygame.sprite.GroupSingle()
    player_one_group.add(player_one)

    player_two_group = pygame.sprite.GroupSingle()
    player_two_group.add(player_two)

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
        player_one_group.draw(screen)
        player_two_group.draw(screen)
        player_one.projectile_group.draw(screen)
        player_one_group.update()
        player_one.projectile_group.update()
        player_two_group.update()
        pygame.display.update()

        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
