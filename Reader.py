import numpy as np
import struct



class Reader:
    openFile
    numSamplesToGet

    def __init__(self, filename, secondsAtATime):
        openedFile = open(filename, 'rb')
        binary_data = openFile.read(2)  # read two bytes (16 bits)
        sampleRateHz = struct.unpack('<H', binary_data)
        numSamplesToGet = sampleRateHz * secondsAtATime


    def get_next_data_instant():
        dataArrayECG = []
        dataArrayPPG = []

        for numSample in range(0, numSamplesToGet):
            appendBinaryData(dataArrayECG)
            appendBinaryData(dataArrayPPG)

        return [dataArrayECG, dataArrayPPG]


    def appendBinaryData(someArray):
        binary_data = openedFile.read(2)
        if !binary_data:
            openedFile.close()
            break
        dataPoint = struct.unpack('<H', binary_data)
        someArray.append(dataPoint[0])

        return someArray