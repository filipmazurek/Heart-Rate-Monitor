from Reader import Reader
from Beat_Detector import BeatDetector
from HR_Processor import HRProcessor
from tkinter import *
import time


root = Tk()  # global root in this case. Only way I know tkinter for now...


class Main:
    """ Initializer method for main. Creates the necessary parameters for other functions to access. Creates the
    StringVars that are later used to display data to the tkinter screen.
    """
    def __init__(self):

        args = self.parse_arguments()

        self.data_filename = args.data_filename
        self.tachycardia = args.tachycardia
        self.bradycardia = args.bradycardia

        # user changable parameters
        self.update_time_seconds = 10  # read in this much data at a time
        self.seconds_between_readings = 1  # time between display updates.
        self.data_bit_length = 16  # length of each information point. Can be 12 or 16
        # end user changable parameters

        self.time_passed = 0
        self.inst_hr_var = StringVar("")
        self.one_min_hr_var = StringVar("")
        self.five_min_hr_var = StringVar("")
        self.alarm_var = StringVar("")
        self.time_passed_string = StringVar("")

    @staticmethod
    def parse_arguments():
        import argparse as ap

        par = ap.ArgumentParser(description="heart rate monitor parameters",
                                formatter_class=ap.ArgumentDefaultsHelpFormatter)

        par.add_argument('--filename',
                         dest='data_filename',
                         help='filename of binary data',
                         type=str,
                         default='test.bin')

        par.add_argument('--tachycardia',
                         dest='tachycardia',
                         help='threshold for tachycardia',
                         type=float,
                         default='200.0')

        par.add_argument('--bradycardia',
                         dest='bradycardia',
                         help='threshold for bradycardia',
                         type=float,
                         default='40.0')

        args = par.parse_args()

        return args

    def run_hr_monitor(self):
        """ The heart of the program. This function runs the while loop that calls all other classes that are part of
        this assignment. It calls the classes that read the data in, find the instant heart rate, and find the average
        heart rates.
        Calls the method to destroy the display and finish running the script.
        """
        reader = Reader(self.data_filename, self.update_time_seconds, self.data_bit_length)
        beat_detector = BeatDetector(self.update_time_seconds)
        processor_hr = HRProcessor(self.update_time_seconds, self.tachycardia, self.bradycardia)

        [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
        while reader.still_reading():
            instant_hr = beat_detector.find_instant_hr(data_array_ecg, data_array_ppg)
            visualization_info = processor_hr.add_inst_hr(instant_hr, self.time_passed_string)
            self.render_information_display(visualization_info)
            [data_array_ecg, data_array_ppg] = reader.get_next_data_instant()
            time.sleep(self.seconds_between_readings)

        print("DONE")
        self.clean_up()

    def render_information_display(self, visualization_info):
        """ Updates all necessary information in the tkinter display by updating the StringVars. Includes an optional
        console print

        :param visualization_info: class which contains all necessary information to display.
        """
        self.inst_hr_var.set(int(visualization_info.get_inst_hr()))
        self.one_min_hr_var.set(int(visualization_info.get_one_min_hr()))
        self.five_min_hr_var.set(int(visualization_info.get_five_min_hr()))
        if visualization_info.get_bradycardia_alarm():
            self.alarm_var.set("Bradycardia!!")
        elif visualization_info.get_tachycardia_alarm():
            self.alarm_var.set("Tachycardia!!")
        else:
            self.alarm_var.set("")

        self.time_passed += self.update_time_seconds
        m, s = divmod(self.time_passed, 60)
        h, m = divmod(m, 60)
        temp_time_string = "%d:%02d:%02d" % (h, m, s)
        self.time_passed_string.set(temp_time_string)

        # uncomment the following lines for a console print

        # print("instant: ", end="")
        # print(int(visualization_info.get_inst_hr()))
        # print("one_min: ", end="")
        # print(int(visualization_info.get_one_min_hr()))
        # print("five_min: ", end="")
        # print(int(visualization_info.get_five_min_hr()))
        # print("time_passed; ", end="")
        # print(temp_time_string)
        # print("#############################")

        root.update()

    def setup_tkinter(self):
        """ Initializes all the labels that are going to be shown in the display. Opens up the display window itself
        by root.mainloop(), then begins the program after half a second (safety) using the .after() method.
        """
        Label(root, text="Instant HR: ").grid(row=0, column=0)
        Label(root, text="One Min HR: ").grid(row=1, column=0)
        Label(root, text="Five Min HR: ").grid(row=2, column=0)
        Label(root, text="Alarm: ").grid(row=3, column=0)
        Label(root, text="Time Passed: ").grid(row=4, column=0)

        Label(root, textvariable=self.inst_hr_var).grid(row=0, column=1)
        Label(root, textvariable=self.one_min_hr_var).grid(row=1, column=1)
        Label(root, textvariable=self.five_min_hr_var).grid(row=2, column=1)
        Label(root, textvariable=self.alarm_var).grid(row=3, column=1)
        Label(root, textvariable=self.time_passed_string).grid(row=4, column=1)

        root.after(500, self.run_hr_monitor())
        root.mainloop()

    @staticmethod
    def clean_up():
        """ Close and destroy the tkinter display. This is where the program will terminate.
        """
        root.quit()
        root.destroy()


if __name__ == "__main__":
    myMain = Main()
    myMain.setup_tkinter()
