import pygame
import support
import settings


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # spells
            "right_heal": support.import_folder(
                settings.GRAPHICS_PATH + "/effects/heal"
            ),
            "right_magic_arrow_direct": support.import_folder(
                settings.GRAPHICS_PATH + "/effects/magic_arrow_direct"
            ),
            "right_magic_arrow_hit": support.import_folder(
                settings.GRAPHICS_PATH + "/effects/magic_arrow_hit"
            ),
            # deaths
            "right_death_familiar": support.import_folder(
                settings.GRAPHICS_PATH + "/effects/deaths/familiar"
            ),
            # interaction
            "right_portal_1": support.import_folder(
                settings.GRAPHICS_PATH + "/effects/portal_1"
            ),
        }
        support.add_reflected(self.frames)

    def create_effect(
        self,
        animation_type,
        pos,
        groups,
        last_remains=False,
        offset=None,
        sprite_type=None,
        follow_hero=False,
        hero=None,
    ):
        if animation_type is None or animation_type not in self.frames:
            return
        animation_frames = self.frames[animation_type]
        Effect(
            pos,
            animation_frames,
            groups,
            last_remains,
            offset,
            sprite_type,
            follow_hero,
            hero,
        )


class Effect(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        animation_frames,
        groups,
        last_remains=False,
        offset=None,
        sprite_type=None,
        follow_hero=False,
        hero=None,
    ):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.33
        self.animation_frames = animation_frames
        self.image = animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.offset = offset
        self.last_remains = last_remains
        self.sprite_type = sprite_type
        self.killing = False
        self.hero = hero
        self.follow_hero = follow_hero

    def animate(self):
        if self.frame_index >= len(self.animation_frames):
            if self.last_remains:
                self.frame_index = len(self.animation_frames) - 1
            else:
                self.kill()
                return
        self.image = self.animation_frames[int(self.frame_index)]
        if self.follow_hero:
            self.rect.center = self.hero.rect.center
        if self.offset is not None:
            self.pos = tuple(p + q for p, q in zip(self.pos, self.offset))
            self.rect = self.image.get_rect(center=self.pos)
        self.frame_index += self.animation_speed

    def kill_with_delay(self, delay):
        if self.killing is True:
            return
        self.delay = delay
        self.hit_time = pygame.time.get_ticks()
        self.killing = True

    def killing_cooldown(self):
        if self.killing is True:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.delay:
                self.kill()

    def update(self):
        self.killing_cooldown()
        self.animate()
