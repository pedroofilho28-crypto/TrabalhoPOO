# Classe Jogador
# Representa um jogador dentro do cassino.
# Oq ela faz:
# - Armazenar nome e saldo
# - Permitir depósitos e saques
# - Registrar histórico de jogadas
# - Atualizar saldo ao ganhar 

class Jogador:
    def __init__(self, nome, saldo):
        self.nome = nome
        self.saldo = saldo
        self.historico = []

    def depositar(self, valor):
        if valor <= 0:
            return False
        
        self.saldo += valor
        return True

    def sacar(self, valor):
        if valor <= 0:
            return False
        
        if valor > self.saldo:
            return False
        
        self.saldo -= valor
        return True
    
    def receber_premio(self, valor):
        if valor > 0:
            self.saldo += valor

    def registrar_jogada(self, descricao):
        self.historico.append(descricao)

    def exibir_dados(self):
        print(f"Jogador: {self.nome}")
        print(f"Saldo atual: {self.saldo: .2f}")