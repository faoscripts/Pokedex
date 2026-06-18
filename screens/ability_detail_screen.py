import pygame

from data.data_loader import ABILITY_DATA


class AbilityDetailScreen:
    def __init__(self, app, ability_name, pokemon_name):
        self.app = app
        self.ability_name = ability_name
        self.pokemon_name = pokemon_name
        self.ability = ABILITY_DATA.get(ability_name, None)

        self.title_font = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 26)
        self.text_font = pygame.font.Font(None, 22)

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.app.open_pokemon_detail(self.pokemon_name)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((230, 230, 230))

        self.draw_top_bar(screen)
        self.draw_main_panel(screen)

        if self.ability is None:
            text = self.font.render("No hay datos de la habilidad.", True, (60, 60, 60))
            screen.blit(text, (55, 140))
        else:
            self.draw_wrapped_text(
                screen,
                self.ability["description"],
                self.text_font,
                (60, 60, 60),
                45,
                85,
                385,
                22
            )

        hint = self.text_font.render("ESC: Volver", True, (60, 60, 60))
        screen.blit(hint, (365, 292))

    def draw_top_bar(self, screen):
        title_name = self.ability_name

        if self.ability is not None:
            title_name = self.ability.get("name", self.ability_name)

        pygame.draw.rect(screen, (180, 20, 30), (0, 0, 480, 38))
        pygame.draw.rect(screen, (90, 0, 0), (0, 35, 480, 4))

        title = self.title_font.render(title_name.upper(), True, (255, 255, 255))
        screen.blit(title, (18, 8))

    def draw_main_panel(self, screen):
        pygame.draw.rect(screen, (245, 245, 245), (14, 52, 452, 230))
        pygame.draw.rect(screen, (60, 60, 60), (14, 52, 452, 230), 2)

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