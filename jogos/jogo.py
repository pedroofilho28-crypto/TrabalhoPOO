from abc import ABC, abstractmethod

# Classe abstrata Jogo
# Serve como base para todos os jogos do cassino.
# Oq faz:
# - Definir atributos comuns aos jogos
# - Garantir que cada jogo implemente o método jogar()

class Jogo(ABC):
    def __init__(self, nome, aposta_minima):
        self.nome = nome
        self.aposta_minima = aposta_minima

    @abstractmethod
    def jogar(self, jogador, valor_aposta, *args):
        pass