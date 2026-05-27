# - Classe Jogador
#   Representa um jogador dentro do cassino.
#   Responsabilidades:
#       - Armazenar o nome, saldo e histórico do jogador
#       - Permitir depósitos e saques
#       - Atualizar o saldo ao receber prêmios
#       - Registrar o histórico das jogadas realizadas
#       - Fornecer getters e setters para encapsulamento

class Jogador:

    def __init__(self, nome, saldo):
        self.__nome = nome
        self.__saldo = saldo
        self.__historico = []

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if nome.strip():
            self.__nome = nome

    def get_saldo(self):
        return self.__saldo

    def set_saldo(self, saldo):
        if saldo >= 0:
            self.__saldo = saldo

    def get_historico(self):
        return self.__historico

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor <= 0:
            return False

        if valor > self.__saldo:
            return False

        self.__saldo -= valor
        return True

    def receber_premio(self, valor):
        if valor > 0:
            self.__saldo += valor

    def registrar_jogada(self, descricao):
        self.__historico.append(descricao)

    def exibir_dados(self):
        print(f"Jogador: {self.__nome}")
        print(f"Saldo atual: R$ {self.__saldo:.2f}")

    def mostrar_historico(self):
        if not self.__historico:
            print("Nenhuma jogada registrada.")
            return

        for jogada in self.__historico:
            print(jogada)

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.set_nome(nome)

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo):
        self.set_saldo(saldo)

    @property
    def historico(self):
        return self.__historico