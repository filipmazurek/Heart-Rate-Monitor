from queue import *
from Information_Passer import InformationPasserClass


class HRProcessor:
    tachycardia = 200  # selected values for tachycardia and bradycardia
    bradycardia = 40

    def __init__(self, update_time_seconds):
        """ Initialize an instance of the HRProcessor class with the time per given instant hr, so that can find how
        many values should be stored in the queue for 1, 5, and 10 minutes.

        :param update_time_seconds:
        """
        self.time_passed_string = ""

        samples_per_1_min = int(60 / update_time_seconds)
        samples_per_5_min = samples_per_1_min * 5
        samples_per_10_min = samples_per_1_min * 10

        self.one_min_queue = Queue(maxsize=samples_per_1_min)
        self.five_min_queue = Queue(maxsize=samples_per_5_min)
        self.ten_min_queue = Queue(maxsize=samples_per_10_min)

    def add_inst_hr(self, inst_hr, time_passed_string):
        """ Add another instant heart rate to the queues. Check for alarms, too.

        :param inst_hr:
        :param time_passed_string: current time, used for writing out log in case of alarm.
        :return:
        """
        self.time_passed_string = time_passed_string
        self.one_min_queue = self.update_queue(self.one_min_queue, inst_hr)
        self.five_min_queue = self.update_queue(self.five_min_queue, inst_hr)
        self.ten_min_queue = self.update_queue(self.ten_min_queue, inst_hr)

        one_min_hr = self.queue_avg(self.one_min_queue)
        five_min_hr = self.queue_avg(self.five_min_queue)

        hr_information_passer = InformationPasserClass(inst_hr, one_min_hr, five_min_hr)

        hr_information_passer = self.check_for_alarm(inst_hr, hr_information_passer)

        return hr_information_passer

    @staticmethod
    def update_queue(queue, hr):
        """ Checks if the queue is full. If yes, remove an item before adding the new one.

        :param queue:
        :param hr:
        :return:
        """
        if queue.full():
            queue.get()

        queue.put(hr)
        return queue

    @staticmethod
    def queue_avg(queue):
        """ Finds the average of the entered queue. Uses a helper queue so that the method is not destructive.

        :param queue:
        :return: average value of the queue.
        """
        helper_queue = Queue()
        queue_total = 0
        queue_size = 0
        while not queue.empty():
            temp_val = queue.get()
            queue_total += temp_val
            queue_size += 1
            helper_queue.put(temp_val)

        queue_avg = queue_total / queue_size

        while not helper_queue.empty():
            temp_val = helper_queue.get()
            queue_total += temp_val
            queue_size += 1
            queue.put(temp_val)

        return queue_avg

    def check_for_alarm(self, hr, information_passer):
        """ Checks if the given heartrate is beyond normal values. Sets an alarm and writes out a log for inspection if
        true.

        :param hr:
        :param information_passer:
        :return:
        """
        if hr < HRProcessor.bradycardia:
            information_passer.set_bradycardia_alarm()
            self.write_log("bradycardia")

        if hr > HRProcessor.tachycardia:
            information_passer.add_ten_min_log(self.ten_min_queue)
            information_passer.set_tachycardia_alarm()
            self.write_log("tachycardia")

        return information_passer

    def write_log(self, type_alarm):
        """ In case of alarm, creates a new file and writes to it the instant heart rates from the last 10 minutes
        for inspection by the user. The file is named based on when the alarm occured and what type of alarm it was.

        :param type_alarm:
        :return:
        """
        log_name = type_alarm + "_near_time_" + self.time_passed_string
        new_file = open(log_name, 'w')
        helper_queue = Queue()

        while not self.ten_min_queue.empty():
            temp_val = self.ten_min_queue.get()
            new_file.write(str(temp_val) + ", ")
            helper_queue.put(temp_val)

        while not helper_queue.empty():
            self.ten_min_queue.put(helper_queue.get())
