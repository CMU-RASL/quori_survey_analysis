from helper import read_dof_csv, check_matches, check_matches, create_batch
import numpy as np

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

# batch.plot_single_video(single_video_folder)
batch.video_posthoc(video_results_folder)

batch.constraint_posthoc(constraint_results_folder)
batch.plot_single_constraint(single_constraint_folder)
