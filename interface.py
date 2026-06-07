import tkinter as tk
import random
import winsound
from tkinter import messagebox
from banco_dados import salvar_jogador, carregar_jogador
from jogador import Jogador
from jogos.roleta import Roleta
from jogos.caca_niquel import CacaNiquel
from jogos.copa_brasil import CopaDoBrasil
from jogos.bozo import Bozo

# - Classe InterfaceCassino
#   Responsável por construir e controlar toda a interface gráfica do cassino.
#   Responsabilidades:
#       - Criar as telas do sistema usando Tkinter
#       - Exibir informações do jogador, como nome, saldo e histórico
#       - Integrar a interface com os jogos do cassino
#       - Controlar a navegação entre menus, jogos, carteira e histórico
#       - Tratar entradas do usuário e exibir mensagens de erro ou sucesso
#       - Atualizar visualmente saldo, resultados e informações das partidas

class InterfaceCassino:
    def __init__(self, root):
        self.root = root
        self.root.title("Cassino Python")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        self.root.state("zoomed")
        self.largura_tela = self.root.winfo_screenwidth()
        self.altura_tela = self.root.winfo_screenheight()

        self.root.geometry(f"{int(self.largura_tela * 0.9)}x{int(self.altura_tela * 0.85)}")
        self.root.minsize(850, 600)
        self.root.configure(bg="#0b3d0b")

        self.jogador = None
        self.roleta = Roleta()
        self.caca_niquel = CacaNiquel()
        self.copa_brasil = CopaDoBrasil()
        self.bozo = Bozo()

        self.criar_tela_login()

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def atualizar_saldo(self):
        if self.jogador:
            self.label_saldo.config(text=f"Saldo: R$ {self.jogador.saldo:.2f}")

    def criar_tela_login(self):
        self.limpar_janela()

        self.root.configure(bg="#06420f")

        tk.Label(
            self.root,
            text="♦ ♣ ♠ ♥",
            font=("Times New Roman", 26, "bold"),
            bg="#06420f",
            fg="gold"
        ).pack(pady=(20, 0))

        titulo = tk.Label(
            self.root,
            text="CUIABET",
            font=("Times New Roman", 34, "bold"),
            bg="#06420f",
            fg="gold"
        )
        titulo.pack(pady=(5, 5))

        subtitulo = tk.Label(
            self.root,
            text="Entre na mesa e teste sua sorte",
            font=("Arial", 14, "italic"),
            bg="#06420f",
            fg="white"
        )
        subtitulo.pack(pady=(0, 20))

        frame_madeira = tk.Frame(self.root, bg="#6b3e0a")
        frame_madeira.pack(pady=10)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5)

        frame_login = tk.Frame(frame_ouro, bg="#145214", padx=40, pady=30)
        frame_login.pack(padx=5, pady=5)

        tk.Label(
            frame_login,
            text="★ IDENTIFICAÇÃO DO JOGADOR ★",
            font=("Times New Roman", 18, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=(0, 20))

        tk.Label(
            frame_login,
            text="Nome do jogador:",
            font=("Arial", 14, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(5, 5))

        self.entry_nome = tk.Entry(
            frame_login,
            font=("Arial", 15),
            width=28,
            justify="center",
            bd=3,
            relief="sunken"
        )
        self.entry_nome.pack(pady=(0, 15), ipady=5)

        tk.Label(
            frame_login,
            text="Saldo inicial:",
            font=("Arial", 14, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(5, 5))

        self.entry_saldo = tk.Entry(
            frame_login,
            font=("Arial", 15),
            width=28,
            justify="center",
            bd=3,
            relief="sunken"
        )
        self.entry_saldo.pack(pady=(0, 20), ipady=5)

        btn_entrar = tk.Button(
            frame_login,
            text="ENTRAR NO CASSINO",
            font=("Arial", 14, "bold"),
            command=self.entrar_cassino,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=22
        )
        btn_entrar.pack(pady=(5, 10), ipady=4)

        def carregar_jogador_salvo():
            jogador_salvo = carregar_jogador()

            if jogador_salvo is None:
                messagebox.showwarning("Aviso", "Nenhum jogador salvo encontrado.")
                return

            self.jogador = jogador_salvo
            self.criar_tela_principal()
        
        tk.Button(
            frame_login,
            text="Carregar Jogador Salvo",
            font=("Arial", 13, "bold"),
            command=carregar_jogador_salvo,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=22
        ).pack(pady=8)

        tk.Label(
            self.root,
            text="Aposte com segurança",
            font=("Times New Roman", 13, "bold"),
            bg="#06420f",
            fg="#b20a0a"
        ).pack(pady=20)

    def entrar_cassino(self):
        nome = self.entry_nome.get().strip()
        saldo_texto = self.entry_saldo.get().strip()

        if nome == "":
            messagebox.showwarning("Aviso", "Digite o nome do jogador.")
            return

        try:
            saldo = float(saldo_texto)
        except ValueError:
            messagebox.showerror("Erro", "Digite um saldo inicial válido.")
            return

        if saldo <= 0:
            messagebox.showwarning("Aviso", "O saldo inicial deve ser maior que zero.")
            return

        self.jogador = Jogador(nome, saldo)
        salvar_jogador(self.jogador)
        self.criar_tela_principal()

    def botao_estilizado(self, parent, texto, comando, largura=15):
        return tk.Button(
            parent,
            text=texto,
            font=("Arial", 14, "bold"),
            command=comando,
            width=largura,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2"
        )

    def tela_menu_jogos(self):
        self.limpar_area()

        tk.Label(
            self.frame_conteudo,
            text="ESCOLHA SEU JOGO",
            font=("Times New Roman", 20, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=8)

        frame_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_madeira.pack(pady=8)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5)

        frame_jogos = tk.Frame(frame_ouro, bg="#000000", padx=20, pady=14)
        frame_jogos.pack(padx=5, pady=5)

        jogos = [
            ("🎡", "Roleta", self.tela_roleta),
            ("🎰", "Caça-Níquel", self.tela_caca_niquel),
            ("⚽", "Copa do Brasil", self.tela_copa_brasil),
            ("🎲", "Bozó", self.tela_bozo),
        ]

        altura_card = max(95, int(self.altura_tela * 0.13))
        largura_card = max(120, int(self.largura_tela * 0.12))
        fonte_icone = max(20, int(self.altura_tela * 0.035))

        for i, (icone, nome, comando) in enumerate(jogos):
            card = tk.Frame(
                frame_jogos,
                bg="#145214",
                bd=2,
                relief="ridge",
                width=largura_card,
                height=altura_card
            )
            card.grid(row=i // 2, column=i % 2, padx=12, pady=8)
            card.pack_propagate(False)

            tk.Label(
                card,
                text=icone,
                font=("Arial", fonte_icone),
                bg="#145214",
                fg="gold"
            ).pack(pady=(6, 2))

            tk.Label(
                card,
                text=nome,
                font=("Arial", 10, "bold"),
                bg="#145214",
                fg="white"
            ).pack(pady=2)

            tk.Button(
                card,
                text="Jogar",
                font=("Arial", 9, "bold"),
                command=comando,
                bg="#8b0000",
                fg="white",
                activebackground="#a00000",
                activeforeground="white",
                bd=2,
                relief="raised",
                cursor="hand2",
                width=10
        ).pack(pady=(4, 6))

    def tela_menu_carteira(self):
        self.limpar_area()

        tk.Label(
            self.frame_conteudo,
            text="CARTEIRA",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=20)

        frame_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_madeira.pack(pady=20)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5)

        frame_carteira = tk.Frame(frame_ouro, bg="#000000", padx=35, pady=30)
        frame_carteira.pack(padx=5, pady=5)

        opcoes = [
            ("💰", "Depositar", self.tela_deposito),
            ("🏦", "Sacar", self.tela_saque),
        ]

        for i, (icone, nome, comando) in enumerate(opcoes):
            card = tk.Frame(frame_carteira, bg="#145214", bd=3, relief="ridge")
            card.grid(row=0, column=i, padx=18, pady=10)

            tk.Label(
                card,
                text=icone,
                font=("Arial", 34),
                bg="#145214",
                fg="gold"
            ).pack(pady=(12, 4))

            tk.Label(
                card,
                text=nome,
                font=("Arial", 14, "bold"),
                bg="#145214",
                fg="white"
            ).pack(pady=4)

            tk.Button(
                card,
                text="Abrir",
                font=("Arial", 12, "bold"),
                command=comando,
                bg="#8b0000",
                fg="white",
                activebackground="#a00000",
                activeforeground="white",
                bd=3,
                relief="raised",
                cursor="hand2",
                width=12
            ).pack(pady=(8, 12))

    def criar_tela_principal(self):
        self.limpar_janela()

        titulo = tk.Label(
            self.root,
            text="♦ ♣ CASSINO ♦ ♣",
            font=("Times New Roman", 14, "bold"),
            bg="#0b3d0b",
            fg="gold"
        )
        titulo.pack(pady=10)

        self.label_jogador = tk.Label(
            self.root,
            text=f"Jogador: {self.jogador.nome}",
            font=("Arial", 16),
            bg="#0b3d0b",
            fg="white"
        )
        self.label_jogador.pack(pady=5)

        self.label_saldo = tk.Label(
            self.root,
            text=f"Saldo: R$ {self.jogador.saldo:.2f}",
            font=("Arial", 16),
            bg="#0b3d0b",
            fg="white"
        )
        self.label_saldo.pack(pady=5)

        frame_botoes = tk.Frame(self.root, bg="#0b3d0b")
        frame_botoes.pack(pady=10)

        btn_jogos = self.botao_estilizado(frame_botoes, "JOGOS", self.tela_menu_jogos)
        btn_jogos.grid(row=0, column=0, padx=8, pady=5)

        btn_carteira = self.botao_estilizado(frame_botoes, "CARTEIRA", self.tela_menu_carteira)
        btn_carteira.grid(row=0, column=1, padx=8, pady=5)

        btn_historico = self.botao_estilizado(frame_botoes, "HISTÓRICO", self.mostrar_historico)
        btn_historico.grid(row=0, column=2, padx=8, pady=5)

        btn_salvar = self.botao_estilizado(frame_botoes, "SALVAR", self.salvar_jogo)
        btn_salvar.grid(row=0, column=3, padx=8, pady=5)

        btn_trocar = self.botao_estilizado(frame_botoes, "TROCAR JOGADOR", self.criar_tela_login)
        btn_trocar.grid(row=0, column=4, padx=8, pady=5)

        frame_madeira = tk.Frame(self.root, bg="#4b2e05")
        frame_madeira.pack(pady=20, padx=20, fill="both", expand=True)

        frame_ouro = tk.Frame(frame_madeira, bg="gold")
        frame_ouro.pack(fill="both", expand=True, padx=4, pady=4)

        self.frame_conteudo = tk.Frame(frame_ouro, bg="#145214")
        self.frame_conteudo.pack(fill="both", expand=True, padx=4, pady=4)

        decoracao = tk.Label(
            self.frame_conteudo,
            text="♦ ♣ ♠ ♥   ♦ ♣ ♠ ♥   ♦ ♣ ♠ ♥",
            font=("Times New Roman", 14, "bold"),
            bg="#145214",
            fg="#d4af37"
        )
        decoracao.pack(pady=5)

    def limpar_area(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def salvar_jogo(self):
        if self.jogador is None:
            messagebox.showwarning("Aviso", "Nenhum jogador para salvar.")
            return

        salvar_jogador(self.jogador)
        messagebox.showinfo("Salvo", "Jogo salvo com sucesso!")

    def tela_deposito(self):
        self.limpar_area()

        tk.Label(
            self.frame_conteudo,
            text="DEPÓSITO",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=20)

        frame_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_madeira.pack(pady=20)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5)

        frame_painel = tk.Frame(frame_ouro, bg="#2b1a05", padx=40, pady=30)
        frame_painel.pack(padx=5, pady=5)

        tk.Label(
            frame_painel,
            text="💰 ADICIONAR SALDO",
            font=("Arial", 18, "bold"),
            bg="#2b1a05",
            fg="gold"
        ).pack(pady=(0, 15))

        tk.Label(
            frame_painel,
            text=f"Saldo atual: R$ {self.jogador.saldo:.2f}",
            font=("Arial", 14, "bold"),
            bg="#2b1a05",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            frame_painel,
            text="Valor do depósito:",
            font=("Arial", 13),
            bg="#2b1a05",
            fg="white"
        ).pack(pady=(10, 5))

        entrada_valor = tk.Entry(
            frame_painel,
            font=("Arial", 15),
            width=20,
            justify="center",
            bd=3,
            relief="sunken"
        )
        entrada_valor.pack(pady=5, ipady=5)

        resultado_label = tk.Label(
            frame_painel,
            text="",
            font=("Arial", 12, "bold"),
            bg="#2b1a05",
            fg="white"
        )
        resultado_label.pack(pady=10)

        def confirmar_deposito():
            try:
                valor = float(entrada_valor.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor válido.")
                return

            if not self.jogador.depositar(valor):
                messagebox.showwarning("Aviso", "O valor do depósito precisa ser maior que zero.")
                return

            self.atualizar_saldo()
            salvar_jogador(self.jogador)
            resultado_label.config(
                text=f"Depósito de R$ {valor:.2f} realizado com sucesso!",
                fg="gold"
            )

        tk.Button(
            frame_painel,
            text="Confirmar Depósito",
            font=("Arial", 14, "bold"),
            command=confirmar_deposito,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=20
        ).pack(pady=15)

    def tela_saque(self):
        self.limpar_area()

        tk.Label(
            self.frame_conteudo,
            text="SAQUE",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=20)

        frame_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_madeira.pack(pady=20)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5)

        frame_painel = tk.Frame(frame_ouro, bg="#2b1a05", padx=40, pady=30)
        frame_painel.pack(padx=5, pady=5)

        tk.Label(
            frame_painel,
            text="🏦 RETIRAR SALDO",
            font=("Arial", 18, "bold"),
            bg="#2b1a05",
            fg="gold"
        ).pack(pady=(0, 15))

        tk.Label(
            frame_painel,
            text=f"Saldo atual: R$ {self.jogador.saldo:.2f}",
            font=("Arial", 14, "bold"),
            bg="#2b1a05",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            frame_painel,
            text="Valor do saque:",
            font=("Arial", 13),
            bg="#2b1a05",
            fg="white"
        ).pack(pady=(10, 5))

        entrada_valor = tk.Entry(
            frame_painel,
            font=("Arial", 15),
            width=20,
            justify="center",
            bd=3,
            relief="sunken"
        )
        entrada_valor.pack(pady=5, ipady=5)

        resultado_label = tk.Label(
            frame_painel,
            text="",
            font=("Arial", 12, "bold"),
            bg="#2b1a05",
            fg="white"
        )
        resultado_label.pack(pady=10)

        def confirmar_saque():
            try:
                valor = float(entrada_valor.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor válido.")
                return

            if not self.jogador.sacar(valor):
                messagebox.showwarning("Aviso", "Saque inválido ou saldo insuficiente.")
                return

            self.atualizar_saldo()
            salvar_jogador(self.jogador)
            resultado_label.config(
                text=f"Saque de R$ {valor:.2f} realizado com sucesso!",
                fg="gold"
            )

        tk.Button(
            frame_painel,
            text="Confirmar Saque",
            font=("Arial", 14, "bold"),
            command=confirmar_saque,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=20
        ).pack(pady=15)

    def mostrar_historico(self):
        self.limpar_area()

        tk.Label(
            self.frame_conteudo,
            text="HISTÓRICO DE JOGADAS",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=20)

        frame_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_madeira.pack(pady=10, padx=20, fill="both", expand=True)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=5, pady=5, fill="both", expand=True)

        frame_painel = tk.Frame(frame_ouro, bg="#2b1a05", padx=15, pady=15)
        frame_painel.pack(padx=5, pady=5, fill="both", expand=True)

        tk.Label(
            frame_painel,
            text=f"Jogador: {self.jogador.nome}  |  Saldo: R$ {self.jogador.saldo:.2f}",
            font=("Arial", 13, "bold"),
            bg="#2b1a05",
            fg="white"
        ).pack(pady=(0, 10))

        if not self.jogador.historico:
            tk.Label(
                frame_painel,
                text="Nenhuma jogada registrada ainda.",
                font=("Arial", 14, "bold"),
                bg="#2b1a05",
                fg="gold"
            ).pack(pady=40)
            return

        frame_texto = tk.Frame(frame_painel, bg="#2b1a05")
        frame_texto.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side="right", fill="y")

        texto = tk.Text(
            frame_texto,
            width=85,
            height=18,
            font=("Consolas", 10),
            wrap="word",
            bg="#111111",
            fg="white",
            insertbackground="white",
            yscrollcommand=scrollbar.set,
            bd=3,
            relief="sunken"
        )
        texto.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=texto.yview)

        for i, jogada in enumerate(self.jogador.historico, start=1):
            texto.insert(tk.END, f"{i:02d}. {jogada}\n\n")

        texto.config(state="disabled")

        tk.Button(
            frame_painel,
            text="Limpar Histórico",
            font=("Arial", 12, "bold"),
            command=lambda: limpar_historico(),
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2"
        ).pack(pady=10)

        def limpar_historico():
            self.jogador.historico.clear()
            self.mostrar_historico()

    def tela_roleta(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="ROLETA",
            font=("Arial", 20, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=10)

        tk.Label(
            self.frame_conteudo,
            text="Valor da aposta:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack()

        entrada_aposta = tk.Entry(self.frame_conteudo, font=("Arial", 12))
        entrada_aposta.pack(pady=5)

        self.btn_girar_roleta = tk.Button(
            self.frame_conteudo,
            text="Girar Roleta",
            font=("Arial", 14, "bold"),
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2"
        )
        self.btn_girar_roleta.pack(pady=10)

        tk.Label(
            self.frame_conteudo,
            text="Tipo de aposta:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack()

        tipo_var = tk.StringVar(value="numero")

        frame_tipos = tk.Frame(self.frame_conteudo, bg="#145214")
        frame_tipos.pack(pady=5)

        tk.Radiobutton(frame_tipos, text="Número", variable=tipo_var, value="numero",
                    bg="#145214", fg="white", selectcolor="#145214").grid(row=0, column=0, padx=5)
        tk.Radiobutton(frame_tipos, text="Cor", variable=tipo_var, value="cor",
                    bg="#145214", fg="white", selectcolor="#145214").grid(row=0, column=1, padx=5)
        tk.Radiobutton(frame_tipos, text="Paridade", variable=tipo_var, value="paridade",
                    bg="#145214", fg="white", selectcolor="#145214").grid(row=0, column=2, padx=5)
        tk.Radiobutton(frame_tipos, text="Faixa", variable=tipo_var, value="faixa",
                    bg="#145214", fg="white", selectcolor="#145214").grid(row=0, column=3, padx=5)

        tk.Label(
            self.frame_conteudo,
            text="Escolha:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack()

        entrada_escolha = tk.Entry(self.frame_conteudo, font=("Arial", 12))
        entrada_escolha.pack(pady=5)

        frame_roleta_madeira = tk.Frame(self.frame_conteudo, bg="#6b3e0a")
        frame_roleta_madeira.pack(pady=15)

        frame_roleta_ouro = tk.Frame(frame_roleta_madeira, bg="#d4af37")
        frame_roleta_ouro.pack(padx=5, pady=5)

        frame_roleta = tk.Frame(frame_roleta_ouro, bg="#111111", padx=25, pady=20)
        frame_roleta.pack(padx=5, pady=5)

        tk.Label(
            frame_roleta,
            text="★ ROLETA VIP ★",
            font=("Times New Roman", 18, "bold"),
            bg="#111111",
            fg="gold"
        ).pack(pady=(0, 10))

        resultado_label = tk.Label(
            frame_roleta,
            text="?",
            font=("Arial", 50, "bold"),
            width=5,
            height=2,
            bg="#222222",
            fg="white",
            relief="ridge",
            bd=4
        )
        resultado_label.pack(pady=10)

        cor_label = tk.Label(
            frame_roleta,
            text="Aguardando giro...",
            font=("Arial", 14, "bold"),
            bg="#111111",
            fg="white"
        )
        cor_label.pack(pady=(5, 0))

        info_label = tk.Label(
            self.frame_conteudo,
            text="",
            font=("Arial", 14),
            bg="#145214",
            fg="white"
        )
        info_label.pack(pady=10)

        def cor_do_numero(numero):
            vermelhos = {
                1, 3, 5, 7, 9, 12, 14, 16, 18,
                19, 21, 23, 25, 27, 30, 32, 34, 36
            }

            if numero == 0:
                return "green"
            elif numero in vermelhos:
                return "red"
            else:
                return "black"

        def piscar(cor_base):
            for i in range(6):
                cor = "gold" if i % 2 == 0 else cor_base
                self.root.after(
                    i * 150,
                    lambda c=cor: resultado_label.config(bg=c)
                )

        def animar_numero(final):
            contador = 15

            def loop():
                nonlocal contador

                if contador > 0:
                    fake = random.randint(0, 36)
                    cor_fake = cor_do_numero(fake)

                    resultado_label.config(
                        text=str(fake),
                        bg=cor_fake,
                        fg="white"
                    )

                    cor_label.config(text="Girando...", fg="white")

                    contador -= 1
                    self.root.after(60, loop)

                else:
                    if final["cor"] == "vermelho":
                        cor_fundo = "red"
                    elif final["cor"] == "preto":
                        cor_fundo = "black"
                    else:
                        cor_fundo = "green"

                    resultado_label.config(
                        text=str(final["numero"]),
                        bg=cor_fundo,
                        fg="white"
                    )

                    cor_label.config(
                        text=f"COR: {final['cor'].upper()}",
                        fg=cor_fundo if cor_fundo != "black" else "white"
                    )

                    texto = (
                        f"Número: {final['numero']}\n"
                        f"Cor: {final['cor']}\n"
                        f"Paridade: {final['paridade']}\n"
                        f"Faixa: {final['faixa']}\n"
                    )

                    if final["ganhou"]:
                        texto += f"\nGANHOU R$ {final['premio']:.2f}"
                        info_label.config(text=texto, fg="gold")
                        piscar(cor_fundo)
                        winsound.Beep(1200, 200)
                    else:
                        texto += "\nPERDEU"
                        info_label.config(text=texto, fg="white")
                        winsound.Beep(400, 200)

                    self.atualizar_saldo()
                    self.btn_girar_roleta.config(text="Girando...", state="normal")

            loop()

        def jogar_roleta():
            try:
                valor = float(entrada_aposta.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor de aposta válido.")
                return

            tipo_aposta = tipo_var.get()
            escolha = entrada_escolha.get().strip().lower()

            if escolha == "":
                messagebox.showwarning("Aviso", "Preencha o campo de escolha.")
                return

            resultado = self.roleta.jogar(self.jogador, valor, tipo_aposta, escolha)

            if "erro" in resultado:
                messagebox.showerror("Erro", resultado["erro"])
                return
            
            salvar_jogador(self.jogador)

            info_label.config(text="Girando a roleta...", fg="white")
            self.btn_girar_roleta.config(text="Girando...", state="disabled")
            animar_numero(resultado)

        self.btn_girar_roleta.config(command=jogar_roleta)

    def tela_caca_niquel(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="CAÇA-NÍQUEL",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=10)

        frame_principal = tk.Frame(self.frame_conteudo, bg="#145214")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        #lado esq
        frame_esquerda = tk.Frame(self.frame_principal if hasattr(self, 'frame_principal') else frame_principal, bg="#145214")
        frame_esquerda.pack(side="left", fill="y", padx=(0, 25))

        jackpot_box = tk.Frame(frame_esquerda, bg="#2b1a05", bd=3, relief="ridge")
        jackpot_box.pack(pady=8, fill="x")

        jackpot_label = tk.Label(
            jackpot_box,
            text=f"💰 JACKPOT ATUAL\nR$ {self.caca_niquel.jackpot:.2f}",
            font=("Arial", 14, "bold"),
            bg="#2b1a05",
            fg="gold",
            justify="center",
            padx=12,
            pady=10
        )
        jackpot_label.pack()

        tk.Label(
            frame_esquerda,
            text="Valor da aposta:",
            font=("Arial", 12, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(12, 4))

        entrada_aposta = tk.Entry(
            frame_esquerda,
            font=("Arial", 12),
            width=18,
            justify="center",
            bd=3,
            relief="sunken"
        )
        entrada_aposta.pack(pady=5, ipady=4)

        tabela_box = tk.Frame(frame_esquerda, bg="#2b1a05", bd=3, relief="ridge")
        tabela_box.pack(pady=12, fill="x")

        tabela_label = tk.Label(
            tabela_box,
            text=(
                "Tabela de Prêmios\n\n"
                "7 7 7      → JACKPOT\n"
                "⭐ ⭐ ⭐    → 6x\n"
                "🍒 🍒 🍒 → 5x + rodada grátis\n"
                "🔔 🔔 🔔 → 5x\n"
                "3 iguais   → 4x\n\n"
                "Valem:\n"
                "• 3 linhas\n"
                "• 3 colunas\n"
                "• 2 diagonais\n\n"
                "🚫 Duplas não pagam\n"
                "🔥 2+ combinações → bônus"
            ),
            font=("Arial", 10),
            bg="#2b1a05",
            fg="white",
            justify="left",
            padx=12,
            pady=12
        )
        tabela_label.pack()

        ultimo_box = tk.Frame(frame_esquerda, bg="#2b1a05", bd=3, relief="ridge")
        ultimo_box.pack(pady=12, fill="x")

        ultimo_premio_label = tk.Label(
            ultimo_box,
            text="🎁 ÚLTIMO PRÊMIO\nNenhum ainda",
            font=("Arial", 12, "bold"),
            bg="#2b1a05",
            fg="gold",
            justify="center",
            padx=12,
            pady=10
        )
        ultimo_premio_label.pack()

        #lado dir
        frame_direita = tk.Frame(frame_principal, bg="#145214")
        frame_direita.pack(side="right", fill="both", expand=True)

        frame_madeira = tk.Frame(frame_direita, bg="#6b3e0a")
        frame_madeira.pack(pady=20)

        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=4, pady=4)

        frame_interno = tk.Frame(frame_ouro, bg="#2b1a05", padx=15, pady=15)
        frame_interno.pack(padx=4, pady=4)

        tk.Label(
            frame_interno,
            text="★ SLOT MACHINE ★",
            font=("Times New Roman", 18, "bold"),
            bg="#2b1a05",
            fg="gold"
        ).pack(pady=(0, 10))

        frame_slots = tk.Frame(frame_interno, bg="#2b1a05")
        frame_slots.pack()

        slots = []
        for i in range(3):
            linha_slots = []
            for j in range(3):
                lbl = tk.Label(
                    frame_slots,
                    text="❔",
                    font=("Arial", 28, "bold"),
                    width=3,
                    height=2,
                    bg="#f8f8f8",
                    fg="black",
                    relief="ridge",
                    bd=3
                )
                lbl.grid(row=i, column=j, padx=6, pady=6)
                linha_slots.append(lbl)
            slots.append(linha_slots)

        # Resultado (sem caixa feia)
        resultado_label = tk.Label(
            frame_direita,
            text="",
            font=("Arial", 16, "bold"),
            bg="#145214",
            fg="white",
            justify="center",
            wraplength=360,
            pady=20
        )
        resultado_label.pack()

        btn_girar = tk.Button(
            frame_esquerda,
            text="Girar",
            font=("Arial", 14, "bold"),
            command=lambda: jogar_caca(),
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=16
        )
        btn_girar.pack(pady=10)

        def tocar_som_vitoria(tipo_resultado):
            if tipo_resultado == "jackpot":
                winsound.Beep(900, 120)
                winsound.Beep(1100, 120)
                winsound.Beep(1300, 180)
                winsound.Beep(1500, 220)
            elif tipo_resultado == "super_premio":
                winsound.Beep(800, 120)
                winsound.Beep(1000, 120)
                winsound.Beep(1200, 180)
            else:
                winsound.Beep(700, 100)
                winsound.Beep(900, 100)
                winsound.Beep(1100, 150)

        def tocar_som_derrota():
            winsound.Beep(350, 180)

        def limpar_destaques():
            for i in range(3):
                for j in range(3):
                    slots[i][j].config(bg="#f8f8f8")

        def acender_combinacao(combinacao, cor="gold"):
            tipo = combinacao["tipo"]
            indice = combinacao["indice"]

            if tipo == "linha":
                for j in range(3):
                    slots[indice][j].config(bg=cor)

            elif tipo == "coluna":
                for i in range(3):
                    slots[i][indice].config(bg=cor)

            elif tipo == "diagonal":
                if indice == 0:
                    slots[0][0].config(bg=cor)
                    slots[1][1].config(bg=cor)
                    slots[2][2].config(bg=cor)
                else:
                    slots[0][2].config(bg=cor)
                    slots[1][1].config(bg=cor)
                    slots[2][0].config(bg=cor)

        def animar_combinacoes_premiadas(combinacoes, indice=0):
            if not combinacoes:
                return

            if indice >= len(combinacoes):
                limpar_destaques()
                for combinacao in combinacoes:
                    acender_combinacao(combinacao, "gold")
                return

            limpar_destaques()
            acender_combinacao(combinacoes[indice], "gold")

            self.root.after(
                350,
                lambda: (
                    limpar_destaques(),
                    self.root.after(120, lambda: animar_combinacoes_premiadas(combinacoes, indice + 1))
                )
            )

        def atualizar_jackpot():
            jackpot_label.config(text=f"💰 JACKPOT ATUAL\nR$ {self.caca_niquel.jackpot:.2f}")

        def atualizar_ultimo_premio(texto):
            ultimo_premio_label.config(text=f"🎁 ÚLTIMO PRÊMIO\n{texto}")

        def animar_slots(resultado_final, valor_aposta):
            contador = 18

            def loop():
                nonlocal contador

                if contador > 0:
                    limpar_destaques()
                    for i in range(3):
                        for j in range(3):
                            slots[i][j].config(
                                text=random.choice(self.caca_niquel.simbolos),
                                bg="#f8f8f8"
                            )

                    contador -= 1
                    self.root.after(90, loop)

                else:
                    grade_final = resultado_final["grade"]

                    for i in range(3):
                        for j in range(3):
                            slots[i][j].config(
                                text=grade_final[i][j],
                                bg="#f8f8f8"
                            )

                    self.atualizar_saldo()
                    atualizar_jackpot()

                    tipo = resultado_final["tipo_resultado"]
                    premio = resultado_final["premio"]
                    bonus_multilinha = resultado_final["bonus_multilinha"]

                    if resultado_final["ganhou"]:
                        if resultado_final["combinacoes_premiadas"]:
                            animar_combinacoes_premiadas(resultado_final["combinacoes_premiadas"])

                        if tipo == "jackpot":
                            mensagem = f"🎰 JACKPOT!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"JACKPOT — R$ {premio:.2f}")
                        elif tipo == "super_premio":
                            mensagem = f"⭐ SUPER PRÊMIO!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"SUPER PRÊMIO — R$ {premio:.2f}")
                        elif tipo == "rodada_gratis":
                            mensagem = f"🍒 Você ganhou R$ {premio:.2f}\n+ rodada grátis!"
                            atualizar_ultimo_premio(f"RODADA GRÁTIS — R$ {premio:.2f}")
                        elif tipo == "sino_dourado":
                            mensagem = f"🔔 BÔNUS DO SINO!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"SINO DOURADO — R$ {premio:.2f}")
                        elif tipo == "tripla":
                            mensagem = f"🎉 TRINCA!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"TRINCA — R$ {premio:.2f}")
                        elif tipo == "multilinha":
                            mensagem = f"🔥 MULTILINHA!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"MULTILINHA — R$ {premio:.2f}")
                        else:
                            mensagem = f"✨ Boa!\nVocê ganhou R$ {premio:.2f}"
                            atualizar_ultimo_premio(f"PRÊMIO — R$ {premio:.2f}")

                        if bonus_multilinha > 0:
                            mensagem += f"\n🔥 Bônus multilinha: R$ {bonus_multilinha:.2f}"

                        resultado_label.config(text=mensagem, fg="gold")
                        tocar_som_vitoria(tipo)

                    else:
                        resultado_label.config(text="❌ Você perdeu!", fg="red")
                        atualizar_ultimo_premio("Sem prêmio")
                        tocar_som_derrota()

                    if resultado_final["rodada_gratis"]:
                        self.root.after(1200, lambda: executar_rodada_gratis(valor_aposta))
                    else:
                        btn_girar.config(state="normal")

            loop()

        def executar_rodada_gratis(valor_aposta):
            resultado_label.config(text="🎁 Rodada grátis!", fg="gold")
            resultado = self.caca_niquel.jogar(self.jogador, valor_aposta, True)
            animar_slots(resultado, valor_aposta)

        def jogar_caca():
            try:
                valor = float(entrada_aposta.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor válido.")
                return

            resultado = self.caca_niquel.jogar(self.jogador, valor)

            if "erro" in resultado:
                messagebox.showerror("Erro", resultado["erro"])
                return
            
            salvar_jogador(self.jogador)

            resultado_label.config(text="Girando...", fg="white")
            btn_girar.config(state="disabled")
            animar_slots(resultado, valor)
            
    def tela_copa_brasil(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="COPA DO BRASIL",
            font=("Arial", 20, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=10)

        frame_principal = tk.Frame(self.frame_conteudo, bg="#145214")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        frame_esquerda = tk.Frame(frame_principal, bg="#145214")
        frame_esquerda.pack(side="left", fill="y", padx=(0, 20))

        frame_direita = tk.Frame(frame_principal, bg="#145214")
        frame_direita.pack(side="right", fill="both", expand=True)

        tk.Label(frame_esquerda, text="Valor da aposta:", font=("Arial", 12),
                bg="#145214", fg="white").pack()

        entrada_aposta = tk.Entry(frame_esquerda, font=("Arial", 12), width=18)
        entrada_aposta.pack(pady=5)

        tk.Label(frame_esquerda, text="Escolha o time:", font=("Arial", 12),
                bg="#145214", fg="white").pack(pady=(10, 5))

        nomes_times = [time.nome for time in self.copa_brasil.times]
        time_var = tk.StringVar(value=nomes_times[0])

        menu_times = tk.OptionMenu(frame_esquerda, time_var, *nomes_times)
        menu_times.config(font=("Arial", 12), bg="white", width=14)
        menu_times.pack(pady=5)

        tk.Label(frame_esquerda, text="Odds dos times:", font=("Arial", 12, "bold"),
                bg="#145214", fg="gold").pack(pady=(12, 5))

        frame_odds = tk.Frame(frame_esquerda, bg="#2b1a05", bd=3, relief="ridge")
        frame_odds.pack(pady=5, padx=5)

        tk.Label(
            frame_odds,
            text="TABELA DE ODDS",
            font=("Arial", 10, "bold"),
            bg="#2b1a05",
            fg="gold"
        ).grid(row=0, column=0, columnspan=2, pady=(6, 4))

        for i, time in enumerate(self.copa_brasil.times):
            odd = self.copa_brasil.calcular_odd(time)

            texto = f"{time.nome}: {odd:.1f}"

            tk.Label(
                frame_odds,
                text=texto,
                font=("Arial", 9, "bold"),
                bg="#2b1a05",
                fg="white",
                width=16,
                anchor="w"
            ).grid(
                row=(i // 2) + 1,
                column=i % 2,
                padx=8,
                pady=2
            )

        tk.Label(frame_esquerda, text="Tipo de aposta:", font=("Arial", 12),
                bg="#145214", fg="white").pack(pady=(12, 5))

        tipo_var = tk.StringVar(value="campeao")

        frame_tipos = tk.Frame(frame_esquerda, bg="#145214")
        frame_tipos.pack(pady=5)

        tk.Radiobutton(frame_tipos, text="Campeão", variable=tipo_var, value="campeao",
                    bg="#145214", fg="white", selectcolor="#145214").pack(anchor="w")
        tk.Radiobutton(frame_tipos, text="Finalista", variable=tipo_var, value="finalista",
                    bg="#145214", fg="white", selectcolor="#145214").pack(anchor="w")
        tk.Radiobutton(frame_tipos, text="Semifinalista", variable=tipo_var, value="semifinalista",
                    bg="#145214", fg="white", selectcolor="#145214").pack(anchor="w")

        btn_simular = tk.Button(
            frame_esquerda,
            text="Simular Copa",
            font=("Arial", 14, "bold"),
            command=lambda: jogar_copa(),
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2"
        )
        btn_simular.pack(pady=15)


        canvas_chave = tk.Canvas(
            frame_direita,
            width=680,
            height=430,
            bg="#0f4a1f",
            highlightthickness=2,
            highlightbackground="gold"
        )
        canvas_chave.pack(pady=10)

        resumo_label = tk.Label(
            frame_direita,
            text="Simule a Copa para ver o chaveamento.",
            font=("Arial", 13, "bold"),
            bg="#145214",
            fg="white",
            justify="center",
            wraplength=620
        )
        resumo_label.pack(pady=8)

        def texto_partida(partida):
            texto = f"{partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}"

            if partida["penaltis1"] is not None:
                texto += f" (Pên. {partida['penaltis1']}x{partida['penaltis2']})"

            return texto

        def desenhar_chaveamento(resultado):
            canvas_chave.delete("all")

            def caixa(x, y, texto, vencedor=False):
                cor_fundo = "#d4af37" if vencedor else "#111111"
                cor_texto = "black" if vencedor else "white"

                canvas_chave.create_rectangle(
                    x, y, x + 185, y + 38,
                    fill=cor_fundo,
                    outline="gold",
                    width=2
                )
                canvas_chave.create_text(
                    x + 92,
                    y + 19,
                    text=texto,
                    fill=cor_texto,
                    font=("Arial", 9, "bold"),
                    width=175
                )

            def linha(x1, y1, x2, y2):
                canvas_chave.create_line(x1, y1, x2, y2, fill="gold", width=2)

            canvas_chave.create_text(
                340, 25,
                text="🏆 CHAVEAMENTO DA COPA 🏆",
                fill="gold",
                font=("Times New Roman", 18, "bold")
            )

            quartas = resultado["quartas"]
            semi = resultado["semifinal"]
            final = resultado["final"]
            campeao = resultado["campeao"]

            y_quartas = [70, 150, 230, 310]
            for i, partida in enumerate(quartas):
                caixa(20, y_quartas[i], texto_partida(partida))

            y_semis = [110, 270]
            for i, partida in enumerate(semi):
                caixa(250, y_semis[i], texto_partida(partida))

            partida_final = final[0]
            caixa(475, 190, texto_partida(partida_final))

            caixa(475, 270, f"🏆 {campeao}", vencedor=True)

            linha(205, 89, 250, 129)
            linha(205, 169, 250, 129)

            linha(205, 249, 250, 289)
            linha(205, 329, 250, 289)

            linha(435, 129, 475, 209)
            linha(435, 289, 475, 209)

            linha(567, 228, 567, 270)

        def mostrar_resumo_aposta(resultado):
            texto = (
                f"Campeão: {resultado['campeao']}\n"
                f"Sua aposta: {resultado['time_escolhido']} | "
                f"Tipo: {resultado['tipo_aposta']} | "
                f"Odd: {resultado['odd']:.1f}\n"
            )

            if resultado["ganhou"]:
                texto += f"✅ Você ganhou R$ {resultado['premio']:.2f}!"
                resumo_label.config(text=texto, fg="gold")
            else:
                texto += "❌ Você perdeu a aposta."
                resumo_label.config(text=texto, fg="white")

        def jogar_copa():
            try:
                valor = float(entrada_aposta.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor de aposta válido.")
                return

            time_escolhido = time_var.get()
            tipo_aposta = tipo_var.get()

            resultado = self.copa_brasil.jogar(
                self.jogador,
                valor,
                time_escolhido,
                tipo_aposta
            )

            if "erro" in resultado:
                messagebox.showerror("Erro", resultado["erro"])
                return

            self.atualizar_saldo()
            salvar_jogador(self.jogador)
            desenhar_chaveamento(resultado)
            mostrar_resumo_aposta(resultado)

    def tela_bozo(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="BOZÓ",
            font=("Times New Roman", 24, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=10)

        frame_principal = tk.Frame(self.frame_conteudo, bg="#145214")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        frame_esquerda = tk.Frame(frame_principal, bg="#145214")
        frame_esquerda.pack(side="left", fill="y", padx=(0, 25))

        frame_direita = tk.Frame(frame_principal, bg="#145214")
        frame_direita.pack(side="right", fill="both", expand=True)

        tk.Label(
            frame_esquerda,
            text="Valor da aposta:",
            font=("Arial", 12, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=5)

        entrada_aposta = tk.Entry(
            frame_esquerda,
            font=("Arial", 12),
            width=18,
            justify="center"
        )
        entrada_aposta.pack(pady=5)

        status_label = tk.Label(
            frame_esquerda,
            text="Inicie uma partida",
            font=("Arial", 12, "bold"),
            bg="#145214",
            fg="gold",
            justify="center"
        )
        status_label.pack(pady=10)

        cartela_jogador_label = tk.Label(
            frame_esquerda,
            text="Cartela Jogador",
            font=("Consolas", 10),
            bg="#000000",
            fg="white",
            justify="left",
            bd=3,
            relief="ridge",
            padx=10,
            pady=10
        )
        cartela_jogador_label.pack(pady=5)

        cartela_cassino_label = tk.Label(
            frame_esquerda,
            text="Cartela Cassino",
            font=("Consolas", 10),
            bg="#000000",
            fg="white",
            justify="left",
            bd=3,
            relief="ridge",
            padx=10,
            pady=10
        )
        cartela_cassino_label.pack(pady=5)

        dados_labels = []
        dados_guardados = [False, False, False, False, False]

        frame_dados = tk.Frame(frame_direita, bg="#6b3e0a")
        frame_dados.pack(pady=20)

        frame_ouro = tk.Frame(frame_dados, bg="#d4af37")
        frame_ouro.pack(padx=4, pady=4)

        frame_interno = tk.Frame(frame_ouro, bg="#2b1a05", padx=15, pady=15)
        frame_interno.pack(padx=4, pady=4)

        for i in range(5):
            dado = tk.Label(
                frame_interno,
                text="⚀",
                font=("Arial", 42, "bold"),
                width=3,
                height=2,
                bg="white",
                fg="black",
                relief="ridge",
                bd=3
            )
            dado.grid(row=0, column=i, padx=6, pady=6)
            dados_labels.append(dado)

        tk.Label(
            frame_direita,
            text="Casa para marcar:",
            font=("Arial", 12, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(15, 5))

        casas = {
            "Ás": "as",
            "Duque": "duque",
            "Terno": "terno",
            "Quadra": "quadra",
            "Quina": "quina",
            "Sena": "sena",
            "Full": "full",
            "Seguida": "seguida",
            "Quadrada": "quadrada",
            "General": "general"
        }

        casa_var = tk.StringVar(value="as")

        menu_casas = tk.OptionMenu(frame_direita, casa_var, *casas.values())
        menu_casas.config(font=("Arial", 12), bg="white")
        menu_casas.pack(pady=5)

        log_label = tk.Label(
            frame_direita,
            text="",
            font=("Arial", 12),
            bg="#145214",
            fg="white",
            justify="center",
            wraplength=420
        )
        log_label.pack(pady=15)

        estado = {
            "partida": None,
            "dados": [1, 1, 1, 1, 1],
            "tentativas": 0
        }

        def formatar_cartela(cartela):
            texto = ""
            for casa, pontos in cartela.pontuacoes.items():
                valor = "-" if pontos is None else pontos
                texto += f"{casa}: {valor}\n"
            texto += f"TOTAL: {cartela.total()}"
            return texto

        def atualizar_cartelas():
            if estado["partida"]:
                cartela_jogador_label.config(
                    text="Cartela Jogador\n" + formatar_cartela(estado["partida"]["cartela_jogador"])
                )
                cartela_cassino_label.config(
                    text="Cartela Cassino\n" + formatar_cartela(estado["partida"]["cartela_cassino"])
                )

        def face_dado(valor):
            faces = {
                1: "⚀",
                2: "⚁",
                3: "⚂",
                4: "⚃",
                5: "⚄",
                6: "⚅"
            }
            return faces.get(valor, "🎲")

        def atualizar_dados():
            for i, valor in enumerate(estado["dados"]):
                cor = "gold" if dados_guardados[i] else "white"
                dados_labels[i].config(text=face_dado(valor), bg=cor)

        def alternar_dado(indice):
            if estado["partida"] is None:
                return
            dados_guardados[indice] = not dados_guardados[indice]
            atualizar_dados()

        for i, dado in enumerate(dados_labels):
            dado.bind("<Button-1>", lambda e, idx=i: alternar_dado(idx))

        def iniciar_partida():
            try:
                valor = float(entrada_aposta.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor válido.")
                return

            partida = self.bozo.iniciar_partida(self.jogador, valor)

            if "erro" in partida:
                messagebox.showerror("Erro", partida["erro"])
                return

            estado["partida"] = partida
            estado["dados"] = [1, 1, 1, 1, 1]
            estado["tentativas"] = 0

            for i in range(5):
                dados_guardados[i] = False

            self.atualizar_saldo()
            atualizar_dados()
            atualizar_cartelas()

            status_label.config(text="Rodada 1")
            log_label.config(text="Partida iniciada! Role os dados.")

        def rolar_dados():
            if estado["partida"] is None:
                messagebox.showwarning("Aviso", "Inicie uma partida primeiro.")
                return

            if estado["tentativas"] >= 3:
                messagebox.showwarning("Aviso", "Você já usou as 3 tentativas.")
                return

            for i in range(5):
                if not dados_guardados[i]:
                    estado["dados"][i] = random.randint(1, 6)

            estado["tentativas"] += 1
            atualizar_dados()

            log_label.config(
                text=f"Tentativa {estado['tentativas']}/3. Clique nos dados para guardar."
            )

        def marcar_casa():
            if estado["partida"] is None:
                messagebox.showwarning("Aviso", "Inicie uma partida primeiro.")
                return

            if estado["tentativas"] == 0:
                messagebox.showwarning("Aviso", "Role os dados antes de marcar.")
                return

            cartela_jogador = estado["partida"]["cartela_jogador"]
            cartela_cassino = estado["partida"]["cartela_cassino"]
            casa = casa_var.get()

            if casa not in cartela_jogador.casas_disponiveis():
                messagebox.showwarning("Aviso", "Essa casa já foi usada.")
                return

            pontos = self.bozo.calcular_pontos(estado["dados"], casa)
            cartela_jogador.marcar(casa, pontos)

            jogada_cassino = self.bozo.jogar_turno_cassino(cartela_cassino)

            atualizar_cartelas()

            log_label.config(
                text=(
                    f"Você marcou {pontos} pontos em {casa}.\n"
                    f"Cassino marcou {jogada_cassino['pontos']} em {jogada_cassino['casa']}.\n"
                    f"Dados do cassino: {jogada_cassino['dados']}"
                )
            )

            if cartela_jogador.completa():
                resultado = self.bozo.finalizar_partida(
                    self.jogador,
                    cartela_jogador,
                    cartela_cassino,
                    estado["partida"]["valor_aposta"]
                )

                self.atualizar_saldo()
                salvar_jogador(self.jogador)

                if resultado["ganhou"]:
                    log_label.config(
                        text=f"FIM DE JOGO!\nVocê venceu: {resultado['total_jogador']} x {resultado['total_cassino']}\nPrêmio: R$ {resultado['premio']:.2f}"
                    )
                elif resultado["empatou"]:
                    log_label.config(
                        text=f"FIM DE JOGO!\nEmpate: {resultado['total_jogador']} x {resultado['total_cassino']}\nAposta devolvida."
                    )
                else:
                    log_label.config(
                        text=f"FIM DE JOGO!\nVocê perdeu: {resultado['total_jogador']} x {resultado['total_cassino']}"
                    )

                estado["partida"] = None
                return

            estado["tentativas"] = 0
            for i in range(5):
                dados_guardados[i] = False

            atualizar_dados()

            rodada_atual = len(cartela_jogador.casas_disponiveis())
            status_label.config(text=f"Casas restantes: {rodada_atual}")

        btn_iniciar = tk.Button(
            frame_esquerda,
            text="Iniciar Partida",
            font=("Arial", 13, "bold"),
            command=iniciar_partida,
            bg="#8b0000",
            fg="white",
            width=16
        )
        btn_iniciar.pack(pady=10)

        btn_rolar = tk.Button(
            frame_direita,
            text="Rolar Dados",
            font=("Arial", 13, "bold"),
            command=rolar_dados,
            bg="#8b0000",
            fg="white",
            width=16
        )
        btn_rolar.pack(pady=8)

        btn_marcar = tk.Button(
            frame_direita,
            text="Marcar Casa",
            font=("Arial", 13, "bold"),
            command=marcar_casa,
            bg="#8b0000",
            fg="white",
            width=16
        )
        btn_marcar.pack(pady=8)