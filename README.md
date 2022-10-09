# Nucleic acid target prediction model of triptolide

## Introduction 

Based on the binding information of triptolide and microRNA to build and train a deep learning model for the combination prediction of triptolide and a nucleic acid sequence, and use the library to verify the model, that is, apply this model to the piRNA database to find triptolide target, and compare the obtained results with the results of molecular docking experiments.

## Summary

- Organized, categorized, and pre-processed the available data of the active site of Triptolide on miRNAs.
- Developed various deep learning models, including Deep Neural Networks (DNN), Recurrent-Neural Networks (RNN), and Long-Short Time Memory (LSTM).
- Built a prediction models database based on the binding of Triptolide to miRNA.
- Compared the training effects of each model and selected the optimal one.
- Predicted the action site of Triptolide on siRNAs with the optimal trained model.

## Data Acquisition

- microRNA: [miRBase](https://www.mirbase.org/)

- piRNA: [piRNABank](http://pirnabank.ibab.ac.in/)

- Selected humans as the species and download nucleic acid sequence data from both datasets.

- Results of docking between triptolide and microRNA were obtained from our [lab](https://life.buct.edu.cn/2019/1031/c709a5600/pagem.htm)

## Data Pre-Process

### 1. Read data

**Read the Name File** 

In this file, odd-numbered lines are names, and even-numbered lines are sequences.

- Take the last element after the delimiter and remove the carriage return in the Odd-numbered lines 

- Remove carriage returns from even lines

- Since The average length of the base pair sequence of miRNA is 21 and most of the sequences are less than 23 base pairs, so we only take data with a length of 23 or less as the training and testing of the model.

**Read the affinity file**

- Read names and binding affinity separately

**Cross comparison**

- Filter out the sequences with the overlapping names in the two reads, and search the name in the binding degree to get several corresponding binding degrees
- Classify them together with the name and the sequence, so as to avoid confusion about the sequence and binding affinity

### 2. Normalize the binding affinity

- Take the maximum absolute value of the binding energy of triptolide and miRNA as the benchmark, and divide all the remaining data by this number to get normalization.

- After normalization, it is found that the degree of affinity roughly conforms to the normal distribution, and the distribution of the data is relatively scattered. Therefore, we perform data augmentation.

### 3. Data Augmentation

- Enhance the data: after observation, it is found that the data above 0.75 or below 0.25 only accounts for about 5% of the overall data, 0.6-0.75 and 0.25-0.3 account for about 15%, and 0.4-0.6 accounts for 80%. According to the proportion, we repeatedly read the data with a less binding degree, while the data of 0.4-0.6 is read only once so that the distribution of the data becomes uniform, smooth and random.

- After the enhancement, use `NumPy random shuffle` to randomly shuffle the sequence, note that the name, sequence, and degree of affinity are shuffled together

### 4. Sequence Coding

- Perform one-hot encoding on the sequence, the fixed sequence length is 23, and the shortage is filled with 0
- Get a 3-dimensional matrix to facilitate training.**Number of Samples, Timesteps Features** 

## Determine the type of model classification

### 1. Unary Classification

- For the test group, enter a sequence to obtain an average comparison of the predicted binding affinity and the actual multiple binding affinities, if the difference is within 10%, it is correct, otherwise, it is wrong.

### 2. Binary Classification

- The predicted value is obtained through the model. If the result is greater than 0.5, it is judged as 1. If the result is less than 0.5, it is judged as 0. There is no data exactly equal to 0.5, and the obtained predicted value is compared with the actual degree of association. If it is different, it is recorded as an error

### 3. Ternary Classification

- We tried to divide the normalized affinity into three categories: high affinity after normalization of 0.6 or more; medium affinity between 0.4 and 0.6 after normalization; low affinity after normalization of less than 0.4.

- Add the threshold judgment mode: 

    - First, take the position with the highest probability of judgment
    - If it is the same as the actual result, it is directly judged to be correct
    - If it is not the same, but the predicted probability of the actual correct binding degree point is greater than the **threshold value** is also judged to be correct, Because it indicates that the predicted result is likely to occur above the threshold, the prediction is still considered to be more accurate.


## Neural Network Model


![Model summary](https://github.com/Margery0011/The-research-on-the-Triptolide-nucleic-acid-sequence-target-prediction-model-/blob/4b1a10b280a4178dcdb1a03c2108ebc2433cbf74/pics/model_summary.pic.jpg)

### 1. The First Layer

- One-dimensional convolution: 

    - with a filter (window) size of 5, used to correlate the information of the base position before and after the base position. Use this to extract the features of a small group of bases composed of a window

### 2. The Second Layer

- Bidirectional LSTM

    - LSTM inputs and processes the base set features extracted by the convolution layer in the order of the sequence and performs calculations to associate the features before and after the time series. 
    
    - LSTM introduces input gates, output gates, memory gates, and forgetting gates to associate feature points with large time gaps, so it can solve the problems of gradient disappearance and weight explosion faced by RNN. 
    
    - "Bidirectional" is used because the sequences may be related to each other, especially in RNAs of uncertain starting direction. Each loop is output to the next layer.

### 3. The Third Layer

- Unidirectional RNN

    - Which performs further calculations on the data associated with the LSTM layer. Although RNN may have problems such as gradient disappearance, LSTM is not used here and an additional layer of RNN is added because too many LSTM layers may reduce the fluctuation range of the prediction results and tend to be homogenized, that is, sequences with a large gap in combination degree. The predicted affinity may differ slightly, and such processing can improve efficiency. Only the last loop output, which is the eigenvalue of the affinity.

### 4.The Remaining Layers

- DNN:

    - DNN of the remaining layers:
        - Down-sampling the combined degree feature data extracted from the RNN, that is, the data dimension is reduced, and the ideal data dimension is sampled (Set the direct prediction value and the tertiary classification to 3). 

## Plot the ROC curve


![ROC Curve](https://github.com/Margery0011/The-research-on-the-Triptolide-nucleic-acid-sequence-target-prediction-model-/blob/main/pics/ROCCurve.jpeg)

From the characteristics of the ROC curve, it can be seen that the larger the TPR and the smaller the FPR, the better the classification result is. It is reflected in the graph that the more the ROC curve is skewed to the upper left and the more convex, the better the effect. As can be seen from the figure, the result of the ROC curve is skewed to the upper left, and the AUC (Area Under Curve) is close to 1, indicating that the prediction effect is good.

## piRNA binding affinity prediction

- The average sequence length of pirna is 28, and it is unreasonable to simply use the model trained by miRNA for prediction, **Sliding Windowing** has been performed.

### (1) Sliding Windowing

- We perform windowing on the Pirna sequence, the window length is 23, and the actual length after windowing is -23+1 sequences. Note that the same zero-padding processing for lengths less than 23.

### (2) Predict the degree of affinity for each window

- Then perform one-hot encoding on these sequences with lengths of 23 and add the previous model to predict, and obtain the binding degree of each window, [a, b, c]

### (3) Calculate the binding affinity of the whole sequence

- For each window, we compute the affinity expectation based on the probability distribution properties:
    - According to the boundary conditions, we should ensure that when the probability distribution is [0.5, 0.5, 0], the normalized affinity should be 0.6, when [0, 0.5, 0.5], the normalized affinity should be 0.4, [0,1,0] is 0.7, so it can be determined that the median value greater than 0.6 is 0.7, the median value in the middle is 0.5, and the median value is less than 0.3, so the theoretical expectation of the normalized degree of association after piecewise normalization is obtained: e = 0.7×a + 0.5×b + 0.3×c

    - The expected maximum value is 0.7 and the minimum value is 0.3, and we want to expand it from 0 to 1
    - If the expectation keeps the original value p=e between 0.4 and 0.6, if it is greater than 0.6, the range of 0.6-0.7 needs to be expanded to between 0.6-1 
    - According to the normalization principle. The formula is p= (1-0.6) (e -0.6)0.7-0.6+0.6; if it is expanded to between 0.4-0.3, the formula is p= (0.4-0)(e-0.4)0.4-0.3+0.4.

### (4) Calculate the binding degree of the whole sequence


For each window, we compute the affinity expectation based on the probability distribution properties:
According to the boundary conditions, we should ensure that when the probability distribution is [0.5, 0.5, 0], the normalized affinity should be 0.6, when [0, 0.5, 0.5], the normalized affinity should be 0.4, [0 ,1,0] is 0.7, so it can be determined
The median value greater than 0.6 is 0.7, the median value in the middle is 0.5, and the median value is less than 0.3, so the theoretical expectation of the normalized degree of affinity after piecewise normalization is obtained: e = 0.7×a + 0.5×b + 0.3×c
The expected maximum value is 0.7 and the minimum value is 0.3, and we want to expand it to 0 to 1
If the expectation keeps the original value p=e between 0.4 and 0.6, if it is greater than 0.6, the range of 0.6-0.7 needs to be expanded to between 0.6-1 according to the normalization principle. The formula is p= (1-0.6) (e -0.6)0.7-0.6+0.6; if between 0.4-0.3
The formula is p= (0.4-0)(e-0.4)0.4-0.3+0.4.



### (5) Synthesizing the expectations for each window

- Calculate the average of the normalized degree of affinity between each window e=i=0n-1pi/n, and calculate the normalized degree of affinityaccording to the maximum and minimum values ​​recorded before: p = e*(max_affinity-min_affinity ) + min_affinity. 

- At the same time, statistically speaking, the longer the sequence, the greater the probability of binding and is proportional to the length, so p = p × the length of the pirna / the length of the window 23

### (6) Verification 

- The predicted binding degree of pirna also conforms to a normal distribution, with the strongest -12 and the weakest -3
