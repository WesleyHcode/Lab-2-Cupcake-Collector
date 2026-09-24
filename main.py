import pygame
import asyncio
import os
import random

# Pygame initialization
pygame.init()

# Set up the display and clock
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()


# 🌟 CHANGE 2: Wrap your entire game setup and loop inside an async main function
async def main():
    # Load your assets exactly the same way inside the function
    ball_image = pygame.image.load("assets/ball.png")
    ball_rect = ball_image.get_rect(center=(320, 240))
    speed = [5, 4]
    
    # Audio elements load normally here
    bounce_sound = pygame.mixer.Sound("assets/bounce.wav")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball_rect.x += speed[0]
        ball_rect.y += speed[1]

        # Bounce logic and sound triggers
        if ball_rect.left < 0 or ball_rect.right > 640:
            speed[0] = -speed[0]
            bounce_sound.play()
        if ball_rect.top < 0 or ball_rect.bottom > 480:
            speed[1] = -speed[1]
            bounce_sound.play()

        screen.fill((30, 30, 30))
        screen.blit(ball_image, ball_rect)
        pygame.display.flip()
        
        clock.tick(60)
        
        # 🌟 CHANGE 3: Add this exact line right after your clock tick!
        # This pauses the loop for a microsecond so the browser doesn't freeze.
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
