from utilities import load_image
import pygame

class Static_object:
    def __init__(self,column,row,image_name, img_dir_name = 'Images/Static_objs',w=62,h=62):
        self.row = row
        self.column = column
        self.type = 'type'
        self.image_name = image_name
        self.image = load_image(image_name, path=img_dir_name, alpha_channel=True)
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = self.column*self.rect.w
        self.rect.y = self.row*self.rect.h
        # self.permeability = False
        # if int(image_name[0])>=6:
        #     self.permeability = True

    def get_brush(self):
        return ('st_obj',self.image_name)

    def check_mouse_coords(self,xy):           #проверяет, находятся ли координаты мыши в нужном ректе
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def render(self,surf,rect=None):
        if not rect:
            rect = self.rect
        surf.blit(self.image,rect)
