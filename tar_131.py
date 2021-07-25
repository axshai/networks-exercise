import pygame
from math import *
import numbers
def main():
    clock = pygame.time.Clock()
    namee=r"C:\netandpython\work\image1.jpg"
    player=r"C:\netandpython\work\men.png"
    WINDOW_WIDTH = 668
    WINDOW_HEIGHT = 398
    pygame.init()
    #pygame.mouse.set_visible(False)
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    finish = False
    img = pygame.image.load(namee)
    screen.blit(img, (0, 0))
    player_image = pygame.image.load(player).convert()
    player_image.set_colorkey((80,255,86))
    screen.blit(player_image, [170, 200])
    pygame.display.flip()
    pos=(170,200)
    current= screen.subsurface((0,0,668,398))
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        mouse_point = pygame.mouse.get_pos()
                        screen.blit(player_image, mouse_point)
                        current = screen.subsurface((0, 0, 668, 398))
                        pygame.display.flip()
            elif event.type == pygame:
                if event.key ==pygame.k_up:
                    pos=(pos[0]-1,pos[1])
                elif event.key ==pygame.k_down:
                    pos = (pos[0] + 1, pos[1])
                elif event.key == pygame.k_left:
                    pos = (pos[0] , pos[1]-1)
                elif event.key == pygame.k_right:
                    pos = (pos[0], pos[1] + 1)
                elif event.key == pygame.k_space:
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
            else:
               mouse_point = pygame.mouse.get_pos()
               pos=mouse_point
        screen.blit(current, (0, 0))
        screen.blit(player_image, pos)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()



