import tkinter as tk
from tkinter import Tk, Button, Toplevel, Label
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import matplotlib.dates as mdates
import datetime as dt
import pandas as pd
import matplotlib.patches as patches
import main
import classes

# Create the main window
window = tk.Tk()
window.title("ECG Arrhythmia Detector V 1.0")
window.configure(bg="#87CEEB")  # Set background color to sky blue #87CEEB

# Add a label for the main title
# Create a custom title bar using the ttk module
title_bar = tk.Canvas(window, height=30, bg="#87CEEB", highlightthickness=0)  # Set the desired background color
title_bar.pack(fill="x")

original_image = Image.open("Visuals/logo.png")

# Resize the image
width, height = 170, 170  # Set the desired width and height
resized_image = original_image.resize((width, height), Image.ANTIALIAS)
# Load the image for the title
title_image = ImageTk.PhotoImage(resized_image)

# Create a label widget to display the image
title_label = ttk.Label(title_bar, image=title_image, background="#87CEEB")
title_label.pack(side="left",  padx=400, pady=0)
  # Add left margin

# Add a label for the subtitle
subtitle_label = tk.Label(window, text="Designed by Regina Crespo, Miguel Gaona, Ivan Garza and Lizeth Ramirez", font=("Roboto", 12, "italic"), fg="#212431", bg="#87CEEB", anchor="w")
subtitle_label.pack(pady=(0, 20), padx=(10, 0), anchor="center")  # Add left margin

# Variable to store the selected file path
selected_file_path = ""
    
def update_list(self,lista_dada):
    self['values'] = lista_dada
    selected_number.set(lista_dada[0])
    
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
file_btn = PhotoImage(file = r"Visuals/button_select-ecg-file.png")

browse_button = tk.Button(file_frame, image= file_btn, command=browse_file, font=("Arial", 12), bg="#87CEEB", highlightthickness=0, bd =0, border=0, borderwidth=0)
browse_button.pack(padx=(10, 0))  # Add left margin

# Add a label to display the selected file
derivation_list = [0]
file_label = tk.Label(window, text="No file selected", font=("Roboto", 12), fg="#212431", bg="#87CEEB", anchor="center")
file_label.pack(pady=(5, 10), padx=(10, 0))  # Add left margin and center alignment

selected_number = tk.StringVar(window)
selected_number.set(derivation_list[0])  # Set the default selected derivation

derivation_label = tk.Label(window, text="Derivation:", font=("Arial", 12), fg="#212431", bg="#87CEEB")
derivation_label.pack(anchor="w", padx=(10, 0))  # Add left margin

derivation_combobox = ttk.Combobox(window, values=derivation_list, textvariable=selected_number, font=("Arial", 12), postcommand=update_list)
derivation_combobox.pack(anchor="w", padx=(10, 0))  # Add left margin
    
# Add a drop-down list (combobox) to select a derivation

# Add a field to insert the frequency
frequency_label = tk.Label(window, text="Frequency:", font=("Arial", 12), fg="#212431", bg="#87CEEB")
frequency_label.pack(anchor="w", padx=(10, 0))  # Add left margin

frequency_entry = tk.Entry(window, font=("Arial", 12))
frequency_entry.pack(anchor="w", padx=(10, 0))  # Add left margin

# Add a small blank space
blank_space_label = tk.Label(window, text="", font=("Arial", 6), bg="#87CEEB")
blank_space_label.pack()

