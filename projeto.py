import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

def select_source_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    if source_folder:
        source_label.config(text=f"Origem: {source_folder}")

def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory()
    if destination_folder:
        destination_label.config(text=f"Destino: {destination_folder}")

def convert_files():
    if not source_folder or not destination_folder:
        messagebox.showerror("Erro", "Selecione as pastas de origem e destino!")
        return
    
    selected_format = format_var.get()
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    if not files:
        messagebox.showerror("Erro", "Nenhum arquivo encontrado na pasta de origem!")
        return
    
    try:
        progress_bar["maximum"] = len(files)
        for i, file in enumerate(files):
            file_path = os.path.join(source_folder, file)
            ext = os.path.splitext(file)[-1].lower()
            
            output_file = os.path.join(destination_folder, file.replace(ext, f".{selected_format}"))
            
            try:
                if ext == ".txt":
                    df = pd.read_csv(file_path, delimiter="\t", header=None, encoding="utf-8-sig", errors="replace")
                elif ext == ".csv":
                    df = pd.read_csv(file_path, encoding="utf-8-sig", errors="replace")
                elif ext == ".xlsx":
                    df = pd.read_excel(file_path)
                elif ext == ".json":
                    df = pd.read_json(file_path)
                else:
                    continue
            except Exception as e:
                messagebox.showwarning("Aviso", f"Erro ao ler {file}: {str(e)}")
                continue
            
            if selected_format == "csv":
                df.to_csv(output_file, index=False)
            elif selected_format == "xlsx":
                df.to_excel(output_file, index=False)
            elif selected_format == "json":
                df.to_json(output_file, orient="records")
            
            progress_bar["value"] = i + 1
            root.update_idletasks()
            
        messagebox.showinfo("Sucesso!", "Conversão concluída!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter: {str(e)}")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    
    bg_color = "#2E2E2E" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"
    btn_color = "#555" if dark_mode else "lightgray"
    
    root.config(bg=bg_color)
    source_label.config(bg=bg_color, fg=fg_color)
    destination_label.config(bg=bg_color, fg=fg_color)
    format_label.config(bg=bg_color, fg=fg_color)
    
    source_btn.config(bg=btn_color, fg=fg_color)
    destination_btn.config(bg=btn_color, fg=fg_color)
    convert_btn.config(bg=btn_color, fg=fg_color)
    theme_btn.config(bg=btn_color, fg=fg_color, text="Modo Claro" if dark_mode else "Modo Dark")

root = tk.Tk()
root.title("Conversor de Arquivos")
root.geometry("500x400")

dark_mode = False
root.config(bg="white")

source_label = tk.Label(root, text="Origem: Nenhuma pasta selecionada", wraplength=400, bg="white")
source_label.pack(pady=5)

destination_label = tk.Label(root, text="Destino: Nenhuma pasta selecionada", wraplength=400, bg="white")
destination_label.pack(pady=5)

source_btn = tk.Button(root, text="Selecionar Pasta de Origem", command=select_source_folder, bg="lightgray")
source_btn.pack(pady=5)

destination_btn = tk.Button(root, text="Selecionar Pasta de Destino", command=select_destination_folder, bg="lightgray")
destination_btn.pack(pady=5)

format_label = tk.Label(root, text="Selecionar formato de saída:", bg="white")
format_label.pack(pady=5)

format_var = tk.StringVar(value="csv")
format_dropdown = ttk.Combobox(root, textvariable=format_var, values=["csv", "xlsx", "json"])
format_dropdown.pack(pady=5)

convert_btn = tk.Button(root, text="Converter Arquivos", command=convert_files, bg="lightgray")
convert_btn.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

theme_btn = tk.Button(root, text="Modo Dark", command=toggle_theme, bg="gray")
theme_btn.pack(pady=5)

root.mainloop()
