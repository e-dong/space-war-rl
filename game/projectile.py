"""Collection of classes for weapons"""

from typing import Any

import pygame
from pygame import Surface

from game.base import SpaceEntity


class PhotonTorpedo(SpaceEntity):
    def __init__(self) -> None:
        blankSurf = Surface([12, 12]).convert_alpha()
        super().__init__(start_pos=(430, 300), start_ang=90, surf=blankSurf)

        pygame.draw.polygon(self.image, "white", [[5, 0], [3, 5], [7, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[0, 10], [3, 9], [3, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[7, 5], [7, 9], [11, 10]], 1)
        pygame.draw.line(self.image, "white", (3, 9), (7, 9))
        pygame.draw.line(self.image, "white", (5, 5), (5, 11))

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.x_vel = 3
        super().update()
