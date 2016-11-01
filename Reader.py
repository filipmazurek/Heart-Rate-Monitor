import struct
import sys
import logging


class Reader:

    def __init__(self, filename, seconds_at_a_time=10, data_bit_length=16):  # default values given
        """ Initialize the Reader class. Calculate class variables based on data_bit_length for functions to know how
        much to read from the given document at a time. Sets the opened document as a class variable so it may be
        read from in later function calls.

        :param filename: name of the binary data filename
        :param seconds_at_a_time: how many seconds worth of data will be returned when getting an instant worth of data
        :param data_bit_length: whether the multiplexed PPG and ECG values are 12 bit or 16 bit.
        """
        logging.getLogger('bme590assignment02')
        logging.debug('Reader initialized')

        if seconds_at_a_time <= 0:
            print('Someone is trying to break this... Setting to update every 10 seconds')
            seconds_at_a_time = 10
            logging.error('Nonsensical update time corrected to default value = 10')

        self.is_bin_file = False
        self.is_mat_file = False
        self.mat_index = 0
        self.is_closed = False

        import os.path

        file_extension = os.path.splitext(filename)[1]  # split text returns array. Second item is extention

        if file_extension == '.bin':
            self.is_bin_file = True
            logging.debug('file is a binary file')

        if file_extension == '.mat':
            self.is_mat_file = True
            logging.debug('file is a Matlab file')

        if (not self.is_mat_file) and (not self.is_bin_file):
            logging.error('invalid file extension')
            sys.exit('Please enter a file with a valid extension')

        if self.is_bin_file:

            self.data_bit_length = data_bit_length
            self.bytes_to_load = int(data_bit_length * 2 / 8)  # cast to integer because need integer when reading in
            self.opened_file = open(filename, 'rb')

            try:
                self.opened_file = open(filename, 'rb')
            except FileNotFoundError:
                logging.error('file  not found')
                sys.exit("File not found")

            self.sample_rate_hz = 0

            if data_bit_length == 12:
                logging.debug('file contains 12 bit data')
                binary_data = self.opened_file.read(3)
                self.sample_rate_hz = struct.unpack('<I', binary_data + '\0')[0]  # trick for 24 bit numbers
                # http://stackoverflow.com/questions/3783677/how-to-read-integers-from-a-file-that-are-24bit-and-little-endian-using-python
            if data_bit_length == 16:
                logging.debug('file contains 16 bit data')
                binary_data = self.opened_file.read(2)
                self.sample_rate_hz = struct.unpack('<H', binary_data)[0]  # < means little endian; H is 16 int

        if self.is_mat_file:
            self.mat_dict = self.read_any_mat(filename)
            self.sample_rate_hz = self.mat_dict.get('fs')[0][0]
            print(type(self.sample_rate_hz))

        self.num_samples_to_get = self.sample_rate_hz * seconds_at_a_time

    @staticmethod
    def read_any_mat(infile):
        """ reads in both Matlab v5 and v7.3 files

        :param infile: input file (str)
        :return: mat_dict
        """
        from scipy.io import loadmat
        import h5py

        try:
            mat_file = loadmat(infile)
            logging.debug('trying to load .mat file as Matlab v5')
        except NotImplementedError:
            mat_file = h5py.File(infile)
            logging.debug('file was actually an HDF5 file')

        mat_dict = dict(mat_file)
        return mat_dict

    # @staticmethod
    # def valid_file_extension(filename):
    #     import os.path
    #
    #     file_extension = os.path.splitext(filename)[1]  # split text returns array. Second item is extention
    #
    #     return (file_extension == '.bin') or (file_extension == '.mat')

    def get_next_data_instant(self):
        """ Read from the file the next seconds_at_a_time worth of data.

        :return: two arrays, one of ECG data points and one of PPG data points. For use by the Beat_Detector class to
        find the instant heart rate
        """
        logging.debug('getting next data instant')
        data_array_ecg = []
        data_array_ppg = []

        for numSample in range(0, self.num_samples_to_get):
            [ecg_data_point, ppg_data_point] = self.load_next_data_points()

            if self.is_closed:
                break

            data_array_ecg.append(ecg_data_point)
            data_array_ppg.append(ppg_data_point)

        return [data_array_ecg, data_array_ppg]

    def load_next_data_points(self):
        """ Reads in enough data for one of each data point, demultiplexes the data, and returns the data points.
        Has a safety: if the EOF is reached, then the file is closed.

        :return: one of each ECG and PPG data points
        """
        ecg_data_point = None
        ppg_data_point = None

        if self.is_bin_file:
            binary_data = self.opened_file.read(self.bytes_to_load)

            if not binary_data:  # if EOF reached, close the file and exit.
                self.opened_file.close()
                self.is_closed = True
                return [None, None]

            ecg_data_binary = binary_data[:int(self.bytes_to_load / 2)]
            ppg_data_binary = binary_data[-int(self.bytes_to_load / 2):]

            if self.data_bit_length == 16:
                ecg_data_point = struct.unpack('<H', ecg_data_binary)[0]
                ppg_data_point = struct.unpack('<H', ppg_data_binary)[0]

            if self.data_bit_length == 12:
                ecg_data_point = struct.unpack('<H', ecg_data_binary + '\0')[0]
                ppg_data_point = struct.unpack('<H', ppg_data_binary + '\0')[0]

        if self.is_mat_file:

            try:
                ecg_data_point = self.mat_dict.get('ecg')[0][self.mat_index]
                ppg_data_point = self.mat_dict.get('ppg')[0][self.mat_index]
                self.mat_index += 1
            except IndexError:
                self.is_closed = True
            except TypeError:
                print('data from Matlab file is not unint16')

        return [ecg_data_point, ppg_data_point]

    def still_reading(self):
        """ Tells the caller whether the file still has information left to read.

        :return: boolean
        """
        logging.debug('asked if file was open, and the answer is %r', not self.is_closed)
        return not self.is_closed

    def get_sample_rate(self):
        return self.sample_rate_hz
