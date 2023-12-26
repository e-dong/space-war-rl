"""Contains the main entrypoint logic"""

# TODO: Use dummy display for training headless
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

from game import module_path
from game.conf import MAX_FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.ship import HumanShip


def render_player(player, player_group, player_target_group, surface):
    player_group.draw(surface)
    player.phaser_group.draw(surface)
    player.torpedo_group.draw(surface)

    player_group.update(player_target_group)
    player.phaser_group.update(player_target_group)
    player.torpedo_group.update(player_target_group)


def main():
    """Entrypoint for starting up the pygame"""
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Groups
    player_one = HumanShip(
        image_path=module_path() / "assets" / "player_one.png",
        start_pos=(
            screen.get_width() / 4,
            screen.get_height() / 4,
        ),
        start_ang=0,
    )

    # TODO: Create pixel art for player two
    # player two is just a dummy target that doesn't move nor shoot for now
    player_two = HumanShip(
        image_path=module_path() / "assets" / "player_one.png",
        start_pos=(
            screen.get_width() - screen.get_width() / 4,
            screen.get_height() - screen.get_height() / 4,
        ),
        start_ang=180,
    )

    player_one_group = pygame.sprite.GroupSingle()
    player_one_group.add(player_one)

    player_two_group = pygame.sprite.GroupSingle()
    player_two_group.add(player_two)

    player_one_targets = pygame.sprite.Group()
    player_one_targets.add(player_one, player_two)
    player_two_targets = pygame.sprite.Group()
    player_two_targets.add(player_one, player_two)
    torpedo_group = pygame.sprite.Group()

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

        # Update torpedo group membership
        torpedo_group.add(player_one.torpedo_group, player_two.torpedo_group)
        player_one_targets.add(torpedo_group)
        player_two_targets.add(torpedo_group)

        # draw sprites to screen and update
        render_player(player_one, player_one_group, player_one_targets, screen)
        render_player(player_two, player_two_group, player_two_targets, screen)

        pygame.display.update()
        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
