import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import fitz
import re
from elicpdf import listelic,csvlic
def ajoute_message(message):
        text_area.insert(tk.END, f"{message}")
        text_area.see(tk.END)
        root.update()

def process_pdf(input_file, output_file,massicot=0,workdir=""):
    if var_mode.get() == "CSV":
       ajoute_message(f"traite le fichier {input_file} et génère le fichier {output_file} avec les licences dans {workdir} massicot={massicot}\n")
       csvlic(output_file,input_file,workdir=workdir,massicot=massicot,dconsole=ajoute_message)
    else:
       ajoute_message(f"traite les fichier {input_file} et génère le fichier {output_file} avec massicot={massicot}\n")
       ajoute_message(":".join(input_file.split(',')))
       listelic(output_file,input_file.split(','),massicot=massicot,dconsole=ajoute_message)
    ajoute_message("c'est fait\n")
def select_input_file():
    if var_mode.get() == "CSV":
       input_file = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
    else: 
       input_file = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
       input_file=",".join(list(input_file))
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
    result_label.config(text="Licence(s) reduite et sauvegardée avec succès.")

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

default_font.config(size=12)
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
input_file_entry = tk.Entry(frame2,justify="right")
input_file_entry.pack()

input_dir_button = tk.Button(frame2, text="Sélectionner repertoire d entrée:", command=select_workdir)
#input_dir_button.pack()
input_dir_entry = tk.Entry(frame2,justify="right")
#input_dir_entry.pack()

#output_file_label = tk.Label(frame3, text="Fichier licence de sortie:")
#output_file_label.pack()
output_file_button = tk.Button(frame3, text="Sélectionner le fichier de sortie", command=select_output_file)
output_file_button.pack()
output_file_entry = tk.Entry(frame3,justify="right")
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

text_area=tk.Text(frame5,height=5,width=80)
text_area.configure(font=("TkDefaultFont", 7))
text_area.pack()

root.mainloop()

