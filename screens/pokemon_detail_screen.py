import pygame
import os
from data.data_loader import POKEMON_DATA, MOVE_DATA, ABILITY_DATA

from settings import (
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_BORDER,
    COLOR_TEXT,
    COLOR_SELECTED
)

from settings import (
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_BORDER,
    COLOR_TEXT,
    COLOR_SELECTED,
    TYPE_COLORS
)


class PokemonDetailScreen:
    def __init__(self, app, pokemon_name):
        self.app = app
        self.pokemon_name = pokemon_name
        self.pokemon = POKEMON_DATA[pokemon_name]
        self.tabs = [
            "INFO",
            "STATS",
            "MOVES",
            "ABILITIES",
            "SIZE"
        ]
        self.selected_tab_index = 0
        self.selected_move_index = 0
        self.selected_ability_index = 0
        self.font = pygame.font.Font(None, 28)
        self.type_icons = {}

        sprite_path = self.pokemon.get("sprite_path")

        if sprite_path is not None:
            sprite_path = sprite_path.replace("\\", "/")

        if sprite_path is None or not os.path.exists(sprite_path):
            pokemon_file_name = self.pokemon["name"].lower().replace(" ", "-")
            sprite_path = "assets/sprites/" + pokemon_file_name + ".png"

        if not os.path.exists(sprite_path):
            sprite_path = "assets/sprites/unknown.png"

        human_path = "assets/sprites/human.png"

        if os.path.exists(human_path):
            self.human_sprite = pygame.image.load(human_path).convert_alpha()
            self.human_sprite = self.trim_transparent_pixels(self.human_sprite)
        else:
            self.human_sprite = None

        if sprite_path is None or not os.path.exists(sprite_path):
            sprite_path = "assets/sprites/unknown.png"

        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = self.trim_transparent_pixels(self.sprite)
        self.sprite = self.scale_sprite_keep_aspect(self.sprite, 64, 64)

        self.move_scroll_offset = 0
        self.max_visible_moves = 4

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.app.open_pokemon_list()

            elif event.key == pygame.K_DOWN:
                current_tab = self.tabs[self.selected_tab_index]

                if current_tab == "MOVES":
                    self.selected_move_index += 1

                    if self.selected_move_index >= len(self.pokemon["moves"]):
                        self.selected_move_index = 0
                        self.move_scroll_offset = 0

                    if self.selected_move_index >= self.move_scroll_offset + self.max_visible_moves:
                        self.move_scroll_offset += 1

                elif current_tab == "ABILITIES":
                    self.selected_ability_index += 1

                    if self.selected_ability_index >= len(self.pokemon["abilities"]):
                        self.selected_ability_index = 0

            elif event.key == pygame.K_UP:
                current_tab = self.tabs[self.selected_tab_index]

                if current_tab == "MOVES":
                    self.selected_move_index -= 1

                    if self.selected_move_index < 0:
                        self.selected_move_index = len(self.pokemon["moves"]) - 1
                        self.move_scroll_offset = max(0, len(self.pokemon["moves"]) - self.max_visible_moves)

                    if self.selected_move_index < self.move_scroll_offset:
                        self.move_scroll_offset -= 1

                elif current_tab == "ABILITIES":
                    self.selected_ability_index -= 1

                    if self.selected_ability_index < 0:
                        self.selected_ability_index = len(self.pokemon["abilities"]) - 1

            elif event.key == pygame.K_RIGHT:
                self.selected_tab_index += 1

                if self.selected_tab_index >= len(self.tabs):
                    self.selected_tab_index = 0

            elif event.key == pygame.K_LEFT:
                self.selected_tab_index -= 1

                if self.selected_tab_index < 0:
                    self.selected_tab_index = len(self.tabs) - 1

            elif event.key == pygame.K_RETURN:
                current_tab = self.tabs[self.selected_tab_index]

                if current_tab == "INFO":
                    self.app.open_description(
                        self.pokemon_name,
                        self.pokemon["description"]
                    )

                elif current_tab == "MOVES":
                    selected_move = self.pokemon["moves"][self.selected_move_index]
                    self.app.open_move_detail(selected_move, self.pokemon_name)

                elif current_tab == "ABILITIES":
                    selected_ability = self.pokemon["abilities"][self.selected_ability_index]
                    self.app.open_ability_detail(selected_ability, self.pokemon_name)


    def update(self):
        pass


    def draw(self, screen):
        screen.fill((230, 230, 230))

        self.draw_top_bar(screen)
        self.draw_main_panel(screen)

        current_tab = self.tabs[self.selected_tab_index]

        if current_tab == "INFO":
            self.draw_info_tab(screen)

        elif current_tab == "STATS":
            self.draw_stats_tab(screen)

        elif current_tab == "MOVES":
            self.draw_moves_tab(screen)

        elif current_tab == "ABILITIES":
            self.draw_abilities_tab(screen)

        elif current_tab == "SIZE":
            self.draw_size_tab(screen)

        hint_font = pygame.font.Font(None, 20)
        hint = hint_font.render("ESC: Volver", True, (60, 60, 60))
        screen.blit(hint, (220, 218))

    def draw_top_bar(self, screen):
        pygame.draw.rect(screen, (180, 20, 30), (0, 0, 320, 28))
        pygame.draw.rect(screen, (90, 0, 0), (0, 25, 320, 3))

        title_text = "No." + self.pokemon["number"] + " " + self.pokemon_name.upper()
        title = pygame.font.Font(None, 24).render(title_text, True, (255, 255, 255))
        screen.blit(title, (18, 6))


    def draw_main_panel(self, screen):
        pygame.draw.rect(screen, (245, 245, 245), (10, 38, 300, 172))
        pygame.draw.rect(screen, (60, 60, 60), (10, 38, 300, 172), 2)

        current_tab = self.tabs[self.selected_tab_index]
        tab_display_name = self.get_tab_display_name(current_tab)

        tab_font = pygame.font.Font(None, 22)
        tab = tab_font.render("< " + tab_display_name + " >", True, (180, 20, 30))
        screen.blit(tab, (125, 43))

    def get_dark_text_color(self):
        return (60, 60, 60)


    def get_blue_text_color(self):
        return (20, 40, 80)

    def draw_info_tab(self, screen):
        dark_text = self.get_dark_text_color()

        # Sprite panel
        pygame.draw.rect(screen, (235, 235, 235), (25, 70, 85, 85))
        pygame.draw.rect(screen, (120, 120, 120), (25, 70, 85, 85), 2)

        for x in range(25, 110, 12):
            pygame.draw.line(screen, (210, 210, 210), (x, 70), (x, 155))

        for y in range(70, 155, 12):
            pygame.draw.line(screen, (210, 210, 210), (25, y), (110, y))

        sprite_x = 67 - self.sprite.get_width() // 2
        sprite_y = 112 - self.sprite.get_height() // 2
        screen.blit(self.sprite, (sprite_x, sprite_y))

        # Type badges
        self.draw_type_badges(screen, self.pokemon["type"], 125, 75)

        small_font = pygame.font.Font(None, 20)

        category = self.pokemon.get("category", "Pokemon")
        category_text = small_font.render(category, True, dark_text)
        screen.blit(category_text, (125, 108))

        desc_font = pygame.font.Font(None, 17)

        self.draw_wrapped_text(
            screen,
            self.pokemon["description"],
            desc_font,
            dark_text,
            25,
            165,
            265,
            14,
            2
        )

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

    def draw_stats_tab(self, screen):
        dark_text = self.get_dark_text_color()

        y = 78
        max_stat_value = 150
        bar_max_width = 105

        stat_font = pygame.font.Font(None, 18)
        value_font = pygame.font.Font(None, 18)

        for stat_name, stat_value in self.pokemon["stats"].items():
            label = self.get_stat_label(stat_name)

            stat_text = stat_font.render(label, True, dark_text)
            value_text = value_font.render(str(stat_value), True, dark_text)

            screen.blit(stat_text, (35, y))
            screen.blit(value_text, (112, y))

            bar_width = int((stat_value / max_stat_value) * bar_max_width)
            bar_width = min(bar_width, bar_max_width)

            pygame.draw.rect(
                screen,
                (160, 160, 160),
                (145, y + 4, bar_max_width, 8),
                1
            )

            pygame.draw.rect(
                screen,
                (180, 20, 30),
                (145, y + 4, bar_width, 8)
            )

            y += 20

    def draw_moves_tab(self, screen):
        dark_text = self.get_dark_text_color()
        y = 85

        visible_moves = self.pokemon["moves"][
            self.move_scroll_offset:
            self.move_scroll_offset + self.max_visible_moves
        ]

        for visible_index, move in enumerate(visible_moves):
            i = self.move_scroll_offset + visible_index
            move_data = MOVE_DATA.get(move, None)

            if move_data is not None:
                move_type = move_data["type"]
            else:
                move_type = "Normal"

            type_color = TYPE_COLORS.get(move_type, (120, 120, 120))

            row_x = 35
            row_y = y
            row_width = 250
            row_height = 22

            pygame.draw.rect(
                screen,
                (235, 235, 245),
                (row_x, row_y, row_width, row_height),
                border_radius=6
            )

            pygame.draw.rect(
                screen,
                type_color,
                (row_x, row_y, 32, row_height),
                border_top_left_radius=6,
                border_bottom_left_radius=6
            )

            if i == self.selected_move_index:
                pygame.draw.rect(
                    screen,
                    COLOR_SELECTED,
                    (row_x - 2, row_y - 2, row_width + 4, row_height + 4),
                    2,
                    border_radius=8
                )

            if move_type not in self.type_icons:
                self.type_icons[move_type] = self.load_type_icon(move_type)

            icon = self.type_icons[move_type]

            if icon is not None:
                icon_x = row_x + 8
                icon_y = row_y + 3
                screen.blit(icon, (icon_x, icon_y))

            move_display_name = move

            if move_data is not None:
                move_display_name = move_data.get("name", move)

            move_text = pygame.font.Font(None, 22).render(
                move_display_name,
                True,
                (20, 40, 80)
            )
            screen.blit(move_text, (row_x + 42, row_y + 3))

            y += 28

        self.draw_moves_scrollbar(screen)

    def draw_moves_scrollbar(self, screen):
        bar_x = 292
        bar_y = 78
        bar_w = 10
        bar_h = 112

        pygame.draw.rect(screen, (230, 230, 230), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), 1)

        total_moves = len(self.pokemon["moves"])

        if total_moves <= self.max_visible_moves:
            handle_h = bar_h
            handle_y = bar_y
        else:
            handle_h = max(
                18,
                int((self.max_visible_moves / total_moves) * bar_h)
            )

            max_scroll = total_moves - self.max_visible_moves

            handle_y = bar_y + int(
                (self.move_scroll_offset / max_scroll) * (bar_h - handle_h)
            )

        pygame.draw.rect(
            screen,
            (70, 110, 230),
            (bar_x + 2, handle_y + 2, bar_w - 4, handle_h - 4),
            border_radius=3
        )

    def draw_abilities_tab(self, screen):
        y = 90

        for i, ability in enumerate(self.pokemon["abilities"]):
            row_x = 35
            row_y = y
            row_width = 250
            row_height = 24

            pygame.draw.rect(
                screen,
                (235, 235, 245),
                (row_x, row_y, row_width, row_height),
                border_radius=6
            )

            pygame.draw.rect(
                screen,
                (90, 90, 90),
                (row_x, row_y, 28, row_height),
                border_top_left_radius=6,
                border_bottom_left_radius=6
            )

            if i == self.selected_ability_index:
                pygame.draw.rect(
                    screen,
                    COLOR_SELECTED,
                    (row_x - 2, row_y - 2, row_width + 4, row_height + 4),
                    2,
                    border_radius=8
                )

            icon_text = pygame.font.Font(None, 20).render(
                "A",
                True,
                (255, 255, 255)
            )

            screen.blit(icon_text, (row_x + 9, row_y + 4))

            ability_data = ABILITY_DATA.get(ability, None)
            ability_display_name = ability

            if ability_data is not None:
                ability_display_name = ability_data.get("name", ability)

            ability_text = pygame.font.Font(None, 22).render(
                ability_display_name,
                True,
                (20, 40, 80)
            )

            screen.blit(ability_text, (row_x + 40, row_y + 4))

            y += 30

    def get_height_value(self):
        height_text = self.pokemon["height"]
        height_text = height_text.replace(" m", "")
        return float(height_text)

    def draw_size_tab(self, screen):
        dark_text = self.get_dark_text_color()
        pokemon_height = self.get_height_value()
        human_height = 1.55

        max_draw_height = 80

        tallest = max(pokemon_height, human_height)

        pokemon_draw_height = int((pokemon_height / tallest) * max_draw_height)
        human_draw_height = int((human_height / tallest) * max_draw_height)

        pokemon_sprite = self.scale_sprite_keep_aspect(
            self.sprite,
            90,
            pokemon_draw_height
        )

        if self.human_sprite is not None:
            human_sprite = self.scale_sprite_keep_aspect(
                self.human_sprite,
                60,
                human_draw_height
            )
        else:
            human_sprite = None

        base_y = 150

        pokemon_x = 55
        human_x = 190

        pokemon_y = base_y - pokemon_sprite.get_height()
        screen.blit(pokemon_sprite, (pokemon_x, pokemon_y))

        if human_sprite is not None:
            human_y = base_y - human_sprite.get_height()
            screen.blit(human_sprite, (human_x, human_y))
        else:
            pygame.draw.rect(
                screen,
                COLOR_TEXT,
                (human_x + 15, base_y - human_draw_height, 20, human_draw_height)
            )

        small_font = pygame.font.Font(None, 16)

        pokemon_name_text = small_font.render(self.pokemon_name, True, dark_text)
        pokemon_height_text = small_font.render(
            "Altura: " + self.pokemon["height"],
            True,
            dark_text
        )
        pokemon_weight_text = small_font.render(
            "Peso: " + self.pokemon["weight"],
            True,
            dark_text
        )

        human_text = small_font.render("Humano", True, dark_text)
        human_height_text = small_font.render("Altura: 1.55 m", True, dark_text)

        screen.blit(pokemon_name_text, (35, 158))
        screen.blit(pokemon_height_text, (35, 173))
        screen.blit(pokemon_weight_text, (35, 188))

        screen.blit(human_text, (175, 158))
        screen.blit(human_height_text, (175, 173))

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

    def load_type_icon(self, type_name):
        icon_path = "assets/type_icons/" + type_name.lower() + ".png"

        if not os.path.exists(icon_path):
            return None

        icon = pygame.image.load(icon_path).convert_alpha()
        icon = pygame.transform.scale(icon, (16, 16))

        return icon

    def draw_wrapped_text(self, screen, text, font, color, x, y, max_width, line_height, max_lines):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

                if len(lines) >= max_lines:
                    break

        if current_line != "" and len(lines) < max_lines:
            lines.append(current_line.strip())

        if len(lines) == max_lines:
            full_text = " ".join(words)
            visible_text = " ".join(lines)

            if len(visible_text) < len(full_text):
                last_line = lines[-1]

                while font.render(last_line + "...", True, color).get_width() > max_width:
                    last_line = last_line[:-1]

                lines[-1] = last_line + "..."

        for line in lines:
            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (x, y))
            y += line_height

    def draw_type_badges(self, screen, type_text, x, y):
        types = type_text.split(" / ")

        for type_name in types:
            type_color = TYPE_COLORS.get(type_name, (120, 120, 120))

            badge_width = 30
            badge_height = 24

            pygame.draw.rect(
                screen,
                type_color,
                (x, y, badge_width, badge_height),
                border_radius=5
            )

            if type_name not in self.type_icons:
                self.type_icons[type_name] = self.load_type_icon(type_name)

            icon = self.type_icons[type_name]

            if icon is not None:
                icon_x = x + (badge_width - icon.get_width()) // 2
                icon_y = y + (badge_height - icon.get_height()) // 2
                screen.blit(icon, (icon_x, icon_y))

            x += badge_width + 6

    def get_stat_label(self, stat_name):
        stat_labels = {
            "Hp": "PS",
            "Attack": "Ataque",
            "Defense": "Defensa",
            "Special Attack": "At. Esp",
            "Special Defense": "Def. Esp",
            "Speed": "Velocidad"
        }

        return stat_labels.get(stat_name, stat_name)

    def get_tab_display_name(self, tab_name):
        tab_names = {
            "INFO": "INFO",
            "STATS": "DATOS",
            "MOVES": "MOVS",
            "ABILITIES": "HABS",
            "SIZE": "TAMANO"
        }

        return tab_names.get(tab_name, tab_name)