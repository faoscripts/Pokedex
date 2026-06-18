import pygame
import os

from settings import (
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

        self.title_font = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 22)
        self.tiny_font = pygame.font.Font(None, 19)

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
        screen.fill((230, 230, 230))

        self.draw_top_bar(screen)
        self.draw_main_panel(screen)

        if self.move is None:
            self.draw_missing_move(screen)
        else:
            self.draw_move_data(screen)

        hint = self.small_font.render("ESC: Volver", True, (60, 60, 60))
        screen.blit(hint, (365, 292))

    def draw_top_bar(self, screen):
        title_name = self.move_name

        if self.move is not None:
            title_name = self.move.get("name", self.move_name)

        pygame.draw.rect(screen, (180, 20, 30), (0, 0, 480, 38))
        pygame.draw.rect(screen, (90, 0, 0), (0, 35, 480, 4))

        title = self.title_font.render(title_name.upper(), True, (255, 255, 255))
        screen.blit(title, (18, 8))

    def draw_main_panel(self, screen):
        pygame.draw.rect(screen, (245, 245, 245), (14, 52, 452, 230))
        pygame.draw.rect(screen, (60, 60, 60), (14, 52, 452, 230), 2)

    def draw_missing_move(self, screen):
        text = self.font.render("No hay datos del movimiento.", True, (60, 60, 60))
        screen.blit(text, (55, 140))

    def draw_move_data(self, screen):
        dark_text = (60, 60, 60)

        move_type = self.move["type"]
        category = self.move["category"]

        type_color = TYPE_COLORS.get(move_type, (120, 120, 120))
        category_color = CATEGORY_COLORS.get(category, (90, 90, 90))

        type_icon = self.load_icon(
            "assets/type_icons/" + move_type.lower() + ".png",
            (22, 22)
        )

        category_icon = self.load_icon(
            "assets/category_icons/" + category.lower() + ".png",
            (22, 22)
        )

        self.draw_icon_badge(screen, type_icon, type_color, 45, 78, 42, 34)
        self.draw_icon_badge(screen, category_icon, category_color, 45, 125, 42, 34)

        type_display_name = self.get_type_display_name(move_type)
        category_display_name = self.get_category_display_name(category)

        type_text = self.font.render("Tipo: " + type_display_name, True, dark_text)
        category_text = self.font.render("Clase: " + category_display_name, True, dark_text)

        screen.blit(type_text, (105, 84))
        screen.blit(category_text, (105, 131))

        self.draw_stat_box(screen, "Pot", self.move["power"], 45, 180)
        self.draw_stat_box(screen, "Prec", self.move["accuracy"], 150, 180)
        self.draw_stat_box(screen, "PP", self.move["pp"], 255, 180)
        self.draw_stat_box(screen, "Prio", self.move["priority"], 360, 180)

        self.draw_wrapped_text(
            screen,
            self.move["description"],
            self.tiny_font,
            dark_text,
            45,
            230,
            385,
            18,
            2
        )

    def draw_stat_box(self, screen, label, value, x, y):
        pygame.draw.rect(screen, (235, 235, 245), (x, y, 85, 34), border_radius=7)
        pygame.draw.rect(screen, (120, 120, 120), (x, y, 85, 34), 1, border_radius=7)

        label_text = self.tiny_font.render(label, True, (80, 80, 80))
        value_text = self.small_font.render(str(value), True, (20, 40, 80))

        screen.blit(label_text, (x + 8, y + 4))
        screen.blit(value_text, (x + 44, y + 8))

    def load_icon(self, path, size):
        if not os.path.exists(path):
            return None

        icon = pygame.image.load(path).convert_alpha()
        icon = self.scale_icon_keep_aspect(icon, size[0], size[1])

        return icon

    def scale_icon_keep_aspect(self, surface, max_width, max_height):
        width = surface.get_width()
        height = surface.get_height()

        scale = min(max_width / width, max_height / height)

        new_width = int(width * scale)
        new_height = int(height * scale)

        return pygame.transform.scale(surface, (new_width, new_height))

    def draw_icon_badge(self, screen, icon, color, x, y, width, height):
        pygame.draw.rect(
            screen,
            color,
            (x, y, width, height),
            border_radius=7
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