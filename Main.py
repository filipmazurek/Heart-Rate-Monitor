from Reader import Reader
import BeatDetector
import ProcessorHR
import Visualizer
import numpy as np


class Main:
    data_filename = "default_file.bin"
    update_time_seconds = 20  # read in this much data at a time
    data_bit_length = 16;  # length of each information point. Can be 12 or 16

    if __name__ == "__main__":
        reader = Reader(data_filename, update_time_seconds, data_bit_length)  # instantiate Reader, pass in what file to read in

        beatDetector = BeatDetector()
        processorHR = ProcessorHR()
        visualizer = Visualizer()

        while reader.still_reading():
            [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
            instant_hr = beatDetector.find_instant_hr(data_array_ecg, data_array_ppg)
            visualization_info = processorHR.addInstantHR(instant_hr)
            visualizer.displayNewInfo(visualization_info)

        cleanUp()


def clean_up():
    # TODO: finish the visualization in a clean way, ensure file is closed


class PassInformationToVisualization:
    # TODO: a class that contains arrays returned from the Processor to put into the Visualizer