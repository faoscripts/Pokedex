import pygame
import os

from settings import (
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_BORDER,
    COLOR_TEXT,
    TYPE_COLORS,
    CATEGORY_COLORS
)

from data.data_loader import MOVE_DATA


class MoveDetailScreen:
    def __init__(self, app, move_name, pokemon_name):
        self.app = app
        self.move_name = move_name
        self.pokemon_name = pokemon_name
        self.move = MOVE_DATA.get(move_name, None)

        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 19)
        self.tiny_font = pygame.font.Font(None, 17)

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                if self.pokemon_name is None:
                    self.app.open_move_list()
                else:
                    self.app.open_pokemon_detail(self.pokemon_name)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        title_name = self.move_name

        if self.move is not None:
            title_name = self.move.get("name", self.move_name)

        title = self.font.render(title_name.upper(), True, COLOR_TEXT)
        screen.blit(title, (25, 20))

        pygame.draw.rect(screen, COLOR_PANEL, (20, 55, 280, 150))
        pygame.draw.rect(screen, COLOR_BORDER, (20, 55, 280, 150), 2)

        if self.move is None:
            text = self.small_font.render("No move data found.", True, COLOR_TEXT)
            screen.blit(text, (40, 110))
        else:
            move_type = self.move["type"]
            category = self.move["category"]

            type_color = TYPE_COLORS.get(move_type, (120, 120, 120))
            category_color = CATEGORY_COLORS.get(category, (90, 90, 90))

            type_icon_path = "assets/type_icons/" + move_type.lower() + ".png"
            category_icon_path = "assets/category_icons/" + category.lower() + ".png"

            type_icon = self.load_icon(type_icon_path, (16, 16))
            category_icon = self.load_icon(category_icon_path, (16, 16))

            self.draw_icon_badge(screen, type_icon, type_color, 35, 75, 28, 22)
            self.draw_icon_badge(screen, category_icon, category_color, 35, 102, 28, 22)

            type_display_name = self.get_type_display_name(move_type)
            type_text = self.small_font.render("Tipo: " + type_display_name, True, COLOR_TEXT)
            category_display_name = self.get_category_display_name(category)
            category_text = self.small_font.render("Clase: " + category_display_name, True, COLOR_TEXT)

            screen.blit(type_text, (75, 78))
            screen.blit(category_text, (75, 105))

            power_text = self.small_font.render("Pot: " + self.move["power"], True, COLOR_TEXT)
            accuracy_text = self.small_font.render("Prec: " + self.move["accuracy"], True, COLOR_TEXT)
            pp_text = self.small_font.render("PP: " + self.move["pp"], True, COLOR_TEXT)
            priority_text = self.small_font.render("Prio: " + self.move["priority"], True, COLOR_TEXT)

            screen.blit(power_text, (35, 130))
            screen.blit(accuracy_text, (105, 130))
            screen.blit(pp_text, (180, 130))
            screen.blit(priority_text, (230, 130))

            self.draw_wrapped_text(
                screen,
                self.move["description"],
                self.tiny_font,
                COLOR_TEXT,
                35,
                158,
                250,
                14,
                2
            )

        hint = pygame.font.Font(None, 20).render("ESC: Volver", True, COLOR_TEXT)
        screen.blit(hint, (220, 215))

    def load_icon(self, path, size):
        if not os.path.exists(path):
            return None

        icon = pygame.image.load(path).convert_alpha()
        icon = pygame.transform.scale(icon, size)

        return icon


    def draw_icon_badge(self, screen, icon, color, x, y, width, height):
        pygame.draw.rect(
            screen,
            color,
            (x, y, width, height),
            border_radius=5
        )

        if icon is not None:
            icon_x = x + (width - icon.get_width()) // 2
            icon_y = y + (height - icon.get_height()) // 2
            screen.blit(icon, (icon_x, icon_y))


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

        for line in lines:
            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (x, y))
            y += line_height

    def get_category_display_name(self, category):
        category_names = {
            "Physical": "Fisico",
            "Special": "Especial",
            "Status": "Estado"
        }

        return category_names.get(category, category)

    def get_type_display_name(self, type_name):
        type_names = {
            "Normal": "Normal",
            "Fire": "Fuego",
            "Water": "Agua",
            "Electric": "Electrico",
            "Grass": "Planta",
            "Ice": "Hielo",
            "Fighting": "Lucha",
            "Poison": "Veneno",
            "Ground": "Tierra",
            "Flying": "Volador",
            "Psychic": "Psiquico",
            "Bug": "Bicho",
            "Rock": "Roca",
            "Ghost": "Fantasma",
            "Dragon": "Dragon",
            "Dark": "Siniestro",
            "Steel": "Acero",
            "Fairy": "Hada"
        }

        return type_names.get(type_name, type_name)