from Beat_Detector import Beat_Detector

update_time_seconds = 20

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