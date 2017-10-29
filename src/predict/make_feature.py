import matplotlib.pyplot as plt 
import sys
sys.path.append('..')
import utils
import features
import knn

data_amount = utils.get_last_index_from_folder('../record/one') + 1
training_data_amount = int(data_amount * 0.3)
test_data_amount = data_amount - training_data_amount

tip_distance = features.get_feature_tip_distance(data_amount)

training_tip_data = tip_distance[:, :training_data_amount]
test_tip_data = tip_distance[:, training_data_amount:]

sim_mat = knn.create_similarity_matrix(training_tip_data, test_tip_data)
label_flags = knn.get_label_flags(sim_mat)

# tpr_10, far_10 = knn.calculate_sensitivity(sim_mat, 9, label_flags)
tpr_10 = knn.calculate_sensitivity(sim_mat, 9, label_flags)

plt.imshow(sim_mat,cmap="gray") 
plt.show() 

print("At t = 10 TPR is {0} and FAR is {1}".format(tpr_10, far_10))