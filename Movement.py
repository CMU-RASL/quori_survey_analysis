class Movement(object):
    """docstring for Movement."""

    def __init__(self, index, data):
        super(Movement, self).__init__()
        self.torso_arr = ['forward', 'backward', 'neutral']
        self.torso_deg_arr = ['small', 'large']
        self.speed_arr = ['none', 'slow', 'fast']
        self.arm_arr = ['forward', 'sides', 'high']
        self.emotion_labels = ['Happiness', 'Sadness', 'Fear', 'Disgust', 'Anger', 'Surprise', 'Interest', 'Neutral']
        self.torso_start = data[0]
        self.torso_start_deg = data[1]
        self.torso_end = data[2]
        self.torso_end_deg = data[3]
        self.torso_speed = data[4]
        if self.torso_start == self.torso_end:
            self.torso_speed = 'none'
        self.left_arm_start = data[5]
        self.left_arm_end = data[6]
        self.left_arm_speed = data[7]
        if self.left_arm_start == self.left_arm_end:
            self.left_arm_speed = 'none'
        self.right_arm_start = data[8]
        self.right_arm_end = data[9]
        self.right_arm_speed = data[10]
        if self.right_arm_start == self.right_arm_end:
            self.left_arm_speed = 'none'
        self.index = index
        self.responses = None

    def check_constraints(self, groups=[], vals=[]):
        for group, val in zip(groups, vals):

            if not val in eval("self."+group):
                return False
        return True
        # torso_start, torso_start_deg, \
        #                     torso_end, torso_end_deg, torso_speed, left_arm_start, \
        #                     left_arm_end, left_arm_speed, right_arm_start, right_arm_end, \
        #                     right_arm_speed
        # if (self.torso_start in torso_start) and \
        #     (self.torso_start_deg in torso_start_deg) and \
        #     (self.torso_end in torso_end) and \
        #     (self.torso_end_deg in torso_end_deg) and \
        #     (self.torso_speed in torso_speed) and \
        #     (self.left_arm_start in left_arm_start) and \
        #     (self.left_arm_end in left_arm_end) and \
        #     (self.left_arm_speed in left_arm_speed) and \
        #     (self.right_arm_start in right_arm_start) and \
        #     (self.right_arm_end in right_arm_end) and \
        #     (self.right_arm_speed in right_arm_speed):
        #
        #     return True
        # else:
        #     return False
