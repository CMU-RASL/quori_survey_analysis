from helper import read_dof_csv, check_matches, check_matches, create_batch
# import numpy as np
# import matplotlib.pyplot as plt

dof_csv_filename = 'torso_arm_dof.csv'
qualtrics_filename = 'Batch 1 Data/batch01_qualtrics.csv'
mturk_filename = 'Batch 1 Data/batch01_mturk.csv'
qualtrics_filename2 = 'Batch 2 Data/batch02_qualtrics.csv'
mturk_filename2 = 'Batch 2 Data/batch02_mturk.csv'

video_results_folder = 'video_results'
constraint_results_folder = 'constraint_results'
single_video_folder = 'single_video'
single_constraint_folder = 'single_constraint'

#Step 1: Check MTurk - Qualtrics Matches
user_arr = check_matches(qualtrics_filename, mturk_filename)
user_arr2 = check_matches(qualtrics_filename2, mturk_filename2)
user_arr.extend(user_arr2)

#Step 2: Movement Array
movement_arr = read_dof_csv(dof_csv_filename)

#Step 3: Create Survey Results Object
batch = create_batch(user_arr, movement_arr)

demo_groups = {'ages':['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85 or older'],
            'genders': ['Male', 'Female', 'Other'],
            'ethnicities': ['White', 'Black or African American', 'American Indian or Alaska Native', 'Asian', 'Native Hawaiian or Pacific Islander', 'Other'],
            'robots': ['Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely']}
for group, vals in demo_groups.items():
    batch.test_demo_group(group, vals)


# groups = [['torso_start',['neutral']],
#             ['torso_start_deg',['small', 'large']],
#             ['torso_end',['forward', 'backward']],
#             ['torso_end_deg',['small', 'large']],
#             ['torso_speed',['slow', 'fast']],
#             ['left_arm_start',['forward', 'sides']],
#             ['left_arm_end',['forward', 'sides', 'high']],
#             ['left_arm_speed',['none', 'slow', 'fast']],
#             ['right_arm_start',['forward', 'sides']],
#             ['right_arm_end',['forward', 'sides', 'high']],
#             ['right_arm_speed',['slow', 'fast']]]
# completed = []
# for group1 in groups[2:]:
#     # batch.check_balanced(group1[0], group1[1])
#     # batch.test_group(group1[0], group1[1])
#     for group2 in groups[2:]:
#         if (not (group1 == group2)) and (not (group2, group1) in completed):
#             batch.test_group_2(group1[0], group1[1], group2[0], group2[1])
#     #         batch.check_balanced_2(group1[0], group2[0])
#             completed.append((group1, group2))


# batch.create_csv()
# lengths = []
# for response in batch.responses:
#     lengths.append(np.where(response[:,0] > -1)[0].shape[0])
#
# plt.hist(lengths, bins=np.arange(11))
# plt.title('Number of Users Seeing Each Movement')
# plt.show()
# # batch.plot_single_video(single_video_folder)
# batch.video_posthoc(video_results_folder)
#
# batch.constraint_posthoc(constraint_results_folder)
# batch.plot_single_constraint(single_constraint_folder)
