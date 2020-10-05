import numpy as np

class User(object):
    """docstring for User."""

    def __init__(self, code, start_time, end_time, row, mturk_id=''):
        super(User, self).__init__()
        self.code = code
        self.start_time = start_time
        self.end_time = end_time
        self.mturk_id = mturk_id
        self.ages = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85 or older']
        self.genders = ['Male', 'Female', 'Other']
        self.ethnicities = ['White', 'Black or African American', 'American Indian or Alaska Native', 'Asian', 'Native Hawaiian or Pacific Islander', 'Other']
        self.robot = ['Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely']
        self.process_row(row)

    def process_row(self, row):
        # self.train_response = row[26:34]
        key = {'Not': 0, 'Slightly': 1, 'Somewhat': 2, 'Moderately': 3, 'Intensely': 4}
        self.responses = -1*np.ones((224, 8))
        self.timing = -1*np.zeros((224, 3))
        ii = 0
        if len(row) == 2738:
            for vid_ind in range(36, 2738-14, 12):
                cur_vid = row[vid_ind:vid_ind+12]
                for id, element in enumerate(cur_vid[:3]):
                    if len(element) > 0:
                        self.timing[ii,id] = float(element)
                for id, element in enumerate(cur_vid[4:]):
                    if len(element) > 0:
                        self.responses[ii,id] = key[element]
                ii += 1
        else:
            for vid_ind in range(35, 2713, 12):
                cur_vid = row[vid_ind:vid_ind+12]
                for id, element in enumerate(cur_vid[:3]):
                    if len(element) > 0:
                        self.timing[ii,id] = float(element)
                for id, element in enumerate(cur_vid[4:]):
                    if len(element) > 0:
                        self.responses[ii,id] = key[element]
                ii += 1

        if len(row[-10]) > 0:
            age_ind = self.ages.index(row[-10])
        else:
            age_ind = -1
        if len(row[-9]) > 0:
            gender_ind = self.genders.index(row[-9])
        else:
            gender_ind = -1
        if len(row[-8]) > 0:
            res = row[-8].split(',')
            ethnicity_inds = []
            for r in res:
                ethnicity_inds.append(self.ethnicities.index(r))
        else:
            ethnicity_inds = [-1]
        if len(row[-7]) > 0:
            print(row[-7])
        if len(row[-6]) > 0:
            robot_ind = self.robot.index(row[-6])
        else:
            robot_ind = -1
        self.demographics = [age_ind, gender_ind, ethnicity_inds, robot_ind]
