from Cylinder import Cylinder
from Sphere import Sphere
from math import sin, cos, radians, sqrt, tan
from GeneticLamp import GeneticLamp

point = [-300, -200, 200]

geneticLamp = GeneticLamp(30, 10, 0.05)

lamp = geneticLamp.run(point)

baseParameters = lamp.getBottomPara()
baseDia = baseParameters[0]
baseHeight = baseParameters[1]

legParameters = lamp.getLegPara()
legAngle = radians(legParameters[0])
legDia = legParameters[1]
legHeight = legParameters[2]
legDist = baseDia / 2 * 0.8 - legDia / 2
legX = round(legDist * cos(legAngle))
legY = round(legDist * sin(legAngle))
legZ = baseHeight

buttonParameters = lamp.getButtonPara()
buttonDia = buttonParameters[0]
buttonHeight = buttonParameters[1]
buttonX = -legX
buttonY = -legY
buttonZ = baseHeight

headDia = lamp.getHeadPara()[0]
dHead = 3 / 8 * headDia
headX = legX - dHead*cos(legAngle)


headY = legY - dHead*sin(legAngle)


headZ = baseHeight + legHeight

holeAngle = radians(lamp.getHoleDir()[0])
holeDirectionZ = round(sqrt(legX ** 2 + legY ** 2) / tan(holeAngle))
holeDirection = [-legX, -legY, holeDirectionZ]
holeDia = 8 / 10 * headDia
holeHeight = 4 / 5 * headDia


leg = Cylinder(legX, legY, legZ, legDia, legHeight, [0, 0, 1])
leg.initForNX()

base = Cylinder(0, 0, 0, baseDia, baseHeight, [0, 0, 1])
base.initForNX()

button = Cylinder(buttonX, buttonY, buttonZ, buttonDia, buttonHeight, [0, 0, 1])
button.initForNX()

head = Sphere(headX, headY, headZ, headDia)
head.initForNX()

cylSubtract = Cylinder(headX, headY, headZ, holeDia, holeHeight, holeDirection)
cylSubtract.initForNX()

head.subtract(cylSubtract)
