import pygame


class Button:
    def __init__(self, width, height, pos, font, image_path=None, text=None):
        # top rectangle
        self.top_rect = pygame.rect.Rect(pos, (width, height))
        self.top_color = "#475F77"

        # text
        self.text = text
        if self.text is not None:
            self.text_surf = font.render(text, True, "black")
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.image_path = image_path
        if self.image_path is not None:
            self.image = pygame.image.load(image_path)
            self.image_rect = self.image.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        if self.image_path is not None:
            screen.blit(self.image, self.image_rect)
        if self.text is not None:
            # pygame.draw.rect(screen, self.top_color, self.top_rect)
            screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.top_rect.collidepoint(mouse_pos)