# Function to handle button click event for initiating the ECG analysis process
def initiate_process():
    global window
    if str(selected_number.get()) != '0':
        if selected_file_path:
            # Add your code
            full_record, full_record_data, n_samples, frequency, channels = main.first_step(selected_file_path)
            selected_frequency = int(frequency_entry.get())
            selected_derivation = selected_number.get()
            # Sample data for abnormalities count, bad quality moments count, and heat map result
            ecg, info, clean_data_plot, clean_data_for_plotting = main.second_step(full_record,selected_derivation,selected_frequency)
            ecg_data, ecg_df, bad_quality, good_quality, final_df, result = main.third_step(selected_file_path, n_samples, selected_frequency, selected_derivation)
            abnormalities_text.configure(text=f"Abnormalities found: {result.count(1)}")
            bad_quality_text.configure(text=f"Bad quality segments: {len(bad_quality)}")
            bad_quality_times = bad_quality.index.tolist()

            bad_quality_times_splitted_low = []
            bad_quality_times_splitted_high = []
            good_quality_times_splitted_low = []
            good_quality_times_splitted_high = []

            result_dataframe = pd.DataFrame({'Times': final_df.index.tolist(), 'Prediction': result})
            result_dataframe = result_dataframe[result_dataframe['Prediction']==1]

            good_quality_times = result_dataframe['Times'].values.tolist()
            if good_quality_times:
                for item in good_quality_times:
                    lower, upper = item.split('-')
                    good_quality_times_splitted_low.append(int(lower))
                    good_quality_times_splitted_high.append(int(upper))
            
            if bad_quality_times:
                for item in bad_quality_times:
                    lower, upper = item.split('-')
                    bad_quality_times_splitted_low.append(int(lower))
                    bad_quality_times_splitted_high.append(int(upper))
            global window
            window.update()
            print(bad_quality_times_splitted_low)
            print(bad_quality_times_splitted_high)
            df = pd.DataFrame(clean_data_for_plotting)
            df['X'] = range(len(df))
            df['X']=df['X']/selected_frequency
            df.columns = ['Y','X']
            fig_graph = plt.figure(num="Full Patient ECG Data")
            ax_graph = fig_graph.add_subplot(111)
            ax_graph.plot(df['X'], df['Y'])
            ax_graph.set_xlabel("Time(s)")
            ax_graph.set_ylabel("Amplitude(mV)")
            ax_graph.set_title("Full Patient ECG Data with bad segments and possible arrhythmias")
            # ax_graph.set_xlim(xmin=0)
            
            if bad_quality_times:

                for i in range(0,len(bad_quality_times)):
                    highlight_start = bad_quality_times_splitted_low[i]/frequency
                    highlight_end = bad_quality_times_splitted_high[i]/frequency
                    ax_graph.axvspan(highlight_start, highlight_end, facecolor='yellow', alpha=0.2, edgecolor='black')

            if good_quality_times:
                
                for i in range(0,len(good_quality_times)):
                    highlight_start = good_quality_times_splitted_low[i]/frequency
                    highlight_end = good_quality_times_splitted_high[i]/frequency
                    ax_graph.axvspan(highlight_start, highlight_end, facecolor='red', alpha=0.5, edgecolor='black')

            image = Image.open("myfig.png")
            image.show(title='Full HeatMap of the Patient')
            legend_entries = [
                patches.Patch(facecolor='red', alpha=0.5, label='Possible Arrhythmia'),
                patches.Patch(facecolor='yellow', alpha=0.2, label='Bad Quality Segment')
            ]
            ax_graph.legend(handles=legend_entries, loc='upper right')
            a = classes.ScrollableWindow(fig_graph,ax_graph)

            # messagebox.showinfo(title = "RESULTS", message = f"Abnormalities found: {result.count(1)} \n Bad quality segments: {len(bad_quality)}")
            # Display a message box with the analysis results
        else:
            messagebox.showwarning("File Not Selected", "Please select an ECG file.")
    else:
        messagebox.showwarning("Derivation not selected", "Please select a derivation.")
# Add a button to initiate the ECG analysis process

run_btn = PhotoImage(file = r"Visuals/button_run.png")
initiate_button = tk.Button(window, image = run_btn, command=initiate_process, highlightthickness=0, bd = 0, border= 0, bg = "#87CEEB")
initiate_button.pack(anchor="w", padx=(10, 0), pady=(20, 0))  # Add left margin

def display_instructions():
    # Create a new window
    instructions_window = Toplevel(window)

    # Set the title of the new window
    instructions_window.title("How To Use")
    instructions_window.geometry('440x230')
    canvas = tk.Canvas(instructions_window, bg="#87CEEB")  # Set the desired background color
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create a label with the instructions text
    instructions_text = tk.Text(canvas, width=50,background="#87CEEB", highlightthickness=0, border=0,borderwidth=0)  # Set the width to the desired value
    instructions = """
Instructions of use\n\n1.Click the Select ECG file and select the .dat file.\n2.Select the derivation you want to observe (Results tend to be more visible in 2nd derivation).\n3.You can use the predetermined frequency or change it at will.\n4.Click the 'Run!' Button.\n5. Show the results to a healthcare professional.
    """
    instructions_text.insert(tk.END, instructions)
    instructions_text.configure(font=("Roboto", 13))
    instructions_text.pack(padx=10, pady=10)

    
instr_button = PhotoImage(file = r"Visuals\button_instructions.png")
instructions_btn = Button(window, image=instr_button, text="Instructions", command=display_instructions, highlightthickness=0, bd = 0, border= 0, bg = "#87CEEB")
instructions_btn.pack(padx=10,pady=10, anchor='w')

# Add a label for the abnormalities count
abnormalities_text = tk.Label(window, text="", font=("Roboto", 14), fg="#212431", bg="#87CEEB")
abnormalities_text.pack(side=tk.RIGHT, padx=10)

# Add a label for the bad quality moments count
bad_quality_text = tk.Label(window, text="", font=("Roboto", 14), fg="#212431", bg="#87CEEB")
bad_quality_text.pack(side=tk.RIGHT, padx=10)

# Start the main loop
window.mainloop()