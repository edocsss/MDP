import ArenaMap
from GridState import *

__author__ = 'ECAND_000'

# Should create helper methods to convert HEX to BINARY and BINARY to HEX
class MapDescriptor:
    # Both mapDescriptionPart1 and mapDescriptionPart2 store in HEX!!
    mapDescriptionPart1 = ""
    mapDescriptionPart2 = ""
    translatedMap = ""

    def __init__(self, mapDescriptorFileName=""):
        if len(mapDescriptorFileName) > 0:
            print("Reading map descriptor file...")
            self.readMapDescription(mapDescriptorFileName)
            print("Map descriptor is read!")
            print("Translating map...")
            self.translateFromMapDescription()
            print("Translated map is ready!")
        else:
            print("MapDescriptor is initiated only for writing...")

    def getTranslatedMap(self):
        return self.translatedMap

    def readMapDescription(self, fileName):
        try:
            f = open(fileName, "r")

            # Reading part 1
            self.mapDescriptionPart1 = f.readline().strip()

            # Skip one empty line
            f.readline()

            # Reading part 2
            self.mapDescriptionPart2 = f.readline().strip()
        except Exception as e:
            print("Error while reading map descriptor file!")
            print(e)

    def translateFromMapDescription(self):
        # Part 1
        temp1 = ""
        for n in self.mapDescriptionPart1:
            temp1 += self.hexToBinary(n)

        # Remove the padding bits
        temp1 = temp1[2 : 302]

        # Part 2
        temp2 = ""
        for n in self.mapDescriptionPart2:
            temp2 += self.hexToBinary(n)

        # 0 == NOT EXPLORED
        # 1 == EXPLORED WITH NO OBSTACLE
        # 2 == EXPLORED WITH OBSTACLE

        # TRANSLATING THE MAP DESCRIPTOR, ASSUMING THAT THE PADDING BITS ARE PUT AT THE END OF THE STRING!!
        # If the padding bits are put in the beginning of the string, the parsing should be done from the back to the beginning
        i = 0
        for n in temp1:
            if n == '0':
                self.translatedMap += '0'
            elif n == '1':
                if temp2[i] == '0':
                    self.translatedMap += '1'
                elif temp2[i] == '1':
                    self.translatedMap += '2'

                # Update mapDescriptionPart2 iterator
                i += 1

    def translateToMapDescription(self, arenaMap):
        gridMap = arenaMap.getGridMap()
        r1 = "11"
        r2 = ""

        print("Converting arenaMap into Map Descriptor...")
        for n in range (0, ArenaMap.ArenaMap.MAP_HEIGHT):
            for m in range (0, ArenaMap.ArenaMap.MAP_WIDTH):
                gridState = gridMap[n][m].getGridState()

                if gridState == GridState.UNEXPLORED or gridState == GridState.END_ZONE:
                    r1 += "0"
                elif gridState == GridState.EXPLORED_NO_OBSTACLE or gridState == GridState.START_ZONE or gridState == GridState.END_ZONE_EXPLORED:
                    r1 += "1"
                    r2 += "0"
                elif gridState== GridState.EXPLORED_WITH_OBSTACLE:
                    r1 += "1"
                    r2 += "1"

        r1 += "11"
        while len(r2) % 8 != 0:
            r2 += "0"

        return r1, r2

    def writeMapDescription(self, arenaMap):
        f = open("MapDescriptor.out", "w")
        r1, r2 = self.translateToMapDescription(arenaMap)

        # Writing to file for PART 1
        print("Writing PART 1 to file...")
        for i in range (0, len(r1), 4):
            b = self.binaryToHex(r1[i : i + 4])
            f.write(b)

        # One empty line
        f.write("\n\n")

        print("Writing PART 2 to file...")
        for i in range (0, len(r2), 4):
            b = self.binaryToHex(r2[i : i + 4])
            f.write(b)

        print("Map descriptor has been successfully written!")

    def hexToBinary(self, h):
        if h == '0':
            return '0000'
        elif h == '1':
            return '0001'
        elif h == '2':
            return '0010'
        elif h == '3':
            return '0011'
        elif h == '4':
            return '0100'
        elif h == '5':
            return '0101'
        elif h == '6':
            return '0110'
        elif h == '7':
            return '0111'
        elif h == '8':
            return '1000'
        elif h == '9':
            return '1001'
        elif h == 'A':
            return '1010'
        elif h == 'B':
            return '1011'
        elif h == 'C':
            return '1100'
        elif h == 'D':
            return '1101'
        elif h == 'E':
            return '1110'
        elif h == 'F':
            return '1111'

    def binaryToHex(self, b):
        if b == '0000':
            return '0'
        elif b == '0001':
            return '1'
        elif b == '0010':
            return '2'
        elif b == '0011':
            return '3'
        elif b == '0100':
            return '4'
        elif b == '0101':
            return '5'
        elif b == '0110':
            return '6'
        elif b == '0111':
            return '7'
        elif b == '1000':
            return '8'
        elif b == '1001':
            return '9'
        elif b == '1010':
            return 'A'
        elif b == '1011':
            return 'B'
        elif b == '1100':
            return 'C'
        elif b == '1101':
            return 'D'
        elif b == '1110':
            return 'E'
        elif b == '1111':
            return 'F'