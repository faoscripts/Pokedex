import pygame

from settings import (
    COLOR_TEXT,
    COLOR_SELECTED
)


class MainMenuScreen:
    def __init__(self, app, show_start=False):
        self.app = app

        self.title_font = pygame.font.Font(None, 34)
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)

        if show_start:
            self.state = "start"
        else:
            self.state = "menu"

        self.menu_options = [
            {
                "label": "Pokemon",
                "action": "pokemon_list",
                "color": (220, 20, 40),
                "icon": "P"
            },
            {
                "label": "Movs",
                "action": "move_list",
                "color": (70, 140, 220),
                "icon": "M"
            },
            {
                "label": "Escanear",
                "action": "scan",
                "color": (80, 190, 100),
                "icon": "S"
            },
            {
                "label": "Habs",
                "action": "ability_list",
                "color": (230, 170, 40),
                "icon": "H"
            },
            {
                "label": "Ajustes",
                "action": "settings",
                "color": (130, 90, 180),
                "icon": "A"
            }
        ]

        self.selected_index = 0

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "start":
                self.state = "menu"
                continue

            if event.key == pygame.K_ESCAPE:
                self.app.running = False
            
            if event.key == pygame.K_RIGHT:
                self.selected_index += 1

                if self.selected_index >= len(self.menu_options):
                    self.selected_index = 0

            elif event.key == pygame.K_LEFT:
                self.selected_index -= 1

                if self.selected_index < 0:
                    self.selected_index = len(self.menu_options) - 1

            elif event.key == pygame.K_DOWN:
                self.selected_index += 2

                if self.selected_index >= len(self.menu_options):
                    self.selected_index = self.selected_index % len(self.menu_options)

            elif event.key == pygame.K_UP:
                self.selected_index -= 2

                if self.selected_index < 0:
                    self.selected_index += len(self.menu_options)

            elif event.key == pygame.K_RETURN:
                self.execute_selected_option()

    def execute_selected_option(self):
        selected_option = self.menu_options[self.selected_index]
        action = selected_option["action"]

        if action == "pokemon_list":
            self.app.open_pokemon_list()

        elif action == "move_list":
            self.app.open_move_list()

    def update(self):
        pass

    def draw(self, screen):
        if self.state == "start":
            self.draw_start_screen(screen)
        else:
            self.draw_menu_screen(screen)

    def draw_start_screen(self, screen):
        screen.fill((190, 20, 35))

        pygame.draw.rect(screen, (150, 0, 20), (0, 0, 320, 26))
        pygame.draw.rect(screen, (90, 0, 0), (0, 24, 320, 3))

        pygame.draw.rect(screen, (35, 35, 35), (92, 42, 136, 72))
        pygame.draw.rect(screen, (20, 20, 20), (92, 42, 136, 72), 2)

        logo = self.title_font.render("POKEDEX", True, (240, 190, 40))
        screen.blit(logo, (104, 66))

        pygame.draw.rect(screen, (245, 245, 245), (30, 150, 260, 48))
        pygame.draw.rect(screen, (60, 60, 60), (30, 150, 260, 48), 2)

        text = self.font.render("Pulsa cualquier boton", True, (60, 60, 60))
        screen.blit(text, (84, 166))

    def draw_menu_screen(self, screen):
        screen.fill((205, 20, 45))

        # Decorative diagonal panels
        pygame.draw.polygon(
            screen,
            (180, 10, 35),
            [(0, 0), (120, 0), (45, 240), (0, 240)]
        )

        pygame.draw.polygon(
            screen,
            (225, 45, 65),
            [(205, 0), (320, 0), (320, 240), (145, 240)]
        )

        pygame.draw.rect(screen, (150, 0, 20), (0, 0, 320, 28))
        pygame.draw.rect(screen, (90, 0, 0), (0, 25, 320, 3))

        title = self.title_font.render("POKEDEX", True, (255, 255, 255))
        screen.blit(title, (105, 3))

        positions = [
            (80, 78),
            (160, 78),
            (240, 78),
            (115, 155),
            (205, 155)
        ]

        for i, option in enumerate(self.menu_options):
            if i >= len(positions):
                continue

            x, y = positions[i]
            is_selected = i == self.selected_index

            self.draw_circle_option(
                screen,
                x,
                y,
                option["label"],
                option["icon"],
                option["color"],
                is_selected
            )

        hint = self.small_font.render("Enter: Confirmar", True, (255, 255, 255))
        screen.blit(hint, (102, 218))

    def draw_circle_option(self, screen, x, y, label, icon, color, is_selected):
        if is_selected:
            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                [(x - 38, y - 5), (x - 28, y), (x - 38, y + 5)]
            )

        pygame.draw.circle(screen, (255, 255, 255), (x, y), 27)
        pygame.draw.circle(screen, (235, 235, 235), (x, y), 24)
        pygame.draw.circle(screen, color, (x, y), 20, 4)

        icon_text = self.title_font.render(icon, True, color)
        icon_x = x - icon_text.get_width() // 2
        icon_y = y - icon_text.get_height() // 2
        screen.blit(icon_text, (icon_x, icon_y))

        label_text = self.small_font.render(label, True, (255, 255, 255))
        label_x = x - label_text.get_width() // 2
        screen.blit(label_text, (label_x, y + 34))