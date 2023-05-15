import pygame
import schemas
import settings
from math import sin


class Creature(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.333 * 30 / settings.FPS
        self.direction = pygame.math.Vector2()
        self.x_accum, self.y_accum = 0, 0

    def move(self, speed):
        actual_speed = speed * 30 / settings.FPS
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.x_accum += self.direction.x * actual_speed
        self.hitbox.x += self.x_accum
        hor_collision = self.collision(schemas.DIRECTION.HORIZONTAL)
        self.y_accum += self.direction.y * actual_speed
        self.hitbox.y += self.y_accum
        self.x_accum %= 1
        self.y_accum %= 1
        ver_collision = self.collision(schemas.DIRECTION.VERTICAL)
        self.rect.center = self.hitbox.center

    def check_collision(self, sprite):
        return sprite.hitbox.colliderect(self.hitbox)

    def collision(self, direction):
        if direction == schemas.DIRECTION.HORIZONTAL:
            if self.direction.x == 0:
                return False
            for sprite in self.obstacle_sprites:
                if sprite == self:
                    # print("self")
                    continue
                # if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy":
                #     continue
                if self.check_collision(sprite):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    return True

        elif direction == schemas.DIRECTION.VERTICAL:
            if self.direction.y == 0:
                return False
            for sprite in self.obstacle_sprites:
                if sprite == self:
                    continue
                if self.check_collision(sprite):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    return True

        return False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
