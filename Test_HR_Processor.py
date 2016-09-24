from HR_Processor import HR_Processor
from queue import *

sampling_rate_easy = 2/60  # makes be 2 inst hr per 1 min, 10 inst per 5 min




def test_queue_avg():
    queue_avg_5 = Queue()
    queue_avg_5.put(0)
    queue_avg_5.put(10)
    my_processor = HR_Processor(sampling_rate_easy)
    assert 5 == my_processor.queue_avg(queue_avg_5)
    assert not queue_avg_5.empty()
    assert 0 == queue_avg_5.get()
    assert 10 == queue_avg_5.get()
    assert  queue_avg_5.empty()

def test_update_queue():
    putter = 4
    queue_simple = Queue()
    assert queue_simple.empty()
    my_processor = HR_Processor(sampling_rate_easy)
    my_processor.update_queue(queue_simple, putter)
    assert queue_simple.get() == putter
    assert queue_simple.empty()
