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

        beatDetector = BeatDetector(update_time_seconds)
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


class InformationPasserClass:
    def __init__(self, inst_hr, one_min_hr, five_min_hr):
        self.inst_hr = inst_hr
        self.one_min_hr = one_min_hr
        self.five_min_hr = five_min_hr
        self.ten_min_log = None
        self.bradycardia_alarm = False
        self.tachycardia_alarm = False


    def add_ten_min_log(self, someArray):
        self.ten_min_log = someArray

    def set_bradycardia_alarm(self):
        self.bradycardia_alarm = True

    def set_tachycardia_alarm(self):
        self.tachycardia_alarm = True

    def get_inst_hr(self):
        return self.inst_hr

    def get_one_min_hr(self):
        return self.one_min_hr

    def get_five_min_hr(self):
        return self.one_five_hr

    def get_ten_min_log(self):
        return self.ten_min_log

    def get_tachycardia_alarm(self):
        return self.tachycardia_alarm

    def get_bradycardia_alarm(self):
        return self.bradycardia_alarm