from abc import ABC, abstractmethod

# - Classe abstrata Jogo
#   Serve como base para todos os jogos do cassino.
#   Responsabilidades:
#       - Definir atributos comuns, como nome e aposta mínima
#       - Garantir que todos os jogos implementem o método jogar()
#       - Aplicar herança e polimorfismo no projeto
#       - Fornecer getters e setters para encapsulamento

class Jogo(ABC):
    def __init__(self, nome, aposta_minima):
        self.__nome = nome
        self.__aposta_minima = aposta_minima

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if nome.strip():
            self.__nome = nome

    def get_aposta_minima(self):
        return self.__aposta_minima

    def set_aposta_minima(self, aposta_minima):
        if aposta_minima > 0:
            self.__aposta_minima = aposta_minima

    @abstractmethod
    def jogar(self, jogador, valor_aposta, *args):
        pass

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.set_nome(nome)

    @property
    def aposta_minima(self):
        return self.__aposta_minima

    @aposta_minima.setter
    def aposta_minima(self, aposta_minima):
        self.set_aposta_minima(aposta_minima)