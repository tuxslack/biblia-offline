import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import re

USER_HOME = os.path.expanduser("~")

class BibliaBuscaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(USER_HOME, ".biblia-offline", "search.ui")
        uic.loadUi(ui_path, self)  # Carrega o arquivo .ui diretamente
        self.setWindowTitle("Chave Bíblica")
        self.setWindowIcon(QIcon(f"{USER_HOME}/.biblia-offline/biblia.png"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        QApplication.setApplicationVersion("1.0")

        # Conectar o botão ao método de busca
        self.btn_buscar.clicked.connect(self.buscar_palavra)
        self.btn_buscar.setStyleSheet("""
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

        # Conectar o evento Enter no QLineEdit
        self.input_palavra.returnPressed.connect(self.buscar_palavra)

        self.resultado_busca.setStyleSheet("""
            background: #1e1e1e;
            selection-background-color: #e95420;
            selection-color: #ffffff;
            line-height: 1.5;
            padding: 10px;
        """)

        # Ordem correta dos livros da Bíblia (agora em minúsculas)
        self.livros_ordenados = [
            "gn", "ex", "lv", "nm", "dt",  # Pentateuco
            "js", "jz", "rt", "1sm", "2sm", "1rs", "2rs", "1cr", "2cr", "ed", "ne", "et",  # Livros históricos
            "jo", "sl", "pv", "ec", "ct",  # Livros poéticos
            "is", "jr", "lm", "ez", "dn", "os", "jl", "am", "ob", "jn", "mq", "na", "hc", "sf", "ag", "zc", "ml",  # Profetas
            "mt", "mc", "lc", "jo",  # Evangelhos
            "at",  # Atos dos Apóstolos
            "rm", "1co", "2co", "gl", "ef", "fp", "cl", "1ts", "2ts", "1tm", "2tm", "tt", "fm", "hb", "tg", "1pe", "2pe", "1jo", "2jo", "3jo", "jd",  # Cartas
            "ap"  # Apocalipse
        ]

    def buscar_palavra(self):
        palavra = self.input_palavra.text().strip()  # Obter o texto do QLineEdit
        resultados = self.buscar_palavra_na_biblia(palavra)  # Função para buscar a palavra
        self.resultado_busca.setHtml(resultados)  # Exibir os resultados formatados no QTextEdit

    def buscar_palavra_na_biblia(self, palavra):
        resultados = ""
        contador = 0  # Contador para quantas vezes a palavra foi encontrada
        base_dir = os.path.join(os.path.dirname(__file__), 'livros')

        # Busca recursiva nos arquivos de texto da bíblia, respeitando a ordem dos livros
        for livro in self.livros_ordenados:
            caminho_livro = os.path.join(base_dir, livro)
            if os.path.exists(caminho_livro):
                # Ordenar os arquivos de capítulos numericamente
                capitulos = sorted(os.listdir(caminho_livro), key=lambda x: int(os.path.splitext(x)[0]))
                for file in capitulos:
                    if file.endswith('.txt'):
                        caminho_arquivo = os.path.join(caminho_livro, file)
                        capitulo = os.path.splitext(file)[0]  # O nome do arquivo é o capítulo
                        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                            for linha in f:
                                if re.search(rf'\b{palavra}\b', linha, re.IGNORECASE):
                                    # Destacar a palavra no resultado
                                    linha_formatada = re.sub(
                                        rf'({palavra})', 
                                        r'<span style="color:#f35c2c;"><b>\1</b></span>', 
                                        linha, 
                                        flags=re.IGNORECASE
                                    )
                                    # Adicionar resultado formatado sem o número da linha
                                    resultados += f'<b>{livro.upper()} {capitulo}</b><br>{linha_formatada}<br><br>'
                                    contador += 1  # Incrementar o contador

        # Atualizar a barra de status com o número de resultados encontrados
        self.statusBar().showMessage(f'Resultados para "{palavra}": {contador}')

        return resultados if resultados else "<i>Nenhum resultado encontrado.</i>"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Busca - Escrituras Sagradas")
    janela = BibliaBuscaApp()
    janela.show()
    sys.exit(app.exec_())

