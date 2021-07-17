# Base on this tutorial: https://youtu.be/xYhniILN6Ls

import pygame



# Pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 440
TOOLS_MARGIN = 100

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + TOOLS_MARGIN))
pygame.display.set_caption("Cell Machine Python edition")

clock = pygame.time.Clock()


# Images
BG_COLOR = (0, 0, 0)
background = pygame.image.load("textures/background.png").convert_alpha()



# Movement variables
scroll_speed = 1000 # In px/s
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_horizontal = 0
scroll_vertical = 0



# Main loop
run = True
while run:

    frame_time = clock.get_time()
    clock.tick()

    # Display
    screen.fill(BG_COLOR)
    screen.blit(background, (-scroll_horizontal, scroll_vertical))



    # Move
    if scroll_left:
        scroll_horizontal -= scroll_speed*frame_time/1000
    if scroll_right:
        scroll_horizontal += scroll_speed*frame_time/1000
    if scroll_up:
        scroll_vertical += scroll_speed*frame_time/1000
    if scroll_down:
        scroll_vertical -= scroll_speed*frame_time/1000



    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Change movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_w:
                scroll_up = True
            if event.key == pygame.K_s:
                scroll_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_w:
                scroll_up = False
            if event.key == pygame.K_s:
                scroll_down = False



    pygame.display.update()

pygame.quit()
