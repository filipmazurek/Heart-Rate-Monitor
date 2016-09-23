import struct


class Reader:

    def __init__(self, filename, seconds_at_a_time=20, data_bit_length=16):  # default values given
        """ Initialize the Reader class. Calculate class variables based on data_bit_length for functions to know how
        much to read from the given document at a time. Sets the opened document as a class variable so it may be
        read from in later function calls.

        :param filename: name of the binary data filename
        :param seconds_at_a_time: how many seconds worth of data will be returned when getting an instant worth of data
        :param data_bit_length: whether the multiplexed PPG and ECG values are 12 bit or 16 bit.
        """
        self.data_bit_length = data_bit_length
        self.bytes_to_load = int(data_bit_length * 2 / 8)  # cast to integer becuase need integer when reading in
        self.opened_file = open(filename, 'rb')
        self.sample_rate_hz = 0

        if data_bit_length == 12:
            binary_data = self.opened_file.read(3)
            self.sample_rate_hz = struct.unpack('<I', binary_data + '\0')[0]  # trick for 24 bit numbers
            # http://stackoverflow.com/questions/3783677/how-to-read-integers-from-a-file-that-are-24bit-and-little-endian-using-python
        if data_bit_length == 16:
            binary_data = self.opened_file.read(2)
            self.sample_rate_hz = struct.unpack('<H', binary_data)[0]  # < means little endian; H is 16 int

        self.num_samples_to_get = self.sample_rate_hz * seconds_at_a_time


    def get_next_data_instant(self):
        """ Read from the file the next seconds_at_a_time worth of data.

        :return: two arrays, one of ECG data points and one of PPG data points. For use by the Beat_Detector class to
        find the instant heart rate
        """
        data_array_ecg = []
        data_array_ppg = []

        for numSample in range(0, self.num_samples_to_get):
            [ecg_data_point, ppg_data_point] = self.load_next_data_points()

            if self.opened_file.closed:
                break

            data_array_ecg.append(ecg_data_point)
            data_array_ppg.append(ppg_data_point)

        return [data_array_ecg, data_array_ppg]

    def load_next_data_points(self):
        """ Reads in enough data for one of each data point, demultiplexes the data, and returns the data points.
        Has a safety: if the EOF is reached, then the file is closed.

        :return: one of each ECG and PPG data points
        """
        binary_data = self.opened_file.read(self.bytes_to_load)

        if not binary_data:  # if EOF reached, close the file and exit.
            self.opened_file.close()
            return [None, None]

        ecg_data_point = None
        ppg_data_point = None

        if self.data_bit_length == 16:
            ecg_data_binary = binary_data[:int(self.bytes_to_load / 2)]
            ppg_data_binary = binary_data[-int(self.bytes_to_load / 2):]

            ecg_data_point = struct.unpack('<H', ecg_data_binary)[0]
            ppg_data_point = struct.unpack('<H', ppg_data_binary)[0]

        # TODO: add statement for 12 bit uint
        return [ecg_data_point, ppg_data_point]

    def still_reading(self):
        """ Tells the caller whether the file still has information left to read.

        :return: boolean
        """
        return not self.opened_file.closed

    def get_sample_rate(self):
        return self.sample_rate_hz

