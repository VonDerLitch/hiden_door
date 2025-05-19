import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
from services.books import Books
from services.dice import Dice
from PIL import Image, ImageTk
import importlib.util
from tkinter import ttk


def centralizar_janela(janela, largura=800, altura=600):
    """Centraliza a janela na tela e fixa o tamanho."""
    if isinstance(janela, (tk.Tk, tk.Toplevel)):
        janela.update_idletasks()
    else:
        raise ValueError("The 'janela' parameter must be a valid Tk or Toplevel instance.")
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela //2) - (largura //2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.minsize(largura, altura)
    janela.maxsize(largura, altura)

def abrir_janela(func, root):
    root.withdraw()
    nova_janela = tk.Toplevel()
    centralizar_janela(nova_janela, 800, 600)
    nova_janela.title("Hidden Door - Submenu")

    def fechar():
        nova_janela.destroy()
        root.deiconify()

    btn_voltar = tk.Button(nova_janela, text="Voltar", command=fechar)
    btn_voltar.pack(side="bottom", pady=10)
    func(nova_janela)

def abrir_livros(janela):
    """Exibe a lista de livros centralizada com barra de rolagem responsiva."""
    # Frame centralizado
    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    books = Books()
    pdfs = books.list_books()

    if not pdfs:
        tk.Label(frame, text="Nenhum livro encontrado.").pack()
        return

    tk.Label(frame, text="Livros disponíveis:").pack(pady=5)

    # Frame com barra de rolagem responsiva
    container = tk.Frame(frame)
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
        frame,
        text="Baixar Todos os Livros",
        command=lambda: baixar_todos(books)
    ).pack(pady=5)

def baixar_livro(nome, books):
    """Baixa um livro e oferece opção de abrir."""
    caminho = books.download_book(nome)
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
    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")
    tk.Label(frame, text="Rolar Dados", font=("Arial", 12)).pack(pady=5)
    resultado_var = tk.StringVar(value="Resultado aparecerá aqui.")

    def criar_caracteristicas():
        resultado = Dice.criar_caracteristicas()
        resultado_var.set(str(resultado) if resultado else "Função não retornou nada. Verifique o método.")

    def jogar_d20():
        resultado = Dice.jogar_d20()
        resultado_var.set(f"Você rolou um {resultado}" if resultado else "Função não retornou valor.")

    tk.Button(frame, text="Criar Características", command=criar_caracteristicas).pack(pady=5)
    tk.Button(frame, text="Jogar D20", command=jogar_d20).pack(pady=5)
    tk.Label(frame, textvariable=resultado_var, wraplength=400, fg="blue").pack(pady=10)

def extrair_nivel(descricao):
    for linha in descricao.splitlines():
        if linha.strip().isdigit():
            return linha.strip()
        if any(linha.lower().startswith(escola) for escola in [
            "abjuração", "adivinhação", "conjuração", "encantamento", "evocação", "ilusão", "necromancia", "transmutação"
        ]):
            partes = linha.split()
            if partes and partes[-1].isdigit():
                return partes[-1]
    return ""

