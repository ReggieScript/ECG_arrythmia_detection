import preparation
import analysis

filename = "databases\Healthy\Patient 243\s0472_re"

ecg, info, clean_data_plot, full_record, n_samples, channels = preparation.open_file(filename, "ii",1000,"WFDB")

print(channels, n_samples)

ecg_data = preparation.sampling_data(file = filename,fs=1000, n_samples=n_samples, dev="ii")

ecg_df = preparation.obtaining_values(ecg_data,1000)

clean_data_plot

bad_quality, good_quality = preparation.quality(ecg_df)

final_df = preparation.big_drop_n_order(good_quality)

print(final_df.columns)

result = analysis.evaluation(final_df)

print(result)