### Arrythmia detection using machine learning

This is a machine learning project to try and detect arrythmias based off the PIB ECG database and the MIT arrythmia database. In the folder Jupyter Playground you can find the analysis of it all (it is VERY unclean, need to fix that lol).

# How does it work??

## Data extraction

First, the machine learning model was obtained by obtaining 10s samples from healthy subjects (10s after the begginging of the recording to eliminate nosie) and 10s of arrythmias detected in the MIT database.
With this method, around 90+ samples were used, both with arrythmia and healthy subjects. From each of the 10s samples the following data was obtained using the [neurokit2 library](https://neuropsychology.github.io/NeuroKit/):
- HRV_MeanNN: The mean of the RR intervals.
- HRV_SDNN: The standard deviation of the RR intervals.
- HRV_RMSSD: The square root of the mean of the squared successive differences between adjacent RR intervals. It is equivalent (although on another scale) to SD1, and therefore it is redundant to report correlations with both (Ciccone, 2017).
- HRV_SDSD: The standard deviation of the successive differences between RR intervals.
- HRV_CVNN: The standard deviation of the RR intervals (SDNN) divided by the mean of the RR intervals (MeanNN).
- HRV_CVSD: The root mean square of successive differences (RMSSD) divided by the mean of the RR intervals (MeanNN).
- HRV_MedianNN: The median of the RR intervals.
- HRV_MadNN: The median absolute deviation of the RR intervals.
- HRV_MCVNN: The median absolute deviation of the RR intervals (MadNN) divided by the median of the RR intervals (MedianNN).
- HRV_IQRNN: The interquartile range (IQR) of the RR intervals.
- HRV_Prc20NN: The 20th percentile of the RR intervals (Han, 2017; Hovsepian, 2015).
- HRV_Prc80NN: The 80th percentile of the RR intervals (Han, 2017; Hovsepian, 2015).
- HRV_pNN50: The proportion of RR intervals greater than 50ms, out of the total number of RR intervals.
- HRV_pNN20: The proportion of RR intervals greater than 20ms, out of the total number of RR intervals.
- HRV_MinNN: The minimum of the RR intervals (Parent, 2019; Subramaniam, 2022).
- HRV_MaxNN: The maximum of the RR intervals (Parent, 2019; Subramaniam, 2022).
- HRV_HTI: The HRV triangular index, measuring the total number of RR intervals divided by the height of the RR intervals histogram.
- HRV_TINN: A geometrical parameter of the HRV, or more specifically, the baseline width of the RR intervals distribution obtained by triangular interpolation, where the error of least squares determines the triangle. It is an approximation of the RR interval distribution.
- ECG_P_Peaks: count of the amount of p peaks detected.
- ECG_Q_Peaks: count of the amount of q peaks detected.
- ECG_S_Peaks: count of the amount of s peaks detected.
- ECG_T_Peaks: count of the amount of t peaks detected.
- ECG_R_Peaks: count of the amount of r peaks detected.
- mean_quality: the mean quality over the 10 seconds.
- age
- ratio p/r peaks
- ratio q/r peaks
- ratio s/r peaks
- ratio t/r peaks
- arrythmia: 1 for arrythmia, 0 for healthy *(vector to predict)*.

Due to the quality of the recording, 10s samples below 0.5 were dropped, this improved the accuracy of the model.

Note: PIB database had a 1000 Hz sampling rate whereas the MIT arrythmia database had a 360 Hz sampling rate.

## Machine learning

After successfully processing and cleaning the data, different machine learning models were tested. Including:
- Logistic Regression, score: 0.83
- Decision tree classifier, score: 0.5416
- Random forest, score: 0.625
- K-nearest neighbors, score: 0.666

Neural networks and clusters were tried but failed due to the lack of time to learn how to use them and inexperience. I believe these models and deep learning could improve the predictability.

## Analyzing ECG

To analyze an ECG from zero, the script opens the file (wheter it is a wfdb or a .csv file), divides it in 10s from 10s in to the last possible second, the data is cleaned and variables are obtained, if it is low quality it is dropped, and finally predictions are made. This working model allows us to show where the arrythmia abnormalities lie in the ECG, to help doctors better diagnose patients.

**NOTE**: This is not intended to be used for diagnosis, but rather to be a tool to aid people in the medical field.

### What's next?

- User interface.
- Clean the jupyter data.

