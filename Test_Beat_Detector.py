from Beat_Detector import Beat_Detector

update_time_seconds = 20
update_time_easy = 2  # means enough data for 2 seconds.
array_easy = [0, 2, 5, 10, 5, 2, 0, 2, 5, 10, 5]



# def test_normalize_array():
#     beat_detector = Beat_Detector(update_time_seconds)
#     sample_array = [0, 2, 24, 2, 15]
#
#     normalized_array = beat_detector.normalize_array(sample_array)
#     print(normalized_array)
#     is_normal = True
#     for num in normalized_array:
#         if (num > 1) or (num < 0):
#             is_normal = False
#
#     assert is_normal


def test_get_num_beats():
    beat_detector = Beat_Detector(update_time_seconds)
    assert 2 == beat_detector.get_num_beats(array_easy)

def test_single_array_hr():
    beat_detector = Beat_Detector(update_time_easy)
    assert 60 == beat_detector.single_array_hr(array_easy)  # 2 beats in 2 seconds means 60 bpm

def test_find_inst_hr():
    beat_detector = Beat_Detector(update_time_easy)
    assert 60 == beat_detector.find_instant_hr(array_easy, array_easy)
