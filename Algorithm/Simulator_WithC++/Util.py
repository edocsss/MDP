__author__ = 'ECAND_000'

class Util:
    @staticmethod
    def hexToBinary(h):
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

    @staticmethod
    def binaryToHex(b):
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