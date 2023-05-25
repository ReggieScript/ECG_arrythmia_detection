import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import main

# Create the main window
window = tk.Tk()
window.title("ECG Arrhythmia Detector V 1.0")
window.configure(bg="#87CEEB")  # Set background color to sky blue

# Add a label for the main title
title_label = tk.Label(window, text="ECG Arrhythmia Detector V 1.0", font=("Roboto", 24, "bold"), fg="#000000", bg="#87CEEB", anchor="w")
title_label.pack(pady=20, padx=(10, 0), anchor="w")  # Add left margin

# Add a label for the subtitle
subtitle_label = tk.Label(window, text="Designed by Regina Crespo, Miguel Gaona, Ivan Garza and Lizeth Ramirez", font=("Roboto", 12, "italic"), fg="#000000", bg="#87CEEB", anchor="w")
subtitle_label.pack(pady=(0, 20), padx=(10, 0), anchor="w")  # Add left margin

# Variable to store the selected file path
selected_file_path = ""

# Function to handle button click event for selecting a file
def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Select ECG File", filetypes=[("Data File", ".dat")])
    selected_file_path = selected_file_path[:-4]
    if selected_file_path:
        file_label.configure(text=f"Selected File: {selected_file_path}")
    else:
        file_label.configure(text="No file selected")

# Create a frame for the file selection section
file_frame = tk.Frame(window, bg="#87CEEB")
file_frame.pack(pady=10)

# Add a button to select a file
browse_button = tk.Button(file_frame, text="Select ECG File", command=browse_file, font=("Arial", 12), fg="#000000", bg="#FFFFFF")
browse_button.pack(padx=(10, 0))  # Add left margin

# Add a label to display the selected file
file_label = tk.Label(window, text="No file selected", font=("Roboto", 12), fg="#000000", bg="#87CEEB", anchor="center")
file_label.pack(pady=(5, 10), padx=(10, 0))  # Add left margin and center alignment

# Add a drop-down list (combobox) to select a derivation

selected_number = tk.StringVar(window)
selected_number.set(derivation_list[0])  # Set the default selected derivation

derivation_label = tk.Label(window, text="Derivation:", font=("Arial", 12), fg="#000000", bg="#87CEEB")
derivation_label.pack(anchor="w", padx=(10, 0))  # Add left margin

derivation_combobox = ttk.Combobox(window, values=derivation_list, textvariable=selected_number, font=("Arial", 12))
derivation_combobox.pack(anchor="w", padx=(10, 0))  # Add left margin

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
    if selected_file_path:
        selected_frequency = frequency_entry.get()
        selected_derivation = selected_number.get()

        # Add your code
        full_record, full_record_data, n_samples, frequency, channels = main.first_step(selected_file_path, frequency_entry.get())
        derivation_list = channels
        # Sample data for abnormalities count, bad quality moments count, and heat map result
        abnormalities_count = 5
        bad_quality_count = 2
        heat_map_result = "Sample Heat Map"

        abnormalities_text.configure(text=f"Abnormalities found: {abnormalities_count}")
        bad_quality_text.configure(text=f"Bad quality moments: {bad_quality_count}")
        heat_map_text.configure(text=f"Heat Map: {heat_map_result}")

        # Display a message box with the analysis results
        message = f"ECG analysis process initiated\n\nSelected file path: {selected_file_path}\nSelected frequency: {selected_frequency}\nSelected derivation: {selected_derivation}\n\nAbnormalities found: {abnormalities_count}\nBad quality moments: {bad_quality_count}\nHeat Map: {heat_map_result}"
        messagebox.showinfo("Analysis Results", message)
    else:
        messagebox.showwarning("File Not Selected", "Please select an ECG file.")

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