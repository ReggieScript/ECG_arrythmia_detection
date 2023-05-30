import preparation
import analysis

def first_step(file):

    """
    With the file and frequency,returns the full_record, full_record_data, n_samples, frequency and channels
    """

    filename = file
    full_record, full_record_data, n_samples, frequency, channels = preparation.open_file(filename)

    return full_record, full_record_data, n_samples, frequency, channels

def second_step(full_record, dev, fs):

    """
    Now with the full record, deviation and frequency, the ecg, info, clean data plot and clean data for plotting is returned.
    """

    ecg, info, clean_data_plot, clean_data_for_plotting = preparation.select_dev(full_record, dev, fs)

    #Clean data plot te va a dar el heatmap bonito
    # Y el Clean_data_for_plotting son los datos para poder hacer el scrollable plot

    return ecg, info, clean_data_plot, clean_data_for_plotting

def third_step(filename, n_samples, frequency, dev):

    """
    Finally, the data is analyzed and returned
        """

    ecg_data = preparation.sampling_data(file = filename,fs=frequency, n_samples=n_samples, dev=dev)

    #Historic moment:

    ecg_df = preparation.obtaining_values(ecg_data, frequency)  ## AQUI ESTABA EL ERROR! Frequency estaba en un valor fijo de mil cuando debia ser variable!

    bad_quality, good_quality = preparation.quality(ecg_df)

    final_df = preparation.big_drop_n_order(good_quality)

    result = analysis.evaluation(final_df)

    return ecg_data, ecg_df, bad_quality, good_quality, final_df, result

# For testing

# file_test = r"G:\Shared drives\Proyecto Final\Progra\databases\MIT Arrythmia\100"

# full_record, full_record_data, n_samples, frequency, channels = first_step(file_test)

# ecg, info, clean_data_plot, clean_data_for_plotting = second_step(full_record, "MLII", 360)

# ecg_data, ecg_df, bad_quality, good_quality, final_df, result = third_step(file_test, n_samples, 360, "MLII")

# final_df["arrythmia"] = result

# final_df.to_csv("result_from_py.csv")