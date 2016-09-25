class InformationPasserClass:
    def __init__(self, inst_hr, one_min_hr, five_min_hr):
        self.inst_hr = inst_hr
        self.one_min_hr = one_min_hr
        self.five_min_hr = five_min_hr
        self.bradycardia_alarm = False
        self.tachycardia_alarm = False

    def set_bradycardia_alarm(self):
        self.bradycardia_alarm = True

    def set_tachycardia_alarm(self):
        self.tachycardia_alarm = True

    def get_inst_hr(self):
        return self.inst_hr

    def get_one_min_hr(self):
        return self.one_min_hr

    def get_five_min_hr(self):
        return self.five_min_hr

    def get_tachycardia_alarm(self):
        return self.tachycardia_alarm

    def get_bradycardia_alarm(self):
        return self.bradycardia_alarm
