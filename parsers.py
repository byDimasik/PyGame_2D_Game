import os

def load_data(file_name=None,directory = '',path=None):
    cwd = os.getcwd()                      #получение текущей директории
    if not path:
        file_name = os.path.join(directory,file_name)        #получение пути к файлу, относительно корня проекта
        path = os.path.join(cwd, file_name)    #получение полного пути к файлу
    file = open(path, 'r', encoding="utf-8")                 #открытие файла для чтения
    place = []               #список со списками, каждый элемент которго - тип тайла
    while True:
        line = list(file.readline())  #line - список, состоящий из строки файла
        if not line: break            #условие вихода из цикла (в данном случае конец файла)
        try:                          #попытка проверки условия, что строка начинается с цифры (искючает все строки, которые начинаются не с цифр)
            if type(int(line[0]))==int:   #если строка начинается с решетки, функция сразу перейдет к следующей строке
                lst = []           #список, элементы которого уже будут просто типы тайлов (без пробелов, знаков препинания)
                for i in line:
                    try:
                        lst.append(int(i)) #попытка преобразовать элемент line к типу int, если получилось, этот элемент
                                           #добавится в список, который после обработки всей строки будет добавлен в
                                           #окончательный список
                    except:
                        pass               #если преобразование не удалось, переход к следующему символу
                place.append(lst)          #в конечный список добавляется список, собранный из строки
        except:
            pass
    file.close()         #файл закрывается
    return place         #возвращается нужный список со списками