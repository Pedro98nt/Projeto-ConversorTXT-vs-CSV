import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import threading

# Inicializa a variável do caminho do arquivo
file_path = None

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

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    if file_path:
        file_label.config(text=f"Arquivo selecionado: {os.path.basename(file_path)}")
        check_file_type()

def check_file_type():
    if file_path and file_path.endswith(".txt"):
        type_label.config(text="Tipo de arquivo: TXT", fg="green")
    else:
        type_label.config(text="Tipo de arquivo: Desconhecido", fg="red")

def convert_file():
    global file_path
    
    if not file_path or not file_path.endswith(".txt"):
        messagebox.showerror("Erro", "Selecione um arquivo TXT válido!")
        return
    
    try:
        output_file = file_path.replace(".txt", ".csv")
        
        # Tenta ler o arquivo com diferentes codificações
        lines, encoding_used = read_file_with_encoding(file_path)
        
        # Determine o delimitador com base nas linhas lidas
        first_line = lines[0]
        delimiter = "\t" if "\t" in first_line else ","
        print(f"Delimitador detectado: {delimiter}")
        
        # Cria uma thread para executar a conversão sem travar a interface
        conversion_thread = threading.Thread(target=perform_conversion, args=(output_file, delimiter, encoding_used))
        conversion_thread.start()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter: {str(e)}")

def perform_conversion(output_file, delimiter, encoding_used):
    try:
        print("Iniciando a conversão...")

        # Use chunksize para lidar com grandes arquivos
        chunk_size = 10000  # Tamanho do pedaço (ajuste conforme necessário)
        chunks = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding_used, chunksize=chunk_size)

        # Cria o arquivo CSV a partir dos pedaços
        with open(output_file, 'w', encoding="utf-8", newline='') as out_file:
            for chunk in chunks:
                chunk.to_csv(out_file, index=False, header=out_file.tell()==0)  # Adiciona cabeçalho apenas na primeira iteração

        # Simula o progresso da conversão
        for i in range(101):
            progress_bar["value"] = i
            root.update_idletasks()
            root.after(5)  # Pequeno delay para melhorar a UX
        
        messagebox.showinfo("Sucesso!", f"Conversão concluída!\nArquivo salvo como: {output_file}")
    
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

upload_btn = tk.Button(root, text="Subir Arquivo", command=upload_file)
upload_btn.pack(pady=5)

convert_btn = tk.Button(root, text="Converter para CSV", command=convert_file)
convert_btn.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

theme_btn = tk.Button(root, text="Modo Dark", command=toggle_theme)
theme_btn.pack(pady=5)

root.mainloop()
