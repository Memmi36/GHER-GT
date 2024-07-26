# GHER-GT

![her](https://github.com/user-attachments/assets/abe6a85e-f98a-47c1-b695-366d727b7c6d)



## Abstract
Hand gestures can be studied by analyzing the location and movement of closely spaced and interacting joints, thus requiring tailored methods to accurately capture the joints intricate spatial and temporal dynamics. 
To address this particularity, we propose an approach for dynamic hand gesture recognition, which relies on the Graph Hierarchical Edge Representation-Graph Transformer (GHER-GT). Our approach utilizes a skeleton-based method with an end-to-end graph model integrated within an efficient spatio-temporal block.
This spatio-temporal processing framework leverages multilevel spatial feature representation of hand joints, highlighting both directly connected and distant joints. Subsequently, an attention mechanism within the graph transformer model captures the temporal dynamics effectively. The higher-order information learning models essential interactions between hand joints selectively, enhancing computational efficiency and interpretability. 
An in-depth ablation study underscores the significance of our graph hierarchical approach and the impact of different architectural configurations. Experimental evaluations on three benchmark datasets, namely IPN, SHREC'17, and BRIAREO demonstrate the accuracy of our approach is competitive or even surpasses that reported in the state-of-the-art for the task of dynamic hand gesture recognition.

## Installation
  pip install git+https://github.com/zhijian-liu/torchpack.git

## Data Preprocessing
1. Dawnload Briareo dataset from [the AIMAGELAB Image Lab](https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=31).
2. Execute these commands to prepare the data:
   ```bash
   cd ./data/Briareo 
   python denoising.py
   python frames_aligning.py
   python seq_transformation.py

## Usage
   ```bash
   python main.py --config ./config/briareo/briareo_com_9.yaml --device 0 --optimizer Adam
