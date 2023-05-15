from curses.panel import top_panel
import pygame
import settings
import hero


class Upgrade:
    def __init__(self, hero: hero.Hero):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.display_width, self.display_height = self.display_surface.get_size()
        self.hero = hero
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)
        self.attribute_names = list(hero.upgradable_stats.keys())
        self.attribute_number = len(self.attribute_names)
        self.max_values = list(self.hero.max_stats.values())

        # item creation
        self.height = self.display_height * 0.8
        self.width = self.display_width // (self.attribute_number + 1)
        self.create_items()

        # selection_system
        self.selection_index = 0
        self.selection_time = None
        self.selection_cooldown = 150
        self.can_move = True

    def input(self):
        if self.can_move is False:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
            self.selection_index += 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        elif keys[pygame.K_LEFT] and self.selection_index > 0:
            self.selection_index -= 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.items[self.selection_index].trigger(self.hero)

    def cooldowns(self):
        if self.can_move is False:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.selection_cooldown:
                self.can_move = True

    def create_items(self):
        self.items = []
        for item, index in enumerate(range(self.attribute_number)):
            # horizontal position
            increment = self.display_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2
            # vertical position
            top = self.display_height * 0.1

            item = Item(left, top, self.width, self.height, index, self.font)
            self.items.append(item)

    def display(self):
        self.input()
        self.cooldowns()
        for index, item in enumerate(self.items):
            attribute = self.attribute_names[index]
            value = self.hero.upgradable_stats[attribute]
            max_value = self.max_values[index]
            cost = self.hero.upgrade_cost[attribute]
            item.display(
                self.display_surface,
                self.selection_index,
                attribute,
                value,
                max_value,
                cost,
            )


class Item:
    def __init__(self, left, top, width, heigth, index, font):
        self.rect = pygame.rect.Rect(left, top, width, heigth)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = settings.TEXT_COLOR_SELECTED if selected else settings.TEXT_COLOR
        # title
        title_surface = self.font.render(name, True, color)
        title_rect = title_surface.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20)
        )
        # cost
        cost_surface = self.font.render(str(int(cost)), True, color)
        cost_rect = cost_surface.get_rect(
            midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20)
        )
        # draw
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = settings.BAR_COLOR_SELECTED if selected else settings.BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        height = (value / max_value) * full_height
        value_rect = pygame.rect.Rect(top[0] - 15, bottom[1] - height, 30, 10)

        # draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, hero: hero.Hero):
        upgrade_attribute = list(hero.upgradable_stats.keys())[self.index]
        if (
            hero.exp >= hero.upgrade_cost[upgrade_attribute]
            and hero.upgradable_stats[upgrade_attribute]
            < hero.max_stats[upgrade_attribute]
        ):
            hero.exp -= hero.upgrade_cost[upgrade_attribute]
            hero.increase_stat(upgrade_attribute, 1)

        if hero.upgradable_stats[upgrade_attribute] > hero.max_stats[upgrade_attribute]:
            hero.upgradable_stats[upgrade_attribute] = hero.max_stats[upgrade_attribute]

    def display(self, surface, selection_number, name, value, max_value, cost):
        selected = self.index == selection_number
        if selected is True:
            pygame.draw.rect(surface, settings.UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, settings.UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, settings.UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, settings.UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, selected)
        self.display_bar(surface, value, max_value, selected)
