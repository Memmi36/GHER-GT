import numpy as np
import os
import pickle


def align_frames(skes_joints, frames_cnt):
    """
    Align all sequences with the same frame length.

    """
    num_skes = len(skes_joints)
    max_num_frames = frames_cnt.max()  # 160
    aligned_skes_joints = np.zeros((num_skes, max_num_frames, 66))

    for idx, ske_joints in enumerate(skes_joints):
        ske_joints = np.array(ske_joints)
        num_frames = ske_joints.shape[0]
        ske_joints.shape[1] == 66
        aligned_skes_joints[idx, :num_frames] = ske_joints

    return aligned_skes_joints

if __name__ == '__main__':
        train_skes_joints_pkl = os.path.join('../Briareo/denoised_data', 'train_denoised_joints.pkl')
        validation_skes_joints_pkl = os.path.join('../Briareo/denoised_data', 'validation_denoised_joints.pkl')
        test_skes_joints_pkl = os.path.join('../Briareo/denoised_data', 'test_denoised_joints.pkl')

        frames_file = os.path.join('../Briareo/Preprocessing', 'frames_train.txt')
        frames_train = np.loadtxt(frames_file, dtype=int)
        with open(train_skes_joints_pkl, 'rb') as fr:
                skes_joints = pickle.load(fr)  # a list
        skes_joints_train = align_frames(skes_joints, frames_train) 
        train_aligned_frames_joints_pkl = os.path.join(save_path, 'train_aligned_frames_joints.pkl')
        with open(train_aligned_frames_joints_pkl, 'wb') as f:
            pickle.dump(skes_joints_train, f, pickle.HIGHEST_PROTOCOL)   

        frames_file = os.path.join('../Briareo/Preprocessing', 'frames_test.txt')
        frames_test = np.loadtxt(frames_file, dtype=int)
        with open(test_skes_joints_pkl, 'rb') as fr:
                skes_joints = pickle.load(fr)  # a list
        skes_joints_test = align_frames(skes_joints, frames_test)
        test_aligned_frames_joints_pkl = os.path.join(save_path, 'test_aligned_frames_joints.pkl')
        with open(test_aligned_frames_joints_pkl, 'wb') as f:
            pickle.dump(skes_joints_test, f, pickle.HIGHEST_PROTOCOL)

        frames_file = os.path.join('../Briareo/Preprocessing', 'frames_validation.txt')
        frames_validation = np.loadtxt(frames_file, dtype=int)
        with open(validation_skes_joints_pkl, 'rb') as fr:
                skes_joints = pickle.load(fr)  # a list
        skes_joints_validation = align_frames(skes_joints, frames_validation)
        validation_aligned_frames_joints_pkl = os.path.join(save_path, 'validation_aligned_frames_joints.pkl')
        with open(validation_aligned_frames_joints_pkl, 'wb') as f:
            pickle.dump(skes_joints_validation, f, pickle.HIGHEST_PROTOCOL)    