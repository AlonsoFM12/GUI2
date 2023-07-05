import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import os
import pathlib
import pandas as pd
import csv
import matplotlib
matplotlib.use('TkAgg')  # Reemplaza 'TkAgg' con el backend de tu elección
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import openpyxl
import plotly.graph_objects as go
import seaborn as sns
import datetime


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Analysis tool")
        
        # Obtener el ancho y alto de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calcular la posición x e y para centrar la ventana
        x = (screen_width - 1050) // 2  # Ancho de la ventana: 1050
        y = (screen_height - 940) // 2  # Alto de la ventana: 940
        
        # Establecer la geometría de la ventana centrada
        self.window.geometry(f"1050x940+{x}+{y}")

        self.window.resizable(width=False, height=False)

       # Create Canvas
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Create Scrollbar
        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure the Canvas to be scrollable with the Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Create the Frame inside the Canvas for the content
        self.frame_canvas = tk.Frame(self.canvas)
        # Configure the Canvas to use the Frame as the scrollable region
        self.canvas.create_window((0, 0), window=self.frame_canvas, anchor=tk.NW)
        # Configure the Frame to update its size when the Canvas changes
        self.frame_canvas.bind("<Configure>", self.update_scroll_region)
        # Make frame_canvas occupy all available space
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame_canvas.pack(fill=tk.BOTH, expand=True)

        ####### GUI Widgets
        ### Folder location
        self.folder_location_w()
        ### Label with number of files
        self.number_files = tk.Label(self.frame_canvas, text='Number of files: ')
        self.number_files.pack(anchor="w", fill="x", padx=10, pady=5)
        ### Search 
        self.parameter_search()
        self.output_widgets()

        self.create_button = tk.Button(self.frame_canvas, text='Create', command=self.create_results)
        self.create_button.pack()
        


        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    ########## Widget creation ##########
    def folder_location_w(self):
        ####### GUI Widgets
        ### Folder location
        self.selected_folder = tk.StringVar()
        self.folder_location = tk.LabelFrame(self.frame_canvas, text='Folder location: ', padx=10, pady=5)
        self.folder_location.pack(anchor="w", fill="x", padx=10, pady=5)
        self.select_button = tk.Button(self.folder_location, text="Select folder", command=self.open_folder)
        self.select_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.database_button = tk.Button(self.folder_location, text="Database")
        self.database_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.address_label = tk.Label(self.folder_location, text="File address: ", padx=10, pady=5)
        self.address_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ### File filtering 
        self.filter_machine = tk.StringVar()
        self.filter_machine.set("All")
        self.filter_file = tk.StringVar()
        self.filter_file.set("All")

        self.filter_device_frame = tk.LabelFrame(self.frame_canvas, text="Machine")
        self.filter_device_frame.pack(anchor="w", fill="x", padx=10, pady=5)
        # For the case of adding new machines just add items to the list
        options_m = ["All", "MMS2", "MVS"]
        for i, option in enumerate(options_m):
            radio_button = tk.Radiobutton(self.filter_device_frame, text=option, variable=self.filter_machine, value=option, command=self.update_files)
            radio_button.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        self.filter_file_frame = tk.LabelFrame(self.frame_canvas, text="Files:")
        self.filter_file_frame.pack(anchor="w", fill="x", padx=10, pady=5)
        # For the case of adding new files just add items to the list
        options_f = ["All", "debug.wm", "status_C.txt", ".csv"]
        for i, option in enumerate(options_f):
            radio_button = tk.Radiobutton(self.filter_file_frame, text=option, variable=self.filter_file, value=option, command=self.update_files
            )
            radio_button.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        ### Listbox for file display
        #self.files_list_box = tk.Listbox(self.frame_canvas, height=15)     <--Code to configure/enable the widget "Listbox".
        #self.files_list_box.pack()                                         <--Code to configure/enable the widget "Listbox".
        #self.files_list_box.config(width=168)                              <--Code to configure/enable the widget "Listbox".

    def parameter_search(self):
        self.search_uid_entries = []
        self.search_event_entries = []
        self.parameter_search_lf = tk.LabelFrame(self.frame_canvas, text='Search: ', padx=10, pady=5)
        self.parameter_search_lf.pack(anchor="w", fill="x", padx=10, pady=5)
        self.search_label = tk.Label(self.parameter_search_lf, text='How many searches \n will be performed?')
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.search_entry = tk.Entry(self.parameter_search_lf)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.search_button = tk.Button(self.parameter_search_lf, text='Generate search boxes', command=self.search_box_generator)
        self.search_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.parameter_input = tk.LabelFrame(self.frame_canvas, text='Parameter input')
        self.parameter_input.pack(anchor="w", fill="x", padx=10, pady=5)
        
    def output_widgets(self):
        self.output = tk.StringVar()
        self.output.set(" ")
        self.output_widgets_lf = tk.LabelFrame(self.frame_canvas, text='Output')
        self.output_widgets_lf.pack(anchor="w", fill="x", padx=10, pady=5)
        self.output_num_value = ttk.Radiobutton(self.output_widgets_lf, text='Numerical value', variable=self.output, value='numerical')
        self.output_num_value.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.output_per_value = ttk.Radiobutton(self.output_widgets_lf, text='Percentage value', variable=self.output, value='percentage')
        self.output_per_value.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.output_excel = ttk.Radiobutton(self.output_widgets_lf, text='Excel Table', variable=self.output, value='excel')
        self.output_excel.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.output_graph = ttk.Radiobutton(self.output_widgets_lf, text='Graph', variable=self.output, value='graph')
        self.output_graph.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

    ########## Get files in list form ##########
    def get_files(self, directory):
        files = []
        for file_name in os.listdir(directory):
            path = os.path.join(directory, file_name)
            if os.path.isdir(path):
                # If it is a directory, it gets the files inside the directory recursively.
                files += self.get_files(path)
            else:
                # If it is a file, it adds it to the list.
                files.append(path)
        return files
    ########## Select folder ########## 
    def open_folder(self):
        folder = filedialog.askdirectory()
        self.selected_folder.set(folder)
        self.address_label.config(text=folder)
        self.files = self.get_files(folder)  # Save the result of get_files()
        self.update_files()
    ########## Filter files ##########
    def update_files(self):
        #self.files_list_box.delete(0, tk.END)          <-- These lines are in case the user wants to enable the widget "Listbox".
        files = self.files
        selected_machine = self.filter_machine.get()
        selected_file = self.filter_file.get()
        if selected_machine != "All":
            files = filter(lambda file: selected_machine in os.path.basename(file), files)
        if selected_file != "All":
            files = filter(lambda file: selected_file in os.path.basename(file), files)
        files = list(files)  # Converts the result to a list at the end
        file_count = len(files)
        self.files_filter = files   # List of files after applying filters
        self.number_files.config(text='Number of files: ' + str(file_count))
        #for file in files:                             <-- These lines are in case the user wants to enable the widget "Listbox".
            #self.files_list_box.insert(tk.END, file)   <-- These lines are in case the user wants to enable the widget "Listbox".
    
    ########## Search box generator ##########
    def search_box_generator(self):
        quantity_str = self.search_entry.get()
        if not quantity_str.isdigit():
            # Mostrar un mensaje de error o realizar una acción apropiada
            print("Invalid quantity")
            return

        quantity = int(quantity_str)
        # Eliminar los widgets existentes
        for widget in self.parameter_input.grid_slaves():
            widget.grid_remove()
            widget.destroy()

        self.uid_label = tk.Label(self.parameter_input, text='UID')
        self.uid_label.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.event_label = tk.Label(self.parameter_input, text='Event')
        self.event_label.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.instructions_label = tk.Label(self.parameter_input, text='Write the data correctly so that the generated result is the desired one.')
        self.instructions_label.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        for i in range(quantity):
            label = tk.Label(self.parameter_input, text=f"Search {i+1}:")
            label.grid(row=2+i, column=0, padx=10, pady=5, sticky="ew")
            uid_entry = tk.Entry(self.parameter_input)
            uid_entry.grid(row=2+i, column=1, padx=10, pady=5, sticky="ew")
            event_entry = tk.Entry(self.parameter_input)
            event_entry.grid(row=2+i, column=2, padx=10, pady=5, sticky="ew")

            setattr(self, f"label_{i+1}", label)
            setattr(self, f"entry_uid_{i+1}", uid_entry)
            setattr(self, f"entry_event_{i+1}", event_entry)

    ########## Output ##########
    def create_results(self):
        first_paramether = self.output.get()
        if first_paramether == "numerical":
            self.search_anomalies()
            self.numerical_value()
            self.graph_numerical()
        elif first_paramether == "percentage":
            self.search_anomalies()
            self.numerical_value()
            self.graph_percentage()
        elif first_paramether == "excel":
            self.excel_table()
        elif first_paramether == "graph":
            print ("gráfica")

    ##########  Numerical value ##########
    def search_anomalies(self):         #<--Search for a word in the whole document regardless of the column
        # Create the file "extra_information" on the desktop.
        # Obtener la fecha y hora actual
        self.current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Crear el nombre del archivo con la fecha y hora
        file_name = f"extra_information_{self.current_datetime}.txt"

        # Combinar la ruta del escritorio con el nombre del archivo
        output_file_path = fr"C:\Users\alons\Desktop\{file_name}"

        for file_path in self.files_filter:
            # Create a list to store lines with "?"
            lines_with_question_mark = []

            # Read file content using the 'latin-1' encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                lines = file.readlines()

            # Search for the "?" character in each line of the file and count the number of times.
            count = 0
            for line in lines:
                if "?" in line:
                    lines_with_question_mark.append(line)
                    count += 1

            # Type the name of the file and the number of times the word was found in the file
            if count > 0:
                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    output_file.write(f"Archivo: {file_path}\n")
                    output_file.write(f"number of matches found: {count}\n")
                    for line in lines_with_question_mark:
                        output_file.write(line)
                    output_file.write("\n" * 2)

    def numerical_value(self):          #<-- Search and creation of dataframe
        initial_columns = ['Serial Number', 'Sequences']  # Define the initial columns
        additional_columns = []  # List for storing additional columns
        data = []  # List for data storage
        search = int(self.search_entry.get())  # Gets the number of search iterations

        # Add the additional columns at the beginning of the columns
        for i in range(search):
            uid_entry = getattr(self, f"entry_uid_{i+1}").get()
            additional_columns.extend([f'{uid_entry}', f'{uid_entry}->?'])

        # Concatenate the initial and additional columns
        columns = initial_columns + additional_columns

        # Iterate over the list of files, open them in read mode with the encoding 'latin-1'.
        for file_path in self.files_filter: 
            with open(file_path, 'r', encoding='latin-1') as file: 
                lines = file.readlines()
                
                first_line = lines[0].strip()  # Get the first line that contains the SN of each file
                unique_values = set()  # Set to store the unique values which in this case are the uses (Sequence)
                
                for line in lines:
                    line_columns = line.strip().split('\t')  # Split the line into columns using tabs as the separator
                    if len(line_columns) >= 3:
                        column_3_value = line_columns[2]  # Get the value of the 3rd column
                        unique_values.add(column_3_value)  # Add the value to the unique_values set

                # Get the number of unique values
                num_unique_values = len(unique_values)  
                # Add the data from the first part of the current row to the data list
                data_row = [first_line, num_unique_values]
                
                for i in range(search):  # Iterate over different search combinations
                    combinations_count = 0  # Reset the combinations count for each iteration
                    special_cases_count = 0  # Reset the special cases count for each iteration

                    uid_entry = getattr(self, f"entry_uid_{i+1}").get()  # Get the UID entry value
                    event_entry = getattr(self, f"entry_event_{i+1}").get()  # Get the event entry value
                    parameter = uid_entry + "\t" + event_entry  # Combine the UID and event with a tab

                    # Perform the search on each line of the file
                    for line in lines:
                        if parameter in line:  # If the combination is present in the current line
                            if "?" in line:  # If there is a "?" in the same line
                                special_cases_count += 1  # Increment the special cases count
                            else:
                                combinations_count += 1  # Increment the combinations count

                    # Add the data from the current search to the current data row
                    data_row.append(combinations_count)
                    data_row.append(special_cases_count)
                
                # Add the complete data row to the data list
                data.append(data_row)

        self.df_numerical = pd.DataFrame(data, columns=columns)  # Create the dataframe with the data
        self.df_numerical.index = self.df_numerical.index + 1  # Adjust the index to start from 1
        self.df_numerical_clear = self.df_numerical.loc[(self.df_numerical.iloc[:, 2:] != 0).any(axis=1)]
        
        # Desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        output_file_name = f"dataframe_output_{self.current_datetime}.txt"
        output_file_path = os.path.join(desktop_path, output_file_name)
        self.df_numerical_clear.to_csv(output_file_path, index=False, sep='\t')

        print("Dataframe saved as a text file on the desktop.")

    def graph_numerical(self):
        x_values = self.df_numerical_clear.iloc[:, 0]  # First column as x-axis values
        x_indices = np.arange(len(x_values))
        bar_width = 0.2
        num_groups = len(self.df_numerical_clear.columns) - 1  # Number of groups (excluding the x column)

        fig, ax = plt.subplots()
        bars = []

        # Iterate over the columns (excluding the x column) and create a group of bars for each column
        for i in range(1, num_groups + 1):
            y_values = self.df_numerical_clear.iloc[:, i]  # Select the column as y-axis values
            bar_positions = x_indices + (i - 1) * bar_width  # Calculate the x-coordinate for the group
            bar = ax.bar(bar_positions, y_values, bar_width, label=self.df_numerical_clear.columns[i])
            bars.append(bar)

        ax.set_xlabel('Serial Number')
        ax.set_ylabel('Sequence')
        
        # Construct the title using the variables and current date/time
        machine = self.filter_machine.get()
        files = self.filter_file.get()
        title = f"{machine} _ {files} _ {self.current_datetime}"
        ax.set_title(title)

        ax.set_xticks(x_indices + (num_groups - 1) * bar_width / 2)
        ax.set_xticklabels(x_values, rotation=90)
        ax.legend()

        # Add labels for each bar with 90° rotation
        for bar_group in bars:
            for bar in bar_group:
                height = bar.get_height()
                ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', rotation=90)

        plt.show()

    ##########  Percentage value ##########
    def graph_percentage(self):
        x_values = self.df_numerical_clear.iloc[:, 0]  # First column as x-axis values
        x_indices = np.arange(len(x_values))
        bar_width = 0.2
        num_groups = len(self.df_numerical_clear.columns) - 1  # Number of groups (excluding the x column)

        fig, ax = plt.subplots()
        bars = []

        # Calculate the percentage in relation to the second column of each row
        reference_column = self.df_numerical_clear.iloc[:, 1]
        for i in range(1, num_groups + 1):
            y_values = self.df_numerical_clear.iloc[:, i] / reference_column * 100
            bar_positions = x_indices + (i - 1) * bar_width
            bar = ax.bar(bar_positions, y_values, bar_width, label=self.df_numerical_clear.columns[i])
            bars.append(bar)

        ax.set_xlabel('Serial Number')
        ax.set_ylabel('Percentage')

        machine = self.filter_machine.get()
        files = self.filter_file.get()
        title = f"{machine} _ {files} _ {self.current_datetime} \n"
        ax.set_title(title)

        ax.set_xticks(x_indices + (num_groups - 1) * bar_width / 2)
        ax.set_xticklabels(x_values, rotation=90)
        ax.legend()

        # Add labels for each bar
        for bar_group in bars:
            for bar in bar_group:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', rotation=90)

        plt.show()

    
    
    
    
    def start(self):
        self.window.mainloop()


app = GUI()
app.start()

