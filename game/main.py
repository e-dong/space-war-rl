"""Contains the main entrypoint logic"""

# TODO: Use dummy display for training headless
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

from game import module_path
from game.conf import MAX_FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from game.ship import BaseShip, HumanShip


def render_player(player_cfg, player_target_group, surface):
    for player in player_cfg:
        player["group"].draw(surface)
        player["sprite"].draw_groups(surface)

        player["group"].update(player_target_group)
        player["sprite"].update_groups(player_target_group)


def get_player_sprites_from_pos(pos_iter, instance_iter):
    sprite_cfg = []
    sprites = []
    for player_id, pos in enumerate(pos_iter):
        player_group = pygame.sprite.GroupSingle()
        player_sprite = instance_iter[player_id](
            player_id=player_id,
            image_path=module_path() / "assets" / f"player_{player_id}.png",
            start_pos=pos,
            start_ang=0,
        )

        player_group.add(player_sprite)
        sprites.append(player_sprite)
        sprite_cfg.append(
            {"id": player_id, "sprite": player_sprite, "group": player_group}
        )
    return sprites, sprite_cfg


def main():
    """Entrypoint for starting up the pygame"""
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # TODO: hydra will make this cleaner
    player_sprites, cfg = get_player_sprites_from_pos(
        instance_iter=[HumanShip, BaseShip],
        pos_iter=[
            (
                screen.get_width() / 4,
                screen.get_height() / 4,
            ),
            (
                screen.get_width() - screen.get_width() / 4,
                screen.get_height() - screen.get_height() / 4,
            ),
        ],
    )

    torpedo_group = pygame.sprite.Group()
    player_target_group = pygame.sprite.Group()
    player_target_group.add(player_sprites)

    running = True

    while running:
        # event loop
        for event in pygame.event.get():
            for player in player_sprites:
                if isinstance(player, HumanShip):
                    player.handle_events(event)
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Update torpedo group membership
        torpedo_group.add([player.torpedo_group for player in player_sprites])
        player_target_group.add(torpedo_group)

        # draw sprites to screen and update
        render_player(cfg, player_target_group, screen)

        pygame.display.update()
        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
