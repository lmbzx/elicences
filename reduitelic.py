import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import fitz
from elicpdf import listelic
def process_pdf(input_file, output_file):
    listelic(output_file,input_file.split())

def select_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)

def select_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, output_file)

def process_and_save():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    process_pdf(input_file, output_file)
    result_label.config(text="Fichier traité et sauvegardé avec succès.")

def quit():
    root.destroy()

# Créez la fenêtre principale
root = tk.Tk()
default_font = tkFont.nametofont("TkDefaultFont")

default_font.configure(size=16)
root.option_add("*Font", default_font)


root.title("Traitement PDF")

# Ajoutez des éléments d'interface utilisateur pour sélectionner les fichiers d'entrée et de sortie
input_file_label = tk.Label(root, text="Fichier d'entrée:")
input_file_label.pack()
input_file_entry = tk.Entry(root)
input_file_entry.pack()
input_file_button = tk.Button(root, text="Sélectionner le fichier d'entrée", command=select_input_file)
input_file_button.pack()

output_file_label = tk.Label(root, text="Fichier de sortie:")
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()
output_file_button = tk.Button(root, text="Sélectionner le fichier de sortie", command=select_output_file)
output_file_button.pack()

process_button = tk.Button(root, text="Traitement PDF et sauvegarde", command=process_and_save)
process_button.pack()

quit_button = tk.Button(root, text="Sortie", command=quit)
quit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

