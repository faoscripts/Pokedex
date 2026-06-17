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

class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
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

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()