def abrir_magias(janela):
    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    # Caminho para a pasta de magias
    PASTA_MAGIAS = r"D:\Projetos_Py\hiden_door\data\Magias"

    # Carrega todas as magias e descrições
    magias_lista = []
    for nome_arquivo in os.listdir(PASTA_MAGIAS):
        if nome_arquivo.endswith('.py'):
            caminho = os.path.join(PASTA_MAGIAS, nome_arquivo)
            spec = importlib.util.spec_from_file_location("modulo_temp", caminho)
            if spec is not None and spec.loader is not None:
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                classe = list(modulo.MAGIAS.keys())[0]
                for nome_magia in modulo.MAGIAS[classe]:
                    desc = modulo.DESCRICOES_MAGIAS.get(nome_magia, "")
                    nivel = extrair_nivel(desc)
                    magias_lista.append({
                        "classe": classe,
                        "nome": nome_magia,
                        "nivel": nivel,
                        "descricao": desc
                    })

    # Descobre classes e níveis únicos
    classes = sorted(set(m["classe"] for m in magias_lista))
    niveis = sorted(set(m["nivel"] for m in magias_lista if m["nivel"]))

    # Widgets de filtro
    filtro_frame = tk.Frame(frame)
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Classe:").grid(row=0, column=0, padx=2)
    classe_var = tk.StringVar()
    classe_combo = ttk.Combobox(filtro_frame, values=[""] + classes, textvariable=classe_var, state="readonly")
    classe_combo.grid(row=0, column=1, padx=2)
    classe_combo.set("")

    tk.Label(filtro_frame, text="Nível:").grid(row=0, column=2, padx=2)
    nivel_var = tk.StringVar()
    nivel_combo = ttk.Combobox(filtro_frame, values=[""] + niveis, textvariable=nivel_var, state="readonly")
    nivel_combo.grid(row=0, column=3, padx=2)
    nivel_combo.set("")

    tk.Label(filtro_frame, text="Nome:").grid(row=0, column=4, padx=2)
    nome_var = tk.StringVar()
    tk.Entry(filtro_frame, textvariable=nome_var, width=15).grid(row=0, column=5, padx=2)

    # Listbox para mostrar magias
    lista_magias = tk.Listbox(frame)
    lista_magias.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def atualizar_lista():
        lista_magias.delete(0, tk.END)
        classe = classe_var.get()
        nivel = nivel_var.get()
        nome = nome_var.get().lower()
        for magia in magias_lista:
            if classe and magia["classe"] != classe:
                continue
            if nivel and magia["nivel"] != nivel:
                continue
            if nome and nome not in magia["nome"].lower():
                continue
            # Mostra nome + nível
            lista_magias.insert(tk.END, f"{magia['nome']} (Nível {magia['nivel']})")

    def mostrar_descricao(event):
        selecionado = lista_magias.curselection()
        if selecionado:
            # Extrai apenas o nome da magia (antes do " (Nível X)")
            nome_magia = lista_magias.get(selecionado[0]).rsplit(" (Nível", 1)[0]
            magia = next((m for m in magias_lista if m["nome"] == nome_magia), None)
            if magia:
                detalhes = (
                    f"Nome: {magia['nome']}\n"
                    f"Classe: {magia['classe']}\n"
                    f"Nível: {magia['nivel']}\n"
                    f"Descrição:\n{magia['descricao']}"
                )
                messagebox.showinfo(magia["nome"], detalhes)

    # Botão de filtro
    tk.Button(filtro_frame, text="Filtrar", command=atualizar_lista).grid(row=0, column=6, padx=5)
    tk.Button(filtro_frame, text="Limpar", command=lambda: [classe_var.set(""), nivel_var.set(""), nome_var.set(""), atualizar_lista()]).grid(row=0, column=7, padx=5)

    lista_magias.bind("<<ListboxSelect>>", mostrar_descricao)

    # Inicializa a lista
    atualizar_lista()

def sair(root):
    """Fecha a aplicação."""
    root.destroy()

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hidden Door - Menu Principal")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.maxsize(800, 600)

        # === IMAGEM DE FUNDO ===
        imagem_path = os.path.join(os.path.dirname(__file__), "..", "imagens", "menuded.png")
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((800, 600))  # Ajuste ao novo tamanho da janela
        self.bg_photo = ImageTk.PhotoImage(imagem)
        fundo = tk.Label(self.root, image=self.bg_photo)
        fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame centralizado para os botões
        frame = tk.Frame(self.root)
        frame.pack(anchor='n', pady=20)

        # Botões do menu
        tk.Button(frame, text="1. Livros", font=("Arial", 14),
                  command=lambda: abrir_janela(abrir_livros, self.root)).pack(side="left",pady=8)
        tk.Button(frame, text="2. Rolar Dados", font=("Arial", 14),
                  command=lambda: abrir_janela(rolar_dados, self.root)).pack(side="left",pady=8)
        tk.Button(frame, text="3. Lista de Magias", font=("Arial", 14),
                  command=lambda: abrir_janela(abrir_magias, self.root)).pack(side="left",pady=8)
        tk.Button(frame, text="0. Sair", font=("Arial", 14),
                  command=lambda: sair(self.root)).pack(side="left",pady=8)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
