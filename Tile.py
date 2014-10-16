from utilities import load_image
import pygame,os
from pygame.locals import *

class Tile:
    def __init__(self,column,row,type, image_name=None, parent=None):
        self.image_name = None
        if not image_name:
            if type == 'grass':
                self.image_name = 'tile_grass.jpg'
            elif type == 'hole':
                self.image_name = 'tile_hole.png'
            elif type == 'water':
                self.image_name = 'tile_water.gif'
        else:
            self.image_name = image_name   #имя картинки
        self.image = load_image(self.image_name, path='Images/Tiles')  #сама картинка
        self.transparent_image = load_image('transparent_tile.png',path='Images', alpha_channel=True)  #прозрачная картинка, которая накладывается поверх тайла
        self.rect = self.image.get_rect()  #рект картинки
        self.column = column  #столбик, в котором находится тайл
        self.row = row  #строка, в которой находится тайл
        self.type = type #тип тайла
        self.transparent = False  #показатель невидимости. False - тайл видимый
        x = column*self.rect.w     #координата х тайла равна номер столбика умножить на ширину картинки тайла
        y = row*self.rect.h        #координата у тайла равна номер строки умножить на высоту картинки тайла
        self.rect.x = x
        self.rect.y = y

    def __repr__(self):
        return "Tile %s|%s type:%s, coord(%s,%s)"%(self.column, self.row, self.type, self.rect.x,self.rect.y)

    def get_type(self):
        return self.type

    def get_size(self):
        return self.rect.size

    def get_coord(self):             #получение координат
        return (self.rect.x,self.rect.y)

    def check_mouse_coords(self, xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def change_image(self,status):  #меняет картинка на картинку с тайлом прозрачности и обратно
        if status=='on' and not self.transparent:  #status - если 'on', то картинка делается невидимой, и если тайл еще не невидимый
            self.image.blit(self.transparent_image,(0,0))
            self.transparent = True
        elif status=='off':
            self.image = load_image(self.image_name,path='Images/Tiles', alpha_channel=True)
            self.transparent = False

    def get_type_typetile(self):       #тип типа тайла (проходимый или нет)
        if self.type == 'grass':
            return True
        else:
            return False

    def render(self,surf,coord=None):
        x = self.column*self.rect.w   #здесь не подходят координаты ректа, потому что координаты ректа - это координаты относительно всего окна
        y = self.row*self.rect.h      #поэтому тут считаются координаты исходя ТОЛЬКО из столбца и строки

        if coord:
            x, y = coord[0], coord[1]
        surf.blit(self.image,(x,y))   #и блитуются на поверхность поля.

        #а это рисовашки, чтобы каждый тайл был обведен
        pygame.draw.lines(surf,(250,0,0),True, [(self.rect.x, self.rect.y),
                                        (self.rect.x+self.rect.w,self.rect.y),
                                        (self.rect.x+self.rect.w,self.rect.y+self.rect.h),
                                        (self.rect.x,self.rect.y+self.rect.h)])

class Tile_Brush(Tile):
    def __init__(self,column,row,type,image_name,parent=None):
        Tile.__init__(self,column,row,type,image_name,parent)
        self.brush = False          #если флаг активен, значит, данный тайл является кистью
        self.parent = parent

    def check_mouse_coords(self,xy):           #проверяет, находятся ли координаты мыши в нужном ректе
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def event(self,e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            coord = self.parent.cursor_coord
            if self.check_mouse_coords(coord):
                self.brush = True
                # print('True')

    def get_brush(self):
        return ('tile',self.type)
