import random
from math import cos, sin, acos, radians, tan, pi, atan, sqrt, degrees
from Lamp import Lamp

# Doesnt use this function for the moment
def unitVector(v):
    x = v[0]
    y = v[1]
    vectorLength = sqrt(x ** 2 + y ** 2)
    return [x / vectorLength, y / vectorLength]

# Doesnt use this function for the moment
def isOppositeVectors(v1, v2):
    unit1 = unitVector(v1)
    unit2 = unitVector(v2)
    x1, x2 = unit1[0], unit2[0]
    y1, y2 = unit1[1], unit2[1]
    return (x1 + x2 + y1 + y2) < 0.2


# Returns the theta angle of that vector in spherical coordinates
def thetaOfVector(vector):
    x = vector[0]
    y = vector[1]
    theta = 0
    if x == 0:  # x = 0
        if y < 0:  # and y < 0
            theta = -pi / 2
        else:
            theta = pi / 2
    elif x < 0:
        if y < 0:  # and y < 0
            theta = atan(y / x) - pi  # 3. quadrant
        else:  # and y >= 0
            theta = atan(y / x) + pi  # 2. quadrant
    elif x > 0:
        if y < 0:  # and y < 0
            theta = atan(y / x)  # 4. quadrant
        else:  # and y >= 0
            theta = atan(y / x)  # 1. quadrant
    return round(theta, 10)


# Returns the phi angle of that vector in spherical coordinates
def phiOfVector(vector):
    rho = round(sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2), 5)  # sqrt(x^2+y^2+z^2)
    phi = round(acos(vector[2] / rho), 10)  # phi = arccos(z/Rho)
    return phi


# Returns an array where the best individuals appear exponentially more often
def selection(fitnessResults, currGen):
    matingPool = []
    if len(fitnessResults) == len(currGen):
        j = 0  # Which lamp index in fitnessResults
        for lamp in currGen:
            for i in range(fitnessResults[j]):  # If fitness result = 3 --> lamp appends 3 times to mating pool
                matingPool.append(lamp)
            j += 1  # next fitnessResult
    else:
        print("fitnessResult.length != currGen.length:", len(fitnessResults), len(currGen))
    return matingPool


def crossoverHole(hole_1, hole_2):
    # phi = 90-150 --> binary: 01011010-10010110 (8 bit)
    bit_pos = random.randrange(2, 5)
    if bit_pos == 2:
        head = 192  # 11000000
        tail = 63  # 00111111
    elif bit_pos == 3:
        head = 224  # 11100000
        tail = 31  # 00011111
    elif bit_pos == 4:
        head = 240  # 11110000
        tail = 15  # 00001111
    else:
        raise ValueError('Bit_pos supposed to be 2-4 but was:', bit_pos)

    phi_1, phi_2 = hole_1[0], hole_2[0]

    c1_phi = (phi_1 & head) + (phi_2 & tail)
    c2_phi = (phi_2 & head) + (phi_1 & tail)

    # Phi needs to be higher than 90 degrees
    if c1_phi < 90:
        c1_phi += random.randint(10, 40)
    if c2_phi < 90:
        c2_phi += random.randint(10, 40)

    return [c1_phi], [c2_phi]


def crossoverHead(head_1, head_2):
    # Diameter = 80-250 --> Binary: 01010000-11111010 (8 bit)
    bit_pos = random.randrange(2, 5)
    if bit_pos == 2:
        head = 192  # 11000000
        tail = 63  # 00111111
    elif bit_pos == 3:
        head = 224  # 11100000
        tail = 31  # 00011111
    elif bit_pos == 4:
        head = 240  # 11110000
        tail = 15  # 00001111
    else:
        raise ValueError('Bit_pos supposed to be 2-4 but was:', bit_pos)
    child_1_dia = (head_1[0] & head) + (head_2[0] & tail)
    child_2_dia = (head_2[0] & head) + (head_1[0] & tail)
    # Head dia has to be more than 80
    if child_1_dia < 80:
        child_1_dia += random.randint(30, 100)
    if child_2_dia < 80:
        child_2_dia += random.randint(30, 100)

    return [child_1_dia], [child_2_dia]


