from jogos.roleta import Roleta
from jogos.caca_niquel import CacaNiquel

# Bem opcional, to quase tirando isso
# Classe Cassino
# Representa o cassino como sistema principal.
# Oq ela faz:
# - Armazenar nome do cassino
# - Manter a lista de jogadores cadastrados
# - Manter a lista de jogos disponíveis

class Cassino:
    def __init__(self, nome):
        self.nome = nome
        self.jogadores = []
        self.jogos = []

        self.roleta = Roleta()
        self.caca_niquel = CacaNiquel()

        self.adicionar_jogo(self.roleta)
        self.adicionar_jogo(self.caca_niquel)

    def cadastrar_jogador(self, jogador):
        self.jogadores.append(jogador)

    def adicionar_jogo(self, jogo):
        self.jogos.append(jogo)

    def listar_jogos(self):
        return [jogo.nome for jogo in self.jogos]