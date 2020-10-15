from helper import read_dof_csv, check_matches, check_matches, create_batch
from helper import response_hist
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

#Demographics
# batch.test_demo_group()

#Basic Group Comparison
# batch.check_balanced()
# batch.test_group()

#Creating CSV of results
# batch.create_csv()

#Response histogram
# response_hist(batch)

#Plot Single Video
# batch.plot_single_video(single_video_folder)
