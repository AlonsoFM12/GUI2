import tkinter as tk
from tkinter import ttk
import pandas as pd



tables_window = tk.Tk()
tables_window.geometry("500x400")

def save_selection():
    V1 = parameter1.get()
    V2 = parameter2.get()
    V3 = parameter3.get()
    V4 = parameter4.get()
    V5 = parameter5.get()

    data = {
         V1 : [],
         V2 : [],
         V3 : [],
         V4 : [],
         V5 : []
    }

    df = pd.DataFrame(data)

    # Crear un archivo de Excel
    writer = pd.ExcelWriter('tabla_ejemplo.xlsx', engine='xlsxwriter')

    # Convertir el dataframe a una hoja de Excel
    df.to_excel(writer, sheet_name='Hoja1', index=False)

    # Cerrar el archivo de Excel
    writer.save()

    print(V1, V2, V3, V4, V5)
    

label = tk.Label(tables_window, text = "Select the table headers", font=("consolas", 15, "bold"), width=25, height=3)
label.pack()


selection_box = tk.LabelFrame(tables_window,text= "Selection box", font=("consolas", 10, ""))

option1 = ["Senal number", "Sequence", "Date", "Time", "UID", "Description"] 
option2 = ["Event", "Error", "Alarm"]

label2 = tk.Label(selection_box, text = "First Parameter", width = 20, height = 1, anchor = "w")
label2.pack()
parameter1 = ttk.Combobox(selection_box, values = option1, state = "readonly")
parameter1.pack()

label3 = tk.Label(selection_box, text = "Second Parameter", width = 20, height = 1, anchor = "w")
label3.pack()
parameter2 = ttk.Combobox(selection_box, values = option1, state = "readonly") 
parameter2.pack() 

label4 = tk.Label(selection_box, text = "Third Parameter", width = 20, height = 1, anchor = "w")
label4.pack()
parameter3 = ttk.Combobox(selection_box, values = option1, state = "readonly") 
parameter3.pack() 

label5 = tk.Label(selection_box, text = "Fourth Parameter", width = 20, height = 1, anchor = "w")
label5.pack()
parameter4 = ttk.Combobox(selection_box, values = option1, state = "readonly") 
parameter4.pack() 

label6 = tk.Label(selection_box, text = "Fifth Parameter", width = 20, height = 1, anchor = "w")
label6.pack()
parameter5 = ttk.Combobox(selection_box, values = option2, state = "readonly") 
parameter5.pack() 

selection_box.pack()

separator1 = tk.Label(tables_window)
separator1.pack()

select = tk.Button(tables_window, text = "Select", anchor="e", command=save_selection)
select.pack()

tables_window.mainloop()



