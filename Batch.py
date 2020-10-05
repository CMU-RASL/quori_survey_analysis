import numpy as np
import matplotlib.pyplot as plt
import scikit_posthocs as sp
import pandas as pd
import csv
import scipy.stats as stats

class Batch:
    """docstring for Batch."""

    def __init__(self, movement_arr, user_num):
        super(Batch, self).__init__()
        self.movements = movement_arr
        self.responses = np.zeros((len(movement_arr), user_num, 8))
        self.timing = np.zeros((len(movement_arr), user_num, 3))
        self.age = np.zeros(user_num)
        self.robot = np.zeros(user_num)
        self.ethnicity = np.zeros((user_num, 2))
        self.gender = np.zeros(user_num)
        self.emotion_labels = ['Happiness', 'Sadness', 'Fear', 'Disgust', 'Anger', 'Surprise', 'Interest', 'Neutral']
        self.likert = ['Not', 'Slightly', 'Somewhat', 'Moderately', 'Intensely']
        self.constraints = [['torso_start',['neutral']],
                            ['torso_start_deg',['small', 'large']],
                            ['torso_end',['forward', 'backward']],
                            ['torso_end_deg',['small', 'large']],
                            ['torso_speed',['slow', 'fast']],
                            ['left_arm_start',['forward', 'sides']],
                            ['left_arm_end',['forward', 'sides', 'high']],
                            ['left_arm_speed',['none', 'slow', 'fast']],
                            ['right_arm_start',['forward', 'sides']],
                            ['right_arm_end',['forward', 'sides', 'high']],
                            ['right_arm_speed',['slow', 'fast']]]
        self.single_constraint_num = {}

    def create_csv(self):
        with open('constraints.csv', 'w', newline='') as csvfile:
            fieldnames = ['Constraint Name', 'Option 1', 'Option 2', 'Option 3']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for group, val in self.constraints:
                tmp = list(val)
                for ii in range(3 - len(tmp)):
                    tmp.append('')
                writer.writerow({'Constraint Name': group, 'Option 1': tmp[0], 'Option 2': tmp[1], 'Option 3': tmp[2]})

        with open('likert_names.txt', 'w', newline='') as txtfile:
            for val in self.likert:
                txtfile.write(val + '\n')

        with open('emotion_names.txt', 'w', newline='') as txtfile:
            for val in self.emotion_labels:
                txtfile.write(val + '\n')

        with open('responses.csv', 'w', newline='') as csvfile:
            fieldnames = ['Movement Number', 'User Number'] + self.emotion_labels
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for movement_num in range(self.responses.shape[0]):
                for user_num in range(self.responses.shape[1]):
                    if self.responses[movement_num, user_num, 0] > -1:
                        writer.writerow({'Movement Number': movement_num, 'User Number': user_num,
                                        'Happiness': self.responses[movement_num, user_num, 0],
                                        'Sadness': self.responses[movement_num, user_num, 1],
                                        'Fear': self.responses[movement_num, user_num, 2],
                                        'Disgust': self.responses[movement_num, user_num, 3],
                                        'Anger': self.responses[movement_num, user_num, 4],
                                        'Surprise': self.responses[movement_num, user_num, 5],
                                        'Interest': self.responses[movement_num, user_num, 6],
                                        'Neutral': self.responses[movement_num, user_num, 7]})

        with open('movements.csv', 'w', newline='') as csvfile:
            fieldnames = ['Movement Number'] + [val[0] for val in self.constraints]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for movement_num, movement in enumerate(self.movements):
                row = {'Movement Number': movement_num}
                vals = [movement.get_constraint(group) for group in fieldnames[1:]]
                for group, val in zip(fieldnames[1:], vals):
                    row[group] = val
                writer.writerow(row)


    def add_user_response(self, user, user_num):
        self.responses[:, user_num, :] = user.responses
        self.timing[:, user_num, :] = user.timing
        self.age[user_num] = user.demographics[0]
        self.gender[user_num] = user.demographics[1]
        if len(user.demographics[2]) == 1:
            self.ethnicity[user_num,:] = [user.demographics[2][0], -1]
        else:
            self.ethnicity[user_num,:] = user.demographics[2]
        self.robot[user_num] = user.demographics[3]

    def apply_responses(self):
        for ind, movement in enumerate(self.movements):
            cur_response = self.responses[ind, :, :]
            movement_count = np.zeros((8, 5))
            for emotion in range(8):
                vals, counts = np.unique(cur_response[:,emotion], return_counts=True)
                for val, count in zip(vals.astype('int'), counts):
                    if val >=0:
                        movement_count[emotion, val] = count
            movement.responses = movement_count

    def plot_single_video(self, folder_name):
        for id in range(self.responses.shape[0]):
            plot_grid = np.flipud(self.movements[id].responses.T)
            fig, ax = plt.subplots(figsize=(9,5))
            im = ax.imshow(plot_grid, cmap='YlGn')
            ax.set_title('Movement {0:03d}'.format(id))
            ax.set_xticks(np.arange(8))
            ax.set_yticks(np.arange(5))
            ax.set_xticklabels(self.emotion_labels)
            ax.set_yticklabels(self.likert[::-1])
            cbar = ax.figure.colorbar(im, ax=ax, ticks=[0, 1, 2, 3, 4, 5, 6])
            cbar.ax.set_ylabel('Number of Participants', rotation=-90, va="bottom")
            cbar.ax.set_yticklabels(['0', '1', '2', '3', '4', '5', '6'])
            filename = '{}/{:03d}.png'.format(folder_name, id)
            fig.savefig(filename)
            plt.close(fig)
            print(filename)

    def plot_single_constraint(self, folder):
        for group, vals in self.constraints:
            for val in vals:

                plot_grids = []
                for e_ind in self.emotion_labels:
                    plot_grids.append([])

                for vid_id, movement in enumerate(self.movements):
                    if movement.check_constraints(groups=[group], vals=[val]):
                        for e_ind in range(len(self.emotion_labels)):
                            plot_grids[e_ind].append(movement.responses[e_ind,:])
                if len(plot_grids[0]) > 0:

                    fig, ax = plt.subplots(len(self.emotion_labels), figsize=(20,12))
                    for e_ind in range(len(self.emotion_labels)):
                        im = ax[e_ind].imshow(np.flipud(np.vstack(plot_grids[e_ind]).T), cmap='YlGn', vmin=0, vmax=6)
                        ax[e_ind].set_title(self.emotion_labels[e_ind])
                        ax[e_ind].set_yticks(np.arange(5))
                        ax[e_ind].set_yticklabels(self.likert[::-1], fontsize=5)
                        ax[e_ind].set_xticklabels([])
                    ax[-1].set_xlabel('Movements')

                    fig.subplots_adjust(right=0.8)
                    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
                    cbar = fig.colorbar(im, cax=cbar_ax, ticks=[0, 1, 2, 3, 4, 5, 6])
                    cbar.ax.set_ylabel('Number of Participants', rotation=-90, va="bottom")
                    cbar.ax.set_yticklabels(['0', '1', '2', '3', '4', '5', '6'])
                    fig.suptitle('{} = {}'.format(group, val), fontsize='large')
                    filename = '{}/{}-{}.png'.format(folder, group, val)
                    fig.savefig(filename)
                    plt.close(fig)
                    print(filename)

    def check_balanced(self, group, vals):
        counts = {}
        for val in vals:
            counts[val] = {}
            for g, vs in self.constraints:
                if group == g:
                    pass
                else:
                    counts[val][g] = {}
                    for v in vs:
                        counts[val][g][v] = 0

        for movement_id, movement in enumerate(self.movements):
            for val in vals:
                if movement.check_constraints(groups=[group], vals=[val]):
                    num_responses = np.where(self.responses[movement_id,:,0] > -1)[0].shape[0]
                    for g, vs in self.constraints:
                        if group == g:
                            pass
                        else:
                            v = movement.get_constraint(g)
                            counts[val][g][v] += num_responses

        fig, ax = plt.subplots(len(vals), len(self.constraints)-3, sharey=True, figsize=(18,6))
        for val_ind, val in enumerate(vals):
            col_ind = 0
            for col in counts[val].keys():
                if col == 'torso_start' or col == 'torso_start_deg':
                    pass
                else:
                    keys = list(counts[val][col].keys())
                    data = np.array(list(counts[val][col].values()))
                    ax[val_ind, col_ind].bar(keys, data, align='center')
                    # ax[val_ind, col_ind].set_ylim([0, 1])
                    ax[len(vals)-1, col_ind].set_xlabel(col)
                    col_ind += 1
            ax[val_ind, 0].set_ylabel(val)
        fig.suptitle('Group = {}'.format(group), fontsize='large')
        filename = '{}/{}.png'.format('balanced', group)
        fig.savefig(filename)
        plt.close(fig)
        print(filename)

    def check_balanced_2(self, group1, group2):
        for g, vs in self.constraints:
            if group1 == g:
                vals1 = vs
            if group2 == g:
                vals2 = vs
        vals = [vals1, vals2]
        counts = {}
        for v1 in vals1:
            for v2 in vals2:
                counts[(v1, v2)] = {}
                for g, vs in self.constraints:
                    if group1 == g or group2 == g:
                        pass
                    else:
                        counts[(v1, v2)][g] = {}
                        for v in vs:
                            counts[(v1, v2)][g][v] = 0

        for movement_id, movement in enumerate(self.movements):
            for v1 in vals1:
                for v2 in vals2:
                    if movement.check_constraints(groups=[group1, group2], vals=[v1, v2]):
                        num_responses = np.where(self.responses[movement_id,:,0] > -1)[0].shape[0]
                        for g, vs in self.constraints:
                            if group1 == g or group2 == g:
                                pass
                            else:
                                v = movement.get_constraint(g)
                                for v in vs:
                                    counts[(v1, v2)][g][v] += num_responses

        fig, ax = plt.subplots(len(counts.keys()), len(self.constraints)-4, sharey=True, figsize=(18,12))
        v_ind = 0
        for v1_ind, v1 in enumerate(vals1):
            for v2_ind, v2 in enumerate(vals2):
                col_ind = 0
                for col in counts[(v1, v2)].keys():
                    if col == 'torso_start' or col == 'torso_start_deg':
                        pass
                    else:
                        keys = list(counts[(v1, v2)][col].keys())
                        data = np.array(list(counts[(v1, v2)][col].values()))
                        ax[v_ind, col_ind].bar(keys, data, align='center')
                        # ax[v_ind, col_ind].set_ylim([0, 1])
                        ax[len(counts.keys())-1, col_ind].set_xlabel(col)
                        col_ind += 1
                ax[v_ind, 0].set_ylabel('{} = {}\n{} = {}'.format(group1, v1, group2, v2))
                v_ind += 1
        fig.suptitle('Groups {} and {}'.format(group1, group2), fontsize='large')
        filename = '{}/{}-{}.png'.format('balanced', group1, group2)
        fig.savefig(filename)
        plt.close(fig)
        print(filename)

    def test_group(self, group, vals):
        print('Testing the differences in {}'.format(group))
        likert = []
        user = []
        emotion = []
        comparisons = []
        for e in self.emotion_labels:
            cur = []
            for val1 in vals:
                str1 = '{}-{}'.format(e, val1)
                for val2 in vals:
                    str2 = '{}-{}'.format(e, val2)
                    if (not val1 == val2) and (not (str2, str1) in comparisons):
                        comparisons.append((str1, str2))
        # print(comparisons)
        for movement_id, movement in enumerate(self.movements):
            for val_ind, val in enumerate(vals):
                if movement.check_constraints(groups=[group], vals=[val]):
                    cur_ind = np.where(self.responses[movement_id,:,0] > -1)[0]
                    for ind in cur_ind:
                        for e_ind in range(8):
                            likert.append(self.responses[movement_id, ind, e_ind])
                            user.append(ind)
                            emotion.append('{}-{}'.format(self.emotion_labels[e_ind], val))

        data = {'User': user, 'Likert': likert, 'Emotion': emotion}
        df = pd.DataFrame(data=data)
        pc = sp.posthoc_nemenyi_friedman(df, y_col='Likert', block_col='User', group_col='Emotion', melted=True)
        # print(pc)
        selected_pc = pc.stack().loc[comparisons]
        # print(selected_pc)

        for comp, p_value in zip(comparisons, selected_pc):
            if p_value < 0.05:
                emotion = comp[0].split('-')[0]
                print('\t', comp)
                print('\t{} is significantly different with a p-value of {:.3f}'.format(emotion, p_value))
                for val in vals:
                    selected = df.loc[df['Emotion'] == '{}-{}'.format(emotion, val)]
                    mean, median = np.mean(selected['Likert']), np.median(selected['Likert'])
                    print('\t\t{}-{} has a mean of {:.3f} and median of {:.3f}'.format(group, val, mean, median))

    def test_group_2(self, group1, vals1, group2, vals2):
        print('Testing the differences in {}-{}'.format(group1, group2))
        likert = []
        user = []
        emotion = []
        comparisons = []
        for e in self.emotion_labels:
            cur = []
            for val1 in vals1:
                for val2 in vals2:
                    str1 = '{}-{}-{}'.format(e, val1, val2)
                    for val1_1 in vals1:
                        for val2_1 in vals2:
                            str2 = '{}-{}-{}'.format(e, val1_1, val2_1)
                            if (not val1 == val1_1) and (not val2 == val2_1) and (not (str2, str1) in comparisons):
                                comparisons.append((str1, str2))

        for movement_id, movement in enumerate(self.movements):
            for v1 in vals1:
                for v2 in vals2:
                    if movement.check_constraints(groups=[group1, group2], vals=[v1, v2]):
                        cur_ind = np.where(self.responses[movement_id,:,0] > -1)[0]
                        for ind in cur_ind:
                            for e_ind in range(8):
                                likert.append(self.responses[movement_id, ind, e_ind])
                                user.append(ind)
                                emotion.append('{}-{}-{}'.format(self.emotion_labels[e_ind], v1, v2))


        data = {'User': user, 'Likert': likert, 'Emotion': emotion}
        df = pd.DataFrame(data=data)
        pc = sp.posthoc_nemenyi_friedman(df, y_col='Likert', block_col='User', group_col='Emotion', melted=True)
        col_names = pc.columns.values
        new_comparisons = []
        for comparison in comparisons:
            if comparison[0] in col_names and comparison[1] in col_names:
                new_comparisons.append(comparison)

        selected_pc = pc.stack().loc[new_comparisons]

        for comp, p_value in zip(new_comparisons, selected_pc):
            if p_value < 0.05:
                emotion = comp[0].split('-')[0]
                print('\t', comp)
                print('\t{} is significantly different with a p-value of {:.3f}'.format(emotion, p_value))
                for v1 in vals1:
                    for v2 in vals2:
                        selected = df.loc[df['Emotion'] == '{}-{}-{}'.format(emotion, v1, v2)]
                        mean, median = np.mean(selected['Likert']), np.median(selected['Likert'])
                        print('\t\t{}-{}-{}-{} has a mean of {:.3f} and median of {:.3f}'.format(group1, v1, group2, v2, mean, median))

    def test_demo_group(self, group, vals):
        print('Testing the differences in {}'.format(group))
        likert = []
        user = []
        emotion = []
        comparisons = []

        for e in self.emotion_labels:
            cur = []
            for val1 in vals:
                str1 = '{}-{}'.format(e, val1)
                for val2 in vals:
                    str2 = '{}-{}'.format(e, val2)
                    if (not val1 == val2) and (not (str2, str1) in comparisons):
                        comparisons.append((str1, str2))

        for movement_id, movement in enumerate(self.movements):
            cur_ind = np.where(self.responses[movement_id,:,0] > -1)[0]
            for ind in cur_ind:
                for e_ind in range(8):
                    if group == 'ages' and self.age[ind].astype('int') > -0.5:
                        likert.append(self.responses[movement_id, ind, e_ind])
                        user.append(ind)
                        emotion.append('{}-{}'.format(self.emotion_labels[e_ind], vals[self.age[ind].astype('int')]))
                    if group == 'genders' and self.gender[ind].astype('int') > -0.5:
                        likert.append(self.responses[movement_id, ind, e_ind])
                        user.append(ind)
                        emotion.append('{}-{}'.format(self.emotion_labels[e_ind], vals[self.gender[ind].astype('int')]))
                    if group == 'robots' and self.robot[ind].astype('int') > -0.5:
                        likert.append(self.responses[movement_id, ind, e_ind])
                        user.append(ind)
                        emotion.append('{}-{}'.format(self.emotion_labels[e_ind], vals[self.robot[ind].astype('int')]))
                    if group == 'ethnicities' and self.ethnicity[ind,0].astype('int') > -0.5:
                        likert.append(self.responses[movement_id, ind, e_ind])
                        user.append(ind)
                        emotion.append('{}-{}'.format(self.emotion_labels[e_ind], vals[self.ethnicity[ind,0].astype('int')]))
                        if self.ethnicity[ind,1] > -0.5:
                            likert.append(self.responses[movement_id, ind, e_ind])
                            user.append(ind)
                            emotion.append('{}-{}'.format(self.emotion_labels[e_ind], vals[self.ethnicity[ind,1].astype('int')]))

        data = {'User': user, 'Likert': likert, 'Emotion': emotion}
        df = pd.DataFrame(data=data)
        pc = sp.posthoc_nemenyi_friedman(df, y_col='Likert', block_col='User', group_col='Emotion', melted=True)
        col_names = pc.columns.values
        new_comparisons = []
        for comparison in comparisons:
            if comparison[0] in col_names and comparison[1] in col_names:
                new_comparisons.append(comparison)
        selected_pc = pc.stack().loc[new_comparisons]

        for comp, p_value in zip(new_comparisons, selected_pc):
            if p_value < 0.05:
                emotion = comp[0].split('-')[0]
                print('\t', comp)
                print('\t{} is significantly different with a p-value of {:.3f}'.format(emotion, p_value))
                for val in vals:
                    selected = df.loc[df['Emotion'] == '{}-{}'.format(emotion, val)]
                    if selected.shape[0] > 0:
                        mean, median = np.mean(selected['Likert']), np.median(selected['Likert'])
                        print('\t\t{}-{} has a mean of {:.3f} and median of {:.3f} - {}'.format(group, val, mean, median, selected.shape[0]))
                    else:
                        print('\t\t{}-{} has a mean of {:.3f} and median of {:.3f}'.format(group, val, -1, -1))
