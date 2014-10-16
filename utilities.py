import pygame,os
from pygame.locals import *

def load_image(name,path = 'Images', alpha_channel=False): #функция загрузки картинки
    fullname = os.path.join(path, name) #путь картинки
    try:
        image = pygame.image.load(fullname) #загрузка картинки
    except (pygame.error):
        print("Cannot load image:", name)
        return 0
    if (alpha_channel): #если есть альфа канал, конвертирование картинки с учетом альфа канала
        image = image.convert_alpha()
    else:
        image = image.convert() #если альфа канала нету, конвертирование без учета альфа канала (непонятно зачем, но надо)

    return image

class Container:
    def __init__(self):
        self.g_objects = []

    def add(self, object):
        self.g_objects.append(object)

    def adds(self, *objects):
        for obj in objects:
            self.g_objects.append(obj)

    def clear(self):
        self.g_objects = []

    def event(self, e):
        for obj in self.g_objects:
            obj.event(e)

    def update(self, dt):
        for obj in self.g_objects:
            obj.update(dt)

    def render(self, screen):
        for obj in self.g_objects:
            obj.render(screen)

class Text:   #простой класс, для вывода текста
    def __init__(self,text,x = 0,y = 0):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, 24)

    def render(self, screen):
        surf = self.font.render(str(self.text), True, (255,0,0))
        screen.blit(surf,(self.x,self.y))

