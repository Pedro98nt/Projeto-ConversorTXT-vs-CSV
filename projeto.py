import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_label.config(text=f"Arquivo selecionado: {os.path.basename(file_path)}")
        check_file_type()

def check_file_type():
    if file_path.endswith(".txt"):
        type_label.config(text="Tipo de arquivo: TXT", fg="green")
    else:
        type_label.config(text="Tipo de arquivo: Desconhecido", fg="red")

def convert_file():
    if not file_path or not file_path.endswith(".txt"):
        messagebox.showerror("Erro", "Selecione um arquivo TXT válido!")
        return
    
    try:
        output_file = file_path.replace(".txt", ".csv")
        df = pd.read_csv(file_path, delimiter="\t", header=None)
        df.to_csv(output_file, index=False)
        
        for i in range(101):
            progress_bar["value"] = i
            root.update_idletasks()
            root.after(10)
        
        messagebox.showinfo("Sucesso!", "Conversão concluída! 🎉")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter: {str(e)}")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode  # Alterna entre True e False

    if dark_mode:
        root.config(bg="#2E2E2E")
        file_label.config(bg="#2E2E2E", fg="white")
        type_label.config(bg="#2E2E2E", fg="lightgreen")
        upload_btn.config(bg="#555", fg="white", activebackground="#777")
        convert_btn.config(bg="#555", fg="white", activebackground="#777")
        theme_btn.config(bg="#444", fg="white", activebackground="#666", text="Modo Claro")
    else:
        root.config(bg="white")
        file_label.config(bg="white", fg="black")
        type_label.config(bg="white", fg="blue")
        upload_btn.config(bg="lightgray", fg="black", activebackground="darkgray")
        convert_btn.config(bg="lightgray", fg="black", activebackground="darkgray")
        theme_btn.config(bg="gray", fg="black", activebackground="darkgray", text="Modo Dark")

root = tk.Tk()
root.title("Conversor de TXT para CSV")
root.geometry("400x300")

# Estilo inicial
dark_mode = False  # Começa no modo claro
root.config(bg="white")

# Widgets
file_label = tk.Label(root, text="Nenhum arquivo selecionado", wraplength=300, bg="white")
file_label.pack(pady=5)

type_label = tk.Label(root, text="Tipo de arquivo: -", fg="blue", bg="white")
type_label.pack(pady=5)

upload_btn = tk.Button(root, text="Subir Arquivo", command=upload_file, bg="lightgray", fg="black")
upload_btn.pack(pady=5)

convert_btn = tk.Button(root, text="Converter para CSV", command=convert_file, bg="lightgray", fg="black")
convert_btn.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

theme_btn = tk.Button(root, text="Modo Dark", command=toggle_theme, bg="gray", fg="black")
theme_btn.pack(pady=5)

root.mainloop()
