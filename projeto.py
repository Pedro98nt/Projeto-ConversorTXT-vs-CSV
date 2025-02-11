import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import threading

# Inicializa a variável do caminho dos arquivos
file_paths = []

# Função para tentar abrir o arquivo com diferentes codificações
def read_file_with_encoding(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']  # Lista de codificações a tentar
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                print(f"Arquivo lido com sucesso usando a codificação: {encoding}")
                return f.readlines(), encoding  # Retorna as linhas lidas e a codificação usada
        except UnicodeDecodeError as e:
            print(f"Falha ao tentar abrir com {encoding}: {e}")
            continue  # Tenta a próxima codificação
    raise ValueError("Não foi possível ler o arquivo com as codificações tentadas.")  # Se todas falharem

def upload_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])  # Permite selecionar múltiplos arquivos
    
    if file_paths:
        file_label.config(text=f"{len(file_paths)} Arquivo(s) selecionado(s)")
        check_file_type()

def check_file_type():
    if file_paths and all(file.endswith(".txt") for file in file_paths):
        type_label.config(text="Tipo de arquivo: TXT", fg="green")
    else:
        type_label.config(text="Tipo de arquivo: Desconhecido", fg="red")

def convert_files():
    if not file_paths:
        messagebox.showerror("Erro", "Selecione arquivos TXT válidos!")
        return
    
    if len(file_paths) > 100:
        messagebox.showwarning("Aviso", "Você selecionou mais de 100 arquivos. Isso pode demorar um pouco.")
    
    try:
        # Cria uma thread para executar a conversão sem travar a interface
        conversion_thread = threading.Thread(target=perform_conversion)
        conversion_thread.start()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter: {str(e)}")

def perform_conversion():
    try:
        total_files = len(file_paths)
        for index, file_path in enumerate(file_paths):
            output_file = file_path.replace(".txt", ".csv")
            
            # Tenta ler o arquivo com diferentes codificações
            lines, encoding_used = read_file_with_encoding(file_path)
            
            # Determine o delimitador com base nas linhas lidas
            first_line = lines[0]
            delimiter = "\t" if "\t" in first_line else ","
            print(f"Delimitador detectado para {file_path}: {delimiter}")
            
            # Use chunksize para lidar com grandes arquivos
            chunk_size = 10000  # Tamanho do pedaço (ajuste conforme necessário)
            chunks = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding_used, chunksize=chunk_size)

            # Cria o arquivo CSV a partir dos pedaços
            with open(output_file, 'w', encoding="utf-8", newline='') as out_file:
                for chunk in chunks:
                    chunk.to_csv(out_file, index=False, header=out_file.tell()==0)  # Adiciona cabeçalho apenas na primeira iteração

            # Atualiza o progresso geral da conversão de arquivos
            progress = (index + 1) / total_files * 100
            progress_bar["value"] = progress
            root.update_idletasks()
            root.after(5)  # Pequeno delay para melhorar a UX

        messagebox.showinfo("Sucesso!", f"Conversão concluída para todos os arquivos.")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao realizar a conversão: {str(e)}")

def toggle_theme():
    current_theme = root.tk.call("ttk::style", "theme", "use")
    
    if current_theme == "clam":
        root.tk.call("ttk::style", "theme", "use", "alt")
        root.config(bg="white")
        theme_btn.config(text="Modo Dark")
    else:
        root.tk.call("ttk::style", "theme", "use", "clam")
        root.config(bg="black")
        theme_btn.config(text="Modo Light")

# Criação da interface
root = tk.Tk()
root.title("Conversor de TXT para CSV")
root.geometry("400x300")

style = ttk.Style()
style.theme_use("clam")

file_label = tk.Label(root, text="Nenhum arquivo selecionado", wraplength=300)
file_label.pack(pady=5)

type_label = tk.Label(root, text="Tipo de arquivo: -", fg="blue")
type_label.pack(pady=5)

upload_btn = tk.Button(root, text="Subir Arquivos", command=upload_files)
upload_btn.pack(pady=5)

convert_btn = tk.Button(root, text="Converter para CSV", command=convert_files)
convert_btn.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

theme_btn = tk.Button(root, text="Modo Dark", command=toggle_theme)
theme_btn.pack(pady=5)

root.mainloop()
