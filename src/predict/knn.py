import numpy as np

def create_similarity_matrix(T, D):
    total_T_amount = T.shape[1]
    total_D_amount = D.shape[1]
    
    sim_mat = np.zeros([total_T_amount, total_D_amount])

    for i in range(total_T_amount):
        for j in range(total_D_amount):
            sim_mat[i,j] = np.linalg.norm(T[:, i] - D[:, j])

    return sim_mat

def get_label_flags(sim_mat):
    label_flags = np.zeros([sim_mat.shape[0], sim_mat.shape[1]])

    start = 0
    end = sim_mat.shape[1]
    label_flags[start][start:end] = 1

    return label_flags

def calculate_sensitivity(sim_mat, t, flags):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    
    for j in range(sim_mat.shape[1]):
        min_euclidean = min(sim_mat[0, j], sim_mat[1, j], sim_mat[2, j])
        print(t, min_euclidean)
        if min_euclidean < t and flags[0, j] == 1:
            true_positive += 1
        elif min_euclidean > t and flags[0, j] == 0:
            true_negative += 1
        elif min_euclidean < t and flags[0, j] == 0:
            false_positive += 1
        else:
            false_negative += 1
    # print(true_positive, true_negative, false_positive, false_negative)
    true_positive_rate = true_positive / (true_positive + false_negative)
    false_alarm_rate = false_positive / (false_positive + true_negative)
    
    return true_positive_rate, false_alarm_rate
    # return true_positive_rate

def plot_roc(sim_mat, label_flags, title, label=None, show=True):
    threshold = np.linspace(np.amin(sim_mat), np.amax(sim_mat), num = 1000)
    TPR_list, FAR_list, FNR_list = [], [], []
    
    for t in threshold:
        tpr, far = calculate_sensitivity(sim_mat, t, label_flags)
        TPR_list.append(tpr)
        FNR_list.append(1-tpr)
        FAR_list.append(far) 
    if label is None:
        label = 'TPR'
    
    roc = plt.plot(FAR_list, TPR_list, label=label)
    if show:
        plt.plot(FAR_list, [1 - far for far in FAR_list], color='orange', label='EER Line')
        plt.legend(bbox_to_anchor=(1.05, 0.85, 0.4, 0.15), loc=2, ncol=1, mode="expand", borderaxespad=0.)
        plt.title(title)
        plt.xlabel('False Alarm Rate')
        plt.ylabel('True Positive Rate')
        plt.show()
    
    return roc, FAR_list, FNR_list, TPR_list

def get_eer(far, fnr):
    eer = 0
    prev_far = None
    prev_fnr = None
    for i in range(len(fnr)):
        if far[i] < fnr[i]:
            prev_far = far[i]
            prev_fnr = fnr[i]
        else:
            #solve eer from linear equation
            y1 = prev_fnr
            y2 = fnr[i]

            x1 = prev_far
            x2 = far[i]

            delta_y = y2 - y1
            delta_x = x2 - x1

            m = delta_y / delta_x
            c = y2 - (m*x2)

            eer = c / (1-m)
            break
        
    return eer