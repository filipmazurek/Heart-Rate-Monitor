import math
from SignalChoice import *


class BeatDetector:

    def __init__(self, update_time_seconds, signal_chosen):
        """ Initialize the BeatDetector by setting a class instance variable so the detector knows how much time passes
        between updates so can correctly calculate bpm.

        :param update_time_seconds: time amount of data received at every call.
        :param signal_chosen: to use ECG, PPG, or both to calculate heart rate
        """
        self.update_time_seconds = update_time_seconds
        self.signal_chosen = signal_chosen

    def find_instant_hr(self, data_array_ecg, data_array_ppg):
        """ Given the data read from the binary file, finds the number of 'upbeats' and counts those as heartbeats

        :param data_array_ecg: array of ecg data
        :param data_array_ppg: array of ppg data
        :return: calculated beats per minute
        """

        inst_ecg_hr = self.single_array_hr(data_array_ecg)
        inst_ppg_hr = self. single_array_hr(data_array_ppg)

        instant_hr = self.reconcile_hr(inst_ecg_hr, inst_ppg_hr)

        if self.signal_chosen == SignalChoice.ecg:
            return inst_ecg_hr

        if self.signal_chosen == SignalChoice.ppg:
            return inst_ppg_hr

        if self.signal_chosen == SignalChoice.both:
            return instant_hr

    def single_array_hr(self, data_array):
        """ A simplified function to find the bpm of a single array. Used for the repeated calls for each array.

        :param data_array: data array that should be of ecg or ppg data
        :return: beats per minute
        """
        num_beats = self.get_num_beats(data_array)

        bpm = num_beats / (self.update_time_seconds / 60)  # 60 seconds in a minute

        return bpm

    def get_num_beats(self, some_array):
        """ The actual calculation part of the class: counts how many upbeats occur in the given data.

        :param some_array: data array that should be of ecg or ppg data
        :return: beats per minute
        """
        num_beats = 0
        threshold = (max(some_array) - self.safe_mean(some_array)) / 2

        for i in range(0, len(some_array) - 1):
            if not math.isnan(some_array[i]):
                next_val = self.find_next_value(some_array, i)
                if next_val >= 0 and\
                        (some_array[i] < threshold) and (next_val > threshold):
                    num_beats += 1

        return num_beats

    @staticmethod
    def reconcile_hr(hr_one, hr_two):
        """ In case the ECG heart rate and PPG heart rate disagree, return the average of the two.

        :param hr_one: one heart rate that disagrees with the second
        :param hr_two: second heart rate that disagrees with the first
        :return: if close in value, return hr_one. If far, return the average of the two.
        """
        if abs(hr_one - hr_two) < 3:  # where 3 has been arbitrarily set as the 'close enough' limit
            return hr_one

        else:
            return (hr_one + hr_two) / 2

    @staticmethod
    def safe_mean(array):
        """ Finds the mean of an array by ignoring any NaN values, just by skipping over them.

        :param array: array whose mean is to be found
        :return: mean that doesn't include NaN
        """
        total_items = 0
        total_value = 0
        for i in range(0, len(array)):
            if not math.isnan(i):
                total_items += 1
                total_value += array[i]
        return total_value / total_items

    @staticmethod
    def find_next_value(array, item_num):
        """ Find the next value in the array that is not a NaN.

        :param array: array of values and NaNs
        :param item_num: where to start looking in the array
        :return:
        """
        item_num += 1
        while item_num < len(array):
            if not math.isnan(array[item_num]):
                return array[item_num]
        return -1
