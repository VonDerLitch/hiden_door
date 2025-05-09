import os
import shutil

class Books():
    def __init__(self, pdf_dir=None):
        if pdf_dir is None:
            self._pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data','PDFS RPG')
        else:
            self._pdf_dir = pdf_dir

    def _get_default_download_dir(self):
        return os.path.join(os.path.expanduser("~"), "Downloads")
    
    def list_books(self):
        try:
            if not os.path.exists(self._pdf_dir):
                raise FileNotFoundError(f"Diretorio {self._pdf_dir} não encontrado")
            return [f for f in os.listdir(self._pdf_dir) if f.lower().endswith('.pdf')]
        except FileNotFoundError as e:
            print(e)
            return []
        except PermissionError:
            print(f"Permissão negada para acessar o diretório {self._pdf_dir}.")
            return []
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return []
        
    def download_book(self, filename, dest_dir=None):
        if dest_dir is None:
            dest_dir = self._get_default_download_dir()
        src_path = os.path.join(self._pdf_dir, filename)
        if not os.path.exists(src_path):
            print(f"Arquivo {filename} não encontrado no diretório {self._pdf_dir}.")
            return False
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src_path, dest_dir)
        print(f"Arquivo {filename} baixado para {dest_dir}.")
        return
    
    def download_all_books(self, dest_dir):
        if dest_dir is None:
            dest_dir = self._get_default_download_dir()
        books = self.list_books()
        if not books:
            print("Nenhum livro encontrado para download.")
            return False
        os.makedirs(dest_dir, exist_ok=True)
        for book in books:
            src_path = os.path.join(self._pdf_dir, book)
            shutil.copy2(src_path, dest_dir)
            print(f"Arquivo {book} baixado para {dest_dir}.")
        return True