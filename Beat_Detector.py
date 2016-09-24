import numpy as np


class Beat_Detector:

    def __init__(self, update_time_seconds):
        self.update_time_seconds = update_time_seconds

    def find_instant_hr(self, data_array_ecg, data_array_ppg):

        inst_ecg_hr = self.single_array_hr(data_array_ecg)
        inst_ppg_hr = self. single_array_hr(data_array_ppg)

        instant_hr = self.reconcile_hr(inst_ecg_hr, inst_ppg_hr)
        return instant_hr

    def single_array_hr(self, data_array):

        num_beats = self.get_num_beats(data_array)

        bpm = num_beats / (self.update_time_seconds / 60)  # 60 seconds in a minute

        return bpm

    def get_num_beats(self, some_array):
        num_beats = 0
        threshold = (max(some_array) - np.mean(some_array)) / 2

        for i in range(0, len(some_array) - 1):
            if (some_array[i] < threshold) and (some_array[i+1] > threshold):
                num_beats += 1

        return num_beats

    def reconcile_hr(self, hr_one, hr_two):
        if abs(hr_one - hr_two) > 3:
            return hr_one

        else:
            return (hr_one + hr_two) / 2

        # TODO: make actual good reconciliation. Not this lazy implementation.
