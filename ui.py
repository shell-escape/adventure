import pygame
import settings
import hero


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, settings.HEALTH_BAR_WIDTH, settings.BAR_HEIGHT
        )
        self.energy_bar_rect = pygame.Rect(
            10, 34, settings.ENERGY_BAR_WIDTH, settings.BAR_HEIGHT
        )

        # convert spell dictionary
        self.spell_graphics = []
        for spell in settings.spell_data.values():
            graphic_path = spell["graphic"]
            spell_image = pygame.image.load(graphic_path).convert_alpha()
            self.spell_graphics.append(spell_image)

    def show_bar(
        self, current_amount: int, max_amount: int, bg_rect: pygame.Rect, color: str
    ):
        # drawing bg
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp: int):
        text_surf = self.font.render(str(int(exp)), False, settings.TEXT_COLOR)
        x, y = self.display_surface.get_size()
        x -= 20
        y -= 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pygame.draw.rect(
            self.display_surface, settings.UI_BG_COLOR, text_rect.inflate(20, 20)
        )
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface, settings.UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

    def selection_box(
        self, left: int, top: int, has_switched: bool, enough_energy: bool
    ) -> pygame.Rect:
        bg_rect = pygame.Rect(left, top, settings.ITEM_BOX_SIZE, settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(
                self.display_surface, settings.UI_BORDER_COLOR_ACTIVE, bg_rect, 3
            )
        else:
            pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)
        if not enough_energy:
            pygame.draw.rect(
                self.display_surface, settings.UI_BORDER_COLOR_LACK, bg_rect, 3
            )
        return bg_rect

    def spell_overlay(self, spell_index: int, has_switched: bool, enough_energy: bool):
        bg_rect = self.selection_box(10, 630, has_switched, enough_energy)
        spell_surface = self.spell_graphics[spell_index]
        spell_rect = spell_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(spell_surface, spell_rect)

    def display(self, hero: hero.Hero):
        self.show_bar(
            hero.health, hero.max_health, self.health_bar_rect, settings.HEALTH_COLOR
        )
        self.show_bar(
            hero.energy, hero.max_energy, self.energy_bar_rect, settings.ENERGY_COLOR
        )
        self.show_exp(hero.exp)
        self.spell_overlay(
            hero.spell_index, not hero.can_switch_spell, hero.enough_energy
        )

        # self.show_selection_box(80, 635)
