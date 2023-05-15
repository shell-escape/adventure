import pygame
import settings
import hero
import effects


class SpellPlayer(pygame.sprite.Sprite):
    def __init__(self, animation_player: effects.AnimationPlayer):
        self.animation_player = animation_player

    def heal(self, hero: hero.Hero, strength, cost, groups):
        hero.energy -= cost
        hero.restore_health(strength)
        animation_type = hero.current_side + "_heal"
        self.animation_player.create_effect(animation_type, hero.rect.center, groups)

    def magic_arrow(self, hero: hero.Hero, strength, cost, groups):
        hero.energy -= cost
        animation_type = hero.current_side + "_magic_arrow_direct"
        offset = (10, 0) if hero.current_side == "right" else (-10, 0)
        start_offset = (35, 0) if hero.current_side == "right" else (-35, 0)
        start_pos = tuple((p + o) for p, o in zip(hero.rect.center, start_offset))
        self.animation_player.create_effect(
            animation_type,
            start_pos,
            groups,
            offset=offset,
            sprite_type="magic_arrow",
        )

    def spell_hit(self, spell, target, groups):
        animation_type = f"{target.current_side}_{spell}_hit"
        self.animation_player.create_effect(animation_type, target.rect.center, groups)
