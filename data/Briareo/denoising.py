import numpy as np
import os
import pickle
import json

with open('validation.json', 'r') as f:
    validation = json.load(f)

with open('train.json', 'r') as f:
    train = json.load(f)

with open('test.json', 'r') as f:
    test = json.load(f)    


def get_frames(data):
  frames_cnt=[]
  for seq in data:
    frames_cnt.append(len(seq['skeleton']))
  return(frames_cnt)

def get_labels(data):
  labels=[]
  for seq in data:
    labels.append(seq['label'])
  return(labels)

def get_raw_joints(data):
  raw_joints=[]
  for seq in data:
    num_frames= len(seq['skeleton'])
    frame_joints=[]
    for i in range(num_frames):
        full_joints=[]
        for k in range(len(seq['skeleton'][i])):
          for j in range(3):
            full_joints.append(seq['skeleton'][i][k][j])
        frame_joints.append(full_joints)
    raw_joints.append(frame_joints)
  return(raw_joints)  

if __name__ == '__main__':
    with open('../Briareo/validation.json', 'r') as f:
    validation = json.load(f)

    with open('../Briareo/train.json', 'r') as f:
        train = json.load(f)

    with open('../Briareo/test.json', 'r') as f:
        test = json.load(f)   

    frames_train=get_frames(train)
    frames_validation=get_frames(validation)
    frames_test=get_frames(test)

    labels_train=get_labels(train)
    labels_validation=get_labels(validation)
    labels_test=get_labels(test)

    raw_joints_train=get_raw_joints(train)
    raw_joints_validation=get_raw_joints(validation)
    raw_joints_test=get_raw_joints(test)

    save_path = os.path.join('../Briareo/', 'Preprocessing')
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    np.savetxt(os.path.join(save_path, 'frames_train.txt'), frames_train, fmt='%d')
    np.savetxt(os.path.join(save_path, 'frames_validation.txt'), frames_validation, fmt='%d')
    np.savetxt(os.path.join(save_path, 'frames_test.txt'), frames_test, fmt='%d')

    np.savetxt(os.path.join(save_path, 'labels_train.txt'), labels_train, fmt='%d')
    np.savetxt(os.path.join(save_path, 'labels_validation.txt'), labels_validation, fmt='%d')
    np.savetxt(os.path.join(save_path, 'labels_test.txt'), labels_test, fmt='%d')



    save_path = os.path.join('../Briareo/', 'denoised_data')
    if not os.path.exists(save_path):
        os.mkdir(save_path)


    train_skes_joints_pkl = os.path.join(save_path, 'train_denoised_joints.pkl')
    with open(train_skes_joints_pkl, 'wb') as f:
        pickle.dump(raw_joints_train, f, pickle.HIGHEST_PROTOCOL)

    validation_skes_joints_pkl = os.path.join(save_path, 'validation_denoised_joints.pkl')
    with open(validation_skes_joints_pkl, 'wb') as f:
        pickle.dump(raw_joints_validation, f, pickle.HIGHEST_PROTOCOL)

    test_skes_joints_pkl = os.path.join(save_path, 'test_denoised_joints.pkl')
    with open(test_skes_joints_pkl, 'wb') as f:
        pickle.dump(raw_joints_test, f, pickle.HIGHEST_PROTOCOL)    