def crossoverLeg(leg_1, leg_2):
    # Theta = 0-360 --> binary: 000000000-101101000
    # Define random position for crossover bit
    bit_pos = random.randrange(2, 7)
    if bit_pos == 2:
        head = 385  # 110000000
        tail = 127  # 001111111
    elif bit_pos == 3:
        head = 448  # 111000000
        tail = 63  # 000111111
    elif bit_pos == 4:
        head = 480  # 111100000
        tail = 31  # 000011111
    elif bit_pos == 5:
        head = 496  # 111110000
        tail = 15  # 000001111
    elif bit_pos == 6:
        head = 504  # 111111000
        tail = 7  # 000000111
    else:
        raise ValueError('Bit_pos supposed to be 2-6 but was:', bit_pos)
    c1_theta = (leg_1[0] & head) + (leg_2[0] & tail)
    c2_theta = (leg_2[0] & head) + (leg_1[0] & tail)
    # Diameter = 10-50 --> binary: 0001010-110010 (6 bit)
    bit_pos = random.randrange(2, 5)
    if bit_pos == 2:
        head = 48  # 110000
        tail = 15  # 001111
    elif bit_pos == 3:
        head = 56  # 111000
        tail = 7  # 000111
    elif bit_pos == 4:
        head = 60  # 111100
        tail = 3  # 000011
    else:
        raise ValueError('Bit_pos supposed to be 2-4 but was:', bit_pos)
    c1_dia = (leg_1[1] & head) + (leg_2[1] & tail)
    c2_dia = (leg_2[1] & head) + (leg_1[1] & tail)
    # Diameter has to be bigger than 10
    if c1_dia < 10:
        c1_dia += random.randint(5, 30)
    if c2_dia < 10:
        c2_dia += random.randint(5, 30)

    # Length = 200-500 --> binary: 11001000-111110100 (9 bit)
    # Define random position for crossover bit
    bit_pos = random.randrange(2, 7)
    if bit_pos == 2:
        head = 385  # 110000000
        tail = 127  # 001111111
    elif bit_pos == 3:
        head = 448  # 111000000
        tail = 63  # 000111111
    elif bit_pos == 4:
        head = 480  # 111100000
        tail = 31  # 000011111
    elif bit_pos == 5:
        head = 496  # 111110000
        tail = 15  # 000001111
    elif bit_pos == 6:
        head = 504  # 111111000
        tail = 7  # 000000111
    else:
        raise ValueError('Bit_pos supposed to be 2-6 but was:', bit_pos)

    c1_length = (leg_1[2] & head) + (leg_2[2] & tail)
    c2_length = (leg_2[2] & head) + (leg_1[2] & tail)
    # Leg length has to be more than 200
    if c1_length < 200:
        c1_length += random.randint(50, 200)
    if c2_length < 200:
        c2_length += random.randint(50, 200)

    child_1, child_2 = [c1_theta, c1_dia, c1_length], [c2_theta, c2_dia, c2_length]
    return child_1, child_2


def crossoverButton(button_1, button_2):
    # Diameter = 5-25 --> binary: 00101-11001 (5 bit)
    # Height = 3-20 --> binary: 00011-10100 (5 bit)
    # Define random position for crossover bit
    bit_pos = random.randrange(1, 4)

    if bit_pos == 1:
        head = 16  # 10000
        tail = 15  # 01111
    elif bit_pos == 2:
        head = 24  # 11000
        tail = 7  # 00011
    elif bit_pos == 3:
        head = 28  # 11100
        tail = 3  # 00011
    else:
        raise ValueError('Bit_pos supposed to be 1-3 but was:', bit_pos)

    c1_dia = (button_1[0] & head) + (button_2[0] & tail)
    c2_dia = (button_2[0] & head) + (button_1[0] & tail)
    # button dia has to be more than 5
    if c1_dia < 5:
        c1_dia += random.randint(5, 15)
    if c2_dia < 5:
        c2_dia += random.randint(5, 15)

    c1_height = (button_1[1] & head) + (button_2[1] & tail)
    c2_height = (button_2[1] & head) + (button_1[1] & tail)
    # Button height has to be more than 3
    if c1_height < 3:
        c1_height += random.randint(5, 15)
    if c2_height < 3:
        c2_height += random.randint(5, 15)

    child_1, child_2 = [c1_dia, c1_height], [c2_dia, c2_height]
    return child_1, child_2


