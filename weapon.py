import pygame
import hero
import settings


class Weapon(pygame.sprite.Sprite):
    def __init__(self, hero: hero.Hero, groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = hero.status.split("_")[0]

        # graphic
        full_path = f"{settings.GRAPHICS_PATH}/weapon/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=hero.hitbox.midright + pygame.math.Vector2(-23, 16)
            )
        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=hero.hitbox.midleft + pygame.math.Vector2(23, 16)
            )
