import csv

torso_start_arr = ['forward', 'backward', 'neutral']
torso_start_deg_arr = ['small', 'medium', 'large']
torso_end_arr = ['forward', 'backward', 'neutral']
torso_end_deg_arr = ['small', 'medium', 'large']
torso_speed_arr = ['slow', 'medium', 'fast']
left_arm_start_arr = ['forward', 'sides', 'high', 'out']
left_arm_end_arr = ['forward', 'sides', 'high', 'out']
left_arm_speed_arr = ['slow', 'medium', 'fast']
right_arm_start_arr = ['forward', 'sides', 'high', 'out']
right_arm_end_arr = ['forward', 'sides', 'high', 'out']
right_arm_speed_arr = ['slow', 'medium', 'fast']

with open('torso_arm_dof.csv', 'w', newline='') as csvfile:
    fieldnames = ['torso_start', 'torso_start_deg', 'torso_end', 'torso_end_deg', 'torso_speed', 'left_arm_start', 'left_arm_end', 'left_arm_speed', 'right_arm_start', 'right_arm_end', 'right_arm_speed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    options = 0
    for torso_start in torso_start_arr:
        for torso_start_deg in torso_start_deg_arr:
            for torso_end in torso_end_arr:
                for torso_end_deg in torso_end_deg_arr:
                    for torso_speed in torso_speed_arr:
                        for left_arm_start in left_arm_start_arr:
                            for left_arm_end in left_arm_end_arr:
                                for left_arm_speed in left_arm_speed_arr:
                                    for right_arm_start in right_arm_start_arr:
                                        for right_arm_end in right_arm_end_arr:
                                            for right_arm_speed in right_arm_speed_arr:

                                                add_flag = True

                                                #Torso

                                                #Degree does not matter for neutral torso
                                                if (torso_start == 'neutral') and (not torso_start_deg == 'small'):
                                                    add_flag = False
                                                if (torso_end == 'neutral') and (not torso_end_deg == 'small'):
                                                    add_flag = False

                                                #Speed does not matter if start and end position are the same
                                                if (torso_start == torso_end) and (torso_start_deg == torso_end_deg) and (not torso_end_deg == 'small'):
                                                    add_flag = False

                                                #The torso cannot start and end in the same direction (i.e. forward small to forward large)
                                                if (torso_start == torso_end):
                                                    add_flag = False

                                                #Only two speeds of the torso (slow and fast)
                                                if (torso_speed == 'medium'):
                                                    add_flag = False

                                                #Only two degrees of the torso (small and large)
                                                if (torso_start_deg == 'medium') or (torso_end_deg == 'medium'):
                                                    add_flag = False

                                                #Can only start at a “neutral” position
                                                if (not torso_start == 'neutral'):
                                                    add_flag = False

                                                #Arms

                                                #Speed does not matter for stationary arm
                                                if (left_arm_start == left_arm_end) and (not left_arm_speed == 'slow'):
                                                    add_flag = False
                                                if (right_arm_start == right_arm_end) and (not right_arm_speed == 'slow'):
                                                    add_flag = False

                                                #Arms are always symmetric in speed

                                                #Only two speeds (slow and fast)
                                                if (left_arm_speed == 'medium') or (right_arm_speed == 'medium'):
                                                    add_flag = False

                                                #Eliminate all left arm alone actions (for symmetry)
                                                if (right_arm_start == right_arm_end) and (not left_arm_start == left_arm_end):
                                                    add_flag = False

                                                #If both arms are moving, must be symmetric
                                                if (not right_arm_start == right_arm_end) and (not left_arm_start == left_arm_end):
                                                    if (not right_arm_start == left_arm_start) or (not left_arm_end == right_arm_end) or (not right_arm_speed == left_arm_speed):
                                                        add_flag = False

                                                #Eliminate the “out” position
                                                if (left_arm_start == 'out') or (right_arm_start == 'out') or (left_arm_end == 'out') or (right_arm_end == 'out'):
                                                    add_flag = False

                                                #Do not start from a high position
                                                if (left_arm_start == 'high') or (right_arm_start == 'high'):
                                                    add_flag = False

                                                if add_flag:
                                                    options += 1
                                                    writer.writerow({'torso_start': torso_start, 'torso_start_deg': torso_start_deg, 'torso_end': torso_end, 'torso_end_deg': torso_end_deg, 'torso_speed': torso_speed, 'left_arm_start': left_arm_start, 'left_arm_end': left_arm_end, 'left_arm_speed': left_arm_speed, 'right_arm_start': right_arm_start, 'right_arm_end': right_arm_end, 'right_arm_speed': right_arm_speed})
                                                    # print({'left_arm_start': left_arm_start, 'left_arm_end': left_arm_end, 'left_arm_speed': left_arm_speed, 'right_arm_start': right_arm_start, 'right_arm_end': right_arm_end, 'right_arm_speed': right_arm_speed})


print(options)
