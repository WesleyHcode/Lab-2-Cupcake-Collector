
import pygame
import asyncio  # 1. Import asyncio
import random  # Required to generate random positions
import sys



# Initialize Pygame
pygame.init()

# Window Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Cupcakes")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (30, 30, 40)
RED = (255, 0, 0)
BLUE = (0, 122, 255)
YELLOW = (255, 223, 0)   # Cupcake color

# Player Configuration (Red Square)
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(
    player_image,
    (50, 50)
)
player_rect = pygame.Rect(380, 100, 40, 40)
player_vel_x = 0
player_vel_y = 0
player_speed = 6

# Physics Constants
GRAVITY = 0.8
JUMP_STRENGTH = -15
is_grounded = False  

# 3 Platforms (Blue Rectangles)
platforms = [
    pygame.Rect(0, 550, 800, 50),     # Ground floor
    pygame.Rect(100, 400, 250, 20),   # Left floating platform
    pygame.Rect(450, 300, 250, 20)    # Right floating platform
]

# --- ADDING 10 CUPCAKES ---
cupcakes = []
for _ in range(10):
    # Generate random coordinates within screen limits
    cx = random.randint(50, 750)
    # Kept above the floor (550) so they don't spawn inside the ground
    cy = random.randint(50, 500)
   
    # Store cupcake as a Rect for clean collision detection math
    cupcakes.append(pygame.Rect(cx, cy, 16, 16))

# Main Game Loop
running = True

async def main():  # 2. Add 'async' before your main function definition
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # --- Your Game Logic & Drawing Code Here ---
        keys = pygame.key.get_pressed()
        player_vel_x = 0
    
        if keys[pygame.K_LEFT]:
            player_vel_x = -player_speed
        if keys[pygame.K_RIGHT]:
            player_vel_x = player_speed
        if keys[pygame.K_UP] and is_grounded:
            player_vel_y = JUMP_STRENGTH
            is_grounded = False

        # Apply Gravity
        player_vel_y += GRAVITY

        # Move Horizontally & Handle Screen Boundaries
        player_rect.x += player_vel_x
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > WIDTH: player_rect.right = WIDTH

        # Move Vertically & Handle Safe Platform Collisions
        player_rect.y += player_vel_y
        is_grounded = False  

        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_vel_y > 0:  # Falling down
                    player_rect.bottom = platform.top
                    player_vel_y = 0
                    is_grounded = True
                elif player_vel_y < 0:  # Jumping up
                    player_rect.top = platform.bottom
                    player_vel_y = 0
        # Fall-back safety screen floor boundary check
        if player_rect.bottom > 550:
            player_rect.bottom = 550
            player_vel_y = 0
            is_grounded = True


        # --- CUPCAKE COLLECTION LOGIC ---
        # Slicing the list [:] creates a shallow copy, allowing safe item removal
        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)


        # 3. Rendering
        screen.fill(BACKGROUND)


        # Draw 3 Blue Platforms
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, platform)


        # Draw Cupcakes (Yellow Circles drawn using the center of the bounding Rect)
        for cupcake in cupcakes:
            pygame.draw.circle(screen, YELLOW, cupcake.center, 8)

        # Draw Player
        pygame.draw.rect(screen, RED, player_rect)

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

        
        await asyncio.sleep(0)  # 3. CRITICAL: Add this at the VERY END of your while loop

# Run the game using asyncio
asyncio.run(main())  # 4. Initialize the loop

pygame.quit()
sys.exit()
