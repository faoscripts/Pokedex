import pygame


class MainMenuScreen:
    def __init__(self, app, show_start=False):
        self.app = app

        self.title_font = pygame.font.Font(None, 52)
        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 20)
        self.icon_font = pygame.font.Font(None, 42)

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

            elif event.key == pygame.K_RIGHT:
                self.selected_index += 1

                if self.selected_index >= len(self.menu_options):
                    self.selected_index = 0

            elif event.key == pygame.K_LEFT:
                self.selected_index -= 1

                if self.selected_index < 0:
                    self.selected_index = len(self.menu_options) - 1

            elif event.key == pygame.K_DOWN:
                self.selected_index += 3

                if self.selected_index >= len(self.menu_options):
                    self.selected_index = self.selected_index % len(self.menu_options)

            elif event.key == pygame.K_UP:
                self.selected_index -= 3

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

        pygame.draw.polygon(
            screen,
            (150, 0, 20),
            [(0, 0), (180, 0), (80, 320), (0, 320)]
        )

        pygame.draw.polygon(
            screen,
            (220, 45, 60),
            [(300, 0), (480, 0), (480, 320), (210, 320)]
        )

        pygame.draw.rect(screen, (120, 0, 15), (0, 0, 480, 40))
        pygame.draw.rect(screen, (70, 0, 0), (0, 36, 480, 5))

        pygame.draw.rect(screen, (35, 35, 35), (125, 75, 230, 95), border_radius=8)
        pygame.draw.rect(screen, (15, 15, 15), (125, 75, 230, 95), 3, border_radius=8)

        logo = self.title_font.render("POKEDEX", True, (240, 190, 40))
        logo_x = 240 - logo.get_width() // 2
        screen.blit(logo, (logo_x, 105))

        pygame.draw.rect(screen, (245, 245, 245), (75, 215, 330, 58), border_radius=8)
        pygame.draw.rect(screen, (60, 60, 60), (75, 215, 330, 58), 2, border_radius=8)

        text = self.font.render("Pulsa cualquier boton", True, (60, 60, 60))
        text_x = 240 - text.get_width() // 2
        screen.blit(text, (text_x, 234))

    def draw_menu_screen(self, screen):
        screen.fill((205, 20, 45))

        pygame.draw.polygon(
            screen,
            (180, 10, 35),
            [(0, 0), (170, 0), (65, 320), (0, 320)]
        )

        pygame.draw.polygon(
            screen,
            (225, 45, 65),
            [(310, 0), (480, 0), (480, 320), (220, 320)]
        )

        pygame.draw.rect(screen, (150, 0, 20), (0, 0, 480, 42))
        pygame.draw.rect(screen, (90, 0, 0), (0, 38, 480, 5))

        title = self.title_font.render("POKEDEX", True, (255, 255, 255))
        title_x = 240 - title.get_width() // 2
        screen.blit(title, (title_x, 3))

        positions = [
            (120, 115),
            (240, 115),
            (360, 115),
            (175, 220),
            (305, 220)
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

        hint = self.small_font.render("ENTER: Confirmar   ESC: Salir", True, (255, 255, 255))
        hint_x = 240 - hint.get_width() // 2
        screen.blit(hint, (hint_x, 292))

    def draw_circle_option(self, screen, x, y, label, icon, color, is_selected):
        if is_selected:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 43)
            pygame.draw.circle(screen, (255, 230, 80), (x, y), 40, 3)

        pygame.draw.circle(screen, (255, 255, 255), (x, y), 35)
        pygame.draw.circle(screen, (235, 235, 235), (x, y), 31)
        pygame.draw.circle(screen, color, (x, y), 25, 5)

        icon_text = self.icon_font.render(icon, True, color)
        icon_x = x - icon_text.get_width() // 2
        icon_y = y - icon_text.get_height() // 2
        screen.blit(icon_text, (icon_x, icon_y))

        label_text = self.font.render(label, True, (255, 255, 255))
        label_x = x - label_text.get_width() // 2
        screen.blit(label_text, (label_x, y + 47))