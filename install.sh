#!/usr/bin/env bash
# --------------------------------------------------------------
# Projeto	: Bíblia Offline
# Arquivo	: install.sh
# Descrição : Script de instalação para a Bíblia Offline
# Versão	: 1.0
# Data		: $(date '+%d/%m/%Y - %R')
# Autor		: Sob Dex
# --------------------------------------------------------------

# URL do repositório Git
REPO_URL="https://github.com/SobDex/biblia-offline.git"

# Função de instalação
install() {
    echo "Instalando a Bíblia Offline..."

    # Criar diretório oculto na home do usuário
    INSTALL_DIR="$HOME/.biblia-offline"
    mkdir -p "$INSTALL_DIR"

    # Clonar o repositório se o diretório não existir
    if [ ! -d "$INSTALL_DIR/.git" ]; then
        echo "Clonando o repositório..."
        git clone "$REPO_URL" "$INSTALL_DIR" || { echo "Erro ao clonar o repositório."; exit 1; }
    fi

    # Ir para o diretório de instalação
    cd "$INSTALL_DIR" || { echo "Erro ao acessar o diretório de instalação."; exit 1; }

    # Verificar se o arquivo livros.zip existe no diretório
    echo "Verificando se livros.zip existe..."
    if [ -f "livros.zip" ]; then
        echo "Arquivo livros.zip encontrado. Descompactando os livros..."
        
        # Verificar se o unzip está instalado
        if command -v unzip &> /dev/null; then
            unzip -o livros.zip -d "$INSTALL_DIR/livros"
        else
            echo "unzip não instalado. Instalando unzip..."
            sudo apt install unzip -y || { echo "Erro ao instalar unzip."; exit 1; }
            unzip -o livros.zip -d "$INSTALL_DIR/livros"
        fi

        # Remover o arquivo compactado
        rm livros.zip
    else
        echo "Erro: O arquivo livros.zip não foi encontrado no repositório."
        exit 1
    fi

    # Criar o ambiente virtual
    echo "Criando ambiente virtual..."
    python3 -m venv venv || { echo "Erro ao criar o ambiente virtual."; exit 1; }

    # Instalar dependências
    echo "Instalando dependências do Python..."
    "$INSTALL_DIR/venv/bin/pip" install -r requirements.txt || { echo "Erro ao instalar dependências."; exit 1; }

    # Criar arquivo .desktop para o programa
    echo "Criando atalho no menu..."
    DESKTOP_FILE="$HOME/.local/share/applications/biblia-offline.desktop"
    echo "[Desktop Entry]
Name=Bíblia Offline
Exec=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/biblia.py
Icon=$INSTALL_DIR/bible.png
Type=Application
Terminal=false" > $DESKTOP_FILE

    # Tornar o .desktop executável
    chmod +x $DESKTOP_FILE

    echo "Instalação concluída! Use o atalho para executar o programa."
}

# Função de desinstalação
uninstall() {
    echo "Desinstalando a Bíblia Offline..."

    # Remover o diretório de instalação
    rm -rf "$HOME/.biblia-offline"

    # Remover o arquivo .desktop
    rm "$HOME/.local/share/applications/biblia-offline.desktop"

    echo "Desinstalação concluída!"
}

# Função principal com case para selecionar as opções
menu() {
    echo "Escolha uma opção:"
    echo "1) Instalar"
    echo "2) Desinstalar"
    echo "3) Sair"
    read -rp "Opção: " option
    case $option in
        1) install ;;
        2) uninstall ;;
        3) exit 0 ;;
        *) echo "Opção inválida." ;;
    esac
}

# Executar menu
menu
