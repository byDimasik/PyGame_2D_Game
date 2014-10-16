# -*- coding:UTF-8 -*-
import pygame, LoadSave
from Scrollbar import ScrollBar
from Buttons import Button
from Tile import *
from parsers import *
from Static_object import *

class Place_editor:
    """
    Класс согласует работу (раздает события, отрисовывает) объектов редактора
    (самого поля, ползунков, палитр и т.д.)
    """
    def __init__(self,wh):
        self.objs_list = []            #список перемещаемых объектов
        self.static_objects_list = []  #список не перемещаемых объектов
        self.image = pygame.Surface(wh, pygame.SRCALPHA)    #поверхность редактора, на которую рендерятся все объекты
        self.scroll_column = ScrollBar(10,30,50,1,text='Кол-во столбцов:') #ползунок, устанавливающий кол-во столбиков
        self.scroll_column.set_num(5)
        self.scroll_row = ScrollBar(10,95,50,1,text='Кол-во строк:')       #ползунок, устанавливающий кол-во строк
        self.scroll_row.set_num(5)

        self.field = Editing_field((370,130), self)   #изменяемое поле, то есть будущая карта для игры
        self.objs_list.append(self.field)

        self.tiles_pallet = Window(20,150,400,100,parent=self)    #палитра с тайлами
        self.objs_list.append(self.tiles_pallet)

        #----- тут создаются особые тайлы - кисти и добавлятся в палитру
        tile1 = Tile_Brush(0,0,'hole','tile_hole.png',parent=self.tiles_pallet)
        self.tiles_pallet.add_obj(tile1)
        tile2 = Tile_Brush(0,0,'grass','tile_grass.jpg',parent=self.tiles_pallet)
        tile3 = Tile_Brush(0,0,'water','tile_water.gif',parent=self.tiles_pallet)
        self.tiles_pallet.add_obj(tile2)
        self.tiles_pallet.add_obj(tile3)
        #-----

        #создается палитра статических объектов, для нее создаются обычные статические объекты и запихиваются в палитру
        self.static_objects_pallet = Window(20,350,100,100,parent=self)
        self.objs_list.append(self.static_objects_pallet)

        st_obj_palm = Static_object(0,0,'1.png')
        self.static_objects_pallet.add_obj(st_obj_palm)
        st_obj_penek = Static_object(0,0,'3.png')
        self.static_objects_pallet.add_obj(st_obj_penek)
        #----

        #кнопки сохранения и загрузки
        self.save_matrix_button = Button(250,10,('button_click.png','button_hover.png','button_off.png'),
                                        self.field.save_tile_matrix,text='Сохранить')
        self.load_matrix_button = Button(450,10,('button_click.png','button_hover.png','button_off.png'),
                                        self.field.load_tile_matrix,text='Загрузить')
        self.static_objects_list.append(self.save_matrix_button)
        self.static_objects_list.append(self.load_matrix_button)
        #----

        self.objs_list_for_events = []
        """
        список объектов для передачи событий, тут все объекты, как статические, так и динамические.
        Ползунки не входят ни в список статических, ни в список динамических, потому что не относятся ни к тем,
        ни к другим. Они "полудинамичесие", так как подвижна их Часть, но не входят в список динамических, чтобы
        не рисоваться поверх динамических объектов, если ползунки будут в фокусе.
        """
        self.objs_list_for_events.append(self.scroll_column)
        self.objs_list_for_events.append(self.scroll_row)
        for obj in self.objs_list:
            self.objs_list_for_events.append(obj)
        for obj in self.static_objects_list:
            self.objs_list_for_events.append(obj)

    def event(self,e):
        """
        метод передает кому надо, какие надо события
        """
        # for scroll in self.scrolls_list:  #ползнукам
        #     scroll.event(e)

        if e.type == pygame.MOUSEMOTION:  #событие движения мыши отдельно передается всем объектом, кроме тому, который
                                          #в фокусе, тому и так предастся. Только для красоты.
            for obj in self.objs_list_for_events[1:]:
                obj.event(e)

        if e.type == pygame.MOUSEBUTTONDOWN: #при нажатии клавиши мыши, определяется объект в фокусе (на который ткнули)
                                             #и перемещается в начало списка объектов для передачи событий
            for i in range(0,len(self.objs_list_for_events)):
                if self.objs_list_for_events[i].check_mouse_coords(e.pos):
                    self.objs_list_for_events[i].CursorOnImage = True
                    self.objs_list_for_events.insert(0,self.objs_list_for_events[i])
                    self.objs_list_for_events.pop(i+1)
                    break
            for i in range(0,len(self.objs_list)):
                if self.objs_list[i].check_mouse_coords(e.pos):
                    self.objs_list[i].CursorOnImage = True
                    self.objs_list.insert(0,self.objs_list[i])
                    self.objs_list.pop(i+1)
                    break

        if e.type == USEREVENT+1:   #событие движения ползунка, передается полю, чтобы то изменило свой размер,
                                    #даже если поле не находится в фокусе
            self.field.event(e)

        self.objs_list_for_events[0].event(e)  #ВСЕ события передаются объекту, который в фокусе

    def render(self, screen):
        """
        Метод рендерит объекты на self.image, заодно тут объясняется надобность списков отдельно для ползунков,
        статических и динамичческих объектов
        """
        self.image.fill((255,255,255))
        # for scroll in self.scrolls_list:  #СНАЧАЛА рендерятся ползунки, они всегда внизу
        #     scroll.render(self.image)
        # for obj in self.static_objects_list: #рисуются статические объекты, ВО ВТОРУЮ ОЧЕРЕДЬ
        #     obj.render(self.image)
        # self.objs_list.reverse()
        # for obj in self.objs_list: #поверх всех рисуются динамические объекты начиная с конца
        #     obj.render(self.image)
        # self.objs_list.reverse()
        self.objs_list_for_events.reverse()
        for obj in self.objs_list_for_events:
            obj.render(self.image)
        self.objs_list_for_events.reverse()
        screen.blit(self.image,(0,0))

