import random
from jogos.jogo import Jogo

class Time:
    def __init__(self, nome, forca):
        self.nome = nome
        self.forca = forca

    def __str__(self):
        return self.nome

class Partida:
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.vencedor = None
        self.perdedor = None
        self.gols_time1 = 0
        self.gols_time2 = 0
        self.penaltis_time1 = None
        self.penaltis_time2 = None

    def jogar(self):
        self.gols_time1 = random.randint(0, 3)
        self.gols_time2 = random.randint(0, 3)

        if self.gols_time1 > self.gols_time2:
            self.vencedor = self.time1
            self.perdedor = self.time2

        elif self.gols_time2 > self.gols_time1:
            self.vencedor = self.time2
            self.perdedor = self.time1

        else:
            self.penaltis_time1 = random.randint(3, 5)
            self.penaltis_time2 = random.randint(3, 5)

            while self.penaltis_time1 == self.penaltis_time2:
                self.penaltis_time1 = random.randint(3, 5)
                self.penaltis_time2 = random.randint(3, 5)

            if self.penaltis_time1 > self.penaltis_time2:
                self.vencedor = self.time1
                self.perdedor = self.time2
            else:
                self.vencedor = self.time2
                self.perdedor = self.time1

        return self.vencedor

class CopaDoBrasil(Jogo):
    def __init__(self, nome="Copa do Brasil", aposta_minima=10):
        super().__init__(nome, aposta_minima)
        self.times = [
            Time("Flamengo", 78),
            Time("Palmeiras", 12),
            Time("Atlético-MG", 74),
            Time("Cruzeiro", 76),
            Time("Fluminense", 72),
            Time("São Paulo", 90),
            Time("Corinthians", 80),
            Time("Cuiabá", 70),
        ]

    def criar_confrontos(self, lista_times):
        confrontos = []
        for i in range(0, len(lista_times), 2):
            confrontos.append(Partida(lista_times[i], lista_times[i + 1]))
        return confrontos

    def simular_rodada(self, lista_times, nome_rodada):
        confrontos = self.criar_confrontos(lista_times)
        vencedores = []
        resultados = []

        for partida in confrontos:
            vencedor = partida.jogar()
            vencedores.append(vencedor)

            resultados.append({
                "time1": partida.time1.nome,
                "time2": partida.time2.nome,
                "gols1": partida.gols_time1,
                "gols2": partida.gols_time2,
                "penaltis1": partida.penaltis_time1,
                "penaltis2": partida.penaltis_time2,
                "vencedor": vencedor.nome
            })

        return {
            "rodada": nome_rodada,
            "resultados": resultados,
            "vencedores": vencedores
        }

    def jogar(self, jogador, valor_aposta, nome_time_escolhido, tipo_aposta, *args):
        if valor_aposta < self.aposta_minima:
            return {"erro": f"A aposta mínima é R$ {self.aposta_minima:.2f}"}

        if not jogador.sacar(valor_aposta):
            return {"erro": "Saldo insuficiente."}

        time_escolhido = None
        for time in self.times:
            if time.nome.lower() == nome_time_escolhido.lower():
                time_escolhido = time
                break

        if time_escolhido is None:
            jogador.receber_premio(valor_aposta)
            return {"erro": "Time inválido."}
        
        odd_time = self.calcular_odd(time_escolhido, tipo_aposta)

        times_embaralhados = self.times[:]
        random.shuffle(times_embaralhados)

        quartas = self.simular_rodada(times_embaralhados, "Quartas de Final")
        semifinal = self.simular_rodada(quartas["vencedores"], "Semifinal")
        final = self.simular_rodada(semifinal["vencedores"], "Final")

        campeao = final["vencedores"][0]

        finalistas = [
            final["resultados"][0]["time1"],
            final["resultados"][0]["time2"]
        ]

        semifinalistas = [time.nome for time in quartas["vencedores"]]

        ganhou = False

        if tipo_aposta == "campeao":
            ganhou = campeao.nome.lower() == time_escolhido.nome.lower()

        elif tipo_aposta == "finalista":
            ganhou = time_escolhido.nome in finalistas

        elif tipo_aposta == "semifinalista":
            ganhou = time_escolhido.nome in semifinalistas

        premio = 0

        if ganhou:
            premio = valor_aposta * odd_time
            jogador.receber_premio(premio)

        resultado_texto = "GANHOU" if ganhou else "PERDEU"

        jogador.registrar_jogada(
            f"Copa do Brasil | aposta: R$ {valor_aposta:.2f} | "
            f"time escolhido: {time_escolhido.nome} | campeão: {campeao.nome} | "
            f"resultado: {resultado_texto} | saldo: R$ {jogador.saldo:.2f}"
        )

        return {
            "quartas": quartas["resultados"],
            "semifinal": semifinal["resultados"],
            "final": final["resultados"],
            "campeao": campeao.nome,
            "time_escolhido": time_escolhido.nome,
            "tipo_aposta": tipo_aposta,
            "odd": odd_time,
            "ganhou": ganhou,
            "premio": premio
        }
    
    
    def calcular_odd(self, time, tipo_aposta="campeao"):
        if time.forca >= 88:
            base = 2.0
        elif time.forca >= 74:
            base = 3.0
        elif time.forca >= 70:
            base = 4.0
        else:
            base = 5.0

        if tipo_aposta == "campeao":
            return base
        elif tipo_aposta == "finalista":
            return base * 0.6
        elif tipo_aposta == "semifinalista":
            return base * 0.4