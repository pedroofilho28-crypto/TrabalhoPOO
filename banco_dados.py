import json
import os
from jogador import Jogador

# - Arquivo banco_dados
# - Responsável por salvar e carregar os dados do jogador em arquivo JSON.
#   Responsabilidades:
#       - Criar a pasta de dados, caso ela ainda não exista
#       - Salvar nome, saldo e histórico do jogador
#       - Carregar um jogador salvo anteriormente
#       - Permitir persistência dos dados mesmo após fechar o programa

CAMINHO_ARQUIVO = "dados/jogador.json"


def salvar_jogador(jogador):
    os.makedirs("dados", exist_ok=True)

    dados = {
        "nome": jogador.nome,
        "saldo": jogador.saldo,
        "historico": jogador.historico
    }

    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def carregar_jogador():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return None

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    jogador = Jogador(dados["nome"], dados["saldo"])

    for jogada in dados.get("historico", []):
        jogador.registrar_jogada(jogada)

    return jogador