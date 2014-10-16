from utilities import *
from Tile import *
import math
from findPathLee import *

class Unit:
    def __init__(self,column,row,parent, places = None):
        self.parent = parent            #родитель
        self.column = column            #столбик
        self.row = row                  #строка
        self.start_speed = 500          #начальная скорость
        self.speed = None               #скорость с учетом задержки
        self.temp_tile = Tile(0, 0, 'temp', 'tile_grass.jpg')  #временный тайл
        self.image = load_image('Unit.png', path='Images', alpha_channel=True)       #картинка персонажа
        self.rect = self.image.get_rect()
        self.rect.x = self.temp_tile.rect.w*column+self.temp_tile.rect.w/2-self.rect.w/2
        self.rect.y = self.temp_tile.rect.h*row+self.temp_tile.rect.h/2-self.rect.h/2
        self.target_row = None      #целевая строка
        self.target_column = None   #целевой столбик
        self.moving = False
        self.places = parent.places
        self.counter = 1
        self.target_coords = None
        self.stop = False           #останавливает персонажа, если поле перетаскивалось
        self.distance = 0           #пройденное расстояние

    def event(self,e):
        if e.type == MOUSEBUTTONUP:
            if self.parent.temp_tile:
                if self.stop or self.moving or not self.parent.temp_tile.get_type_typetile():
                    self.stop = False    #поле перестало перетаскиваться, персонаж снова бегает
                    return -1
            self.set_target()

        if e.type == MOUSEMOTION:# and self.parent.MouseOnImage:   #drag&drop персонажа вместе с полем
            if self.parent.temp_tile and not self.moving:
                finish = (self.parent.temp_tile.column,self.parent.temp_tile.row)
                self.target_coords = findPath(self.parent.matrix_permeability,(self.column,self.row),finish)
            if self.parent.MouseOnImage:
                if self.parent.drag:
                    rel = e.rel
                    self.rect.x += rel[0]
                    self.rect.y += rel[1]

    def set_target(self, target_tile=0):    #fixme установить целевые столбик, строку и координаты
        if target_tile:
            self.target_coords = findPath(self.parent.matrix_permeability,(self.column,self.row),target_tile)
        if self.target_coords == -1 or not self.target_coords:
            return -1
        if self.counter<len(self.target_coords):
            coord = self.target_coords[self.counter]
            if self.moving:
                return -1
            d_column = int(math.fabs(coord[0]-self.column))    #дельта столбца
            d_row = int(math.fabs(coord[1]-self.row))          #дельта строки
            if ((d_column == 1 and d_row == 0) or (d_column == 0 and d_row == 1)):
                self.moving = True
                self.target_row = coord[1]
                self.target_column = coord[0]
                self.target_x = int(self.parent.rect.x+coord[0]*self.temp_tile.rect.w+self.temp_tile.rect.w/2-self.rect.w/2)
                self.target_y = int(self.parent.rect.y+coord[1]*self.temp_tile.rect.h+self.temp_tile.rect.h/2-self.rect.h/2)
                self.counter += 1
            else:
                return -1
        # print('counter',self.counter)

    def moving_to_target(self):   #плавное движение персонажа
        if self.target_row == self.row:   #если целевая строка равна текущей строке, то идет перемещение по столбикам
            if self.target_column<self.column:
                self.rect.x-=self.speed
            elif self.target_column>self.column:
                self.rect.x+=self.speed
            if int(math.fabs(self.rect.x-self.target_x))<=self.speed:   #если персонаж приблизился к целевой точке,
                self.column = self.target_column                        #то его исходные столбик, срока и координаты
                self.rect.x = self.target_x                             #приравниваются к целевым
                #if self.counter>len(self.target_coords):
                self.moving = False
            self.distance += self.speed
            if self.distance >= self.parent.temp_tile.rect.w:             #когда персонаж прошел тайл, за ним стирается след
                self.parent.traces_coords = self.parent.traces_coords[1:]
                self.distance = 0
                self.parent.draw_traces(self.parent.traces_coords)

        elif self.target_column == self.column:  #если целевой столбик равен текущему столбику, то идет перемещение по строкам
            if self.target_row<self.row:
                self.rect.y-=self.speed
            elif self.target_row>self.row:
                self.rect.y+=self.speed
            if int(math.fabs(self.rect.y-self.target_y))<=self.speed:
                self.row = self.target_row
                self.rect.y = self.target_y
                #if self.counter>len(self.target_coords):
                self.moving = False
            self.distance += self.speed
            if self.distance >= self.parent.temp_tile.rect.h:            #когда персонаж прошел тайл, за ним стирается след
                self.parent.traces_coords = self.parent.traces_coords[1:]
                self.distance = 0
                self.parent.draw_traces(self.parent.traces_coords)

    def update(self, dt):
        if self.moving:
            self.speed = self.start_speed*(dt/1000)
            self.parent.drag = False
            self.moving_to_target()
            self.set_target()
        else:
            self.parent.drag = True
            self.counter = 1

    def render(self,surf):
        surf.blit(self.image,self.rect)


