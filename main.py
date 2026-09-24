import pygame
import asyncio
import os
import random

# Pygame initialization
pygame.init()

# Set up the display and clock
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupcake Collector")
clock = pygame.time.Clock()

async def main():
    score = 0

    # Wikipedia-style colors
    BACKGROUND = (246, 246, 246)
    PLATFORM_COLOR = (176, 190, 197)
    PLATFORM_TOP = (51, 102, 153)
    OUTLINE_COLOR = (70, 70, 70)
    TEXT_COLOR = (32, 33, 34)

    platforms = [
        pygame.Rect(0, 350, WIDTH, 50),
        pygame.Rect(30, 270, 120, 20),
        pygame.Rect(160, 190, 120, 20),
        pygame.Rect(330, 120, 120, 20),
        pygame.Rect(470, 230, 100, 20)
    ]

    # Define cupcakes
    cupcakes = []

    cupcake_positions = [
        (70, 250),
        (275, 250),
        (335, 140),
        (115, 95),
        (370, 320)
    ]

    for cx, cy in cupcake_positions:
        cupcakes.append(pygame.Rect(cx, cy, 40, 40))

    # Load and scale player
    player_image = pygame.image.load(
        "assets/player.png"
    ).convert_alpha()

    player_image = pygame.transform.smoothscale(
        player_image,
        (50, 50)
    )

    player_rect = player_image.get_rect(
        center=(300, 300)
    )

    # Load and scale cupcake
    cupcake_image = pygame.image.load(
        "assets/cupcake.png"
    ).convert_alpha()

    cupcake_image = pygame.transform.smoothscale(
        cupcake_image,
        (40, 40)
    )

    player_speed = 5
    gravity = 0.5
    jump_speed = -10
    player_dy = 0
    is_grounded = False

    running = True

    while running:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Keyboard controls
        keys = pygame.key.get_pressed()
        player_dx = 0

        if keys[pygame.K_LEFT]:
            player_dx = -player_speed

        if keys[pygame.K_RIGHT]:
            player_dx = player_speed

        if keys[pygame.K_UP] and is_grounded:
            player_dy = jump_speed
            is_grounded = False

        # Horizontal movement
        player_rect.x += player_dx

        if player_rect.left < 0:
            player_rect.left = 0

        if player_rect.right > WIDTH:
            player_rect.right = WIDTH

        # Gravity
        player_dy += gravity
        player_rect.y += player_dy
        is_grounded = False

        # Platform collision
        for platform in platforms:

            if player_rect.colliderect(platform):

                if player_dy > 0:
                    player_rect.bottom = platform.top
                    player_dy = 0
                    is_grounded = True

                elif player_dy < 0:
                    player_rect.top = platform.bottom
                    player_dy = 0

        # Cupcake collision
        for cupcake in cupcakes[:]:

            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                score += 1

        while len(cupcakes) < 10:

            cx = random.randint(0, WIDTH - 40)
            cy = random.randint(30, 320)

            new_cupcake = pygame.Rect(
                cx,
                cy,
                40,
                40
            )
            cupcakes.append(new_cupcake)

        screen.fill(BACKGROUND)

        for platform in platforms:
            pygame.draw.rect(
                screen,
                PLATFORM_COLOR,
                platform
            )

        # Draw cupcakes
        for cupcake in cupcakes:
            screen.blit(
                cupcake_image,
                cupcake
            )

        # Draw player
        screen.blit(
            player_image,
            player_rect
        )

        font = pygame.font.Font(None, 32)

        text_surface = font.render(
            "Score: " + str(score),
            True,
            TEXT_COLOR
        )

        screen.blit(
            text_surface,
            (20, 20)
        )

        info_font = pygame.font.Font(None, 20)

        info_text = info_font.render(
            "Cupcake Collector",
            True,
            (90, 90, 90)
        )

        screen.blit(
            info_text,
            (WIDTH - info_text.get_width() - 10, 15)
        )
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())