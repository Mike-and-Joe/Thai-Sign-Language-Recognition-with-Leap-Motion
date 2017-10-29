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

        if min_euclidean < t and flags[0, j] == 1:
            true_positive += 1
        elif min_euclidean > t and flags[0, j] == 0:
            true_negative += 1
        elif min_euclidean < t and flags[0, j] == 0:
            false_positive += 1
        else:
            false_negative += 1
    print(true_positive, true_negative, false_positive, false_negative)
    true_positive_rate = true_positive / (true_positive + false_negative)
    # false_alarm_rate = false_positive / (false_positive + true_negative)
    
    # return true_positive_rate, false_alarm_rate
    return true_positive_rate
