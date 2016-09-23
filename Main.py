from Reader import Reader
from BeatDetector import BeatDetector
from ProcessorHR import ProcessorHR
from Visualizer import Visualizer
from Information_Passer import *
from tkinter import *

class Main:
    def __init__(self):
        self.data_filename = "default_file.bin"
        self.update_time_seconds = 20  # read in this much data at a time
        self.data_bit_length = 16  # length of each information point. Can be 12 or 16

    def run_hr_monitor(self, root):
        reader = Reader(self.data_filename, self.update_time_seconds, self.data_bit_length)  # instantiate Reader, pass in what file to read in

        beatDetector = BeatDetector(self.update_time_seconds)
        processorHR = ProcessorHR()
        visualizer = Visualizer()

        while reader.still_reading():
            [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
            instant_hr = beatDetector.find_instant_hr(data_array_ecg, data_array_ppg)
            visualization_info = processorHR.addInstantHR(instant_hr)
            visualizer.displayNewInfo(visualization_info, root)

        self.cleanUp()

    def clean_up(self):
        # TODO: finish the visualization in a clean way, ensure file is closed

    if __name__ == "__main__":
        root = Tk()
        root.after(0, run_hr_monitor(root))
        root.mainloop()
