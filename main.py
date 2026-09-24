import pygame
import asyncio
import os
import random

# Pygame initialization
pygame.init()

# Set up the display and clock
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define the platforms
platforms = [
    pygame.Rect(0, 350, WIDTH, 50),   
    pygame.Rect(80, 260, 180, 20), 
    pygame.Rect(340, 180, 180, 20)
]

# Define the cupcakes
cupcakes = []
for _ in range(10):
    cx = random.randint(0, WIDTH - 50)
    cy = random.randint(0, HEIGHT - 50)
    cupcakes.append(pygame.Rect(cx, cy, 50, 50))

# Wrap your entire game setup and loop inside an async main function
async def main():
    score = 0

    # Load your images
    player_image = pygame.image.load("assets/player.png")
    player_rect = player_image.get_rect(center=(320, 240))
    
    player_speed = 5 
    gravity = 0.5
    jump_speed = -10
    player_dy = 0 
    is_grounded = False

    cupcake_image = pygame.image.load("assets/cupcake.png")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                 
        keys = pygame.key.get_pressed()
        
        player_dx = 0
        
        if keys[pygame.K_LEFT]:
            player_dx = -player_speed
        if keys[pygame.K_RIGHT]:
            player_dx = player_speed
        if keys[pygame.K_UP] and is_grounded:
            player_dy = jump_speed
            is_grounded = False
        
        player_rect.x += player_dx
        
        if player_rect.left < 0: 
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
            
        player_dy += gravity     
        
        player_rect.y += player_dy
        is_grounded = False  
   
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_dy > 0:
                    player_rect.bottom = platform.top
                    player_dy = 0
                    is_grounded = True
                elif player_dy < 0:
                    player_rect.top = platform.bottom
                    player_dy = 0

        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                score += 1
            
        screen.fill((0, 255, 0)) 
        
        for platform in platforms:
            pygame.draw.rect(
                screen,
                (100, 180, 100),
                platform
            )
        
        for cupcake in cupcakes:
            screen.blit(
                cupcake_image,
                (cupcake.x, cupcake.y)
            )

        font = pygame.font.Font(None, 50)
        text_surface = font.render("score: " + str(score), False, (255, 255, 255))
        screen.blit(text_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Pauses the loop for a microsecond so the browser doesn't freeze.
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
