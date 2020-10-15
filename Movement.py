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
        if self.left_arm_speed == self.right_arm_speed:
            self.symmetric = 'true'
        else:
            self.symmetric = 'false'
        self.arm_speed = self.right_arm_speed
        self.arm_end = self.right_arm_end


    def get_constraint(self, group):
        return eval("self."+group)

    def check_constraints(self, groups=[], vals=[]):
        for group, val in zip(groups, vals):

            if not val in eval("self."+group):
                return False
        return True
