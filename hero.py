import pygame
import settings
import debug
import support
import creature


class Hero(creature.Creature):
    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        create_attack,
        destroy_attack,
        create_spell,
        create_interaction,
    ):
        super().__init__(groups)

        # general
        self.status = "right_idle"
        self.obstacle_sprites = obstacle_sprites

        # graphics and hitbox
        self.animations = self.import_animations()
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, settings.HITBOX_OFFSET["hero"])

        # action
        self.action = None
        self.action_time = None

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # spells
        self.create_spell = create_spell
        self.spell_index = 0
        self.spell_list = list(settings.spell_data.keys())
        self.can_switch_spell = True
        self.spell_switch_time = None
        self.switch_duration_cooldown = 200

        # stats
        self.stats = settings.STATS[settings.HERO_NAME]
        self.max_stats = settings.MAX_STATS[settings.HERO_NAME]

        self.upgradable_stats = {
            "attack": self.stats["attack"],
            "defence": self.stats["defence"],
            "spellpower": self.stats["spellpower"],
            "knowledge": self.stats["knowledge"],
        }

        self.upgrade_cost = {
            "attack": 100,
            "defence": 100,
            "spellpower": 100,
            "knowledge": 100,
        }

        self.max_health = self.stats["health"]
        self.health = self.stats["health"] - 50
        self.energy = self.stats["energy"]

        self.basic_damage = self.stats["damage"]

        self.speed = self.stats["speed"]
        self.exp = 10000

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 800

        # interaction
        self.create_interaction = create_interaction
        self.can_interact = True
        self.interact_time = None
        self.uninteract_duration = 500

        # import a sound
        # self.weapon_attack_sound = pygame.mixer.Sound('../audio/')
        # self.weapon_attack_sound.set_volume(0.4)

    @property
    def current_side(self):
        return self.status.split("_")[0]

    @property
    def current_spell(self):
        return self.spell_list[self.spell_index]

    @property
    def current_spell_stats(self):
        return settings.spell_data[self.current_spell]

    @property
    def current_spell_strength(self):
        basic_strength = self.current_spell_stats["strength"]
        spellpower_factor = self.current_spell_stats["factor"]
        return basic_strength + self.spellpower * spellpower_factor

    @property
    def current_spell_cost(self):
        return self.current_spell_stats["cost"]

    @property
    def current_action_cooldown(self):
        animation_frames_number = int((1 / self.animation_speed)) * len(
            self.animations[self.status + "_" + self.action]
        )
        return 0.95 * int(animation_frames_number / settings.FPS * 1000)

    @property
    def max_energy(self):
        return self.knowledge * 10

    @property
    def enough_energy(self):
        return self.energy >= self.current_spell_cost

    @property
    def current_damage(self):
        return self.basic_damage

    @property
    def attack(self):
        return self.upgradable_stats["attack"]

    @property
    def defence(self):
        return self.upgradable_stats["defence"]

    @property
    def spellpower(self):
        return self.upgradable_stats["spellpower"]

    @property
    def knowledge(self):
        return self.upgradable_stats["knowledge"]

    def increase_stat(self, stat, amount):
        self.upgradable_stats[stat] += amount

    def spell_strength(self, spell):
        spell_stats = settings.spell_data[spell]
        basic_strength = spell_stats["strength"]
        spellpower_factor = spell_stats["factor"]
        return basic_strength + self.spellpower * spellpower_factor

    # def get_value_by_index(self, index):
    #     return list(self.upgradable_stats.values())[index]

    # def get_cost_by_index(self, index):
    #     return list(self.upgrade_cost.values())[index]

    def import_animations(self):
        animation_types = [
            "move",
            "idle",
            "action_attack_direct",
            "action_spell",
        ]
        animations = {}
        for animation in animation_types:
            full_path = settings.HERO_IMAGES_PATH + "/" + animation
            animations["right_" + animation] = support.import_folder(full_path)
        support.add_reflected(animations)
        return animations

    def stop(self):
        self.status = f"{self.current_side}_idle"
        self.direction = pygame.math.Vector2()

    def input(self):
        if self.action is not None or self.can_interact is False:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "right_move" if "right" in self.status else "left_move"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "right_move" if "right" in self.status else "left_move"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right_move"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left_move"
        else:
            self.direction.x = 0

        # attack input
        if keys[pygame.K_SPACE]:
            self.action = "attack_direct"
            self.action_time = pygame.time.get_ticks()
            self.frame_index = 0
            self.create_attack()
            # self.weapon_attack_sound.play()

        # magic input
        if keys[pygame.K_LCTRL]:
            if self.enough_energy:
                self.action = "spell"
                self.action_time = pygame.time.get_ticks()
                self.create_spell(
                    self.current_spell,
                    self.current_spell_strength,
                    self.current_spell_cost,
                )
                self.frame_index = 0

        # change spell
        if keys[pygame.K_q] and self.can_switch_spell:
            self.can_switch_spell = False
            self.spell_switch_time = pygame.time.get_ticks()

            if self.spell_index < len(self.spell_list) - 1:
                self.spell_index += 1
            else:
                self.spell_index = 0
            self.spell = self.spell_list[self.spell_index]

        # interaction
        if keys[pygame.K_f] and self.can_interact:
            self.create_interaction()
            self.interact_time = pygame.time.get_ticks()
            self.can_interact = False

        # tmp
        if keys[pygame.K_r]:
            self.energy = self.max_energy

    def restore_health(self, strength):
        self.health = min(self.health + strength, self.max_health)

    def energy_recovery(self):
        energy_per_sec = 0.1
        if self.energy < self.max_energy:
            self.energy += energy_per_sec / settings.FPS * self.knowledge
        else:
            self.energy = self.max_energy

    def get_status(self):
        side = self.current_side
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "action" in self.status:
                self.status = side + "_idle"

        if self.action is not None:
            self.direction.x, self.direction.y = 0, 0
            if not "action" in self.status:
                self.status = side + "_action"
        else:
            if "action" in self.status:
                self.status = side + "_idle"

    def animate(self):
        if self.action is not None:
            animation = self.animations[self.status + "_" + self.action]
        else:
            animation = self.animations[self.status]
        if self.frame_index >= len(animation):
            self.frame_index = int("move" in self.status)

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.frame_index += self.animation_speed

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.action is not None:
            if current_time - self.action_time >= self.current_action_cooldown:
                if "attack" in self.action:
                    self.destroy_attack()
                self.action = None

        if not self.can_switch_spell:
            if current_time - self.spell_switch_time >= self.switch_duration_cooldown:
                self.can_switch_spell = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_interact:
            if current_time - self.interact_time >= self.uninteract_duration:
                self.can_interact = True

    def update(self):
        self.cooldowns()
        self.input()
        # debug.debug(self.status)
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
