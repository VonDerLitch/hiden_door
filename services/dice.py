import time
import random
class Dice:
    def rolar_dados(num_dados=4, lados=6):
        """Rola um número de dados com a quantidade de lados especificada."""
        return [random.randint(1, lados) for _ in range(num_dados)]

    def criar_caracteristicas():
        """Cria características rolando 4 dados de 6 lados e somando os 3 maiores."""
        print('Criando suas características...')
        for c in range(1, 7): 
            dados = Dice.rolar_dados()
            tres_maiores = sorted(dados, reverse=True)[:3]
            soma = sum(tres_maiores)
            time.sleep(1)
            print(f"Rolagem {c}: Dados: {dados} total: {soma}")

    def jogar_d20():
        """Simula o lançamento de um dado de 20 lados."""
        print('Jogando um dado de 20 lados...')
        resultado = random.randint(1, 20)
        print(f"> > {resultado} < <")




