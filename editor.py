# Base on this tutorial: https://youtu.be/xYhniILN6Ls

import pygame
import cell_manager



# Pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 440
TOOLS_MARGIN = 100
BG_COLOR = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + TOOLS_MARGIN))
pygame.display.set_caption("Cell Machine Python edition")

clock = pygame.time.Clock()



# Import base cells
cell_manager.register_all()
BG = cell_manager.get_background()
CELL_SIZE = cell_manager.CELL_SIZE



# Movement variables
scroll_speed = 1000 # In px/s
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_horizontal = 0
scroll_vertical = 0
zoom = 1



grid = cell_manager.Grid(10, 10)

def draw_grid():
    scaling = int(CELL_SIZE*zoom)
    for y in range(grid.height):
        for x in range(grid.width):
            coords = coords_to_pxl(x, y)
            screen.blit(grid[x, y].texture, coords)

def coords_to_pxl(x, y):
    return ((scroll_horizontal+CELL_SIZE*x)*zoom, (scroll_vertical+CELL_SIZE*y)*zoom)



# Main loop
run = True
while run:

    frame_time = clock.get_time()
    clock.tick()



    # Display
    screen.fill(BG_COLOR)
    draw_grid()



    # Move
    if scroll_left:
        scroll_horizontal += scroll_speed*frame_time/1000
    if scroll_right:
        scroll_horizontal -= scroll_speed*frame_time/1000
    if scroll_up:
        scroll_vertical += scroll_speed*frame_time/1000
    if scroll_down:
        scroll_vertical -= scroll_speed*frame_time/1000



    # Event handling
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False

        # Zoom
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1 and zoom < 8:
                zoom *= 2
            if event.y == -1 and zoom > 0.05:
                zoom /= 2
            grid.resize_textures(int(zoom*CELL_SIZE))

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
