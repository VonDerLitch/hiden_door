import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
from services.books import Books
from services.dice import Dice

def centralizar_janela(janela, largura=450, altura=450):
    """Centraliza a janela na tela."""
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def abrir_janela(func):
    """Abre uma nova janela centralizada e executa a função de conteúdo."""
    root.withdraw()
    nova_janela = tk.Toplevel()
    centralizar_janela(nova_janela)
    nova_janela.title("Hidden Door - Submenu")

    def fechar():
        nova_janela.destroy()
        root.deiconify()

    btn_voltar = tk.Button(nova_janela, text="Voltar", command=fechar)
    btn_voltar.pack(side="bottom", pady=10)
    func(nova_janela)

def abrir_livros(janela):
    """Exibe a lista de livros com barra de rolagem responsiva."""
    books = Books()
    pdfs = books.list_books()

    if not pdfs:
        tk.Label(janela, text="Nenhum livro encontrado.").pack()
        return

    tk.Label(janela, text="Livros disponíveis:").pack(pady=5)

    # Frame com barra de rolagem responsiva
    container = tk.Frame(janela)
    container.pack(fill="both", expand=True, padx=5, pady=5)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(container)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Adiciona botões para cada livro
    for nome in pdfs:
        tk.Button(
            scrollable_frame,
            text=nome,
            width=40,
            anchor="w",
            command=lambda n=nome: baixar_livro(n, books)
        ).pack(pady=2, fill="x", expand=True)

    tk.Button(
        janela,
        text="Baixar Todos os Livros",
        command=lambda: baixar_todos(books)
    ).pack(pady=5)

def baixar_livro(nome, books):
    """Baixa um livro e oferece opção de abrir."""
    caminho = books.download_book(nome)
    if caminho and os.path.exists(caminho):
        abrir = messagebox.askyesno("Download concluído", f"Livro baixado:\n{caminho}\n\nDeseja abrir?")
        if abrir:
            webbrowser.open(caminho)
    else:
        messagebox.showinfo("Erro", f"Não foi possível localizar o livro em:\n{caminho}")

def baixar_todos(books):
    """Baixa todos os livros."""
    books.download_all_books()
    messagebox.showinfo("Download", "Todos os livros foram baixados com sucesso.")

def rolar_dados(janela):
    """Menu de rolagem de dados."""
    tk.Label(janela, text="Rolar Dados", font=("Arial", 12)).pack(pady=5)
    resultado_var = tk.StringVar(value="Resultado aparecerá aqui.")

    def criar_caracteristicas():
        resultado = Dice.criar_caracteristicas()
        resultado_var.set(str(resultado) if resultado else "Função não retornou nada. Verifique o método.")

    def jogar_d20():
        resultado = Dice.jogar_d20()
        resultado_var.set(f"Você rolou um {resultado}" if resultado else "Função não retornou valor.")

    tk.Button(janela, text="Criar Características", command=criar_caracteristicas).pack(pady=5)
    tk.Button(janela, text="Jogar D20", command=jogar_d20).pack(pady=5)
    tk.Label(janela, textvariable=resultado_var, wraplength=400, fg="blue").pack(pady=10)

def abrir_magias(janela):
    """Menu de magias (não implementado)."""
    tk.Label(janela, text="Função ainda não implementada.").pack(pady=20)

def sair():
    """Fecha a aplicação."""
    root.destroy()

def main():
    """Função principal da interface."""
    global root
    root = tk.Tk()
    root.title("Hidden Door - Menu Principal")
    centralizar_janela(root)

    tk.Label(root, text="Escolha uma opção:", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="1. Livros", width=25, command=lambda: abrir_janela(abrir_livros)).pack(pady=5)
    tk.Button(root, text="2. Rolar Dados", width=25, command=lambda: abrir_janela(rolar_dados)).pack(pady=5)
    tk.Button(root, text="3. Lista de Magias", width=25, command=lambda: abrir_janela(abrir_magias)).pack(pady=5)
    tk.Button(root, text="0. Sair", width=25, command=sair).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()