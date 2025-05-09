from services.books import Books

def exibir_menu():
    print("Bem-vindo! Escolha uma das opções abaixo:")
    print("1. Livros")
    print("2. Rolar Dados")
    print("3. Lista de Magias")
    print("0. Sair")

def opcao_livros():
    books = Books()
    pdfs = books.list_books()
    if not pdfs:
        print("Nenhum livro encontrado.")
        return
    print("Livros disponíveis:")
    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf}")
    print("a. Baixar todos os livros")
    print("0. Voltar")
    escolha = input("Digite o número do livro para baixar, 'a' para todos ou '0' para voltar: ")
    dest_dir = None

    if escolha == "a":
        books.download_all_books(dest_dir)
        print("Download concluído. Pressione qualquer tecla para continuar.")
        input()
    elif escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(pdfs):
            books.download_book(pdfs[idx])
            print("Download concluído. Pressione qualquer tecla para continuar.")
            input()
        else:
            print("Opção inválida.")
    elif escolha == "0":
        return
    else:
        print("Opção inválida.")

def opcao_rolar_dados():
    print("Você escolheu a opção 'Rolar Dados'.")
    # Adicione aqui a lógica para rolar dados

def opcao_lista_de_magias():
    print("Você escolheu a opção 'Lista de Magias'.")
    # Adicione aqui a lógica para a lista de magias

def main():
    while True:
        exibir_menu()
        escolha = input("Digite o número da sua escolha: ")

        if escolha == "1":
            opcao_livros()
        elif escolha == "2":
            opcao_rolar_dados()
        elif escolha == "3":
            opcao_lista_de_magias()
        elif escolha == "0":
            print("Saindo... Até a próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()