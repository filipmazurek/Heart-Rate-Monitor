import struct


class Reader:

    def __init__(self, filename, seconds_at_a_time, data_bit_length):
        """ Initialize the Reader class. Calculate class variables based on data_bit_length for functions to know how
        much to read from the given document at a time. Sets the opened document as a class variable so it may be
        read from in later function calls.

        :param filename: name of the binary data filename
        :param seconds_at_a_time: how many seconds worth of data will be returned when getting an instant worth of data
        :param data_bit_length: whether the multiplexed PPG and ECG values are 12 bit or 16 bit.
        """
        self.data_bit_length = data_bit_length
        self.bytes_to_load = data_bit_length * 2 / 8
        self.openedFile = open(filename, 'rb')
        binary_data = None

        if data_bit_length == 12:
            binary_data = self.openedFile.read(3)
        if data_bit_length == 16:
            binary_data = self.openedFile.read(2)

        sample_rate_hz = struct.unpack('<H', binary_data)  # <H means little endian
        self.num_samples_to_get = (sample_rate_hz * seconds_at_a_time)[0]

    def get_next_data_instant(self):
        """ Read from the file the next seconds_at_a_time worth of data.

        :return: two arrays, one of ECG data points and one of PPG data points. For use by the Beat_Detector class to
        find the instant heart rate
        """
        data_array_ecg = []
        data_array_ppg = []

        for numSample in range(0, self.num_samples_to_get):
            [ecg_data_point, ppg_data_point] = self.load_next_data_points()

            if self.openedFile.closed:
                break

            data_array_ecg.append(ecg_data_point)
            data_array_ppg.append(ppg_data_point)

        return [data_array_ecg, data_array_ppg]

    def load_next_data_points(self):
        """ Reads in enough data for one of each data point, demultiplexes the data, and returns the data points.
        Has a safety: if the EOF is reached, then the file is closed.

        :return: one of each ECG and PPG data points
        """
        binary_data = self.openedFile.read(self.bytes_to_load)

        if binary_data == '':  # if EOF reached, close the file and exit.
            self.openedFile.close()
            return [None, None]

        joint_data = struct.unpack('<H', binary_data)[0]  # unpack always returns a tuple. Get the only data point.
        ppg_data_point = joint_data << self.data_bit_length
        ecg_data_point = (joint_data >> self.data_bit_length) << self.data_bit_length

        return [ecg_data_point, ppg_data_point]

    def still_reading(self):
        """ Tells the caller whether the file still has information left to read.

        :return: boolean
        """
        return self.openedFile.closed
