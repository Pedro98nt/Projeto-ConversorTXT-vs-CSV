from cx_Freeze import setup, Executable

# Informações do executável
setup(
    name="ProjetoTXT",
    version="1.0",
    description="Conversor de TXT para CSV",
    executables=[Executable("projeto.py", base="Win32GUI", icon="icone.ico")]
)
