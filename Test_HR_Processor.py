from HR_Processor import HRProcessor
from queue import *
from tkinter import *

# must initialize a tkinter root for the HRProcessor to be able to initialize StringVar
root = Tk()

sampling_rate_easy = 2/60  # makes be 2 inst hr per 1 min, 10 inst per 5 min (30 second updates)

# the following are default values from Main
tachycardia = 200.0
bradycardia = 40.0
multi_minute_mean_1 = 1
multi_minute_mean_2 = 5


def test_queue_avg():
    queue_avg_5 = Queue()
    queue_avg_5.put(0)
    queue_avg_5.put(10)
    my_processor = HRProcessor(sampling_rate_easy, tachycardia, bradycardia, multi_minute_mean_1, multi_minute_mean_2)
    assert 5 == my_processor.queue_avg(queue_avg_5)
    assert not queue_avg_5.empty()
    assert 0 == queue_avg_5.get()
    assert 10 == queue_avg_5.get()
    assert queue_avg_5.empty()


def test_update_queue():
    putter = 4
    queue_simple = Queue()
    assert queue_simple.empty()
    my_processor = HRProcessor(sampling_rate_easy, tachycardia, bradycardia, multi_minute_mean_1, multi_minute_mean_2)
    my_processor.update_queue(queue_simple, putter)
    assert queue_simple.get() == putter
    assert queue_simple.empty()
