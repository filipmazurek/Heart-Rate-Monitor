from Reader import Reader
from Beat_Detector import Beat_Detector
from HR_Processor import HR_Processor
from tkinter import *
import time

root = Tk()  # global root in this case. Only way I know tkinter for now...


class Main:
    def __init__(self, filename_new="HRTester.bin", seconds_at_a_time_new=20,
                 seconds_between_display_new=1, data_bit_length_new=16):
        self.time_passed = 0
        if filename == "":
            filename_new = "HRTester.bin"
        self.data_filename = filename_new
        if seconds_at_a_time_new == "":
            seconds_at_a_time_new= 20
        self.update_time_seconds = int(seconds_at_a_time_new)  # read in this much data at a time
        if seconds_between_display_new == "":
            seconds_between_display_new = 1
        self.seconds_between_readings = float(seconds_between_display_new)  # ideally same as update. But make lower for quicker progress.
        if data_bit_length_new == "":
            data_bit_length_new = 16
        self.data_bit_length = int(data_bit_length_new)  # length of each information point. Can be 12 or 16

        self.inst_hr_var = StringVar("")
        self.one_min_hr_var = StringVar("")
        self.five_min_hr_var = StringVar("")
        self.alarm_var = StringVar("")
        self.time_passed_string = StringVar("")

    def run_hr_monitor(self):
        reader = Reader(self.data_filename, self.update_time_seconds, self.data_bit_length)
        beatDetector = Beat_Detector(self.update_time_seconds)
        processorHR = HR_Processor(self.update_time_seconds)
        # visualizer = Visualizer()

        [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
        while reader.still_reading():
            instant_hr = beatDetector.find_instant_hr(data_array_ecg, data_array_ppg)
            visualization_info = processorHR.add_inst_hr(instant_hr)
            self.render_information_display(visualization_info)
            [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
            time.sleep(self.seconds_between_readings)

        print("DONE")
        self.cleanUp()

    def render_information_display(self, visualization_info):
        self.inst_hr_var.set(int(visualization_info.get_inst_hr()))
        self.one_min_hr_var.set(int(visualization_info.get_one_min_hr()))
        self.five_min_hr_var.set(int(visualization_info.get_five_min_hr()))

        self.time_passed += self.update_time_seconds
        m, s = divmod(self.time_passed, 60)
        h, m = divmod(m, 60)
        temp_time_string = "%d:%02d:%02d" % (h, m, s)
        self.time_passed_string.set(temp_time_string)

        # uncomment the following lines for a terminal print
        print("instant: ", end="")
        print(int(visualization_info.get_inst_hr()))
        print("one_min: ", end="")
        print(int(visualization_info.get_one_min_hr()))
        print("five_min: ", end="")
        print(int(visualization_info.get_five_min_hr()))
        print("time_passed", end="")
        print (temp_time_string)
        print("#############################")

        root.update()

    def setup_tkinter(self):

        Label(root, text="Instant HR: ").grid(row=0, column=0)
        Label(root, text="One Min HR: ").grid(row=1, column=0)
        Label(root,  text="Five Min HR: ").grid(row=2, column=0)
        Label(root,  text="Alarm: ").grid(row=3, column=0)
        Label(root, text="Time Passed: ").grid(row=4, column=0)

        Label(root, textvariable=self.inst_hr_var).grid(row=0, column=1)
        Label(root, textvariable=self.one_min_hr_var).grid(row=1, column=1)
        Label(root, textvariable=self.five_min_hr_var).grid(row=2, column=1)
        Label(root, textvariable=self.alarm_var).grid(row=3, column=1)
        Label(root, textvariable=self.time_passed_string).grid(row=4, column=1)

        root.after(500, self.run_hr_monitor())
        root.mainloop()

    def cleanUp(self):
        root.quit()
        root.destroy()


if __name__ == "__main__":
    filename = input("Please enter the binary file name: ")
    seconds_at_a_time = input("How many seconds of data will be read at a time? : ")
    seconds_between_display = input("How many seconds to wait between displaying data? : ")
    data_bit_length = input("Is the data 12 or 16-bit? Enter '12' or '16' only: ")
    myMain = Main(filename, seconds_at_a_time, seconds_between_display, data_bit_length)
    myMain.setup_tkinter()