class Editing_field:       #редактируемое поле
    def __init__(self,coord,parent):
        self.parent = parent
        self.coord = coord
        self.column_amt = 0 #количество столбцов
        self.row_amt = 0    #количество строк

        self.brush_type = 'tile'
        self.brush = 'hole'      #кисть
        self.tile_list = []      #список тайлов
        self.st_objs_list = []

        self.pre_tile = None
        self.test_tile = Tile(0,0,'temp','tile_hole.png')     #тестовый тайл
        self.temp_tile = None

        self.tile_grid = None      #поверхность с тайлами
        self.st_objs_grid = None      #поверхность со статическими объектами
        self.rect = None
        self.recreate_surf()

        self.CursorOnImage = False   #показатель наличия курсора на картинке

        self.create_tiles()
        self.draw_tiles()

    def save_tile_matrix(self):
        """
        Сохранение матрицы тайлов в виде форматированной строки в файл
        """
        # tile_matrix = []
        tile_matrix_str = ''
        for tile_lst in self.tile_list:
            # row_tile = []
            for tile in tile_lst:
                type = tile.get_type()
                if type == 'hole':
                    tile_matrix_str += '0 '
                    # row_tile.append(0)
                elif type == 'grass':
                    tile_matrix_str += '1 '
                    # row_tile.append(1)
                elif type == 'water':
                    tile_matrix_str += '2 '
                    # row_tile.append(2)
            tile_matrix_str = tile_matrix_str[:len(tile_matrix_str)]+'\n'
            # tile_matrix.append(row_tile)

        st_objs_matrix_str = ''
        for st_objs_lst in self.st_objs_list:
            for st_obj in st_objs_lst:
                if st_obj == 0:
                    st_objs_matrix_str += '0 '
                else:
                    st_objs_matrix_str += st_obj.image_name[0]+' '
            st_objs_matrix_str = st_objs_matrix_str[:len(st_objs_matrix_str)]+'\n'

        load_or_save = LoadSave.LoadSave()
        load_or_save.saveFile()
        if load_or_save.savePath:
            file = open(load_or_save.savePath, 'w')
            file.write(tile_matrix_str)
            file.close()

            path = load_or_save.savePath[:load_or_save.savePath.rfind('.')]+'_st_objs'+load_or_save.savePath[load_or_save.savePath.rfind('.'):]
            file = open(path, 'w')
            file.write(st_objs_matrix_str)
            file.close()

    def load_tile_matrix(self):
        """
        Загрузка поля из файла
        """
        load_or_save = LoadSave.LoadSave()
        load_or_save.openFile()
        if load_or_save.openPath:
            self.tile_list = []
            tile_list = load_data(path=load_or_save.openPath)
            self.parent.scroll_row.set_num(len(tile_list))
            self.parent.scroll_column.set_num(len(tile_list[0]))
            for index_row, row in enumerate(tile_list):
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

            self.st_objs_list = []
            path = load_or_save.openPath[:load_or_save.openPath.rfind('.')]+'_st_objs'+load_or_save.openPath[load_or_save.openPath.rfind('.'):]
            st_objs_list = load_data(path=path)
            for index_row, row in enumerate(st_objs_list):
                objs_lst = []
                for index_coord, coord in enumerate(row):
                    for i in range(1,10):
                        if i == coord:
                            img_name = '%s.png'%i
                            static_obj = Static_object(index_coord,index_row,img_name)
                            objs_lst.append(static_obj)
                    if coord == 0:
                        objs_lst.append(0)
                self.st_objs_list.append(objs_lst)

            self.recreate_surf()

    def recreate_surf(self):   #пересоздает поверхность
        w = self.parent.scroll_column.get_num()*self.test_tile.rect.w  #размеры поля
        h = self.parent.scroll_row.get_num()*self.test_tile.rect.h
        self.tile_grid = pygame.Surface((w,h))    #поверхность сетки Тайлов
        self.st_objs_grid = pygame.Surface((w,h), pygame.SRCALPHA)    #поверхность со статическими объектами
        self.rect = self.tile_grid.get_rect()
        self.rect.x = self.coord[0]
        self.rect.y = self.coord[1]
        if self.parent.scroll_column.get_num()-self.column_amt>0 and self.tile_list:
            self.change_columns(self.parent.scroll_column.get_num()-self.column_amt)
        elif self.parent.scroll_column.get_num()-self.column_amt<0:
            self.change_columns(self.parent.scroll_column.get_num()-self.column_amt)

        if self.parent.scroll_row.get_num()-self.row_amt>0 and self.tile_list:
            self.change_rows(self.parent.scroll_row.get_num()-self.row_amt)
        elif self.parent.scroll_row.get_num()-self.row_amt<0 and self.tile_list:
            self.change_rows(self.parent.scroll_row.get_num()-self.row_amt)

        self.draw_tiles()
        self.draw_st_objs()

    def change_columns(self,num):
        if num>0:
            for i in range(0,num):
                for i, lst in enumerate(self.tile_list):
                    tile = Tile(len(lst),i,'hole','tile_hole.png')
                    lst.append(tile)
        else:
            for i in range(0,(-1*num)):
                for lst in self.tile_list:
                    lst.pop()
        self.column_amt = self.parent.scroll_column.get_num()

    def change_rows(self,num):
        if num>0:
            for i in range(0,num):
                lst = []
                for j in range(0,len(self.tile_list[0])):
                    tile = Tile(j,len(self.tile_list),'hole','tile_hole.png')
                    lst.append(tile)
                self.tile_list.append(lst)
        else:
            for i in range(0,(-1*num)):
                self.tile_list.pop()
        self.row_amt = self.parent.scroll_row.get_num()

    def create_tiles(self):     #заполение списка тайлов
        self.tile_list = []
        self.st_objs_list = []
        for i in range(0,self.parent.scroll_row.get_num()):
            lst = []
            lst_st = []
            for j in range(0,self.parent.scroll_column.get_num()):
                tile = Tile(j,i,'hole','tile_hole.png')
                lst.append(tile)
                lst_st.append(0)
            self.tile_list.append(lst)
            self.st_objs_list.append(lst_st)
        self.draw_tiles()
        self.row_amt = len(self.tile_list)
        self.column_amt = len(self.tile_list[0])

    def draw_tiles(self, redrawing_tiles = None, redrawing_tile=None,st_obj=None):
        if not redrawing_tiles and not redrawing_tile:
            for tile_lst in self.tile_list:
                for tile in tile_lst:
                    tile.render(self.tile_grid)
        elif redrawing_tiles:
            for tile in redrawing_tiles:
                tile.render(self.tile_grid)
        else:
            redrawing_tile.render(self.tile_grid)

    def draw_st_objs(self):
        self.st_objs_grid.fill(pygame.SRCALPHA)
        for lst in self.st_objs_list:
            for obj in lst:
                if obj:
                    obj.render(self.st_objs_grid)
        # if obj_list:
        #     for lst in obj_list:
        #         for obj in lst:
        #             if obj:
        #                 obj.render(self.st_objs_grid)
        # elif obj:
        #     obj.render(self.st_objs_grid)

    def set_brush(self, brush):
        self.brush_type = brush[0]
        self.brush = brush[1]

    def check_mouse_coords(self, xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def event(self,e):
        if e.type == USEREVENT+1:
            self.recreate_surf()

        if e.type == pygame.MOUSEBUTTONUP:
            self.CursorOnImage = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            if not self.check_mouse_coords(e.pos):
                return -1
            coord = (int((e.pos[0]-self.rect.x)/self.test_tile.rect.h),int((e.pos[1]-self.rect.y)/self.test_tile.rect.w))
            #вычисляются столбик и строка тайла, по которому тыкнули, и этот тайл, если он типа, отличного от кисти, меняется.
            if self.brush_type == 'tile':
                if self.tile_list[coord[1]][coord[0]].type != self.brush:
                    self.tile_list[coord[1]][coord[0]] = Tile(coord[0],coord[1],self.brush,parent=self)
                    self.draw_tiles(redrawing_tile=self.tile_list[coord[1]][coord[0]])
            elif self.brush_type == 'st_obj':
                if self.st_objs_list[coord[1]][coord[0]]:
                    if self.st_objs_list[coord[1]][coord[0]].image_name == self.brush:
                        self.st_objs_list[coord[1]][coord[0]] = 0
                    else:
                        st_obj = Static_object(coord[0],coord[1],self.brush)
                        self.st_objs_list[coord[1]][coord[0]] = st_obj
                else:
                    st_obj = Static_object(coord[0],coord[1],self.brush)
                    self.st_objs_list[coord[1]][coord[0]] = st_obj
                self.draw_st_objs()#(obj=self.st_objs_list[coord[1]][coord[0]])

        if e.type == pygame.MOUSEMOTION:
            coord = e.pos
            coord = (coord[0]-self.rect.x,coord[1]-self.rect.y)   #координаты мыши перводятся из системы окна в систему ректа поля,
                                                                  #относительно которого будет определятся положение мыши для тайлов
            tile_coord = (int(coord[0]/self.test_tile.rect.w),int(coord[1]/self.test_tile.rect.h))

            if self.check_mouse_coords(e.pos):
                if tile_coord[0]>len(self.tile_list[0]) or tile_coord[1]>len(self.tile_list):
                    return -1

                if self.temp_tile:
                    self.temp_tile.change_image('off')
                self.pre_tile = self.temp_tile
                self.temp_tile = self.tile_list[tile_coord[1]][tile_coord[0]]
                self.temp_tile.change_image('on')
                if self.pre_tile:
                    self.draw_tiles((self.pre_tile,self.temp_tile))
                    # self.draw_st_objs(obj=self.st_objs_list[self.pre_tile.column][self.pre_tile.row])
                    # print(self.st_objs_list[self.temp_tile.row][self.temp_tile.column])
                    # if self.st_objs_list[self.temp_tile.row][self.temp_tile.column] != 0:
                    #     self.draw_st_objs(obj=self.st_objs_list[self.temp_tile.row][self.temp_tile.column])

            if self.CursorOnImage:
                self.rect.x += e.rel[0]
                self.rect.y += e.rel[1]
                self.coord = (self.rect.x,self.rect.y)


    def render(self,surf):
        surf.blit(self.tile_grid, self.rect)
        surf.blit(self.st_objs_grid, self.rect)

        pygame.draw.lines(screen,(255,0,0),True, [(self.rect.x, self.rect.y),
                                                  (self.rect.x+self.rect.w,self.rect.y),
                                                  (self.rect.x+self.rect.w,self.rect.y+self.rect.h),
                                                  (self.rect.x,self.rect.y+self.rect.h)])

class Window:                     #класс пустого окна
    def __init__(self,x,y,w,h,text='Window',draganddrop=True,parent=None):
        self.coord = (x,y)
        self.parent = parent
        self.w = w
        self.h = h
        self.topbox_h = 20
        self.surf = pygame.Surface((w,h+self.topbox_h))
        self.surf.fill((0,255,145))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.CursorOnImage = False
        self.cursor_coord = (0,0)
        self.objs_list = []
        pygame.draw.rect(self.surf, (0,0,0), (0,0,self.w,self.topbox_h))

    def add_obj(self,obj):
        obj.rect.x = len(self.objs_list)*obj.rect.w + (len(self.objs_list)+1)*self.topbox_h
        obj.rect.y = 2*self.topbox_h

        self.objs_list.append(obj)
        self.resize_window()

    def resize_window(self):
        self.surf = pygame.Surface((self.objs_list[0].rect.w*len(self.objs_list)+(len(self.objs_list)+1)*self.topbox_h,
                                    self.objs_list[0].rect.h+self.topbox_h+2*self.topbox_h))
        self.surf.fill((0,255,145))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord[0], self.coord[1]
        pygame.draw.rect(self.surf, (0,0,0), (0,0,self.rect.w,self.topbox_h))

    def check_mouse_coords(self, xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def event(self,e):
        if e.type == MOUSEBUTTONDOWN:
            if self.check_mouse_coords(e.pos) and self.parent:
                self.cursor_coord = (e.pos[0]-self.rect.x,e.pos[1]-self.rect.y)
                for obj in self.objs_list:
                    if obj.check_mouse_coords(self.cursor_coord):
                        self.parent.field.set_brush(obj.get_brush())
        if e.type == pygame.MOUSEBUTTONUP:
            self.CursorOnImage = False

        if e.type == pygame.MOUSEMOTION:
            if self.CursorOnImage:
                self.rect.x += e.rel[0]
                self.rect.y += e.rel[1]

    def render(self,screen):
        for obj in self.objs_list:
            obj.render(self.surf, obj.rect)

        screen.blit(self.surf, self.rect)

        #рисовашка ,чтобы окно было обведено
        pygame.draw.lines(screen,(255,0,0),True, [(self.rect.x, self.rect.y),
                                        (self.rect.x+self.rect.w,self.rect.y),
                                        (self.rect.x+self.rect.w,self.rect.y+self.rect.h),
                                        (self.rect.x,self.rect.y+self.rect.h)])

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))

    editor = Place_editor((800,600))

    clock = pygame.time.Clock()

    done = False

    while not done:
        screen.fill((255, 255, 255))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

            editor.event(e)

        editor.render(screen)

        pygame.display.flip()