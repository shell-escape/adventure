import pygame
import settings
import creature
import support
import hero
import random


class Enemy(creature.Creature):
    def __init__(
        self,
        monster_name,
        pos,
        groups,
        obstacle_sprites,
        damage_to_hero,
        trigger_death_effect,
        add_exp,
    ):
        # general setup
        super().__init__(groups)
        # general
        self.sprite_type = "enemy"
        self.status = self.get_direction_status(self.direction) + "_idle"

        # graphics setup
        self.animations = self.import_animations(monster_name)
        self.image = self.animations[self.status][0]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-50, -50)
        # self.collide_hitbox = self.rect.inflate(-40, -20)

        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = settings.monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["health"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        # self.attack_type = monster_info['attack_type']

        # hero interaction
        self.can_attack = True
        self.attack_cooldown = 1000
        self.attack_time = None
        self.damage_to_hero = damage_to_hero
        self.trigger_death_effect = trigger_death_effect
        self.add_exp = add_exp

        # invulnerability_timer
        self.vulnerable = True
        #  self.hit_time = None
        #  self.invulnerability_duration = 1000

    @property
    def current_side(self):
        return self.status.split("_")[0]

    def import_animations(self, name):
        animation_types = [
            "move",
            "idle",
            "attack",
            "hit_reaction",
        ]
        animations = {}
        base_path = f"{settings.GRAPHICS_PATH}/monsters/{name}/"
        for animation in animation_types:
            animations["right_" + animation] = support.import_folder(
                base_path + animation
            )
        support.add_reflected(animations)
        return animations

    def get_player_distance_direction(self, hero: hero.Hero):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(hero.rect.center)
        subtr_vec = player_vector - enemy_vector
        distance = subtr_vec.magnitude()
        direction = subtr_vec.normalize() if distance > 0 else pygame.math.Vector2()
        return (distance, direction)

    def get_direction_status(self, direction: pygame.math.Vector2):
        if direction.x == 0:
            return random.choice(["right", "left"])
        return "right" if direction.x > 0 else "left"

    def get_status(self, hero: hero.Hero):
        if self.vulnerable is False:
            return
        distance, direction = self.get_player_distance_direction(hero)
        direction_status = self.get_direction_status(direction)
        # if "death" in self.status:
        #     pass
        if distance <= self.attack_radius:
            if self.can_attack is True:
                if "attack" not in self.status:
                    self.frame_index = 0
                self.status = direction_status + "_attack"
            else:
                self.status = direction_status + "_idle"
        elif distance <= self.notice_radius:
            if "move" not in self.status:
                self.frame_index = 0
            self.status = direction_status + "_move"
        elif "idle" in self.status:
            pass
        else:
            self.status = direction_status + "_idle"

    def actions(self, hero: hero.Hero):
        if "attack" in self.status:
            self.damage_to_hero(self.attack_damage)
            self.direction = pygame.math.Vector2()
        elif "move" in self.status:
            self.direction = self.get_player_distance_direction(hero)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if "attack" in self.status:
                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()
            elif "hit_reaction" in self.status:
                self.vulnerable = True
            #     self.frame_index = len(animation) - 1
            #  self.kill()
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # if not self.vulnerable:
        #     self.image.set_alpha(self.wave_value())
        # else:
        #     self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        # if not self.vulnerable:
        #     if current_time - self.hit_time >= self.invulnerability_duration:
        #         self.vulnerable = True

    def get_damage(self, hero: hero.Hero, sprite_type):
        if not self.vulnerable:
            return
        self.direction = self.get_player_distance_direction(hero)[1]
        if sprite_type == "weapon":
            self.health -= hero.current_damage
        else:
            self.health -= hero.spell_strength(sprite_type)
        # if sprite_type == "magic_arrow":
        #     self.health -= hero.spell_strength("magic_arrow")
        # self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False
        self.frame_index = 0
        self.status = self.current_side + "_hit_reaction"

    # def hit_reaction(self):
    #     if not self.vulnerable:
    #         self.status = self.current_side + "_hit_reaction"
    #         # self.direction *= -1

    def check_death(self):
        if self.health <= 0:  # and "death" not in self.status:
            self.kill()
            self.trigger_death_effect(
                self.rect.center,
                self.monster_name,
                self.get_direction_status(self.direction),
            )
            self.add_exp(self.exp)
            # self.status = self.status.split("_")[0] + "_death"
            # self.frame_index = 0

    def update(self):
        # self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, hero):
        self.get_status(hero)
        self.actions(hero)
