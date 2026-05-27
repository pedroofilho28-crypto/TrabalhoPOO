import random
from collections import Counter
from jogos.jogo import Jogo

# Nesse código possuimos 2 classes a Bozó e a Cartela do jogo:
# - Classe CartelaBozo
#   Representa a cartela de pontuação do jogador ou do cassino.
#   Responsabilidades:
#       - Armazenar as casas de pontuação do Bozó
#       - Verificar quais casas ainda estão disponíveis
#       - Marcar pontos em uma casa escolhida
#       - Calcular a pontuação total da cartela
# - Classe Bozo
#   Representa o jogo Bozó contra o cassino.
#   Responsabilidades:
#       - Controlar as regras principais do Bozó
#       - Rolar os dados do jogador e do cassino
#       - Calcular a pontuação de cada casa
#       - Controlar a jogada automática do cassino
#       - Iniciar e finalizar partidas com aposta
#       - Registrar o resultado no histórico do jogador

class CartelaBozo:
    def __init__(self):
        self.pontuacoes = {
            "as": None,
            "duque": None,
            "terno": None,
            "quadra": None,
            "quina": None,
            "sena": None,
            "full": None,
            "seguida": None,
            "quadrada": None,
            "general": None
        }

    def casas_disponiveis(self):
        return [casa for casa, valor in self.pontuacoes.items() if valor is None]

    def marcar(self, casa, pontos):
        if casa not in self.pontuacoes:
            return False

        if self.pontuacoes[casa] is not None:
            return False

        self.pontuacoes[casa] = pontos
        return True

    def total(self):
        return sum(valor for valor in self.pontuacoes.values() if valor is not None)

    def completa(self):
        return all(valor is not None for valor in self.pontuacoes.values())


class Bozo(Jogo):
    def __init__(self, nome="Bozó", aposta_minima=10):
        super().__init__(nome, aposta_minima)

    def jogar(self, jogador, valor_aposta, *args):
        return self.iniciar_partida(jogador, valor_aposta)

    def rolar_dados(self, quantidade=5):
        return [random.randint(1, 6) for _ in range(quantidade)]

    def calcular_pontos(self, dados, casa):
        contagem = Counter(dados)
        ordenados = sorted(dados)
        valores_contagem = sorted(contagem.values())

        if casa == "as":
            return dados.count(1) * 1

        elif casa == "duque":
            return dados.count(2) * 2

        elif casa == "terno":
            return dados.count(3) * 3

        elif casa == "quadra":
            return dados.count(4) * 4

        elif casa == "quina":
            return dados.count(5) * 5

        elif casa == "sena":
            return dados.count(6) * 6

        elif casa == "full":
            return 20 if valores_contagem == [2, 3] else 0

        elif casa == "seguida":
            return 30 if ordenados in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) else 0

        elif casa == "quadrada":
            return 40 if 4 in contagem.values() else 0

        elif casa == "general":
            return 50 if 5 in contagem.values() else 0

        return 0

    def melhor_casa_para_cassino(self, dados, cartela):
        melhor_casa = None
        melhor_pontos = -1

        for casa in cartela.casas_disponiveis():
            pontos = self.calcular_pontos(dados, casa)

            if pontos > melhor_pontos:
                melhor_pontos = pontos
                melhor_casa = casa

        return melhor_casa, melhor_pontos

    def jogar_turno_cassino(self, cartela):
        dados = self.rolar_dados()

        for _ in range(2):
            contagem = Counter(dados)
            numero_mais_comum, quantidade = contagem.most_common(1)[0]

            dados_guardados = [dado for dado in dados if dado == numero_mais_comum]
            quantidade_rerrolar = 5 - len(dados_guardados)

            dados = dados_guardados + self.rolar_dados(quantidade_rerrolar)

        casa, pontos = self.melhor_casa_para_cassino(dados, cartela)
        cartela.marcar(casa, pontos)

        return {
            "dados": dados,
            "casa": casa,
            "pontos": pontos
        }

    def iniciar_partida(self, jogador, valor_aposta):
        if valor_aposta < self.aposta_minima:
            return {"erro": f"A aposta mínima é R$ {self.aposta_minima:.2f}"}

        if not jogador.sacar(valor_aposta):
            return {"erro": "Saldo insuficiente."}

        return {
            "cartela_jogador": CartelaBozo(),
            "cartela_cassino": CartelaBozo(),
            "valor_aposta": valor_aposta,
            "rodada": 1
        }

    def finalizar_partida(self, jogador, cartela_jogador, cartela_cassino, valor_aposta):
        total_jogador = cartela_jogador.total()
        total_cassino = cartela_cassino.total()

        ganhou = total_jogador > total_cassino
        empatou = total_jogador == total_cassino
        premio = 0

        if ganhou:
            premio = valor_aposta * 2
            jogador.receber_premio(premio)
        elif empatou:
            premio = valor_aposta
            jogador.receber_premio(premio)

        jogador.registrar_jogada(
            f"Bozó | aposta: R$ {valor_aposta:.2f} | "
            f"jogador: {total_jogador} | cassino: {total_cassino} | "
            f"resultado: {'GANHOU' if ganhou else 'EMPATOU' if empatou else 'PERDEU'} | "
            f"saldo: R$ {jogador.saldo:.2f}"
        )

        return {
            "total_jogador": total_jogador,
            "total_cassino": total_cassino,
            "ganhou": ganhou,
            "empatou": empatou,
            "premio": premio
        }