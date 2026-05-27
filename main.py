import tkinter as tk 
from interface import InterfaceCassino

# - Arquivo principal do programa
# - Responsável por iniciar a aplicação gráfica do cassino.
#   Responsabilidades:
#       - Criar a janela principal do programa
#       - Inicializar a interface gráfica
#       - Iniciar o loop principal da aplicação
#       - Servir como ponto de entrada do sistema

def main():
    root = tk.Tk()
    app = InterfaceCassino(root)
    root.mainloop()

if __name__ == "__main__":
    main()