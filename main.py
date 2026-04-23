import tkinter as tk 
from interface import InterfaceCassino

# Arquivo principal do programa
# Inicializa a aplicação gráfica do cassino

def main():
    root = tk.Tk()
    app = InterfaceCassino(root)
    root.mainloop()

if __name__ == "__main__":
    main()