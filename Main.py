from Reader import Reader
from Beat_Detector import Beat_Detector
from HR_Processor import HR_Processor
from tkinter import *

root = Tk()  # global root in this case. Only way I know tkinter for now...


class Main:
    def __init__(self):
        self.data_filename = "60bpm16uintTest.bin"
        self.update_time_seconds = 20  # read in this much data at a time
        self.data_bit_length = 16  # length of each information point. Can be 12 or 16

        self.inst_hr_var = StringVar("")
        self.one_min_hr_var = StringVar("")
        self.five_min_hr_var = StringVar("")
        self.alarm_var = StringVar("")

    def run_hr_monitor(self):
        reader = Reader(self.data_filename, self.update_time_seconds, self.data_bit_length)
        beatDetector = Beat_Detector(self.update_time_seconds)
        processorHR = HR_Processor(reader.get_sample_rate())
        # visualizer = Visualizer()

        while reader.still_reading():
            [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
            instant_hr = beatDetector.find_instant_hr(data_array_ecg, data_array_ppg)
            visualization_info = processorHR.add_inst_hr(instant_hr)
            self.render_information_display(visualization_info)

    def render_information_display(self, visualization_info):
        self.inst_hr_var = visualization_info.get_inst_hr()
        self.one_min_hr_var = visualization_info.get_one_min_hr()
        self.five_min_hr_var = visualization_info.get_five_min_hr()

    def setup_tkinter(self):

        Label(root, anchor = NW, text = "Instant HR: ").pack()
        Label(root, anchor=W, text="One Min HR: ").pack()
        Label(root, anchor=SW, text="Five Min HR: ").pack()
        Label(root, anchor=E, text="Alarm").pack()

        Label(root, anchor=N, textvariable=self.inst_hr_var).pack()
        Label(root, anchor=CENTER, textvariable=self.one_min_hr_var).pack()
        Label(root, anchor=S, textvariable=self.five_min_hr_var).pack()
        Label(root, anchor=SE, textvariable=self.alarm_var, bg="red").pack()

        root.after(10, self.run_hr_monitor())
        root.mainloop()

if __name__ == "__main__":
    myMain = Main()
    myMain.setup_tkinter()
