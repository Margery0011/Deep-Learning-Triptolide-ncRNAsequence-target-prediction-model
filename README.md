# The-research-on-the-Triptolide-nucleic-acid-sequence-target-prediction-model-

- Organized, categorized and pre-processed the available data of the action site of Triptolide on miRNAs. 
- Developed various deep learning models, including Deep Neural Network (DNN), Recurrent Neural Network (RNN), and Long-Short Time Memory (LSTM).
- Built a prediction models database based on the binding of Triptolide to miRNA. 
- Compared the training effects of each model and selected the optimal one.
- Predicted the action site of Triptolide on siRNAs with the optimal trained model.

# Pre-Preprocess

- Each sequence is arranged in columns
- Each 4th row of data in each column is a one-hot encoding of 1 base
- There are 100 sequences so there are 100 columns
- The longest is 24 bases, so there are 24*4=96 lines
- Insufficient to make up 0


## Import library

import xlrd
import numpy as np
from shape_3d import *
import scipy.io as scio

## Import Excel Data 

book = xlrd.open_workbook('data.xls')
sheet = book.sheets()[0]
affinity = sheet.col_values(0)
seq = sheet.col_values(1)
name = sheet.col_values(2)
affi = np.zeros((1,len(affinity)))
affi[0,:] = affinity

## One- hot Transfer 

A_oh = [1,0,0,0]
U_oh = [0,1,0,0]
C_oh = [0,0,1,0]
G_oh = [0,0,0,1]
max_length = 0
for rna in seq:
    if len(rna) > max_length:
        max_length = len(rna)

seq_oh=np.zeros((4*max_length, len(seq)))
for i in range(len(seq)):
    j = 0
    for base in seq[i]:
        if base == 'A':
            seq_oh[4*j:4*(j+1),i] = A_oh
        elif base == 'U':
            seq_oh[4 * j:4 * (j + 1), i] = U_oh
        elif base == 'C':
            seq_oh[4 * j:4 * (j + 1), i] = C_oh
        elif base == 'G':
            seq_oh[4 * j:4 * (j + 1), i] = G_oh
        j += 1

seq_3D = shape23D(seq_oh)
affi_n = affi / (-15.0)
scio.savemat('data100.mat',
             {'sample':name,
             'affinity':affinity,
             'normalized affinity':affi_n,
             'sequence':seq,
             'one-hot sequence':seq_oh,
             '3D sequence':seq_3D})

