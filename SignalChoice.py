from enum import Enum


class SignalChoice(Enum):
    """
    Enumeration to limit responses of which signal to use to calculate heart rate
    """
    ecg = 'ECG'
    ppg = 'PPG'
    both = 'ECG and PPG'
