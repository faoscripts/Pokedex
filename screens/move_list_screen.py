import pygame

from settings import (
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_BORDER,
    COLOR_TEXT,
    COLOR_SELECTED,
    TYPE_COLORS,
    CATEGORY_COLORS
)

from data.data_loader import MOVE_DATA


class MoveListScreen:
    def __init__(self, app):
        self.app = app

        self.title_font = pygame.font.Font(None, 26)
        self.font = pygame.font.Font(None, 21)
        self.small_font = pygame.font.Font(None, 18)

        self.move_list = list(MOVE_DATA.keys())

        self.selected_index = 0
        self.scroll_offset = 0
        self.max_visible_moves = 7

        self.type_icons = {}
        self.category_icons = {}

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_DOWN:
                self.selected_index += 1

                if self.selected_index >= len(self.move_list):
                    self.selected_index = 0
                    self.scroll_offset = 0

                if self.selected_index >= self.scroll_offset + self.max_visible_moves:
                    self.scroll_offset += 1

            elif event.key == pygame.K_UP:
                self.selected_index -= 1

                if self.selected_index < 0:
                    self.selected_index = len(self.move_list) - 1
                    self.scroll_offset = max(0, len(self.move_list) - self.max_visible_moves)

                if self.selected_index < self.scroll_offset:
                    self.scroll_offset -= 1

            elif event.key == pygame.K_ESCAPE:
                self.app.open_main_menu()

            elif event.key == pygame.K_RETURN:
                selected_move = self.move_list[self.selected_index]
                self.app.open_move_detail(selected_move, None)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((230, 230, 230))

        self.draw_top_bar(screen)
        self.draw_move_list(screen)
        self.draw_scrollbar(screen)

        hint = self.small_font.render("ESC: Volver", True, (60, 60, 60))
        screen.blit(hint, (220, 218))

    def draw_top_bar(self, screen):
        pygame.draw.rect(screen, (180, 20, 30), (0, 0, 320, 28))
        pygame.draw.rect(screen, (90, 0, 0), (0, 25, 320, 3))

        title = self.title_font.render("MOVIMIENTOS", True, (255, 255, 255))
        screen.blit(title, (90, 5))

    def draw_move_list(self, screen):
        list_x = 20
        list_y = 40
        list_w = 280
        list_h = 165

        pygame.draw.rect(screen, (245, 245, 245), (list_x, list_y, list_w, list_h))
        pygame.draw.rect(screen, (60, 60, 60), (list_x, list_y, list_w, list_h), 2)

        visible_moves = self.move_list[
            self.scroll_offset:
            self.scroll_offset + self.max_visible_moves
        ]

        row_height = 22

        for visible_index, move_name in enumerate(visible_moves):
            real_index = self.scroll_offset + visible_index
            move = MOVE_DATA[move_name]

            row_x = list_x + 8
            row_y = list_y + 8 + visible_index * row_height
            row_w = list_w - 16
            row_h = 19

            move_type = move["type"]
            type_color = TYPE_COLORS.get(move_type, (120, 120, 120))

            if real_index == self.selected_index:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (row_x, row_y, row_w, row_h),
                    border_radius=5
                )
                pygame.draw.rect(
                    screen,
                    COLOR_SELECTED,
                    (row_x - 2, row_y - 2, row_w + 4, row_h + 4),
                    2,
                    border_radius=7
                )
            else:
                pygame.draw.rect(
                    screen,
                    (235, 235, 245),
                    (row_x, row_y, row_w, row_h),
                    border_radius=5
                )

            pygame.draw.rect(
                screen,
                type_color,
                (row_x, row_y, 28, row_h),
                border_top_left_radius=5,
                border_bottom_left_radius=5
            )

            icon = self.get_type_icon(move_type)

            if icon is not None:
                icon_x = row_x + (28 - icon.get_width()) // 2
                icon_y = row_y + (row_h - icon.get_height()) // 2
                screen.blit(icon, (icon_x, icon_y))

            display_name = move.get("name", move_name)

            move_text = self.font.render(display_name, True, (20, 40, 80))
            screen.blit(move_text, (row_x + 38, row_y + 2))

            category = move["category"]
            category_color = CATEGORY_COLORS.get(category, (90, 90, 90))
            category_icon = self.get_category_icon(category)

            category_x = row_x + row_w - 28
            category_y = row_y

            pygame.draw.rect(
                screen,
                category_color,
                (category_x, category_y, 28, row_h),
                border_top_right_radius=5,
                border_bottom_right_radius=5
            )

            if category_icon is not None:
                icon_x = category_x + (28 - category_icon.get_width()) // 2
                icon_y = category_y + (row_h - category_icon.get_height()) // 2
                screen.blit(category_icon, (icon_x, icon_y))

    def draw_scrollbar(self, screen):
        bar_x = 305
        bar_y = 42
        bar_w = 10
        bar_h = 160

        pygame.draw.rect(screen, (230, 230, 230), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), 1)

        if len(self.move_list) <= self.max_visible_moves:
            handle_h = bar_h
            handle_y = bar_y
        else:
            handle_h = max(18, int((self.max_visible_moves / len(self.move_list)) * bar_h))
            max_scroll = len(self.move_list) - self.max_visible_moves
            handle_y = bar_y + int((self.scroll_offset / max_scroll) * (bar_h - handle_h))

        pygame.draw.rect(
            screen,
            (70, 110, 230),
            (bar_x + 2, handle_y + 2, bar_w - 4, handle_h - 4),
            border_radius=3
        )

    def get_type_icon(self, type_name):
        if type_name in self.type_icons:
            return self.type_icons[type_name]

        path = "assets/type_icons/" + type_name.lower() + ".png"

        try:
            icon = pygame.image.load(path).convert_alpha()
            icon = pygame.transform.scale(icon, (14, 14))
            self.type_icons[type_name] = icon
            return icon
        except:
            self.type_icons[type_name] = None
            return None

    def get_category_icon(self, category):
        if category in self.category_icons:
            return self.category_icons[category]

        path = "assets/category_icons/" + category.lower() + ".png"

        try:
            icon = pygame.image.load(path).convert_alpha()
            icon = pygame.transform.scale(icon, (14, 14))
            self.category_icons[category] = icon
            return icon
        except:
            self.category_icons[category] = None
            return None