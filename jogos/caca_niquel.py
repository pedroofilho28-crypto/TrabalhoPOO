from jogos.jogo import Jogo
import random

# Classe CacaNiquel
# Implementa o jogo de caça-níquel em grade 3x3.
# Oq faz:
# - Sortear símbolos em uma matriz 3x3
# - Verificar prêmios nas 3 linhas horizontais
# - Aplicar bônus especiais
# - Controlar jackpot acumulado
# - Registrar histórico das jogadas

class CacaNiquel(Jogo):
    def __init__(self, nome="Caça-Níquel", aposta_minima=5):
        super().__init__(nome, aposta_minima)
        self.simbolos = ["🍒", "🍋", "🔔", "7", "⭐"]
        self.jackpot = 500.0

    def girar(self):
        return [
            [random.choice(self.simbolos) for _ in range(3)]
            for _ in range(3)
        ]

    def calcular_resultado_linha(self, linha, valor_aposta):
        if linha == ["7", "7", "7"]:
            premio = self.jackpot
            self.jackpot = 500.0
            return premio, "jackpot", False

        elif linha == ["⭐", "⭐", "⭐"]:
            return valor_aposta * 6, "super_premio", False

        elif linha == ["🍒", "🍒", "🍒"]:
            return valor_aposta * 5, "rodada_gratis", True

        elif linha == ["🔔", "🔔", "🔔"]:
            return valor_aposta * 5, "sino_dourado", False

        elif linha[0] == linha[1] == linha[2]:
            return valor_aposta * 4, "tripla", False

        else:
            return 0, "perdeu", False

    def jogar(self, jogador, valor_aposta, usar_rodada_gratis=False, *args):
        if not usar_rodada_gratis:
            if valor_aposta < self.aposta_minima:
                return {"erro": f"A aposta mínima é R$ {self.aposta_minima:.2f}"}

            if not jogador.sacar(valor_aposta):
                return {"erro": "Saldo insuficiente."}

            self.jackpot += 3.0

        resultado = self.girar()

        combinacoes = [
            ("linha", 0, resultado[0]),
            ("linha", 1, resultado[1]),
            ("linha", 2, resultado[2]),

            ("coluna", 0, [resultado[0][0], resultado[1][0], resultado[2][0]]),
            ("coluna", 1, [resultado[0][1], resultado[1][1], resultado[2][1]]),
            ("coluna", 2, [resultado[0][2], resultado[1][2], resultado[2][2]]),

            ("diagonal", 0, [resultado[0][0], resultado[1][1], resultado[2][2]]),
            ("diagonal", 1, [resultado[0][2], resultado[1][1], resultado[2][0]])
        ]

        premio_total = 0
        rodada_gratis = False
        combinacoes_premiadas = []
        tipos_resultado = []

        for tipo_combinacao, indice, valores in combinacoes:
            premio, tipo_resultado, ganhou_rodada_gratis = self.calcular_resultado_linha(valores, valor_aposta)

            if premio > 0:
                premio_total += premio
                combinacoes_premiadas.append({
                    "tipo": tipo_combinacao,
                    "indice": indice
                })
                tipos_resultado.append(tipo_resultado)

            if ganhou_rodada_gratis:
                rodada_gratis = True

        bonus_multilinha = 0
        if len(combinacoes_premiadas) >= 2:
            bonus_multilinha = valor_aposta * len(combinacoes_premiadas)
            premio_total += bonus_multilinha
            tipos_resultado.append("multilinha")

        ganhou = premio_total > 0

        if ganhou:
            jogador.receber_premio(premio_total)

        if "jackpot" in tipos_resultado:
            tipo_principal = "jackpot"
        elif "super_premio" in tipos_resultado:
            tipo_principal = "super_premio"
        elif "rodada_gratis" in tipos_resultado:
            tipo_principal = "rodada_gratis"
        elif "sino_dourado" in tipos_resultado:
            tipo_principal = "sino_dourado"
        elif "tripla" in tipos_resultado:
            tipo_principal = "tripla"
        elif "dupla" in tipos_resultado:
            tipo_principal = "dupla"
        elif "multilinha" in tipos_resultado:
            tipo_principal = "multilinha"
        else:
            tipo_principal = "perdeu"

        resultado_formatado = " / ".join([" | ".join(linha) for linha in resultado])
        origem = "Rodada grátis" if usar_rodada_gratis else "Aposta normal"

        jogador.registrar_jogada(
            f"Caça-Níquel 3x3 | {origem} | aposta: R$ {valor_aposta:.2f} | "
            f"resultado: {resultado_formatado} | prêmio total: R$ {premio_total:.2f} | "
            f"combinações premiadas: {combinacoes_premiadas if combinacoes_premiadas else 'nenhuma'} | "
            f"bônus multilinha: R$ {bonus_multilinha:.2f} | "
            f"jackpot atual: R$ {self.jackpot:.2f} | saldo: R$ {jogador.saldo:.2f}"
        )

        return {
            "grade": resultado,
            "ganhou": ganhou,
            "premio": premio_total,
            "tipo_resultado": tipo_principal,
            "rodada_gratis": rodada_gratis,
            "jackpot_atual": self.jackpot,
            "combinacoes_premiadas": combinacoes_premiadas,
            "bonus_multilinha": bonus_multilinha
        }