#
#Matrix = [[1, 0, 1, 1],
#          [1, 0, 1, 1],
#          [1, 1, 1, 0],
#          [1, 0, 1, 0]]
#Start =  (2, 0)
#Finish = (0, 2)


def findPath(Matrix, Start, Finish):
    resPath = {0:[Start], }
    res = []
    check = True
    currentPosition = Start
    i = 0
    counter = 0
    if Matrix[Start[1]][Start[0]] and Matrix[Finish[1]][Finish[0]]:
        while currentPosition != Finish:
            if len(Matrix[0])* len(Matrix)<= counter:
                return -1
            for currentPosition in resPath[i]:
                if currentPosition == Finish:
                    break
                newPoints = checkAround(currentPosition, Matrix)
                for newPoint in newPoints:
                    for j in list(resPath.values()):
                        if newPoint in j:
                            check = False
                    if not newPoint in res and check:
                        res+=[newPoint]
                    check = True

            if Finish in res:
                res = [Finish]
            i+=1
            resPath[i] = res
            res = []
            counter+=1
        resPath = output(resPath, i, Matrix, Start)
        return resPath
    else:
        return -1

def output(resPath, endOfDictionary, Matrix, Start):
    try:
        res = [resPath[len(resPath.keys())-2][0], ]
    except KeyError:
        return -1
    endOfDictionary-=1
    while not Start in res:
        for i in range(0, endOfDictionary):
            pointsAround = checkAround(res[len(res)-1], Matrix)
            for j in pointsAround:
                if j in resPath[i] and not j in res:
                    res.append(j)
                    endOfDictionary-=1
                    break
    res.reverse()
    return res


def checkAround(currentPosition, Matrix):
    res = []
    currentPositionX, currentPositionY = currentPosition
    MatrixSize = (len(Matrix[0]), len(Matrix))

    if(currentPositionX + 1 < MatrixSize[1] and Matrix[currentPositionY][currentPositionX+1]): # Проверка справа
        res.append((currentPositionX+1, currentPositionY))

    if(currentPositionX - 1 >= 0 and Matrix[currentPositionY][currentPositionX-1]): # Проверка слева
        res.append((currentPositionX-1, currentPositionY))

    if(currentPositionY + 1 < MatrixSize[0] and Matrix[currentPositionY+1][currentPositionX]): # Проверка снизу
        res.append((currentPositionX, currentPositionY+1))

    if(currentPositionY - 1 >= 0 and Matrix[currentPositionY-1][currentPositionX]): # Проверка сверху
        res.append((currentPositionX, currentPositionY-1))

    return res  # 1 Проверка справа, 2 Проверка слева, 3 Проверка снизу, 4 Проверка сверху

#print(findPath(Matrix, Start, Finish))