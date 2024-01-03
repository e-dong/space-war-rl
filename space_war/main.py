"""Contains the main entrypoint logic"""
import asyncio
from pathlib import Path

import pygame

from space_war.sim.conf import (
    MAX_FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SpriteConfig,
)
from space_war.sim.ship import BaseShip, HumanShip

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# TODO: Use dummy display for training headless
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"


def render_sprites(sprite_cfg, player_target_group, surface):
    """Draws and updates sprites and groups to screen"""
    for player in sprite_cfg:
        player["sprite"].draw_groups(surface)
        player["group"].draw(surface)
        player["group"].update(target_group=player_target_group)
        player["sprite"].update_groups(target_group=player_target_group)


def get_player_sprites(
    pos_iter: list[tuple[int, int]],
    ang_iter: list[int],
    instance_iter: list[BaseShip],
) -> tuple[list[BaseShip], list[SpriteConfig]]:
    """Initialize player sprites and returns a list of sprites and
    configuration
    """
    sprites = []
    sprite_cfg = []
    for player_id, instance in enumerate(instance_iter):
        player_sprite = instance(
            player_id=player_id,
            image_path=Path(
                "space_war", "sim", "assets", f"player_{player_id}.png"
            ),
            start_pos=pos_iter[player_id],
            start_ang=ang_iter[player_id],
        )
        player_group = pygame.sprite.GroupSingle()
        player_group.add(player_sprite)
        sprites.append(player_sprite)
        sprite_cfg.append(
            {"id": player_id, "sprite": player_sprite, "group": player_group}
        )
    return sprites, sprite_cfg


def init():
    """Initialize sprites, groups, and configuration"""
    # TODO: hydra will make this cleaner
    player_sprites, cfg = get_player_sprites(
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
        ang_iter=[0, 180],
    )

    torpedo_group = pygame.sprite.Group()
    player_target_group = pygame.sprite.Group()
    player_target_group.add(player_sprites)

    return player_sprites, cfg, torpedo_group, player_target_group


async def main():
    """Entrypoint for starting up the pygame"""
    player_sprites, cfg, torpedo_group, player_target_group = init()

    running = True

    while running:
        # event loop
        for event in pygame.event.get():
            for player in player_sprites:
                if isinstance(player, HumanShip):
                    player.handle_events(event)
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.constants.K_r
            ):
                torpedo_group.empty()
                player_target_group.empty()
                for sprite_cfg in cfg:
                    sprite_cfg["group"].empty()
                player_sprites, cfg, torpedo_group, player_target_group = init()
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Update torpedo group membership
        torpedo_group.add([player.torpedo_group for player in player_sprites])
        player_target_group.add(torpedo_group)

        # draw sprites to screen and update
        render_sprites(cfg, player_target_group, screen)

        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(MAX_FPS)

    pygame.quit()


if __name__ == "__main__":
    # This is the program entry point:
    asyncio.run(main())
