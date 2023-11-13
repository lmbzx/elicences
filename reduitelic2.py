import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import fitz
from elicpdf import listelic,csvlic
def process_pdf(input_file, output_file,massicot=0,workdir=""):
    if var_mode.get() == "CSV":
       csvlic(output_file,input_file,workdir=workdir,massicot=massicot)
    else:
       listelic(output_file,input_file.split(),massicot=massicot)

def select_input_file():
    if var_mode.get() == "CSV":
       input_file = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
    else: 
       input_file = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)

def select_csv_file():
    input_file = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)

def select_workdir():
    input_dir = filedialog.askdirectory(title="Sélectionner un répertoire")
    input_dir_entry.delete(0, tk.END)
    input_dir_entry.insert(0, input_dir)

def select_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, output_file)

def process_and_save():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    process_pdf(input_file, output_file,workdir=input_dir_entry.get(),massicot=var_massicot.get())
    result_label.config(text="Licence reduite et sauvegardée avec succès.")

def quit():
    root.destroy()

def on_mode_change():
    
    if var_mode.get() == "CSV":
      #input_dir_entry.config(show="*") 
      input_dir_button.pack()
      input_dir_entry.pack()
      #input_dir_button.pack_forget()
      #input_file_label.config(text="Fichier CSV:")
      input_file_button.config(text="Selectionne un fichier CSV:")
    else:
      input_dir_entry.pack_forget()
      #input_dir_button.config(state="disabled")
      input_dir_button.pack_forget()
      #input_dir_button.pack()
      #input_file_label.config(text="Fichier licences:")
      input_file_button.config(text="Selectionne des fichiers licences:")

    result_label.config(text=var_mode.get())

# Créez la fenêtre principale
root = tk.Tk()
default_font = tkFont.nametofont("TkDefaultFont")

default_font.config(size=16)
root.option_add("*Font", default_font)


root.title("Reduit elicence PDF")

# Ajoutez des éléments d'interface utilisateur pour sélectionner les fichiers d'entrée et de sortie
frame1 = tk.Frame(root)
frame1.pack()

frame2 = tk.Frame(root)
frame2.pack()

frame3 = tk.Frame(root)
frame3.pack()

frame4 = tk.Frame(root)
frame4.pack()

frame5 = tk.Frame(root)
frame5.pack()

var_mode = tk.StringVar(value="list")  # Valeur par défaut pour "Liste de fichiers"
radio_list = tk.Radiobutton(frame1, text="liste de PDF", variable=var_mode, value="list", command=on_mode_change)
radio_csv = tk.Radiobutton(frame1, text="CSV", variable=var_mode, value="CSV", command=on_mode_change)
radio_list.grid(row=0,column=0)
radio_csv.grid(row=0,column=1)

#input_file_label = tk.Label(frame2, text="Fichiers licence d'entrée:")
#input_file_label.pack()
input_file_button = tk.Button(frame2, text="Sélectionner les fichier d'entrée", command=select_input_file)
input_file_button.pack()
input_file_entry = tk.Entry(frame2)
input_file_entry.pack()

input_dir_button = tk.Button(frame2, text="Sélectionner repertoire d entrée:", command=select_workdir)
#input_dir_button.pack()
input_dir_entry = tk.Entry(frame2)
#input_dir_entry.pack()

#output_file_label = tk.Label(frame3, text="Fichier licence de sortie:")
#output_file_label.pack()
output_file_button = tk.Button(frame3, text="Sélectionner le fichier de sortie", command=select_output_file)
output_file_button.pack()
output_file_entry = tk.Entry(frame3)
output_file_entry.pack()

process_button = tk.Button(frame4, text="Reduit et sauvegarde", command=process_and_save)
process_button.grid(row=0,column=0)

var_massicot= tk.BooleanVar()
toggle_massicot = tk.Checkbutton(frame4, text="massicot", variable=var_massicot)
toggle_massicot.grid(row=0, column=1)

#process_button.pack()

quit_button = tk.Button(frame5, text="Sortie", command=quit)
quit_button.pack()

result_label = tk.Label(frame5, text="")
result_label.pack()

root.mainloop()

