from jogos.jogo import Jogo
import random

# - Classe Roleta
#   Representa o jogo de roleta do cassino.
#   Responsabilidades:
#       - Sortear um número entre 0 e 36
#       - Determinar a cor, a paridade e a faixa do número sorteado
#       - Validar os diferentes tipos de aposta do jogador
#       - Calcular o resultado da aposta e o valor do prêmio
#       - Atualizar o saldo do jogador em caso de vitória
#       - Registrar o histórico das jogadas realizadas

class Roleta(Jogo):
    def __init__(self, nome="Roleta", aposta_minima=10):
        super().__init__(nome, aposta_minima)

        self.numeros_vermelhos = {
            1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36
        }

    def cor_numero(self, numero):
        if numero == 0:
            return "verde"
        elif numero in self.numeros_vermelhos:
            return "vermelho"
        else:
            return "preto"

    def paridade_numero(self, numero):
        if numero == 0:
            return "nenhum"
        elif numero % 2 == 0:
            return "par"
        else:
            return "impar"

    def faixa_numero(self, numero):
        if numero == 0:
            return "nenhuma"

        inicio = ((numero - 1) // 4) * 4 + 1
        fim = inicio + 3

        return f"{inicio}-{fim}"

    def validar_aposta(self, tipo_aposta, escolha):
        if tipo_aposta == "numero":
            try:
                numero = int(escolha)
                return 0 <= numero <= 36
            except ValueError:
                return False

        elif tipo_aposta == "cor":
            return escolha in ["vermelho", "preto"]

        elif tipo_aposta == "paridade":
            return escolha in ["par", "impar"]

        elif tipo_aposta == "faixa":
            return escolha in ["1-4", "5-8", "9-12", "13-16", "17-20", "21-24",
        "25-28", "29-32", "33-36"]

        return False

    def jogar(self, jogador, valor_aposta, tipo_aposta, escolha):
        if valor_aposta < self.aposta_minima:
            return {"erro": f"A aposta mínima é R$ {self.aposta_minima:.2f}"}

        if not self.validar_aposta(tipo_aposta, escolha):
            return {"erro": "Aposta inválida."}

        if not jogador.sacar(valor_aposta):
            return {"erro": "Saldo insuficiente."}

        numero_sorteado = random.randint(0, 36)
        cor_sorteada = self.cor_numero(numero_sorteado)
        paridade_sorteada = self.paridade_numero(numero_sorteado)
        faixa_sorteada = self.faixa_numero(numero_sorteado)

        ganhou = False
        premio = 0

        if tipo_aposta == "numero":
            escolha = int(escolha)
            if escolha == numero_sorteado:
                ganhou = True
                premio = valor_aposta * 35

        elif tipo_aposta == "cor":
            if escolha == cor_sorteada:
                ganhou = True
                premio = valor_aposta * 2

        elif tipo_aposta == "paridade":
            if escolha == paridade_sorteada:
                ganhou = True
                premio = valor_aposta * 2

        elif tipo_aposta == "faixa":
            if escolha == faixa_sorteada:
                ganhou = True
                premio = valor_aposta * 9

        if ganhou:
            jogador.receber_premio(premio)

        jogador.registrar_jogada(
            f"Roleta | aposta: R$ {valor_aposta:.2f} | tipo: {tipo_aposta} | escolha: {escolha} | sorteado: {numero_sorteado} | resultado: {'GANHOU' if ganhou else 'PERDEU'} | saldo: R$ {jogador.saldo:.2f}"
        )

        return {
            "numero": numero_sorteado,
            "cor": cor_sorteada,
            "paridade": paridade_sorteada,
            "faixa": faixa_sorteada,
            "ganhou": ganhou,
            "premio": premio
        }