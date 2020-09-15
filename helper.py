from Batch import Batch
from Movement import Movement
from User import User
import csv
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

#Read dof_csv_filename
def read_dof_csv(filename):
    movement_arr = []
    with open(filename) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        ii = 0
        for row in rows:
            if ii == 0:
                headers = row
            else:
                movement_arr.append(Movement(ii, row))
            ii += 1
    return movement_arr

def check_matches(qualtrics, mturk):
    response_arr = []
    code_arr = []
    start_time_arr = []
    end_time_arr = []
    with open(qualtrics) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        ii = 0
        for row in rows:
            if ii < 3:
                pass
            else:
                if row[0][4] == '-':
                    start_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                else:
                    start_time = datetime.strptime(row[0], '%d/%m/%Y %H:%M')
                    end_time = datetime.strptime(row[1], '%d/%m/%Y %H:%M')
                code = row[-1]
                if len(code) < 6:
                    code = ''
                code_arr.append(code)
                start_time_arr.append(start_time)
                end_time_arr.append(end_time)
                response_arr.append(User(code, start_time, end_time, row))
            ii += 1

    user_arr = []
    with open(mturk) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        ii = 0
        claimed = []
        for row in rows:
            if ii < 1:
                pass
            else:
                # print(row)
                start_time = datetime.strptime(row[6][:-9] + ' 2020', '%a %b %d %H:%M:%S %Y') + timedelta(hours=2)
                end_time = datetime.strptime(row[18][:-9] + ' 2020', '%a %b %d %H:%M:%S %Y') + timedelta(hours=2)
                code = row[-1]
                if len(code) < 6:
                    code = ''
                mturk_id = row[15]
                if code in code_arr:
                    code_ind = code_arr.index(code)
                    claimed.append(code_ind)
                    cur_user = response_arr[code_ind]
                    cur_user.mturk_id = mturk_id
                    user_arr.append(cur_user)
                else:
                    # print(mturk_id)
                    best_diff = timedelta(minutes = 10)
                    best_ind = -1
                    for cur_resp, (start, end) in enumerate(zip(start_time_arr, end_time_arr)):
                        diff = abs(start - start_time) + abs(end - end_time)
                        if diff < best_diff and start > start_time and (not cur_resp in claimed):
                            best_diff = diff
                            best_ind = cur_resp
                    claimed.append(best_ind)
                    cur_user = response_arr[best_ind]
                    cur_user.mturk_id = mturk_id
                    user_arr.append(cur_user)
            ii += 1
    return user_arr

def create_batch(user_arr, movement_arr):

    batch = Batch(movement_arr, len(user_arr))

    for user_num, user in enumerate(user_arr):
        batch.add_user_response(user, user_num)

    batch.apply_responses()

    return batch
