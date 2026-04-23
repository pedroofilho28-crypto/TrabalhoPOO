import tkinter as tk
import random
import winsound
from tkinter import messagebox
from jogador import Jogador
from jogos.roleta import Roleta
from jogos.caca_niquel import CacaNiquel
from jogos.copa_brasil import CopaDoBrasil

class InterfaceCassino:
    def __init__(self, root):
        self.root = root
        self.root.title("Cassino Python")
        self.root.geometry("800x600")
        self.root.configure(bg="#0b3d0b")

        self.jogador = None
        self.roleta = Roleta()
        self.caca_niquel = CacaNiquel()
        self.copa_brasil = CopaDoBrasil()

        self.criar_tela_login()

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def atualizar_saldo(self):
        if self.jogador:
            self.label_saldo.config(text=f"Saldo: R$ {self.jogador.saldo:.2f}")

    def criar_tela_login(self):
        self.limpar_janela()

        titulo = tk.Label(
            self.root,
            text="CUIABET",
            font=("Times New Roman", 28, "bold"),
            bg="#0b3d0b",
            fg="gold"
        )
        titulo.pack(pady=(30, 10))

        subtitulo = tk.Label(
            self.root,
            text="♦ ♣ Faça seu cadastro e entre na mesa ♠ ♥",
            font=("Times New Roman", 15, "bold"),
            bg="#0b3d0b",
            fg="#d4af37"
        )
        subtitulo.pack(pady=(0, 20))

    # Moldura de madeira
        frame_madeira = tk.Frame(self.root, bg="#6b3e0a")
        frame_madeira.pack(pady=20, padx=20)

    # Moldura de ouro
        frame_ouro = tk.Frame(frame_madeira, bg="#d4af37")
        frame_ouro.pack(padx=4, pady=4)

    # Área principal do login
        frame_login = tk.Frame(frame_ouro, bg="#145214", padx=30, pady=25)
        frame_login.pack(padx=4, pady=4)

        tk.Label(
            frame_login,
            text="Nome do jogador:",
            font=("Arial", 16, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(10, 8))

        self.entry_nome = tk.Entry(
            frame_login,
            font=("Arial", 16),
            width=28,
            justify="center",
            bd=3,
            relief="sunken"
        )
        self.entry_nome.pack(pady=(0, 15), ipady=6)

        tk.Label(
            frame_login,
            text="Saldo inicial:",
            font=("Arial", 16, "bold"),
            bg="#145214",
            fg="white"
        ).pack(pady=(5, 8))

        self.entry_saldo = tk.Entry(
            frame_login,
            font=("Arial", 16),
            width=28,
            justify="center",
            bd=3,
            relief="sunken"
        )
        self.entry_saldo.pack(pady=(0, 20), ipady=6)

        btn_entrar = tk.Button(
            frame_login,
            text="Entrar no Cassino",
            font=("Arial", 15, "bold"),
            command=self.entrar_cassino,
            bg="#8b0000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            bd=3,
            relief="raised",
            cursor="hand2",
            width=18
        )
        btn_entrar.pack(pady=(10, 15), ipady=4)

        rodape = tk.Label(
            self.root,
            text="♠ Experiência clássica de cassino com roleta e caça-níquel ♣",
            font=("Arial", 11, "italic"),
            bg="#0b3d0b",
            fg="white"
        )
        rodape.pack(pady=(10, 0))

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

        btn_roleta = self.botao_estilizado(frame_botoes, "Roleta", self.tela_roleta)
        btn_roleta.grid(row=0, column=0, padx=10, pady=5)

        btn_caca = self.botao_estilizado(frame_botoes, "Caça-Níquel", self.tela_caca_niquel)
        btn_caca.grid(row=0, column=1, padx=10, pady=5)

        btn_historico = self.botao_estilizado(frame_botoes, "Histórico", self.mostrar_historico)
        btn_historico.grid(row=0, column=2, padx=10, pady=5)

        btn_depositar = self.botao_estilizado(frame_botoes, "Depositar", self.tela_deposito)
        btn_depositar.grid(row=1, column=0, padx=10, pady=5)

        btn_sacar = self.botao_estilizado(frame_botoes, "Sacar", self.tela_saque)
        btn_sacar.grid(row=1, column=1, padx=10, pady=5)

        btn_trocar = self.botao_estilizado(frame_botoes, "Trocar Jogador", self.criar_tela_login)
        btn_trocar.grid(row=1, column=2, padx=10, pady=5)

        btn_copa = self.botao_estilizado(frame_botoes, "Aposta esportiva", self.tela_copa_brasil)
        btn_copa.grid(row=0, column=3, padx=10, pady=5)

        frame_madeira = tk.Frame(self.root, bg="#4b2e05")
        frame_madeira.pack(pady=20, padx=20, fill="both", expand=True)

        frame_ouro = tk.Frame(frame_madeira, bg="gold")
        frame_ouro.pack(fill="both", expand=True, padx=4, pady=4)

        self.frame_conteudo = tk.Frame(frame_ouro, bg="#145214")
        self.frame_conteudo.pack(fill="both", expand=True, padx=4, pady=4)

    def limpar_area(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def tela_deposito(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="DEPÓSITO",
            font=("Arial", 20, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=20)

        tk.Label(
            self.frame_conteudo,
            text="Valor do depósito:",
            font=("Arial", 14),
            bg="#145214",
            fg="white"
        ).pack(pady=10)

        entrada_valor = tk.Entry(self.frame_conteudo, font=("Arial", 14))
        entrada_valor.pack(pady=5)

        def confirmar_deposito():
            try:
                valor = float(entrada_valor.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor válido.")
                return

            if self.jogador.depositar(valor) is False:
                messagebox.showwarning("Aviso", "Depósito inválido.")
                return

            self.atualizar_saldo()
            messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado.")

        tk.Button(
            self.frame_conteudo,
            text="Confirmar Depósito",
            font=("Arial", 14),
            command=confirmar_deposito
        ).pack(pady=20)

    def tela_saque(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="SAQUE",
            font=("Arial", 20, "bold"),
            bg="#145214",
            fg="gold"
        )
        titulo.pack(pady=20)

        tk.Label(
            self.frame_conteudo,
            text="Valor do saque:",
            font=("Arial", 14),
            bg="#145214",
            fg="white"
        ).pack(pady=10)

        entrada_valor = tk.Entry(self.frame_conteudo, font=("Arial", 14))
        entrada_valor.pack(pady=5)

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
            messagebox.showinfo("Sucesso", f"Saque de R$ {valor:.2f} realizado.")

        tk.Button(
            self.frame_conteudo,
            text="Confirmar Saque",
            font=("Arial", 14),
            command=confirmar_saque
        ).pack(pady=20)

    def mostrar_historico(self):
        self.limpar_area()

        titulo = tk.Label(
            self.frame_conteudo,
            text="Histórico de Jogadas",
            font=("Arial", 18, "bold"),
            bg="#145214",
            fg="white"
        )
        titulo.pack(pady=10)

        if not self.jogador.historico:
            vazio = tk.Label(
                self.frame_conteudo,
                text="Nenhuma jogada registrada.",
                font=("Arial", 14),
                bg="#145214",
                fg="white"
            )
            vazio.pack(pady=20)
            return

        texto = tk.Text(self.frame_conteudo, width=80, height=18, font=("Arial", 11))
        texto.pack(pady=10)

        for jogada in self.jogador.historico:
            texto.insert(tk.END, jogada + "\n")

        texto.config(state="disabled")

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

        resultado_label = tk.Label(
            self.frame_conteudo,
            text="?",
            font=("Arial", 40, "bold"),
            width=5,
            height=2,
            bg="#222222",
            fg="white"
        )
        resultado_label.pack(pady=20)

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
                    self.root.after(i * 150, lambda c=cor: resultado_label.config(bg=c))

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
                    else:
                        texto += "\nPERDEU"
                        info_label.config(text=texto, fg="white")

                    self.atualizar_saldo()
                    btn_girar.config(state="normal")

            loop()

            if final["ganhou"]:
                winsound.Beep(1200, 200)
            else:
                winsound.Beep(400, 200)    

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
            
            info_label.config(text="Girando a roleta...", fg="white")
            btn_girar.config(state="disabled")
            animar_numero(resultado)

        btn_girar = tk.Button(
            self.frame_conteudo,
            text="Girar Roleta",
            font=("Arial", 14),
            command=jogar_roleta
        )
        btn_girar.pack(pady=10)
   
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

        tk.Label(
            frame_esquerda,
            text="Valor da aposta:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack()

        entrada_aposta = tk.Entry(frame_esquerda, font=("Arial", 12), width=18)
        entrada_aposta.pack(pady=5)

        tk.Label(
            frame_esquerda,
            text="Escolha o time:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack(pady=(10, 5))

        nomes_times = [time.nome for time in self.copa_brasil.times]
        time_var = tk.StringVar(value=nomes_times[0])

        menu_times = tk.OptionMenu(frame_esquerda, time_var, *nomes_times)
        menu_times.config(font=("Arial", 12), bg="white", width=14)
        menu_times.pack(pady=5)

        tk.Label(
            frame_esquerda,
            text="Odds dos times:",
            font=("Arial", 12, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=(12, 5))

        texto_odds = tk.Text(
            frame_esquerda,
            width=28,
            height=8,
            font=("Arial", 10),
            wrap="word"
        )
        texto_odds.pack(pady=5)
        texto_odds.config(state="normal")

        for time in self.copa_brasil.times:
            odd = self.copa_brasil.calcular_odd(time)
            texto_odds.insert(tk.END, f"{time.nome} — odd {odd:.1f}\n")

        texto_odds.config(state="disabled")

        tk.Label(
            frame_esquerda,
            text="Tipo de aposta:",
            font=("Arial", 12),
            bg="#145214",
            fg="white"
        ).pack(pady=(12, 5))

        tipo_var = tk.StringVar(value="campeao")

        frame_tipos = tk.Frame(frame_esquerda, bg="#145214")
        frame_tipos.pack(pady=5)

        tk.Radiobutton(
            frame_tipos,
            text="Campeão",
            variable=tipo_var,
            value="campeao",
            bg="#145214",
            fg="white",
            selectcolor="#145214"
        ).pack(anchor="w")

        tk.Radiobutton(
            frame_tipos,
            text="Finalista",
            variable=tipo_var,
            value="finalista",
            bg="#145214",
            fg="white",
            selectcolor="#145214"
        ).pack(anchor="w")

        tk.Radiobutton(
            frame_tipos,
            text="Semifinalista",
            variable=tipo_var,
            value="semifinalista",
            bg="#145214",
            fg="white",
            selectcolor="#145214"
        ).pack(anchor="w")

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

        tk.Label(
            frame_direita,
            text="Resultados do Campeonato",
            font=("Arial", 14, "bold"),
            bg="#145214",
            fg="gold"
        ).pack(pady=(0, 8))

        frame_texto = tk.Frame(frame_direita, bg="#145214")
        frame_texto.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side="right", fill="y")

        resultado_texto = tk.Text(
            frame_texto,
            width=60,
            height=20,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=scrollbar.set
        )
        resultado_texto.pack(side="left", fill="both", expand=True)
        resultado_texto.config(state="disabled")

        scrollbar.config(command=resultado_texto.yview)

        def mostrar_resultado(resultado):
            resultado_texto.config(state="normal")
            resultado_texto.delete("1.0", tk.END)

            resultado_texto.insert(tk.END, "=== QUARTAS DE FINAL ===\n")
            for partida in resultado["quartas"]:
                if partida["penaltis1"] is not None:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🎯 Pênaltis: {partida['penaltis1']} x {partida['penaltis2']}\n"
                        f"🏆 Vencedor: {partida['vencedor']}\n\n"
                    )
                else:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🏆 Vencedor: {partida['vencedor']}\n\n"
                    )

            resultado_texto.insert(tk.END, "=== SEMIFINAL ===\n")
            for partida in resultado["semifinal"]:
                if partida["penaltis1"] is not None:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🎯 Pênaltis: {partida['penaltis1']} x {partida['penaltis2']}\n"
                        f"🏆 Vencedor: {partida['vencedor']}\n\n"
                    )
                else:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🏆 Vencedor: {partida['vencedor']}\n\n"
                    )

            resultado_texto.insert(tk.END, "=== FINAL ===\n")
            for partida in resultado["final"]:
                if partida["penaltis1"] is not None:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🎯 Pênaltis: {partida['penaltis1']} x {partida['penaltis2']}\n"
                        f"🏆 Campeão: {partida['vencedor']}\n\n"
                    )
                else:
                    resultado_texto.insert(
                        tk.END,
                        f"⚽ {partida['time1']} {partida['gols1']} x {partida['gols2']} {partida['time2']}\n"
                        f"🏆 Campeão: {partida['vencedor']}\n\n"
                    )

            resultado_texto.insert(tk.END, f"\n🏆 CAMPEÃO: {resultado['campeao']}\n")
            resultado_texto.insert(tk.END, f"🎯 SUA APOSTA: {resultado['time_escolhido']}\n")
            resultado_texto.insert(tk.END, f"📌 TIPO DE APOSTA: {resultado['tipo_aposta']}\n")
            resultado_texto.insert(tk.END, f"💰 ODD DO SEU TIME: {resultado['odd']:.1f}\n")

            if resultado["ganhou"]:
                resultado_texto.insert(
                    tk.END,
                    f"✅ VOCÊ GANHOU R$ {resultado['premio']:.2f}!\n"
                )
            else:
                resultado_texto.insert(tk.END, "❌ VOCÊ PERDEU A APOSTA.\n")

            resultado_texto.config(state="disabled")

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
            mostrar_resultado(resultado)