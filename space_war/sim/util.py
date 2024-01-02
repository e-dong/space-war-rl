"""Miscellaneous Utility Functions"""
import math

import pygame


def check_overlapping_sprites(
    sprite: pygame.sprite.Sprite, sprite_other: pygame.sprite.Sprite
):
    """Returns the amount of overlap between 2 sprites"""
    overlap_x, overlap_y = (0, 0)
    if sprite.rect.centerx < sprite_other.rect.centerx:
        overlap_x = sprite.rect.right - sprite_other.rect.left
    elif sprite.rect.centerx > sprite_other.rect.centerx:
        overlap_x = -(sprite_other.rect.right - sprite.rect.left)

    if sprite.rect.centery < sprite_other.rect.centery:
        overlap_y = sprite.rect.bottom - sprite_other.rect.top
    elif sprite.rect.centery > sprite_other.rect.centery:
        overlap_y = -(sprite_other.rect.bottom - sprite.rect.top)

    return overlap_x, overlap_y


def create_linear_eq(angle, point):
    """Creates x and y linear equations from angle and a point"""
    slope_ang = angle % 180
    slope = (
        math.tan(slope_ang * (math.pi / 180))
        if slope_ang < 90
        else 1 / math.tan(slope_ang * (math.pi / 180))
    )

    intercept = (
        point[1] - slope * point[0]
        if slope_ang < 90
        else point[0] - slope * point[1]
    )

    # get y coordinate from x
    y_linear_eq = (
        (lambda x: slope * x + intercept)
        if slope_ang < 90
        else (lambda x: (x - intercept) / slope)
    )

    # get x coordinate from y
    x_linear_eq = (
        (lambda y: (y - intercept) / slope)
        if slope_ang < 90
        else (lambda y: slope * y + intercept)
    )

    return x_linear_eq, y_linear_eq, slope
