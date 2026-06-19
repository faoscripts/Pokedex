import os
import platform
import pygame
import sys

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from screens.main_menu_screen import MainMenuScreen
from screens.pokemon_list_screen import PokemonListScreen
from screens.pokemon_detail_screen import PokemonDetailScreen
from screens.move_detail_screen import MoveDetailScreen
from screens.ability_detail_screen import AbilityDetailScreen
from screens.description_screen import DescriptionScreen
from screens.move_list_screen import MoveListScreen


FB_PATH = "/dev/fb1"


def draw_to_framebuffer(surface):
    data = pygame.image.tostring(surface, "RGB")
    width, height = surface.get_size()
    out = bytearray(width * height * 2)

    j = 0

    for i in range(0, len(data), 3):
        r = data[i]
        g = data[i + 1]
        b = data[i + 2]

        value = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

        out[j] = value & 0xFF
        out[j + 1] = (value >> 8) & 0xFF
        j += 2

    with open(FB_PATH, "wb") as fb:
        fb.write(out)


class App:
    def __init__(self):
        self.use_framebuffer = platform.system() != "Windows"

        if self.use_framebuffer:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        pygame.init()

        if self.use_framebuffer:
            self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Pokedex UI")

        self.clock = pygame.time.Clock()
        self.running = True

        self.has_shown_start_screen = False
        self.current_screen = MainMenuScreen(self, show_start=True)
        self.has_shown_start_screen = True

    def change_screen(self, new_screen):
        self.current_screen = new_screen

    def open_main_menu(self):
        self.change_screen(MainMenuScreen(self, show_start=False))

    def open_pokemon_list(self):
        self.change_screen(PokemonListScreen(self))

    def open_move_list(self):
        self.change_screen(MoveListScreen(self))

    def open_pokemon_detail(self, pokemon_name):
        self.change_screen(PokemonDetailScreen(self, pokemon_name))

    def open_move_detail(self, move_name, pokemon_name):
        self.change_screen(MoveDetailScreen(self, move_name, pokemon_name))

    def open_ability_detail(self, ability_name, pokemon_name):
        self.change_screen(AbilityDetailScreen(self, ability_name, pokemon_name))

    def open_description(self, pokemon_name, description):
        self.change_screen(DescriptionScreen(self, pokemon_name, description))

    def run(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(self.screen)

            if self.use_framebuffer:
                draw_to_framebuffer(self.screen)
            else:
                pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()