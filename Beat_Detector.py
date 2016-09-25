import numpy as np


class BeatDetector:

    def __init__(self, update_time_seconds):
        """ Initialize the BeatDetector by setting a class instance variable so the detector knows how much time passes
        between updates so can correctly calculate bpm.

        :param update_time_seconds: time amount of data received at every call.
        """
        self.update_time_seconds = update_time_seconds

    def find_instant_hr(self, data_array_ecg, data_array_ppg):
        """ Given the data read from the binary file, finds the number of 'upbeats' and counts those as heartbeats

        :param data_array_ecg:
        :param data_array_ppg:
        :return: calculated beats per minute
        """

        inst_ecg_hr = self.single_array_hr(data_array_ecg)
        inst_ppg_hr = self. single_array_hr(data_array_ppg)

        instant_hr = self.reconcile_hr(inst_ecg_hr, inst_ppg_hr)
        return instant_hr

    def single_array_hr(self, data_array):
        """ A simplified function to find the bpm of a single array. Used for the repeated calls for each array.

        :param data_array:
        :return: beats per minute
        """
        num_beats = self.get_num_beats(data_array)

        bpm = num_beats / (self.update_time_seconds / 60)  # 60 seconds in a minute

        return bpm

    @staticmethod
    def get_num_beats(some_array):
        """ The actual calculation part of the class: counts how many upbeats occur in the given data.

        :param some_array:
        :return: beats per minute
        """
        num_beats = 0
        threshold = (max(some_array) - np.mean(some_array)) / 2

        for i in range(0, len(some_array) - 1):
            if (some_array[i] < threshold) and (some_array[i+1] > threshold):
                num_beats += 1

        return num_beats

    @staticmethod
    def reconcile_hr(hr_one, hr_two):
        """ In case the ECG heart rate and PPG heart rate disagree, return the average of the two.

        :param hr_one:
        :param hr_two:
        :return: if close in value, return hr_one. If far, return the average of the two.
        """
        if abs(hr_one - hr_two) < 3:  # where 3 has been arbitrarily set as the 'close enough' limit
            return hr_one

        else:
            return (hr_one + hr_two) / 2
