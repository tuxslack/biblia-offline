import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDateTime, Qt

USER_HOME = os.path.expanduser("~")

class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        ui_path = os.path.join(USER_HOME, ".biblia-offline", "notes.ui")
        loadUi(ui_path, self)

        # Carregar o último livro e capítulo
        self.setWindowTitle("Anotações Bíblicas")
        self.load_last_book_and_chapter()
        self.setWindowTitle("Anotações Bíblicas")
        self.setWindowIcon(QIcon(f'{USER_HOME}/.biblia-offline/gnome-books.svg'))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Conectar o botão de salvar à função save_notes
        self.btn_save.clicked.connect(self.save_notes)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                border: 1px solid #000;
                border-radius: 8px;   
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #e95420;
            }
        """)   
        
                # Aplicar cor de seleção do QTextEdit
        self.textEdit.setStyleSheet("""
            background: #1e1e1e;
            selection-background-color: #e95420;
            selection-color: #ffffff;
            line-height: 1.5;
            padding: 10px;
        """)

    def load_last_book_and_chapter(self):
        # Lê o arquivo ultimo_livro.json
        try:
            with open(f"{USER_HOME}/.biblia-offline/ultimo_livro.json", "r") as file:
                data = json.load(file)
                livro = data.get("livro")
                capitulo = data.get("capitulo")

                # Atualiza as labels
                self.name_book.setText(livro.upper())  # Nome do livro em maiúsculas
                self.number_book.setText(str(capitulo))  # Número do capítulo

                # Cria o diretório e arquivo para anotações
                self.create_notes_file(livro, capitulo)
        except Exception as e:
            print(f"Erro ao carregar o livro e capítulo: {e}")

    def create_notes_file(self, livro, capitulo):
        # Define o caminho para o diretório de notas
        directory = f"{USER_HOME}/.biblia-offline/notas/{livro}"
        file_path = f"{directory}/{capitulo}.txt"

        # Cria o diretório se não existir
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Verifica se o arquivo já existe
        if os.path.exists(file_path):
            self.load_existing_notes(file_path)  # Carrega notas existentes
        else:
            # Cria um novo arquivo se não existir
            with open(file_path, "w") as f:
                f.write("")  # Cria um arquivo vazio

    def load_existing_notes(self, file_path):
        # Carrega as anotações existentes no QTextEdit
        try:
            with open(file_path, "r") as f:
                notes = f.read()
                self.textEdit.setPlainText(notes)  # Carrega as notas no QTextEdit
        except Exception as e:
            print(f"Erro ao carregar notas existentes: {e}")

    def save_notes(self):
        # Salva as notas escritas no QTextEdit
        livro = self.name_book.text().lower()  # Usar a abreviatura do livro
        capitulo = self.number_book.text()
        file_path = f"{USER_HOME}/.biblia-offline/notas/{livro}/{capitulo}.txt"

        try:
            with open(file_path, "w") as f:
                f.write(self.textEdit.toPlainText())  # Salva o texto do QTextEdit
            
            # Atualiza a barra de status com a mensagem de sucesso e a hora
            current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
            self.statusBar().showMessage(f"Notas salvas com sucesso às {current_time}")
            print("Notas salvas com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar notas: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Sagradas Escrituras - Notas")
    app.setWindowIcon(QIcon(f"{USER_HOME}/.biblia-offline/biblia.png"))
    ui = MainUi()
    ui.show()
    app.exec_()

