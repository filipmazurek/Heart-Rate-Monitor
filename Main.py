import Reader
import BeatDetector
import ProcessorHR
import Visualizer
import numpy as np


class Main:
    dataFilename = "default_file.bin"
    updateTimeSeconds= 20  # read in this much data at a time

    if __name__ == "__main__":
        reader = Reader(dataFilename, updateTimeSeconds)  # instantiate Reader, pass in what file to read in

        beatDetector = BeatDetector()
        processorHR = ProcessorHR()
        visualizer = Visualizer()

        while(reader.notDone()):
            [dataECG, dataPPG] = reader.getNextDataInstant()
            instantHR = beatDetector.findInstantHR(dataECG, dataPPG)
            visualizationInfo = processorHR.addInstantHR(instantHR)
            visualizer.displayNewInfo(visualizationInfo)

        cleanUp()


def clean_up():
    # TODO: finish the visualization in a clean way, ensure file is closed


class PassInformationToVisualization:
      # TODO: a class that contains arrays returned from the Processor to put into the Visualizer