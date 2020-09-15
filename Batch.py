import numpy as np
import matplotlib.pyplot as plt
import scikit_posthocs as sp
import pandas as pd

class Batch:
    """docstring for Batch."""

    def __init__(self, movement_arr, user_num):
        super(Batch, self).__init__()
        self.movements = movement_arr
        self.responses = np.zeros((len(movement_arr), user_num, 8))
        self.timing = np.zeros((len(movement_arr), user_num, 3))
        self.emotion_labels = ['Happiness', 'Sadness', 'Fear', 'Disgust', 'Anger', 'Surprise', 'Interest', 'Neutral']
        self.likert = ['Not', 'Slightly', 'Somewhat', 'Moderately', 'Intensely']
        self.constraints = [['torso_start',['neutral']],
                            ['torso_start_deg',['small', 'large']],
                            ['torso_end',['neutral', 'forward', 'backward']],
                            ['torso_end_deg',['small', 'large']],
                            ['torso_speed',['none', 'slow', 'fast']],
                            ['left_arm_start',['forward', 'sides']],
                            ['left_arm_end',['forward', 'sides', 'high']],
                            ['left_arm_speed',['none', 'slow', 'fast']],
                            ['right_arm_start',['forward', 'sides']],
                            ['right_arm_end',['forward', 'sides', 'high']],
                            ['right_arm_speed',['slow', 'fast']]]
        self.single_constraint_num = {}

    def add_user_response(self, user, user_num):
        self.responses[:, user_num, :] = user.responses
        self.timing[:, user_num, :] = user.timing

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

    def constraint_posthoc(self, folder_name):
        emotions_labels2 = [emotion + '-2' for emotion in self.emotion_labels]
        heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True, 'cbar_ax_bbox': [0.87, 0.35, 0.04, 0.3]}

        for group1, vals1 in self.constraints:
                for val1 in vals1:
                    for group2, vals2 in self.constraints:
                        for val2 in vals2:

                            data = [[],[],[]]
                            totals = [[], [], [], [], [], [], [], []]
                            totals2 = [[], [], [], [], [], [], [], []]
                            movcount = 0
                            movcount2 = 0
                            fig, ax = plt.subplots(figsize=(10,9))
                            if group1 == group2 and val1 == val2:
                                for vid_ind1, movement in enumerate(self.movements):
                                    if movement.check_constraints(groups=[group1], vals=[val1]):
                                        movcount += 1
                                        for row_ind, row in enumerate(self.responses[vid_ind1,:,:]):
                                            if row[0]> -1:
                                                for col_ind, col in enumerate(row):
                                                    data[0].append(self.emotion_labels[col_ind])
                                                    data[1].append(str(row_ind))
                                                    data[2].append(int(col))
                                                    totals[col_ind].append(int(col))

                                data = {'Emotion': data[0], 'Rater': data[1], 'Likert': data[2]}
                                df = pd.DataFrame(data=data)
                                pc = sp.posthoc_mannwhitney(df, val_col='Likert', group_col='Emotion')
                                sp.sign_plot(pc, ax=ax, **heatmap_args)
                                ax.set_title('Constraint {}-{} (n = {})- P-Values'.format(group1, val1, movcount))
                                labels = []
                                for e_ind, emotion in enumerate(self.emotion_labels):
                                    labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals[e_ind]), np.median(totals[e_ind])))

                                ax.xaxis.set(ticks=np.arange(0.5, len(self.emotion_labels)), ticklabels=labels)
                                ax.yaxis.set(ticks=np.arange(0.1, len(self.emotion_labels)), ticklabels=self.emotion_labels)

                            else:
                                for vid_ind1, movement in enumerate(self.movements):
                                    if movement.check_constraints(groups=[group1], vals=[val1]):
                                        movcount += 1
                                        for row_ind, row in enumerate(self.responses[vid_ind1,:,:]):
                                            if row[0]> -1:
                                                for col_ind, col in enumerate(row):
                                                    data[0].append(self.emotion_labels[col_ind])
                                                    data[1].append(str(row_ind))
                                                    data[2].append(int(col))
                                                    totals[col_ind].append(int(col))
                                for vid_ind2, movement in enumerate(self.movements):
                                    if movement.check_constraints(groups=[group2], vals=[val2]):
                                        movcount2 += 1
                                        for row_ind, row in enumerate(self.responses[vid_ind2,:,:]):
                                            if row[0]> -1:
                                                for col_ind, col in enumerate(row):
                                                    data[0].append(self.emotion_labels[col_ind]+'-2')
                                                    data[1].append(str(row_ind))
                                                    data[2].append(int(col))
                                                    totals2[col_ind].append(int(col))

                                data = {'Emotion': data[0], 'Rater': data[1], 'Likert': data[2]}
                                df = pd.DataFrame(data=data)
                                pc = sp.posthoc_mannwhitney(df, val_col='Likert', group_col='Emotion', sort=False)
                                # pc = pc.loc[self.emotion_labels , emotions_labels2]

                                sp.sign_plot(pc, ax=ax, **heatmap_args)

                                ax.set_title('Constraint {}-{} (n = {}) vs {}-{} (n = {}) - P-Values'.format(group1, val1, movcount, group2, val2, movcount2))
                                labels = []
                                for e_ind, emotion in enumerate(self.emotion_labels):
                                    labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals[e_ind]), np.median(totals[e_ind])))
                                for e_ind, emotion in enumerate(emotions_labels2):
                                    labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals2[e_ind]), np.median(totals2[e_ind])))

                                ax.xaxis.set(ticks=np.arange(0.5, len(labels)), ticklabels=labels)
                                ax.yaxis.set(ticks=np.arange(0.5, len(labels)), ticklabels=labels)

                            filename = '{}/{}-{}-{}-{}.png'.format(folder_name, group1, val1, group2, val2)
                            # plt.show()
                            # return
                            fig.savefig(filename)
                            plt.close(fig)
                            print(filename)
                            # return

    def video_posthoc(self, folder_name):
        emotions_labels2 = [emotion + '-2' for emotion in self.emotion_labels]
        heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True, 'cbar_ax_bbox': [0.87, 0.35, 0.04, 0.3]}

        for vid_ind1 in range(self.responses.shape[0]):
            for vid_ind2 in range(self.responses.shape[0]):

                if vid_ind1 == vid_ind2:
                    data = [[],[],[]]
                    totals = [[], [], [], [], [], [], [], []]
                    totals2 = [[], [], [], [], [], [], [], []]
                    fig, ax = plt.subplots(figsize=(10,9))
                    for row_ind, row in enumerate(self.responses[vid_ind1,:,:]):
                        if row[0]> -1:
                            for col_ind, col in enumerate(row):
                                data[0].append(self.emotion_labels[col_ind])
                                data[1].append(str(row_ind))
                                data[2].append(int(col))
                                totals[col_ind].append(int(col))
                    data = {'Emotion': data[0], 'Rater': data[1], 'Likert': data[2]}
                    df = pd.DataFrame(data=data)
                    pc = sp.posthoc_mannwhitney(df, val_col='Likert', group_col='Emotion')
                    sp.sign_plot(pc, ax=ax, **heatmap_args)
                    ax.set_title('Movement {0:03d} - P-Values'.format(vid_ind1))
                    labels = []
                    for e_ind, emotion in enumerate(self.emotion_labels):
                        labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals[e_ind]), np.median(totals[e_ind])))

                    ax.xaxis.set(ticks=np.arange(0.5, len(self.emotion_labels)), ticklabels=labels)
                    ax.yaxis.set(ticks=np.arange(0.1, len(self.emotion_labels)), ticklabels=self.emotion_labels)
                    filename = '{}/{:03d}-{:03d}.png'.format(folder_name, vid_ind1, vid_ind2)
                    fig.savefig(filename)
                    plt.close(fig)
                    print(filename)

                else:
                    pass
                    # for row_ind, row in enumerate(self.responses[vid_ind1,:,:]):
                    #     if row[0]> -1:
                    #         for col_ind, col in enumerate(row):
                    #             data[0].append(self.emotion_labels[col_ind])
                    #             data[1].append(str(row_ind))
                    #             data[2].append(int(col))
                    #             totals[col_ind].append(int(col))
                    # for row_ind, row in enumerate(self.responses[vid_ind2,:,:]):
                    #     if row[0]> -1:
                    #         for col_ind, col in enumerate(row):
                    #             data[0].append(self.emotion_labels[col_ind]+'-2')
                    #             data[1].append(str(row_ind))
                    #             data[2].append(int(col))
                    #             totals2[col_ind].append(int(col))
                    #
                    # data = {'Emotion': data[0], 'Rater': data[1], 'Likert': data[2]}
                    # df = pd.DataFrame(data=data)
                    # pc = sp.posthoc_mannwhitney(df, val_col='Likert', group_col='Emotion', sort=False)
                    # # pc = pc.loc[self.emotion_labels , emotions_labels2]
                    #
                    # sp.sign_plot(pc, ax=ax, **heatmap_args)
                    #
                    # ax.set_title('Movement {0:03d} vs {1:03d} - P-Values'.format(vid_ind1, vid_ind2))
                    # labels = []
                    # for e_ind, emotion in enumerate(self.emotion_labels):
                    #     labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals[e_ind]), np.median(totals[e_ind])))
                    # for e_ind, emotion in enumerate(self.emotion_labels):
                    #     labels.append('{}\nMean: {:.2f}\nMedian: {}'.format(emotion, np.mean(totals2[e_ind]), np.median(totals2[e_ind])))
                    #
                    # ax.xaxis.set(ticks=np.arange(0.5, len(labels)), ticklabels=labels)
                    # ax.yaxis.set(ticks=np.arange(0.5, len(self.emotion_labels)), ticklabels=labels2)


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
