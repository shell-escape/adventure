import sys
import pygame
import settings
import level
import menu


class Game:
    def __init__(self):
        pygame.init()
        icon_surface = pygame.image.load(settings.ICON_PATH)
        pygame.display.set_icon(icon_surface)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGTH))
        pygame.display.set_caption(settings.GAME_NAME)
        self.clock = pygame.time.Clock()
        self.level = level.Level()

        # sound
        main_sound = pygame.mixer.Sound(settings.AUDIO_PATH + "/InfernoTown.mp3")
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)

    def main_menu(self):
        background = pygame.image.load(
            settings.GRAPHICS_PATH + "/menu_backgrounds/inferno_croped.png"
        )
        self.screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 30)

        PLAY_BUTTON = menu.Button(
            image_path=settings.GRAPHICS_PATH + "/buttons/start_button_2.png",
            text="Начать",
            width=100,
            height=100,
            pos=(100, 520),
            font=font,
        )
        PLAY_BUTTON.draw(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_click():
                        print("start")
                        self.run_game()

            pygame.display.update()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.main_menu()
