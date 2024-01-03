"""Miscellaneous Utility Functions"""
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


def sign(num):
    return -1 if num < 0 else 1
