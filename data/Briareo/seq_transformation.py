import os
import os.path as osp
import numpy as np
import pickle
import logging
import h5py

test_aligned_pkl = '../Briareo/denoised_data/test_aligned_frames_joints.pkl'
train_aligned_pkl = '../Briareo/denoised_data/train_aligned_frames_joints.pkl'
train_label_file = '../Briareo/Preprocessing/labels_train.txt'
test_label_file = '../Briareo/Preprocessing/labels_test.txt'


def one_hot_vector(labels):
    num_skes = len(labels)
    labels_vector = np.zeros((num_skes, 13))
    for idx, l in enumerate(labels):
        labels_vector[idx, l] = 1

    return labels_vector

def split_dataset(skes_joints_train, skes_joints_test, train_label, test_label):
    m = 'sklearn'  # 'sklearn' or 'numpy'
    # Select validation set from training set
    # train_indices, val_indices = split_train_val(train_indices, m)

    # Save labels and num_frames for each sequence of each data set
   

    train_x = skes_joints_train
    train_y = one_hot_vector(train_label)
    test_x = skes_joints_test
    test_y = one_hot_vector(test_label)

    save_name = 'briareo.npz' 
    np.savez(save_name, x_train=train_x, y_train=train_y, x_test=test_x, y_test=test_y)

    # Save data into a .h5 file
    # h5file = h5py.File(osp.join(save_path, 'NTU_%s.h5' % (evaluation)), 'w')
    # Training set
    # h5file.create_dataset('x', data=skes_joints[train_indices])
    # train_one_hot_labels = one_hot_vector(train_labels)
    # h5file.create_dataset('y', data=train_one_hot_labels)
    # Validation set
    # h5file.create_dataset('valid_x', data=skes_joints[val_indices])
    # val_one_hot_labels = one_hot_vector(val_labels)
    # h5file.create_dataset('valid_y', data=val_one_hot_labels)
    # Test set
    # h5file.create_dataset('test_x', data=skes_joints[test_indices])
    # test_one_hot_labels = one_hot_vector(test_labels)
    # h5file.create_dataset('test_y', data=test_one_hot_labels)

    # h5file.close()

if __name__ == '__main__':

    train_label = np.loadtxt(train_label_file, dtype=int)
    with open(train_aligned_pkl, 'rb') as fr:
        skes_joints_train = pickle.load(fr)  # a list
    
    test_label = np.loadtxt(test_label_file, dtype=int)
    with open(test_aligned_pkl, 'rb') as fr:
        skes_joints_test= pickle.load(fr)  # a list

    split_dataset(skes_joints_train, skes_joints_test, train_label, test_label)