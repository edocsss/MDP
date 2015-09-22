import ArenaMap
from Util import *
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
            temp1 += Util.hexToBinary(n)

        # Remove the padding bits
        temp1 = temp1[2 : 302]

        # Part 2
        temp2 = ""
        for n in self.mapDescriptionPart2:
            temp2 += Util.hexToBinary(n)

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

                if gridState == GridState.END_ZONE:
                    r1 += "0"

                # Assume that those UNEXPLORED are EXPLORED_NO_OBSTACLE --> simple inference
                elif gridState == GridState.UNEXPLORED or  gridState == GridState.EXPLORED_NO_OBSTACLE or gridState == GridState.START_ZONE or gridState == GridState.END_ZONE_EXPLORED:
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
            b = Util.binaryToHex(r1[i : i + 4])
            f.write(b)

        # One empty line
        f.write("\n\n")

        print("Writing PART 2 to file...")
        for i in range (0, len(r2), 4):
            b = Util.binaryToHex(r2[i : i + 4])
            f.write(b)

        print("Map descriptor has been successfully written!")