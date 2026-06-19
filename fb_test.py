import os
import time
import pygame


WIDTH = 480
HEIGHT = 320
FB_PATH = "/dev/fb1"


def surface_to_rgb565_bytes(surface):
    data = pygame.image.tostring(surface, "RGB")
    out = bytearray(WIDTH * HEIGHT * 2)

    j = 0
    for i in range(0, len(data), 3):
        r = data[i]
        g = data[i + 1]
        b = data[i + 2]

        value = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

        out[j] = value & 0xFF
        out[j + 1] = (value >> 8) & 0xFF
        j += 2

    return out


def draw_to_framebuffer(surface):
    buffer = surface_to_rgb565_bytes(surface)

    with open(FB_PATH, "wb") as fb:
        fb.write(buffer)


def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    pygame.font.init()

    screen = pygame.Surface((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)

    x = 0

    while True:
        screen.fill((20, 20, 20))

        pygame.draw.rect(screen, (200, 0, 0), (20, 20, 440, 280), 4)
        pygame.draw.circle(screen, (0, 200, 80), (x, 160), 30)

        text = font.render("Pokedex test", True, (255, 255, 255))
        screen.blit(text, (150, 40))

        draw_to_framebuffer(screen)

        x += 4
        if x > WIDTH:
            x = 0

        time.sleep(1 / 30)


if __name__ == "__main__":
    main()