# Bíblia Offline

A Bíblia Offline possui o modo leitura, anotações e busca de palavras.
![Screenshot do Projeto](https://github.com/SobDex/biblia-offline/raw/main/Screenshot1.png)
## Dependências

Para executar este programa em um sistema Linux, você precisará das seguintes dependências:

1. **Pacote para Ambiente Virtual**: O pacote `python3-venv` deve estar instalado para que o programa possa criar um ambiente virtual. O uso do ambiente virtual isola a aplicação **Bíblia Offline** do restante do sistema, garantindo que as dependências e arquivos da aplicação não interfiram com os arquivos da raiz do sistema. Para instalar o pacote, use o seguinte comando:

   - No Ubuntu ou Debian:
     ```bash
     sudo apt install python3-venv
     ```

2. **`unzip`**: O programa usa do pacote `unzip` para descompactar os livros da Bíblia:

   ```bash
   sudo apt install unzip

3. **`curl`**: Necessário para fazer download do script de instalação e também para a clonagem do repositório.

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

Dentro do diretório `$HOME/.biblia-offline` será criado um ambiente virtual Python para instalar a biblioteca pyQt5. Dessa forma nenhuma biblioteca python será instalada no Python do seu sistema principal, deixando assim a instalação e desisntalação da aplicação muito mais segura.
