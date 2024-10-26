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

    # Verificar se as dependências estão instaladas
    for cmd in curl unzip python3; do
        if ! command --version "$cmd" &> /dev/null; then
            echo "Erro: o pacote $cmd não está instalado. Instale-o e tente novamente."
            exit 1
        fi
    done

    # Verificar se venv está disponível
    if ! python3 -m venv --help &> /dev/null; then
        echo "Erro: O módulo venv do Python não está disponível. Instale-o e tente novamente."
        exit 1
    fi

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
        unzip -o livros.zip -d "$INSTALL_DIR/livros"

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
Terminal=false" > "$DESKTOP_FILE"

    # Verificar se a instalação foi concluída
    echo "Checando instalação..."
    if [ -d "$INSTALL_DIR" ] && [ -f "$DESKTOP_FILE" ] && [ -f "$INSTALL_DIR/venv/bin/python" ]; then
        echo "Instalação concluída! O programa pode ser encontrado no menu de aplicativos do sistema."
    else
        echo "Erro: A instalação não foi concluída corretamente."
        echo "Execute o script de instalação novamente e escolha a opção Desinstalar"
        echo "Ou, se preferir, remova o diretório $HOME/.biblia-offline e o arquivo $HOME/.local/share/applications/biblia-offline.desktop"
        
        exit 1
    fi
}

# Função de desinstalação
uninstall() {
    echo "Checando a instalação da Bíblia Offline..."

    # Remover o diretório de instalação, se existir
    if [ -d "$HOME/.biblia-offline" ]; then
        echo "Removendo diretório $HOME/.biblia-offline..."
        rm -rf "$HOME/.biblia-offline"
    else
        echo "O diretório $HOME/.biblia-offline não foi encontrado."
    fi

    # Remover o arquivo .desktop, se existir
    if [ -f "$HOME/.local/share/applications/biblia-offline.desktop" ]; then
        echo "Removendo o arquivo .desktop $HOME/.local/share/applications/biblia-offline.desktop..."
        rm "$HOME/.local/share/applications/biblia-offline.desktop"
    else
        echo "O arquivo .desktop não foi encontrado."
    fi

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
