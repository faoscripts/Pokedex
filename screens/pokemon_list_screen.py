import pygame
import os

from data.data_loader import POKEMON_DATA


class PokemonListScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 26)
        self.list_font = pygame.font.Font(None, 23)
        self.small_font = pygame.font.Font(None, 20)

        self.pokemon_list = [
            pokemon_name
            for pokemon_name, pokemon in POKEMON_DATA.items()
            if not pokemon.get("is_form_entry", False)
        ]

        self.selected_index = 0
        self.scroll_offset = 0
        self.max_visible_pokemon = 10

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_DOWN:
                self.selected_index += 1

                if self.selected_index >= len(self.pokemon_list):
                    self.selected_index = 0
                    self.scroll_offset = 0

                if self.selected_index >= self.scroll_offset + self.max_visible_pokemon:
                    self.scroll_offset += 1

            elif event.key == pygame.K_UP:
                self.selected_index -= 1

                if self.selected_index < 0:
                    self.selected_index = len(self.pokemon_list) - 1
                    self.scroll_offset = max(0, len(self.pokemon_list) - self.max_visible_pokemon)

                if self.selected_index < self.scroll_offset:
                    self.scroll_offset -= 1

            elif event.key == pygame.K_ESCAPE:
                self.app.open_main_menu()

            elif event.key == pygame.K_RETURN:
                selected_pokemon = self.pokemon_list[self.selected_index]
                self.app.open_pokemon_detail(selected_pokemon)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((230, 230, 230))

        self.draw_top_bar(screen)
        self.draw_left_panel(screen)
        self.draw_right_list(screen)
        self.draw_scrollbar(screen)

    def draw_top_bar(self, screen):
        pygame.draw.rect(screen, (180, 20, 30), (0, 0, 480, 38))
        pygame.draw.rect(screen, (90, 0, 0), (0, 35, 480, 4))

        title = self.title_font.render("POKEDEX NACIONAL", True, (255, 255, 255))
        screen.blit(title, (140, 8))

    def draw_left_panel(self, screen):
        selected_name = self.pokemon_list[self.selected_index]
        pokemon = POKEMON_DATA[selected_name]

        panel_x = 14
        panel_y = 52
        panel_w = 180
        panel_h = 180

        pygame.draw.rect(screen, (245, 245, 245), (panel_x, panel_y, panel_w, panel_h))
        pygame.draw.rect(screen, (60, 60, 60), (panel_x, panel_y, panel_w, panel_h), 2)

        for x in range(panel_x, panel_x + panel_w, 18):
            pygame.draw.line(screen, (210, 210, 210), (x, panel_y), (x, panel_y + panel_h))

        for y in range(panel_y, panel_y + panel_h, 18):
            pygame.draw.line(screen, (210, 210, 210), (panel_x, y), (panel_x + panel_w, y))

        pygame.draw.circle(screen, (225, 225, 225), (104, 142), 65, 2)

        sprite = self.load_sprite(pokemon)

        if sprite is not None:
            sprite = self.trim_transparent_pixels(sprite)
            sprite = self.scale_sprite_keep_aspect(sprite, 110, 110)

            sprite_x = 104 - sprite.get_width() // 2
            sprite_y = 142 - sprite.get_height() // 2

            screen.blit(sprite, (sprite_x, sprite_y))

        info_x = 14
        info_y = 248
        info_w = 180
        info_h = 54

        pygame.draw.rect(screen, (245, 245, 245), (info_x, info_y, info_w, info_h))
        pygame.draw.rect(screen, (180, 20, 30), (info_x, info_y, 18, info_h))
        pygame.draw.rect(screen, (60, 60, 60), (info_x, info_y, info_w, info_h), 2)

        seen_text = self.small_font.render("Vistos", True, (80, 80, 80))
        owned_text = self.small_font.render("Capturados", True, (80, 80, 80))
        seen_number = self.small_font.render(str(len(self.pokemon_list)), True, (80, 80, 80))
        owned_number = self.small_font.render(str(len(self.pokemon_list)), True, (80, 80, 80))

        screen.blit(seen_text, (45, 258))
        screen.blit(owned_text, (45, 280))
        screen.blit(seen_number, (145, 258))
        screen.blit(owned_number, (145, 280))

    def draw_right_list(self, screen):
        list_x = 210
        list_y = 52
        list_w = 230
        list_h = 250

        pygame.draw.rect(screen, (245, 245, 245), (list_x, list_y, list_w, list_h))
        pygame.draw.rect(screen, (60, 60, 60), (list_x, list_y, list_w, list_h), 2)

        visible_pokemon = self.pokemon_list[
            self.scroll_offset:
            self.scroll_offset + self.max_visible_pokemon
        ]

        row_height = 24

        for visible_index, pokemon_name in enumerate(visible_pokemon):
            real_index = self.scroll_offset + visible_index
            pokemon = POKEMON_DATA[pokemon_name]

            row_x = list_x + 8
            row_y = list_y + 7 + visible_index * row_height
            row_w = list_w - 16
            row_h = 21

            if real_index == self.selected_index:
                pygame.draw.rect(screen, (255, 255, 255), (row_x, row_y, row_w, row_h), border_radius=5)
                pygame.draw.rect(screen, (220, 20, 40), (row_x, row_y, row_w, row_h), 2, border_radius=5)

            self.draw_pokeball_icon(screen, row_x + 5, row_y + 3)

            number_text = self.list_font.render(pokemon["number"], True, (80, 80, 80))
            name_text = self.list_font.render(pokemon_name, True, (80, 80, 80))

            screen.blit(number_text, (row_x + 28, row_y + 3))
            screen.blit(name_text, (row_x + 75, row_y + 3))

    def draw_scrollbar(self, screen):
        bar_x = 450
        bar_y = 55
        bar_w = 16
        bar_h = 244

        pygame.draw.rect(screen, (230, 230, 230), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), 2)

        if len(self.pokemon_list) <= self.max_visible_pokemon:
            handle_h = bar_h
            handle_y = bar_y
        else:
            handle_h = max(24, int((self.max_visible_pokemon / len(self.pokemon_list)) * bar_h))
            max_scroll = len(self.pokemon_list) - self.max_visible_pokemon
            handle_y = bar_y + int((self.scroll_offset / max_scroll) * (bar_h - handle_h))

        pygame.draw.rect(
            screen,
            (70, 110, 230),
            (bar_x + 3, handle_y + 3, bar_w - 6, handle_h - 6),
            border_radius=3
        )

    def draw_pokeball_icon(self, screen, x, y):
        pygame.draw.circle(screen, (220, 20, 40), (x + 8, y + 8), 8)
        pygame.draw.circle(screen, (255, 255, 255), (x + 8, y + 8), 6)
        pygame.draw.line(screen, (40, 40, 40), (x + 2, y + 8), (x + 14, y + 8), 2)
        pygame.draw.circle(screen, (40, 40, 40), (x + 8, y + 8), 3)
        pygame.draw.circle(screen, (255, 255, 255), (x + 8, y + 8), 1)

    def load_sprite(self, pokemon):
        sprite_path = pokemon.get("sprite_path")

        if sprite_path is not None:
            sprite_path = sprite_path.replace("\\", "/")

        if sprite_path is None or not os.path.exists(sprite_path):
            pokemon_name = pokemon["name"].lower().replace(" ", "-")
            sprite_path = "assets/sprites/" + pokemon_name + ".png"

        if not os.path.exists(sprite_path):
            sprite_path = "assets/sprites/unknown.png"

        if not os.path.exists(sprite_path):
            return None

        return pygame.image.load(sprite_path).convert_alpha()

    def trim_transparent_pixels(self, surface):
        rect = surface.get_bounding_rect()

        if rect.width == 0 or rect.height == 0:
            return surface

        return surface.subsurface(rect).copy()

    def scale_sprite_keep_aspect(self, surface, max_width, max_height):
        width = surface.get_width()
        height = surface.get_height()

        scale = min(max_width / width, max_height / height)

        new_width = int(width * scale)
        new_height = int(height * scale)

        return pygame.transform.scale(surface, (new_width, new_height))