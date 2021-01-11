from math import degrees


class Lamp:

    def __init__(self, bottomPara, buttonPara, legPara, headPara, holeDir):
        self.__bottomPara = bottomPara  # [diameter, height] (100-300mm, 10-50mm)
        self.__buttonPara = buttonPara  # [diameter, height] (5-25mm, 3-20mm)
        self.__legPara = legPara  # [Theta, diameter, length] (0-360 degrees, 10-50mm, 200-500mm)
        self.__headPara = headPara  # [diameter] (80-250mm)
        self.__holeDir = holeDir  # [Phi] (90-150 degrees) from +z-axis

    def getBottomPara(self):
        return self.__bottomPara

    def setBottomPara(self, bottomPara, i):
        self.__bottomPara[i] = bottomPara

    def getButtonPara(self):
        return self.__buttonPara

    def setButtonPara(self, buttonPara, i):
        self.__buttonPara[i] = buttonPara

    def getLegPara(self):
        return self.__legPara

    def setLegPara(self, legPara, i):
        self.__legPara[i] = legPara

    def getHeadPara(self):
        return self.__headPara

    def setHeadPara(self, headPara, i):
        self.__headPara[i] = headPara

    def getHoleDir(self):
        return self.__holeDir

    def setHoleDir(self, holeDir, i):
        self.__holeDir[i] = holeDir

    # Switches a parameter value with the input value during mutation
    def switch(self, index, valueIndex, value):
        try:
            if index == 0:
                self.setBottomPara(value, valueIndex)
            elif index == 1:
                self.setButtonPara(value, valueIndex)
            elif index == 2:
                self.setLegPara(value, valueIndex)
            elif index == 3:
                self.setHeadPara(value, valueIndex)
            elif index == 4:
                self.setHoleDir(value, valueIndex)
        except IndexError:
            print("Index in mutation was out of range in: def switch()")
