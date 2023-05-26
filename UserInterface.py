import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import pandas as pd
import main

# Create the main window
window = tk.Tk()
window.title("ECG Arrhythmia Detector V 1.0")
window.configure(bg="#87CEEB")  # Set background color to sky blue

# Add a label for the main title
title_label = tk.Label(window, text="ECG Arrythmia Detector V 1.0", font=("Roboto", 24, "bold"), fg="#000000", bg="#87CEEB", anchor="w")
title_label.pack(pady=20, padx=(10, 0), anchor="w")  # Add left margin

# Add a label for the subtitle
subtitle_label = tk.Label(window, text="Designed by Regina Crespo, Miguel Gaona, Ivan Garza and Lizeth Ramirez", font=("Roboto", 12, "italic"), fg="#000000", bg="#87CEEB", anchor="w")
subtitle_label.pack(pady=(0, 20), padx=(10, 0), anchor="w")  # Add left margin

# Variable to store the selected file path
selected_file_path = ""
def update_list(self,lista_dada):
    self['values'] = lista_dada
    
# Function to handle button click event for selecting a file
def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Select ECG File", filetypes=[("Data File", ".dat")])
    selected_file_path = selected_file_path[:-4]
    if selected_file_path:
        file_label.configure(text=f"Selected File: {selected_file_path}")
        full_record, full_record_data, n_samples, frequency, channels = main.first_step(selected_file_path)
        derivation_list = channels
        frequency_entry.delete(0, END) #deletes the current value
        frequency_entry.insert(0, frequency)
        update_list(derivation_combobox, derivation_list)
    else:
        file_label.configure(text="No file selected")

# Create a frame for the file selection section
file_frame = tk.Frame(window, bg="#87CEEB")
file_frame.pack(pady=10)

# Add a button to select a file
browse_button = tk.Button(file_frame, text="Select ECG File", command=browse_file, font=("Arial", 12), fg="#000000", bg="#FFFFFF")
browse_button.pack(padx=(10, 0))  # Add left margin

# Add a label to display the selected file
derivation_list = [0]
file_label = tk.Label(window, text="No file selected", font=("Roboto", 12), fg="#000000", bg="#87CEEB", anchor="center")
file_label.pack(pady=(5, 10), padx=(10, 0))  # Add left margin and center alignment

selected_number = tk.StringVar(window)
selected_number.set(derivation_list[0])  # Set the default selected derivation

derivation_label = tk.Label(window, text="Derivation:", font=("Arial", 12), fg="#000000", bg="#87CEEB")
derivation_label.pack(anchor="w", padx=(10, 0))  # Add left margin

derivation_combobox = ttk.Combobox(window, values=derivation_list, textvariable=selected_number, font=("Arial", 12), postcommand=update_list)
derivation_combobox.pack(anchor="w", padx=(10, 0))  # Add left margin
    
# Add a drop-down list (combobox) to select a derivation

# Add a field to insert the frequency
frequency_label = tk.Label(window, text="Frequency:", font=("Arial", 12), fg="#000000", bg="#87CEEB")
frequency_label.pack(anchor="w", padx=(10, 0))  # Add left margin

frequency_entry = tk.Entry(window, font=("Arial", 12))
frequency_entry.pack(anchor="w", padx=(10, 0))  # Add left margin

# Add a small blank space
blank_space_label = tk.Label(window, text="", font=("Arial", 6), bg="#87CEEB")
blank_space_label.pack()

# Function to handle button click event for initiating the ECG analysis process
def initiate_process():
    if str(selected_number.get()) != '0':
        if selected_file_path:
            # Add your code
            full_record, full_record_data, n_samples, frequency, channels = main.first_step(selected_file_path)
            selected_frequency = frequency_entry.get()
            selected_derivation = selected_number.get()
            
            # Sample data for abnormalities count, bad quality moments count, and heat map result
            ecg, info, clean_data_plot, clean_data_for_plotting = main.second_step(full_record,selected_derivation,frequency)

            image_path = "myfig.png"
            heat_map = Image.open(image_path)
            tk_image = ImageTk.PhotoImage(heat_map)
            image_label = tk.Label(window, image=tk_image)
            
            df = pd.DataFrame(clean_data_for_plotting)
            df['X'] = range(len(df))
            df['X']=df['X']/frequency
            df.columns = ['Y','X']
            fig = plt.figure(figsize=(6, 4), dpi=80)
            plt.plot(df['X'], df['Y'])
            plt.xlabel('Time(s)')
            plt.ylabel('Amplitude')
            plt.title('DataFrame Plot')
            
            plt.show()
            
            ecg_data, ecg_df, bad_quality, good_quality, final_df, result = main.third_step(selected_file_path, n_samples, frequency, selected_derivation)
            abnormalities_text.configure(text=f"Abnormalities found: {len(result)}")
            bad_quality_text.configure(text=f"Bad quality segments: {len(bad_quality)}")

            # Display a message box with the analysis results
        else:
            messagebox.showwarning("File Not Selected", "Please select an ECG file.")
    else:
        messagebox.showwarning("Derivation not selected", "Please select a derivation.")
# Add a button to initiate the ECG analysis process
initiate_button = tk.Button(window, text="Run!", command=initiate_process, font=("Arial", 14, "bold"), fg="#000000", bg="#FFFFFF")
initiate_button.pack(anchor="w", padx=(10, 0), pady=(20, 0))  # Add left margin

# Add a section to display the result
result_label = tk.Label(window, text="Result:", font=("Arial", 16, "bold"), fg="#000000", bg="#87CEEB")
result_label.pack(side=tk.RIGHT)

# Add a label for the abnormalities count
abnormalities_text = tk.Label(window, text="", font=("Roboto", 14), fg="#000000", bg="#87CEEB")
abnormalities_text.pack(side=tk.RIGHT, padx=10)

# Add a label for the bad quality moments count
bad_quality_text = tk.Label(window, text="", font=("Roboto", 14), fg="#000000", bg="#87CEEB")
bad_quality_text.pack(side=tk.RIGHT, padx=10)

# Add a label for the heat map result
heat_map_label = tk.Label(window, text="Heat Map:", font=("Roboto", 12), fg="#000000", bg="#87CEEB")
heat_map_label.pack(anchor="w", padx=(10, 0))  # Add left margin

# Add a label to display the heat map result
heat_map_text = tk.Label(window, text="", font=("Roboto", 12), fg="#000000", bg="#87CEEB")
heat_map_text.pack(anchor="w", padx=(10, 0))  # Add left margin

# Start the main loop
window.mainloop()