def crossoverBottom(bottom_1, bottom_2):
    # Diameter = 100-300 --> binary: 001100100-100101100 (9 bit)
    # Define random position for crossover bit
    bit_pos = random.randrange(2, 7)
    if bit_pos == 2:
        head = 385  # 110000000
        tail = 127  # 001111111
    elif bit_pos == 3:
        head = 448  # 111000000
        tail = 63  # 000111111
    elif bit_pos == 4:
        head = 480  # 111100000
        tail = 31  # 000011111
    elif bit_pos == 5:
        head = 496  # 111110000
        tail = 15  # 000001111
    elif bit_pos == 6:
        head = 504  # 111111000
        tail = 7  # 000000111
    else:
        raise ValueError('Bit_pos supposed to be 2-6 but was:', bit_pos)

    c1_dia = (bottom_1[0] & head) + (bottom_2[0] & tail)
    c2_dia = (bottom_2[0] & head) + (bottom_1[0] & tail)
    if c1_dia < 100:
        c1_dia += random.randint(40, 120)
    if c2_dia < 100:
        c2_dia += random.randint(40, 120)

    # Height = 10-50 --> binary: 0001010-110010 (6 bit)
    bit_pos = random.randrange(2, 5)
    if bit_pos == 2:
        head = 48  # 110000
        tail = 15  # 001111
    elif bit_pos == 3:
        head = 56  # 111000
        tail = 7  # 000111
    elif bit_pos == 4:
        head = 60  # 111100
        tail = 3  # 000011
    else:
        raise ValueError('Bit_pos supposed to be 2-4 but was:', bit_pos)

    c1_height = (bottom_1[1] & head) + (bottom_2[1] & tail)
    c2_height = (bottom_2[1] & head) + (bottom_1[1] & tail)
    if c1_height < 10:
        c1_height += random.randint(10, 30)
    if c2_height < 10:
        c2_height += random.randint(10, 30)

    child_1, child_2 = [c1_dia, c1_height], [c2_dia, c2_height]
    return child_1, child_2


# Returns two children which is a mix of the two input parents
def crossover(parent_1, parent_2):
    botC1, botC2 = crossoverBottom(parent_1.getBottomPara(), parent_2.getBottomPara())
    butC1, butC2 = crossoverButton(parent_1.getButtonPara(), parent_2.getButtonPara())
    legC1, legC2 = crossoverLeg(parent_1.getLegPara(), parent_2.getLegPara())
    headC1, headC2 = crossoverHead(parent_1.getHeadPara(), parent_2.getHeadPara())
    holeC1, holeC2 = crossoverHole(parent_1.getHoleDir(), parent_2.getHoleDir())

    child_1 = Lamp(botC1, butC1, legC1, headC1, holeC1)
    child_2 = Lamp(botC2, butC2, legC2, headC2, holeC2)
    return child_1, child_2


