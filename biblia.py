from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QComboBox, QTextEdit, QLabel, QStatusBar, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QTime
import sys
import os
import json
import subprocess

# Caminho para os livros da Bíblia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIBLE_PATH = os.path.join(BASE_DIR, "livros")
LAST_BOOK_FILE = os.path.join(BASE_DIR, "ultimo_livro.json") # Arquivo para armazenar o último livro e capítulo lidos
USER_HOME = os.path.expanduser("~")
# Estrutura de livros por categoria
LIVROS = {
    "Antigo Testamento": {
        "Lei": {
            "Gênesis": "gn", "Êxodo": "ex", "Levítico": "lv", "Números": "nm", "Deuteronômio": "dt"
        },
        "Livros Históricos": {
            "Josué": "js", "Juízes": "jz", "Rute": "rt", "1 Samuel": "1sm", "2 Samuel": "2sm",
            "1 Reis": "1rs", "2 Reis": "2rs", "1 Crônicas": "1cr", "2 Crônicas": "2cr",
            "Esdras": "ed", "Neemias": "ne", "Ester": "et"
        },
        "Livros Poéticos": {
            "Jó": "jó", "Salmos": "sl", "Provérbios": "pv", "Eclesiastes": "ec", "Cantares": "ct"
        },
        "Livros Proféticos": {
            "Isaías": "is", "Jeremias": "jr", "Lamentações": "lm", "Ezequiel": "ez", "Daniel": "dn",
            "Oseias": "os", "Joel": "jl", "Amós": "am", "Obadias": "ob", "Jonas": "jn",
            "Miquéias": "mq", "Naum": "na", "Habacuque": "hc", "Sofonias": "sf",
            "Ageu": "ag", "Zacarias": "zc", "Malaquias": "ml"
        }
    },
    "Novo Testamento": {
        "Evangelhos": {
            "Mateus": "mt", "Marcos": "mc", "Lucas": "lc", "João": "jo"
        },
        "Atos": {
            "Atos": "at"
        },
        "Epístolas": {
            "Romanos": "rm", "1 Coríntios": "1co", "2 Coríntios": "2co", "Gálatas": "gl",
            "Efésios": "ef", "Filipenses": "fp", "Colossenses": "cl", "1 Tessalonicenses": "1ts",
            "2 Tessalonicenses": "2ts", "1 Timóteo": "1tm", "2 Timóteo": "2tm", "Tito": "tt",
            "Filemom": "fm", "Hebreus": "hb", "Tiago": "tg", "1 Pedro": "1pe", "2 Pedro": "2pe",
            "1 João": "1jo", "2 João": "2jo", "3 João": "3jo", "Judas": "jd"
        },
        "Apocalipse": {
            "Apocalipse": "ap"
        }
    }
}

