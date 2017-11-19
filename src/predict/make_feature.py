import matplotlib.pyplot as plt 
import numpy as np
import sys
sys.path.append('..')
import utils
import features
import knn

records_name = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
dim_amount = (5 * 5)
train_tip_dist = np.zeros([dim_amount,0])
test_tip_dist = np.zeros([dim_amount,0])
training_data_amount = 3
maximum_data_amount = 10

for record_name in records_name:
    data_amount = utils.get_last_index_from_folder('../record/{0}'.format(record_name)) + 1    

    tip_distance = features.get_feature_tip_distance(record_name, data_amount)

    for i in range(tip_distance.shape[1]):
        if i < training_data_amount:
            train_tip_dist = np.append(train_tip_dist, tip_distance[:, i].reshape(dim_amount, 1), axis = 1)
        elif i < maximum_data_amount:
            test_tip_dist = np.append(test_tip_dist, tip_distance[:, i].reshape(dim_amount, 1), axis = 1)
        # train_tip_dist.append( tip_distance[:, :training_data_amount])
        # test_tip_dist.append(tip_distance[:, training_data_amount:maximum_data_amount])
    
# print(train_tip_dist.shape)
# print(test_tip_dist.shape)

sim_mat = knn.create_similarity_matrix(train_tip_dist, test_tip_dist)
# label_flags = knn.get_label_flags(sim_mat)

# # tpr_10, far_10 = knn.calculate_sensitivity(sim_mat, 10, label_flags)
# tpr_10 = knn.calculate_sensitivity(sim_mat, 10, label_flags)

plt.imshow(sim_mat,cmap="gray") 
plt.show() 

# print("At t = 10 TPR is {0} and FAR is {1}".format(tpr_10, far_10))