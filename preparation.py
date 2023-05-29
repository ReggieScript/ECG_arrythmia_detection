## First step, import libraries

import pandas as pd
import neurokit2 as nk
import wfdb #library for reading ecg data https://github.com/MIT-LCP/wfdb-python/blob/main/demo.ipynb
import matplotlib.pyplot as plt
from PIL import Image


def open_file(file):

    """
    Opens the ECG file depending on its type (WFDB or CSV), returns ecg, info, clean_data_plot, full_record, n_samples
    """
    #Note to self: adaptarlo a ambos archivos, arrythmia y de 

    full_record = record = wfdb.rdrecord(file)
    full_record_data = full_record.__dict__
    n_samples = full_record_data['sig_len']
    try:
        frequency = full_record_data["fs"]
    except:
        frequency = 0
    channels = full_record_data["sig_name"]
    
    return full_record, full_record_data, n_samples, frequency, channels

    ## Notes for future: channels can be used for selection of which one, frequency as well.

def select_dev(full_record, dev, fs):

    """
    Now with the dev, it obtains the data from the channel
        """
    try:
         ecg,  info = nk.ecg_process(full_record.to_dataframe()[ dev], sampling_rate =  fs)
    except:
        print("error in the deviation")
        
    clean_data_plot = nk.ecg_plot(ecg, sampling_rate= fs)
    fig = plt.gcf()
    fig.canvas.manager.set_window_title("Patient Full Heat Map")
    fig.savefig("myfig.png")
    clean_data_for_plotting = ecg["ECG_Clean"]
    
    return ecg, info, clean_data_plot, clean_data_for_plotting

def sampling_data(file,fs, n_samples, dev):

    """
    samples in 10s windows all the data contained in the ECG and stores them in a dictionary, returns that same dictionary
    """

    baseline_data =  file

    time = 10
    sample_from = time* fs
    sample_to = 20* fs
    
    #Datos con arrythmia
    data = {
        
    }

    x= True
    while x == True:
        if (time+10)*fs > n_samples*fs:
            print("hey!")
            x = False
        try:
            sample_from = time * fs
            sample_to = (time+10)*fs # 10s de sampleo
            data[f"{sample_from}-{sample_to}"] = {}
            data[f"{sample_from}-{sample_to}"][f"raw_data"] = record = wfdb.rdrecord(baseline_data, sampfrom = sample_from, sampto = sample_to)
        except:
            data.pop(f"{sample_from}-{sample_to}") 
        try:
            data[f"{sample_from}-{sample_to}"]["ecg_signals"], data[f"{sample_from}-{sample_to}"]["info"] = nk.ecg_process(data[f"{sample_from}-{sample_to}"]["raw_data"].to_dataframe()[dev], sampling_rate=fs) 
        except:
            pass #include something to notify that It couldn't be read
        time+=10
    
    return data

def obtaining_values(ecg_data, fs):
    """
    Obtains important data for each of the 10s samples, returns a dataframe containing it all.
    """

    data = ecg_data

    for item in data:
        for feature in data[item]['ecg_signals']:
            data[item][feature]=data[item]['ecg_signals'][feature]
    
    ecg_signal_data = ['ECG_P_Peaks', 'ECG_Q_Peaks', 'ECG_S_Peaks', 'ECG_T_Peaks', 'ECG_R_Peaks']

    for item in data:
        peaks, info = nk.ecg_peaks(data[item]["ecg_signals"]["ECG_Clean"], sampling_rate=fs)
        data[item]["hrv_time"] = nk.hrv_time(peaks, sampling_rate=fs, show=False)
        for var in data[item]["hrv_time"]:
            data[item][var] = data[item]["hrv_time"][var].to_frame().iloc[0][var]
        for feature in ecg_signal_data:
            data[item][feature] = data[item]["ecg_signals"][feature].sum()
        data[item]["mean_quality"]  = data[item]["ecg_signals"]["ECG_Quality"].mean()

    data_df = pd.DataFrame.from_dict(data, orient = 'index')


    data_df["ratio p/r peaks"] = data_df["ECG_P_Peaks"].div(data_df["ECG_R_Peaks"])
    data_df["ratio q/r peaks"] = data_df["ECG_Q_Peaks"].div(data_df["ECG_R_Peaks"])
    data_df["ratio s/r peaks"] = data_df["ECG_S_Peaks"].div(data_df["ECG_R_Peaks"])
    data_df["ratio t/r peaks"] = data_df["ECG_T_Peaks"].div(data_df["ECG_R_Peaks"])

    return data_df

def quality(ecg_data):

    """
    looks for good and bad quality samples, returns a bad quality and a good quality dataframe
    """

    bad_quality = ecg_data[ecg_data["mean_quality"]<0.5]
    good_quality = ecg_data[ecg_data["mean_quality"]>0.5]

    return bad_quality, good_quality

def big_drop_n_order(ecg_data):

    """
    checks for the data that should be in the dataframe and orders it accordingly to fit the model, returns final dataframe
    """

    drop_list=['HRV_MeanNN', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVNN',
       'HRV_CVSD', 'HRV_MedianNN', 'HRV_MadNN', 'HRV_MCVNN', 'HRV_IQRNN',
       'HRV_Prc20NN', 'HRV_Prc80NN', 'HRV_pNN50', 'HRV_pNN20', 'HRV_MinNN',
       'HRV_MaxNN', 'HRV_HTI', 'HRV_TINN', 'ECG_P_Peaks', 'ECG_Q_Peaks',
       'ECG_S_Peaks', 'ECG_T_Peaks', 'ECG_R_Peaks',
       'ratio p/r peaks', 'ratio q/r peaks', 'ratio s/r peaks',
       'ratio t/r peaks']
    
    new_ecg_data = ecg_data
    final_df = pd.DataFrame()
    for item in drop_list:
        final_df[item] = new_ecg_data[item]

    return final_df
