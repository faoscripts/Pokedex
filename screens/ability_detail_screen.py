import pygame

from settings import (
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_BORDER,
    COLOR_TEXT
)

from data.data_loader import ABILITY_DATA


class AbilityDetailScreen:
    def __init__(self, app, ability_name, pokemon_name):
        self.app = app
        self.ability_name = ability_name
        self.pokemon_name = pokemon_name
        self.ability = ABILITY_DATA.get(ability_name, None)

        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.app.open_pokemon_detail(self.pokemon_name)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        title_name = self.ability_name

        if self.ability is not None:
            title_name = self.ability.get("name", self.ability_name)

        title = self.font.render(title_name.upper(), True, COLOR_TEXT)

        screen.blit(title, (25, 20))

        pygame.draw.rect(screen, COLOR_PANEL, (20, 55, 280, 150))
        pygame.draw.rect(screen, COLOR_BORDER, (20, 55, 280, 150), 2)

        if self.ability is None:
            text = self.small_font.render("No ability data found.", True, COLOR_TEXT)
            screen.blit(text, (40, 110))
        else:
            self.draw_wrapped_text(
                screen,
                self.ability["description"],
                self.small_font,
                COLOR_TEXT,
                35,
                85,
                250,
                18
            )

        hint = pygame.font.Font(None, 20).render("ESC: Back", True, COLOR_TEXT)
        screen.blit(hint, (220, 215))

    def draw_wrapped_text(self, screen, text, font, color, x, y, max_width, line_height):
        words = text.split(" ")
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                line_surface = font.render(current_line, True, color)
                screen.blit(line_surface, (x, y))
                y += line_height
                current_line = word + " "

        if current_line != "":
            line_surface = font.render(current_line, True, color)
            screen.blit(line_surface, (x, y))