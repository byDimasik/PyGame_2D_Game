import pygame,os
from pygame.locals import *
from Tile import *
#from parser import load_data
from utilities import *
from Unit import *
from Static_object import *
from findPathLee import *

class Field:
    def __init__(self,x,y,places, static_obj_matrix):
        self.places = places
        self.static_obj_matrix = static_obj_matrix
        self.matrix_permeability = []  #мартица проходимости

        for index_i,i in enumerate(places):
            lst = []
            for index_j,j in enumerate(i):
                if j == 1 and (self.static_obj_matrix[index_i][index_j]>=6 and self.static_obj_matrix[index_i][index_j]<=9):
                    lst.append(1)
                elif j == 1 and not self.static_obj_matrix[index_i][index_j]:
                    lst.append(1)
                else:
                    lst.append(0)
            self.matrix_permeability.append(lst)

        self.static_obj_lst = []
        self.temp_tile = None
        self.pre_tile = None
        self.tile_list = []  #список со списками тайлов, пока пустой
        temp_tile = Tile(0,0,'temp','tile_grass.jpg') #временный тайл, чтобы вычислисть размеры ректа
        w = temp_tile.rect.w*len(places[0])  #ширина ректа поля
        h = temp_tile.rect.h*len(places)     #высота ректа поля
        self.w = w
        self.h = h
        self.image = pygame.Surface((w,h))   #поверхность поля
        self.traces_surf = pygame.Surface((w,h), pygame.SRCALPHA)        #поверхность, на которой будут отрисовываться следы
        self.traces_image = load_image('traces.png',path='Images', alpha_channel=True)
        self.rect_traces = self.traces_image.get_rect()
        self.traces_coords = []              #список с координатами, на которых будут отрисовываться следы
        self.way_surf = pygame.Surface((w,h)) #поверхность для пути
        self.rect = self.image.get_rect()    #рект поля
        self.rect.x = x #координаты поля
        self.rect.y = y
        self.drag = True
        self.unit = None      #Персонаж на поле
        for index_row, row in enumerate(self.places):
            lst = []  #список с тайлами в строке, потом добавится в список со списками тайлов
            for index_coord, coord in enumerate(row):
                if coord==0:  #если элемент равен 0, то создается тайл с дыркой
                    tile = Tile(index_coord,index_row,'hole', 'tile_hole.png',self)
                    lst.append(tile)
                elif coord==1: #если элемент равен 1, то создается тайл травы
                    tile = Tile(index_coord,index_row,'grass', 'tile_grass.jpg',self)
                    lst.append(tile)
                elif coord==2: #если элемент равен 1, то создается тайл воды
                    tile = Tile(index_coord,index_row,'water', 'tile_water.gif',self)
                    lst.append(tile)
            self.tile_list.append(lst)

        for index_row, row in enumerate(self.static_obj_matrix):
            for index_coord, coord in enumerate(row):
                for i in range(1,10):
                    if i == coord:
                        img_name = '%s.png'%i
                        static_obj = Static_object(index_coord,index_row,img_name)
                        self.static_obj_lst.append(static_obj)

        self.MouseOnImage = False  #курсор на поле
        self.draw_tiles()
        self.draw_static_objs()

    def draw_static_objs(self):    #отрисовывает статически объекты на поле
        for obj in self.static_obj_lst:
            obj.render(self.image)

    def draw_tiles(self, redrawing_tiles = None):  #отрисовка тайлов
        if not redrawing_tiles:
            for tile_lst in self.tile_list:
                for tile in tile_lst:
                    tile.render(self.image)
            self.draw_static_objs()
        else:
            for tile in redrawing_tiles:
                tile.render(self.image)
            self.draw_static_objs()

    #magic begins here
    def event(self,e):  #самое интересное, события
        if e.type == MOUSEBUTTONDOWN:
            #if self.check_mouse_coords(e.dict['pos']):
            #    self.MouseOnImage = True   #если ткнули на поле, то поле знает, что на него ткнуто
            self.MouseOnImage = self.check_mouse_coords(e.dict['pos'])
        if e.type == MOUSEBUTTONUP:
            self.MouseOnImage = False     #как только мышь откнулась, поле узнал это и понял, что он откнут
        if e.type == MOUSEMOTION:
            self.drag_and_drop(e.rel)  #поле катается по окну
            #---меняется картинка тайлов
            coord = e.pos
            coord = (coord[0]-self.rect.x,coord[1]-self.rect.y)   #координаты мыши перводятся из системы окна в систему ректа поля,
                                                                  #относительно которого будет определятся положение мыши для тайлов
            target_coords = None

            for tile_lst in self.tile_list:
                for tile in tile_lst:
                    if tile.check_mouse_coords(coord):
                        self.pre_tile = self.temp_tile
                        if self.pre_tile:
                            self.pre_tile.change_image('off')
                        self.temp_tile = tile
                        tile.change_image('on')
                        if self.unit:
                            target_coords = self.unit.target_coords
            if self.pre_tile:
                self.draw_tiles((self.pre_tile,self.temp_tile))
                if not self.unit.moving:
                    self.traces_surf.fill(pygame.SRCALPHA)

            if self.unit.moving:
                return -1

            self.traces_coords = []
            if (target_coords and target_coords != -1) and (self.unit.row != self.temp_tile.row or self.unit.column != self.temp_tile.column):
                for i in target_coords[1:]:
                    coord = self.tile_list[i[1]][i[0]].get_coord()
                    self.traces_coords.append(coord)
                self.draw_traces(self.traces_coords)
            #if self.unit.row != self.temp_tile.row or self.unit.column != self.temp_tile.column:
            #    for i in target_coords[1:]:
            #        coord = self.tile_list[i[1]][i[0]].get_coord()
            #        self.draw_traces(coord)
            #---

    def draw_traces(self,coords):
        self.traces_surf.fill(pygame.SRCALPHA)
        if len(coords) == 1:
            self.traces_surf.fill(pygame.SRCALPHA)
        else:
            for coord in coords:
                coord = list(coord)
                coord[0] += self.tile_list[0][0].rect.w/2-self.rect_traces.w/2
                coord[1] += self.tile_list[0][0].rect.h/2-self.rect_traces.h/2
                self.traces_surf.blit(self.traces_image,coord)

    def check_mouse_coords(self, xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def drag_and_drop(self,rel):  #каталка поля по окну
        if self.drag:
            if self.MouseOnImage:  #если ткнуто на поле, то поле катается исходя из rel события
                self.rect.x += rel[0]
                self.rect.y += rel[1]
                if self.unit:
                    self.unit.stop = True    #поле перетаскивается, останавливаем персонажа

    def add_unit(self,unit):
        self.unit = unit

    def update(self, dt):
        pass

    def render(self,screen):
        screen.blit(self.image, self.rect) #рендер поля
        screen.blit(self.traces_surf,self.rect)

        #рисовашка ,чтобы поле было обведено
        #pygame.draw.lines(screen,(255,0,0),True, [(self.rect.x, self.rect.y),
        #                                (self.rect.x+self.rect.w,self.rect.y),
        #                                (self.rect.x+self.rect.w,self.rect.y+self.rect.h),
        #                                (self.rect.x,self.rect.y+self.rect.h)])


