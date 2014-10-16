from utilities import *
from parsers import load_data
from Field import *
from Unit import *
from settings import *
from Buttons import Button
import pygame

def go_to():
    global unit
    unit.set_target((0,0))

places = load_data('tile1.txt', 'data')
static_obj_lst = load_data('static_obj.txt', 'data')
container = Container()

pygame.init()
screen = pygame.display.set_mode((RES_X,RES_Y))
# pygame.mouse.set_visible(0)

clock = pygame.time.Clock()

done = False

field = Field(0, 0, places, static_obj_lst)
unit = Unit(3, 2, field)
field.add_unit(unit)
button = Button(500,10,('button_click.png','button_hover.png','button_off.png'),
                    function=go_to,text='Go to')

container.adds(field, unit, button)

while not done:
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True

        container.event(e)


    dt = clock.tick(FPS)
    container.update(dt)
    container.render(screen)

    pygame.display.flip()