class MainUi(QMainWindow):
    '''
    Esta função inicializa a interface principal da aplicação. Configura o
    título da janela, o ícone, adiciona a barra de status e carrega a interface
    do arquivo .ui. Também chama outras funções para configurar o menu de 
    livros e conecta as ações de botões e do combobox aos métodos correspondentes.
    Finalmente, carrega o último livro e capítulo lidos ao iniciar a aplicação.
    '''
    def __init__(self):
        super(MainUi, self).__init__()

        ui_path = os.path.join(USER_HOME, "Projetos", "biblia", "biblia.ui")
        loadUi(ui_path, self)
        
        self.setWindowTitle("Bíblia Sagrada")
        self.setWindowIcon(QIcon(f"{USER_HOME}/Projetos/biblia/gnome-books.svg"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        QApplication.setApplicationVersion("1.0")
     

        # Adicionando a barra de status
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Configuração do menu de livros dividido em categorias
        self.setup_menu()
        self.menubar.setStyleSheet("""
            QMenuBar{
                background-color: #2a2a2a; /* Cor de fundo do menu */
                color: #ffffff; /* Cor do texto do menu */
                font-family: "Noto Sans";
                font-size: 11pt;
            }

            QMenu {
                background-color: #2a2a2a; /* Cor de fundo do submenu */
                color: #ffffff; /* Cor do texto do submenu */
                font-family: "Noto Sans";
                font-size: 11pt;
            }

            QMenu::item {
                background-color: transparent; /* Fundo transparente para itens */
                padding: 5px 20px; /* Espaçamento interno */
            }

            QMenu::item:selected {
                background-color: #e95420; /* Cor de fundo do item selecionado */
                color: #ffffff; /* Cor do texto do item selecionado */
            }


        """)

        # Limitar o combobox de capítulos para exibir 15 linhas e permitir rolagem
        self.capitulos.setMaxVisibleItems(15)

        # Conectar ações
        self.capitulos.currentIndexChanged.connect(self.on_chapter_change)
        self.btn_prev.clicked.connect(self.load_previous_chapter)
        self.btn_prev.setStyleSheet("""
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
        self.btn_next.clicked.connect(self.load_next_chapter)
        self.btn_next.setStyleSheet("""
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
        
        # Carregar último livro lido
        self.load_last_book()
        
        # Aplicar cor de seleção do QTextEdit
        self.textEdit.setStyleSheet("""
            background: #1e1e1e;
            selection-background-color: #e95420;
            selection-color: #ffffff;
            line-height: 1.5;
            padding: 10px;
        """)
        # Criação da QLabel para o relógio
        self.clock_label = QLabel(self)
        self.statusBar.addPermanentWidget(self.clock_label)  # Adiciona a QLabel ao lado direito da barra de status

        # Atualiza o relógio a cada minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)  # Conecta o sinal de timeout à função update_clock
        self.timer.start(60000)  # Atualiza a cada 60.000 milissegundos (1 minuto)

        # Chama a função de atualização do relógio uma vez para inicializar
        self.update_clock()
    
    
    def update_clock(self):
        current_time = QTime.currentTime()  # Obtém a hora atual
        self.clock_label.setText(current_time.toString("hh:mm"))  # Formata a hora e atualiza a QLabel

    '''
    Cria os menus para o Antigo e o Novo Testamento. Para cada categoria
    (ex: Lei, Livros Poéticos), é criado um submenu, e dentro de cada submenu, 
    são adicionados os livros correspondentes como ações. Cada ação, ao ser 
    clicada, carrega o primeiro capítulo do livro selecionado.
    '''
    def setup_menu(self):
        # Criação dos menus
        self.menu_antigo = self.menuBar().addMenu("Antigo Testamento")
        self.menu_novo = self.menuBar().addMenu("Novo Testamento")
        self.menu_options = self.menuBar().addMenu("Opções")

        # criar submenu "Anotações"
        acao_notas = QAction("Anotações", self)
        acao_notas.triggered.connect(self.run_notes)
        self.menu_options.addAction(acao_notas)
        # criar submenu "Chave Bíblica"
        acao_cb = QAction("Chave Bíblica", self)
        acao_cb.triggered.connect(self.run_cb)
        self.menu_options.addAction(acao_cb)
        
        # Populando o Antigo Testamento
        for categoria, livros in LIVROS["Antigo Testamento"].items():
            submenu = self.menu_antigo.addMenu(categoria)
            for livro, abreviatura in livros.items():
                acao = QAction(livro, self)
                acao.triggered.connect(lambda checked, abv=abreviatura, nome=livro: self.carregar_capitulo(abv, nome))
                submenu.addAction(acao)

        # Populando o Novo Testamento
        for categoria, livros in LIVROS["Novo Testamento"].items():
            submenu = self.menu_novo.addMenu(categoria)
            for livro, abreviatura in livros.items():
                acao = QAction(livro, self)
                acao.triggered.connect(lambda checked, abv=abreviatura, nome=livro: self.carregar_capitulo(abv, nome))
                submenu.addAction(acao)
    
    
    def run_notes(self):
        subprocess.Popen([f'{USER_HOME}/.scripts/venv/bin/python', f'{BASE_DIR}/notes.py'])
    
    def run_cb(self):
        subprocess.Popen([f'{USER_HOME}/.scripts/venv/bin/python', f'{BASE_DIR}/search.py'])
    


    '''
    Carrega o conteúdo do primeiro capítulo de um livro da Bíblia baseado na
    abreviatura do livro. Ele lê o arquivo do capítulo correspondente (1.txt)
    e exibe o conteúdo no QTextEdit. Também atualiza o status da janela com o
    nome do livro e capítulo e chama a função para carregar a lista de capítulos.
    Salva o livro e o capítulo atual como os últimos lidos.
    '''
    def carregar_capitulo(self, abreviatura_livro, nome_livro):
        # Carregar o primeiro capítulo (1.txt) do livro selecionado
        self.current_book_folder = abreviatura_livro
        caminho_arquivo = os.path.join(BIBLE_PATH, abreviatura_livro, "1.txt")

        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                conteudo = file.read()
                self.textEdit.setPlainText(conteudo)
                # Atualizar a barra de status para o nome do livro e capítulo
                self.statusBar.showMessage(f"{abreviatura_livro.upper()} - capítulo 1")
                # Atualizar os labels
                self.book_name.setText(nome_livro)  # Atualiza o nome do livro
                self.book_number.setText("Capítulo 1")  # Atualiza o número do capítulo
            self.load_chapters(abreviatura_livro)
            self.save_last_book(abreviatura_livro, 1)  # Salvar o livro e capítulo lidos
        else:
            self.textEdit.setPlainText(f"Arquivo {caminho_arquivo} não encontrado!")

    
    '''
    Limpa o QComboBox de capítulos e preenche com os números de capítulos baseados
    nos arquivos de texto presentes na pasta do livro selecionado. Cada arquivo
    .txt corresponde a um capítulo.
    '''
    def load_chapters(self, book_folder):
        # Limpa o combobox
        self.capitulos.clear()

        # Caminho do diretório do livro
        book_path = os.path.join(BIBLE_PATH, book_folder)

        # Conta os arquivos .txt no diretório
        chapters = [f for f in os.listdir(book_path) if f.endswith('.txt')]

        # Adiciona os números de capítulo no combobox
        self.capitulos.addItems([str(i + 1) for i in range(len(chapters))])

    
    '''
    Dispara quando o usuário seleciona um capítulo diferente no QComboBox. 
    Esta função carrega o conteúdo do novo capítulo escolhido, chamando a função
    load_chapter_content com o número do capítulo selecionado.
    '''
    def on_chapter_change(self):
        # Atualiza o conteúdo do capítulo selecionado
        self.load_chapter_content(self.current_book_folder, self.capitulos.currentText())

    
    '''
    Carrega o conteúdo do capítulo escolhido do livro selecionado. Lê o arquivo
    correspondente ao capítulo no formato n.txt e exibe o conteúdo no QTextEdit.
    Também atualiza o status da janela com o nome do livro e capítulo atual
    e salva o estado do último livro e capítulo lido.
    '''
    def load_chapter_content(self, book_folder, chapter_number):
        # Caminho do arquivo do capítulo selecionado
        chapter_path = os.path.join(BIBLE_PATH, book_folder, f"{chapter_number}.txt")

        # Lê o conteúdo do arquivo e exibe no QTextEdit
        if os.path.exists(chapter_path):
            with open(chapter_path, 'r', encoding='utf-8') as file:
                chapter_content = file.read()
                self.textEdit.setPlainText(chapter_content)

            # Atualiza a barra de status
            self.statusBar.showMessage(f"{self.current_book_folder.upper()} - Capítulo {chapter_number}")
            self.book_number.setText(f"capítulo {chapter_number}")  # Atualiza o número do capítulo
            self.save_last_book(self.current_book_folder, chapter_number)  # Salvar o último livro e capítulo lidos
        else:
            self.textEdit.setPlainText(f"Capítulo {chapter_number} não encontrado!")
    
    
    '''
    Tenta carregar o último livro e capítulo lidos a partir de um arquivo JSON.
    Se o arquivo existe, ele carrega o último livro e capítulo e os exibe automaticamente.
    Se o arquivo não existe, cria um arquivo JSON com o livro Gênesis (abreviatura gn)
    e o capítulo 1 como padrão.    
    '''
    def load_last_book(self):
        # Tenta carregar o último livro lido a partir do arquivo JSON
        if os.path.exists(LAST_BOOK_FILE):
            with open(LAST_BOOK_FILE, 'r') as file:
                data = json.load(file)
                livro = data.get("livro", "gn")  # Abreviatura do livro
                capitulo = data.get("capitulo", 1)

                # Procurar o nome completo do livro baseado na abreviatura
                nome_livro = None
                for testamento in LIVROS.values():
                    for categoria in testamento.values():
                        if livro in categoria.values():
                            nome_livro = list(categoria.keys())[list(categoria.values()).index(livro)]
                            break
                    if nome_livro:
                        break

                if nome_livro:
                    self.carregar_capitulo(livro, nome_livro)  # Passa a abreviatura e o nome completo do livro
                    self.capitulos.setCurrentText(str(capitulo))
                    self.load_chapter_content(livro, str(capitulo))
                else:
                    # Se não encontrar o livro, exibe uma mensagem de erro
                    self.textEdit.setPlainText("Erro: Livro não encontrado.")
        else:
            # Se o arquivo não existir, cria um com Gênesis e Capítulo 1
            self.save_last_book("gn", 1)

    
    
    '''
    Salva o último livro e capítulo lidos em um arquivo JSON. O conteúdo do 
    arquivo JSON é atualizado toda vez que o usuário muda de livro ou capítulo.
    '''
    def save_last_book(self, livro, capitulo):
        # Salva o último livro e capítulo lidos em um arquivo JSON
        with open(LAST_BOOK_FILE, 'w') as file:
            json.dump({"livro": livro, "capitulo": capitulo}, file)
    
    
    '''
    Carrega o capítulo anterior ao atualmente exibido no QComboBox. Se o usuário
    está no primeiro capítulo, a função não faz nada. Ao selecionar o capítulo anterior,
    a função chama on_chapter_change para atualizar o conteúdo da janela.
    '''
    def load_previous_chapter(self):
        current_index = self.capitulos.currentIndex()
        if current_index > 0:
            self.capitulos.setCurrentIndex(current_index - 1)
            self.on_chapter_change()


    '''
    Carrega o próximo capítulo no QComboBox. Se o usuário está no último capítulo,
    a função não faz nada. Ao selecionar o próximo capítulo, a função chama 
    on_chapter_change para atualizar o conteúdo da janela.    
    '''
    def load_next_chapter(self):
        current_index = self.capitulos.currentIndex()
        if current_index < self.capitulos.count() - 1:
            self.capitulos.setCurrentIndex(current_index + 1)
            self.on_chapter_change()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Sagradas Escrituras")
    window = MainUi()
    window.show()
    sys.exit(app.exec_())