class GeneticLamp:

    def getPopSize(self):
        return self.__popSize

    def getCurrGeneration(self):
        return self.__currGeneration

    def setCurrGeneration(self, currGeneration):
        self.__currGeneration = currGeneration

    def getMutProb(self):
        return self.__mutProb

    def getGenerations(self):
        return self.__generations

    def __init__(self, popSize, generations, mutProb):
        self.__popSize = popSize  # For random population generation
        self.__generations = generations  # Amount of generations to go iterate
        self.__currGeneration = []
        self.__mutProb = mutProb

    def makeFirstGeneration(self):
        # Initialize random parameters
        lamps = []
        popSize = self.getPopSize()
        if popSize % 2 != 0:
            popSize += 1
        for i in range(popSize):
            # Bottom
            botDia = random.randint(100, 300)
            botHeight = random.randint(10, 50)
            # Button
            butDia = random.randint(5, 25)
            butHeight = random.randint(3, 20)
            # Leg
            leg_theta = random.randint(0, 360)
            legDia = random.randint(10, 50)
            legLength = random.randint(200, 500)
            # Head
            headDia = random.randint(80, 250)
            # Hole theta
            holeTheta = random.randint(80, 160)
            lamps.append(
                Lamp([botDia, botHeight], [butDia, butHeight], [leg_theta, legDia, legLength], [headDia], [holeTheta]))
        self.setCurrGeneration(lamps)
        return

    # Returns an array with fitness scores for each lamp that represents
    # how many times the object at that index is present in the mating pool
    def fitness(self, point):  # vector = [x, y, z]
        fitnessResults = []
        lamps = self.getCurrGeneration()
        for lamp in lamps:
            bottomRadius = lamp.getBottomPara()[0] / 2.0
            bottomHeight = lamp.getBottomPara()[1]

            legRad = lamp.getLegPara()[1] / 2.0
            legLength = lamp.getLegPara()[2]

            headDia = lamp.getHeadPara()[0]

            r = bottomRadius - legRad - 3 / 8 * headDia   # Radius from origin to bulb in xy-plane
            thetaLeg = radians(lamp.getLegPara()[0])  # angle input is degrees --> transform to radians
            x = round(r * cos(thetaLeg), 10)
            y = round(r * sin(thetaLeg), 10)
            z = bottomHeight + legLength
            # Point of the bulb = [x, y, z]
            phi_bulb = radians(lamp.getHoleDir()[0])  # angle input is degrees --> transform to radians
            if phi_bulb == 0:
                phi_bulb += 0.01  # just in case for division by 0
                print("something wrong with phi bulb: Cant be 0!")
            zDirectionHole = round((sqrt(x ** 2 + y ** 2)) / tan(phi_bulb), 10)  # z = sqrt(x^2+y^2)/tan(Phi)

            vectorBulb = [-x, -y, zDirectionHole]  # Vector from bulb
            vectorPoint = [point[0] - x, point[1] - y, point[2] - z]  # vector from bulb to the input point

            # Finds the angles of each vector in spherical coordinates
            phi_point = phiOfVector(vectorPoint)
            theta_bulb = thetaOfVector(vectorBulb)
            theta_point = thetaOfVector(vectorPoint)

            thetaP = thetaOfVector(point)
            thetaL = thetaLeg
            if thetaL > pi:
                thetaL -= 2*pi

            # Differences in angles
            dTheta = abs(theta_point - theta_bulb)
            if dTheta > pi:
                dTheta -= pi
            dPhi = abs(phi_point - phi_bulb)
            dAngle = dTheta + dPhi
            # f(x)=10/x^2 increases exponentially with a decrease in x--> a small decrease in theta equals a better score
            fitness_score = round(10 / dAngle ** 2)  # Rounds up or down to get a score of type int

            # if tPoint and tLeg is closer than pi/4 to eachother --> give low score
            if abs(thetaP - thetaL) < pi/4:
                fitnessResults.append(1)
            elif fitness_score > 10000:  # if the score is over 10000 then dAngle = 0.03 radians --> good enough
                fitnessResults.append(10000)
            else:
                fitnessResults.append(fitness_score)

        return fitnessResults

    # Iterates over current generation in the object and randomly "mutates" the parameters by
    # changing one random bit in each selected value.
    def mutate(self):
        for lamp in self.getCurrGeneration():
            i = 0  # Index of lamp parameter
            for attr, value in lamp.__dict__.items():
                if i > len(vars(lamp)) - 1:  # 5 parameters in each object therefore reset index at 4
                    i = 0
                parameterValues = value  # Example: bottomPara = [diameter, height]
                check = random.random()
                if check < self.getMutProb():
                    j = 0  # Index of value in lamp parameter
                    for val in parameterValues:
                        flipped = False  # removed minus sign?

                        if val < 0:
                            binValue = bin(val)[3:]  # [3:] because first three digits = -0b
                            flipped = True  # Yes -0b is removed --> add later
                        else:
                            binValue = bin(val)[2:]  # [2:] because first two digits = 0b

                        # Change random bit in the value
                        randomBitPos = random.randrange(0, len(binValue))
                        if binValue[randomBitPos] == '0':
                            binValue = binValue[:randomBitPos] + '1' + binValue[randomBitPos + 1:]
                        else:
                            binValue = binValue[:randomBitPos] + '0' + binValue[randomBitPos + 1:]
                        if flipped:
                            binValue = '-' + binValue
                        newValue = int(binValue, 2)
                        lamp.switch(i, j, newValue)
                        j += 1  # Next index for value in lamp parameter

                i += 1  # Next lamp parameter

        return

    # Runs the algorithm. Takes in the point the lamp should converge to
    def run(self, point):
        iterations = 0
        self.makeFirstGeneration()
        fitnessResult = []
        #  Number of iterations
        for i in range(0, self.getGenerations()):
            # If the results havent converged after 10 generations: try a new initial first population
            if i > 10 or i == self.getGenerations() - 1:
                print()
                print("Try running with new initial first population")
                print()
                return self.run(point)
            iterations += 1

            # Fitness evaluation
            fitnessResult = self.fitness(point)
            print("Fitness Results:", fitnessResult)

            for j in range(len(fitnessResult)):
                if fitnessResult[j] == 10000:
                    fittestLamp = self.getCurrGeneration()[j]
                    print("Iterations:", iterations, " Score: 10000")
                    return fittestLamp

            # Natural selection for crossover
            currentGen = self.getCurrGeneration().copy()
            self.setCurrGeneration([])  # Clears generation to add the next later
            fittestLamps = []

            matingPool = selection(fitnessResult, currentGen)  # Only create mating pool once for each gen
            # Randomly chooses parents from the mating pool. Bigger fitness score --> lamp appears more in mating pool
            for _ in currentGen:
                fittestLamps.append(random.choice(matingPool))

            # Crossover
            nextGen = []
            for k in range(0, len(fittestLamps), 2):
                child_1, child_2 = crossover(fittestLamps[k], fittestLamps[k + 1])
                nextGen.append(child_1)
                nextGen.append(child_2)
            self.setCurrGeneration(nextGen)

            # Mutation

            if i < self.getGenerations() - 1:  # Doesnt mutate last generation
                self.mutate()

        indexOfFittest = 0
        for i in range(len(fitnessResult)):
            if fitnessResult[i] > fitnessResult[indexOfFittest]:
                indexOfFittest = i
        print("Iterations:", iterations, " Score:", fitnessResult[indexOfFittest])
        fittestLamp = self.getCurrGeneration()[indexOfFittest]
        return fittestLamp


# Test the class


g1 = GeneticLamp(30, 20, 0.02)

p = [100, -100, 0]

fitLamp = g1.run(p)

print("Fittest Lamp:")
print("Base:", fitLamp.getBottomPara(), ", Button:", fitLamp.getButtonPara(), ", Leg:",
      fitLamp.getLegPara(),
      ", Head:", fitLamp.getHeadPara(), ", Hole:", fitLamp.getHoleDir())

thetaLeg = fitLamp.getLegPara()[0]
thetaP = degrees(thetaOfVector(p))
if thetaP < 0:
    thetaP += 360
if thetaLeg < 180:
    thetaBulb = thetaLeg + 180
else:
    thetaBulb = thetaLeg - 180
print("Theta point:", round(thetaP, 2), ", Theta Bulb:", thetaBulb)
