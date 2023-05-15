import pygame
import settings
import hero
import collections
import random


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((settings.TILESIZE, settings.TILESIZE)),
    ):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(bottomleft=pos)
        # self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] - settings.TILESIZE))
        self.hitbox = self.rect.inflate(0, -10)


class InteractionObject(pygame.sprite.Sprite):
    pair_objects = collections.defaultdict(list)

    def __init__(
        self,
        pos,
        groups,
        object_type,
        images,
    ):
        super().__init__(groups)
        self.object_type = object_type
        self.animation = images
        self.image = self.animation[0]
        # self.rect = self.image.get_rect(topleft=pos)
        self.rect = self.image.get_rect(bottomleft=(pos[0] - settings.TILESIZE, pos[1]))
        self.hitbox = self.rect.inflate(-50, -50)
        self.animation_speed = 0.16666
        self.frame_index = 0
        self.interacting = False
        self.add_pair_objects()

    def add_pair_objects(self):
        if "portal" in self.object_type:
            self.pair_objects[self.object_type].append(self)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def interact(self, hero: hero.Hero, delay):
        if "portal" in self.object_type:
            such_portals = self.pair_objects[self.object_type]
            another_portals = [portal for portal in such_portals if portal != self]
            another_portal = random.choice(another_portals)

            def action():
                hero.hitbox.x = another_portal.rect.x - 25
                hero.hitbox.y = another_portal.rect.y + 65

            self.with_delay(delay, action)

    def with_delay(self, delay, action_function):
        if self.interacting is True:
            return
        self.interacting = True
        self.action_function = action_function
        self.delay = delay
        self.interaction_time = pygame.time.get_ticks()

    def cooldown(self):
        if self.interacting:
            current_time = pygame.time.get_ticks()
            if current_time - self.interaction_time >= self.delay:
                self.action_function()
                self.interacting = False

    def update(self):
        self.cooldown()
        self.animate()


class Mountain(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            settings.GRAPHICS_PATH + "/test/Mountain.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
