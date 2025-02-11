import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import threading

# Inicializa a variável do caminho dos arquivos
file_paths = []
input_folder = ""
output_folder = ""

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

def select_input_folder():
    global input_folder
    input_folder = filedialog.askdirectory(title="Selecione a pasta de origem")
    
    if input_folder:
        input_label.config(text=f"Pasta de Origem: {input_folder}")
        list_files_in_folder()

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Selecione a pasta de destino")
    
    if output_folder:
        output_label.config(text=f"Pasta de Destino: {output_folder}")

def list_files_in_folder():
    global file_paths
    if input_folder:
        # Lista todos os arquivos .txt na pasta de origem
        file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".txt")]
        file_label.config(text=f"{len(file_paths)} Arquivo(s) encontrado(s)")

def convert_files():
    if not file_paths:
        messagebox.showerror("Erro", "Nenhum arquivo .txt encontrado na pasta de origem!")
        return
    if not output_folder:
        messagebox.showerror("Erro", "Selecione uma pasta de destino!")
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
            output_file = os.path.join(output_folder, os.path.basename(file_path).replace(".txt", ".csv"))
            
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
root.geometry("400x350")

style = ttk.Style()
style.theme_use("clam")

file_label = tk.Label(root, text="Nenhum arquivo selecionado", wraplength=300)
file_label.pack(pady=5)

input_label = tk.Label(root, text="Pasta de Origem: -", wraplength=300, fg="blue")
input_label.pack(pady=5)

output_label = tk.Label(root, text="Pasta de Destino: -", wraplength=300, fg="blue")
output_label.pack(pady=5)

upload_input_btn = tk.Button(root, text="Selecionar Pasta de Origem", command=select_input_folder)
upload_input_btn.pack(pady=5)

upload_output_btn = tk.Button(root, text="Selecionar Pasta de Destino", command=select_output_folder)
upload_output_btn.pack(pady=5)

convert_btn = tk.Button(root, text="Converter para CSV", command=convert_files)
convert_btn.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

theme_btn = tk.Button(root, text="Modo Dark", command=toggle_theme)
theme_btn.pack(pady=5)

root.mainloop()
