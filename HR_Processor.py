from queue import *
from Information_Passer import InformationPasserClass


class HR_Processor:
    tachycardia = 200
    bradycardia = 40

    def __init__(self, update_time_seconds):
        samples_per_1_min = int(60 / update_time_seconds)
        samples_per_5_min = samples_per_1_min * 5
        samples_per_10_min = samples_per_1_min * 10

        self.one_min_queue = Queue(maxsize=samples_per_1_min)
        self.five_min_queue = Queue(maxsize=samples_per_5_min)
        self.ten_min_queue = Queue(maxsize=samples_per_10_min)

    def add_inst_hr(self, inst_hr):
        self.one_min_queue = self.update_queue(self.one_min_queue, inst_hr)
        self.five_min_queue = self.update_queue(self.five_min_queue, inst_hr)
        self.ten_min_queue = self.update_queue(self.ten_min_queue, inst_hr)

        one_min_hr = self.queue_avg(self.one_min_queue)
        five_min_hr = self.queue_avg(self.five_min_queue)

        hr_information_passer = InformationPasserClass(inst_hr, one_min_hr, five_min_hr)

        hr_information_passer = self.check_for_alarm(inst_hr, hr_information_passer)

        return hr_information_passer

    def update_queue(self, queue, hr):
        if queue.full():
            queue.get()

        queue.put(hr)
        return queue

    def queue_avg(self, queue):
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
        if hr < HR_Processor.bradycardia:
            information_passer.add_ten_min_log(self.ten_min_queue)
            information_passer.set_bradycardia_alarm()

        if hr > HR_Processor.tachycardia:
            information_passer.add_ten_min_log(self.ten_min_queue)
            information_passer.set_tachycardia_alarm()

        return information_passer

