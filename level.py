from code import interact
import random
import pygame
import settings
import support
import tile
import hero
import debug
import ui
import enemy
import weapon
import effects
import spell
import upgrade


class Level:
    def __init__(self):

        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # attack sprites
        self.current_attack = None

        # user interface
        self.ui = ui.UI()
        self.upgrade = upgrade.Upgrade(self.hero)

        # effects
        self.animation_player = effects.AnimationPlayer()
        self.spell_player = spell.SpellPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            # "boundary": support.import_csv_layout("./map/map_FloorBlocks.csv"),
            "landscape": support.import_csv_layout("./map/map_landscape.csv"),
            "creatures": support.import_csv_layout("./map/map_enemies.csv"),
            "interaction_objects": support.import_csv_layout(
                "./map/map_interaction.csv"
            ),
        }
        interaction_object_types, interaction_object_graphics = support.import_folders(
            settings.GRAPHICS_PATH + "/objects/interaction"
        )
        graphics = {
            "landscape": support.import_folder(settings.GRAPHICS_PATH + "/landscape"),
            # "object": support.import_folder(settings.GRAPHICS_PATH + "/object"),
            "interaction_objects": interaction_object_graphics,
        }
        # only_one = False
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * settings.TILESIZE
                        y = (row_index + 1) * settings.TILESIZE
                        # if style == "boundary":
                        #     tile.Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "landscape":
                            # random_image_grass = random.choice(graphics["grass"])
                            image = graphics["landscape"][int(col)]
                            tile.Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
                                "grass",
                                image,
                            )

                        if style == "interaction_objects":
                            object_type = interaction_object_types[int(col)]
                            images = graphics["interaction_objects"][int(col)]
                            tile.InteractionObject(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.interaction_sprites,
                                ],
                                object_type,
                                images,
                            )

                        if style == "creatures":
                            if col == settings.HERO_COL:
                                self.hero = hero.Hero(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_spell,
                                    self.create_interaction,
                                )
                            # elif only_one is False:
                            else:
                                enemy.Enemy(
                                    settings.monster_names[col],
                                    (x, y),
                                    [
                                        self.visible_sprites,
                                        self.attackable_sprites,
                                        self.obstacle_sprites,
                                    ],
                                    self.obstacle_sprites,
                                    self.damage_to_hero,
                                    self.trigger_death_effect,
                                    self.add_exp,
                                )
                                # only_one = True

        #         if col == "x":
        #             tile.Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         elif col == "p":
        #             self.hero = hero.Hero((x, y), [self.visible_sprites], self.obstacle_sprites)
        #         elif col == "m":
        #             tile.Mountain((x, y), [self.visible_sprites, self.obstacle_sprites])

    def create_spell(self, spell_name, strength, cost):
        if spell_name == "cure":
            self.spell_player.heal(self.hero, strength, cost, [self.visible_sprites])
        elif spell_name == "magic_arrow":
            self.spell_player.magic_arrow(
                self.hero, strength, cost, [self.visible_sprites, self.attack_sprites]
            )

    def create_attack(self):
        self.current_attack = weapon.Weapon(self.hero, [self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_interaction(self):
        def get_sprite_distance(sprite):
            sprite_vector = pygame.math.Vector2(sprite.rect.center)
            player_vector = pygame.math.Vector2(self.hero.rect.center)
            subtr_vec = player_vector - sprite_vector
            distance = subtr_vec.magnitude()
            return distance

        def check_distance(sprite):
            expended_hitbox = sprite.rect.inflate(5, 5)
            return self.hero.hitbox.colliderect(expended_hitbox)

        closest_sprite = min(
            self.interaction_sprites,
            key=lambda sprite: get_sprite_distance(sprite),
        )

        if check_distance(closest_sprite):
            animation_type = f"{self.hero.current_side}_{closest_sprite.object_type}"
            if "portal" in animation_type:
                self.hero.stop()
                self.animation_player.create_effect(
                    animation_type,
                    self.hero.rect.center,
                    [self.visible_sprites],
                    follow_hero=True,
                    hero=self.hero,
                )
                closest_sprite.interact(self.hero, delay=300)

    def hero_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "enemy":
                            target_sprite.get_damage(
                                self.hero, attack_sprite.sprite_type
                            )
                            if attack_sprite.sprite_type == "magic_arrow":
                                attack_sprite.kill_with_delay(delay=100)
                                self.spell_player.spell_hit(
                                    spell="magic_arrow",
                                    target=target_sprite,
                                    groups=[self.visible_sprites],
                                )

    def damage_to_hero(self, amount, attack_type=None):
        if self.hero.vulnerable:
            self.hero.health -= amount
            self.hero.vulnerable = False
            self.hero.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_effect(
                attack_type, self.hero.rect.center, [self.visible_sprites]
            )

    def trigger_death_effect(self, pos, monster_name, direction):
        animation_type = f"{direction}_death_{monster_name}"
        self.animation_player.create_effect(
            animation_type, pos, [self.visible_sprites], True
        )

    def add_exp(self, amount):
        self.hero.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.hero)
        self.ui.display(self.hero)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.hero)
            self.hero_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            settings.GRAPHICS_PATH + "/ground.png"
        ).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        self._enemy_sprites = None

    @property
    def enemy_sprites(self):
        if self._enemy_sprites is None:
            self._enemy_sprites = [
                sprite
                for sprite in self.sprites()
                if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
            ]
        return self._enemy_sprites

    def custom_draw(self, hero):
        # getting the offset
        self.offset.x = hero.rect.centerx - self.half_width
        self.offset.y = hero.rect.centery - self.half_height

        # drawing the floor
        floor_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, hero: hero.Hero):
        for enemy in self.enemy_sprites:
            enemy.enemy_update(hero)
