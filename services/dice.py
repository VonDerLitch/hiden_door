import time
import random

class Dice:
    @staticmethod
    def rolar_dados(num_dados=4, lados=6):
        """Rola um número de dados com a quantidade de lados especificada."""
        return [random.randint(1, lados) for _ in range(num_dados)]

    @staticmethod
    def criar_caracteristicas():
        """Cria características rolando 4d6 e somando os 3 maiores, retornando o texto para a GUI."""
        resultado = []
        for c in range(1, 7): 
            dados = Dice.rolar_dados()
            tres_maiores = sorted(dados, reverse=True)[:3]
            soma = sum(tres_maiores)
            linha = f"Rolagem {c}: Dados: {dados} → Soma dos 3 maiores: {soma}"
            resultado.append(linha)
        return "\n".join(resultado)

    @staticmethod
    def jogar_d20():
        """Simula o lançamento de um dado de 20 lados e retorna o resultado."""
        return random.randint(1, 20)
