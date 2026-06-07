# Trabalho Final de Programação Orientada a Objetos – Cassino Python

## Autores

- Pedro de Oliveira Rodrigues Filho
- Gabriel Boldt Afonso

O sistema simula um cassino virtual em Python, com interface gráfica em Tkinter, múltiplos jogos, controle de saldo, histórico de jogadas e persistência de dados em JSON.

## Jogos disponíveis

- Roleta
- Caça-Níquel
- Copa do Brasil
- Bozó

## Funcionalidades

- Cadastro de jogador
- Depósito e saque
- Controle de saldo
- Histórico de jogadas
- Salvamento e carregamento de dados em JSON
- Interface gráfica com Tkinter
- Menu de jogos
- Sistema de apostas

## Conceitos de POO utilizados

- Classes e objetos
- Herança
- Polimorfismo
- Classe abstrata
- Encapsulamento
- Getters e setters
- Separação de responsabilidades

## Estrutura do projeto

TrabalhoPOO/
├── main.py
├── interface.py
├── jogador.py
├── banco_dados.py
├── dados/
│   └── jogador.json
└── jogos/
    ├── __init__.py
    ├── jogo.py
    ├── roleta.py
    ├── caca_niquel.py
    ├── copa_brasil.py
    └── bozo.py