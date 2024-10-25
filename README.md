# Bíblia Offline

A Bíblia Offline possui o modo leitura, anotações e busca de palavras.
## Dependências

Para executar este programa em um sistema Linux, você precisará das seguintes dependências:

1. **Pacote para Ambiente Virtual**: O pacote `python3-venv` deve estar instalado para que o programa possa criar um ambiente virtual. Para instalar o pacote, use o seguinte comando:

   - No Ubuntu ou Debian:
     ```bash
     sudo apt install python3-venv
     ```

2. **Pacote para Manipulação de Arquivos `.zip`**: Por padrão, recomenda-se o uso do pacote `unzip` (os livros da Bíblia Offline estão compactados), mas você pode usar qualquer programa ou pacote que lide com arquivos `.zip`. Para instalar o `unzip`, use:

   ```bash
   sudo apt install unzip


## Instalação
1. Para instalar a Bíblia Offline faça o download do script de instalação. Para isso, abra o terminal e use o comando:
```
curl -sSL https://raw.githubusercontent.com/SobDex/biblia-offline/refs/heads/main/install.sh -o install.sh
```
Obs: o script de instalação será baixado no diretório atual

2. Após baixar o arquivo install.sh, dê permissão de execução para o mesmo:
```
chmod +x install.sh
```

-3 Execute o script
```
./install.sh
```

A instalação ocorrerá automaticamente. Quando a instalação estiver sido concluída, o aplicativo já deverá aparecer no lançador de aplicativos.

## Onde os arquivos da Bíblia Offline são instalados?

A Bíblia Offline é instalada dentro do diretório `$HOME/.biblia-offline`. Além desse diretório é criado um arquivo `biblia-offline.desktop` em `$HOME/.local/share/applications`.

Dentro do diretório `$HOME/.biblia-offline` será criado um ambiente virtual Python para instalar a biblioteca pyQt5. Dessa forma nenhuma biblioteca python será instalada no Python do seu sistema principal, deixando assim a isntalação e desisntalação da aplicação muito mais segura.
