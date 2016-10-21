from Reader import Reader

# Note that the provided test file is over 40 seconds of data at 60 bpm, 100 Hz
seconds = 40
rate = 100
seconds_at_a_time = 20

filename_list = ['60bpm16uintTest.bin', '60bpm16uintTest.mat']  # '60bpm16uintTest.bin',


def test_get_next_data_instant():
    for filename in filename_list:
        my_reader = Reader(filename)  # opens up a new instance of the Reader
        [array_1, array_2] = my_reader.get_next_data_instant()
        assert len(array_1) == len(array_2)

        assert array_1 == array_2


def test_load_next_data_point():
    for filename in filename_list:
        my_reader = Reader(filename)  # opens up a new instance of the Reader

        [point_1, point_2] = my_reader.load_next_data_points()
        assert point_1 == point_2

        point_3 = None
        point_4 = None
        for i in range(0, rate):
            [point_3, point_4] = my_reader.load_next_data_points()

        assert point_3 == point_4
        assert point_1 == point_4


def test_get_sample_rate():
    for filename in filename_list:
        my_reader = Reader(filename)  # opens up a new instance of the Reader
        assert my_reader.get_sample_rate() == rate


def test_still_reading():
    for filename in filename_list:
        my_reader = Reader(filename, seconds_at_a_time, 16)  # opens up a new instance of the Reader

        assert my_reader.still_reading()

        for i in range(0, int(seconds / seconds_at_a_time)):  # read through all data points
            my_reader.get_next_data_instant()

        assert my_reader.still_reading()

        my_reader.load_next_data_points()  # try to read the next information bit
        assert not my_reader.still_reading()
