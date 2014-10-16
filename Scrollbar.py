from utilities import *
import pygame

class ScrollBar:            #ползунок.
    def __init__(self,x,y,max_num,min_num=0, text=None):
        self.scroll_image = load_image('scroll.png','Images',1)   #картинка ползунка
        self.scrollbar_image = load_image('scrollbar.png','Images',1)  #картинка поля, по которому катается ползунок
        self.x = x
        self.y = y
        self.x_scroll = x #координата х ползунка, сначала равна координате поля
        self.min_num = min_num
        self.max_num = max_num #максимальное значение ползунка
        self.num_text = False #текст с циферкой значения ползунка, который выводится под ползунком
        self.MouseOnScroll = False  #ползунок отпущен
        self.rect = self.scroll_image.get_rect()
        self.rect.move_ip(self.x_scroll,self.y)
        self.num = 0  #значение ползунка, по умолчанию 0
        self.num_scroll() #метод, преобразующий значение ползунка в текст, который потом выводится на экран
        self.text = None #подпись к ползунку
        if text:
            """
            если объекту передана подпись, то она создается в виде текста над ползунком
            """
            self.text = Text(text,x=self.x,y=self.y-20)

    def render(self,screen):
        screen.blit(self.scrollbar_image,(self.x,self.y)) #рендер поля
        screen.blit(self.scroll_image,(self.x_scroll,self.y)) #рендер ползунка
        self.num_text.render(screen)
        if self.text:
            self.text.render(screen)

    def set_num(self,num):   #установка значения ползунка без перетаскивания
        if num < self.min_num: num = self.min_num
        if num > self.max_num: num = self.max_num

        rect = self.scrollbar_image.get_rect()

        if num == self.max_num: #если ползунок уехал за поле, то
            self.x_scroll = self.x+rect.w-self.rect.w #его координата равна концу поля
        elif num == self.min_num:     #а если ползунок уехал за поле в другую сторону
            self.x_scroll = self.x     #координата ползунка приравнивается к началу поля
        else:
            vd = (rect.w-self.rect.w)/(self.max_num-self.min_num)
            self.x_scroll += int((num-self.num)*vd)
        self.num = num
        self.rect.x = self.x_scroll
        self.num_scroll()

    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_mouse_coords(event.pos) == True:
                self.MouseOnScroll = True  #ползунок зацеплен
                #print(self.MouseOnScroll)

        if event.type == pygame.MOUSEBUTTONUP:
            self.MouseOnScroll = False  #ползунок отпущен

        if event.type == pygame.MOUSEMOTION:
            if self.MouseOnScroll == True: #and self.check_mouse_coords(event.pos):  #движение ползунка
            #если на ползунок нажали и держат и курсор находится внутри ползунка
                self.x_scroll += event.rel[0] #новая координата ползунка=старая+смещение
                rect = self.scrollbar_image.get_rect()
                self.num = int((self.x_scroll-self.x)/((rect.w-self.rect.w)/(self.max_num-self.min_num)))
                if self.x_scroll > self.x+rect.w-self.rect.w: #если ползунок уехал за поле, то
                    self.num = self.max_num
                    self.x_scroll = self.x+rect.w-self.rect.w #его координата равна концу поля
                elif self.x_scroll < self.x:     #а если ползунок уехал за поле в другую сторону
                    self.num = self.min_num
                    self.x_scroll = self.x     #координата ползунка приравнивается к началу поля
                else:
                    self.num = int((self.x_scroll-self.x)/((rect.w-self.rect.w)/(self.max_num-self.min_num)))
                self.rect.x = self.x_scroll
                if self.num<self.min_num:
                    self.num = self.min_num
                self.num_scroll()

    def check_mouse_coords(self,xy):
        """
        Метод проверяет, на какую часть ползунка кликнули. Если на левую, то ползунок смещается
        на единицу влево, если на правую, то на единицу вправо, если на середину, то ползунок
        начинает перетаскиваться
        """
        rect_left = Rect((self.rect.x,self.rect.y),(self.rect.w*0.3,self.rect.h))
        rect_right = Rect((self.rect.x+self.rect.w*0.7,self.rect.y),(self.rect.w*0.3,self.rect.h))
        rect_center = Rect((self.rect.x+self.rect.w*0.3,self.rect.y),(self.rect.w*0.3,self.rect.h))
        if rect_center.collidepoint(xy):
            return True
        elif rect_left.collidepoint(xy):
            self.set_num(self.num-1)
        elif rect_right.collidepoint(xy):
            self.set_num(self.num+1)
        else:
            return False

    def num_scroll(self):
        """
        Метод переводящий, цифру положения ползунка в текст, для рендера
        """
        if self.max_num!=0: #если максимальное значение ползунка не равно 0 (чтобы не было деления на ноль)
            self.num_text = Text(self.num,self.x_scroll+19,self.y+25) #и получившееся значение в текст
        else:
            self.num = str(self.min_num)
            self.num_text = Text(str(self.num),self.x_scroll+19,self.y+25)
        change_scroll = pygame.event.Event(USEREVENT+1, num = self.num, sender= self)
        pygame.event.post(change_scroll)
        #print(self, 'value = ' ,self.get_num())

    def get_num(self):
        return self.num