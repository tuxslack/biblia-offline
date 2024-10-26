# Bíblia Offline
A Bíblia Offline utiliza uma lógica baseada na manipulação de arquivos de texto. Cada livro da Bíblia é representado por um diretório, e cada capítulo da Bíblia é um arquivo de texto único, facilitando assim a manipulação dos dados.

Com essa etrutura de dados, foi possível fazer a implementação de sistemas de busca e anotações para que a aplicação fornecesse não apenas mais uma forma de leitura da Bíblia, mas também a possibilide ser usada diáriamente para estudo Bíblico.

A Tradução da Bíblia usada na programe é a Nova Versão Internacional (NVI), com excessão do livro de Apocalipse que está na versão Almeida Corrigida Fiel (ACF).
![Screenshot do Projeto](https://github.com/SobDex/biblia-offline/raw/main/Screenshot1.png)

## Funcionamento
A Bíblia Offline é composta por três scripts Python:
- `biblia.py` (modo leitura da Bíblia)

Este é o programa principal, onde o utilizador tem acesso aos livros da Bíblia por meio dos menus "Antigo Testamento" e "Novo Testamento". Existe também o menu "Opções", através do qual é possível aceder a outros módulos, como "Anotações" e "Chave Bíblica".
  
- `notes.py` (anotações para cada capítulo da Bíblia)

Quando o utilizador está lendo um capítulo da Bíblia e clica em "Opções" >> "Anotações", um editor de texto abre-se, permitindo que anotações sobre o capítulo em leitura sejam feitas. Ao clicar em salvar um arquivo de texto único é criado para aquele
capítulo em leitura. Caso o usuário queira futuramente consultar as anotações, ele precisará acessar novamente o capítulo onde as mesmas foram salvas, então o arquivo anteriormente criado para aquele capítulo específico será carregado no editor de texto podendo mais uma vez ser editado.   

- `search.py` (busca recursiva)

Em qualquer momento o usuário pode clicar em "Opções" >> "Chave Bíblica" para procurar pela incidência de uma palavra em todos os capítulos da Bíblia. Essa ferramenta pode ser usada para diversos objetivos e é indispensável para estudos Bíblicos.

## Dependências

Para executar este programa em um sistema Linux, você precisará das seguintes dependências:

1. **Pacote para Ambiente Virtual**: O pacote `python3-venv` deve estar instalado para que o programa possa criar um ambiente virtual. O uso do ambiente virtual isola a aplicação **Bíblia Offline** do restante do sistema, garantindo que as dependências e arquivos da aplicação não interfiram com os arquivos da raiz do sistema. Para instalar o pacote, use o seguinte comando:

  - Distribuições baseadas no Debian:
     ```bash
     sudo apt install python3-venv
     ```
  - Fedora/Red Hat:
    ```bash
    sudo dnf install python3-venv
    ```
  - openSUSE:
    ```bash
    sudo zypper install python3-venv
    ```   
  - Distribuições baseadas no Arch Linux: O `venv` já vem incluso com o pacote Python no Arch Linux, então não é necessário instalar separadamente.


2. **`unzip`**: O programa usa do pacote `unzip` para descompactar os livros da Bíblia:

   ```bash
   sudo apt install unzip


3. **`curl`**: Necessário para fazer download do script de instalação e também para a clonagem do repositório.

## Instalação
1. Para instalar a Bíblia Offline faça o download do script de instalação. Para isso, abra o terminal e use o comando:
```
curl -sSL https://raw.githubusercontent.com/SobDex/biblia-offline/refs/heads/main/install.sh -o install.sh
```
Obs: o script de instalação será baixado no diretório atual.

2. Após baixar o arquivo install.sh, dê permissão de execução para o mesmo:
```
chmod +x install.sh
```

-3 Execute o script
```
./install.sh
```
O script de instalação possui 3 opções: instalar, desinstalar e sair.
Ao escolher a opção `instalar`, a instalação ocorrerá automaticamente. Quando a instalação estiver sido concluída, o aplicativo já deverá aparecer no menu de aplicações do sistema.

## Desinstalação: Onde ficam os arquivos da Bíblia Offline?

A Bíblia Offline é instalada dentro do diretório `$HOME/.biblia-offline`. Além desse diretório é criado um arquivo `biblia-offline.desktop` em `$HOME/.local/share/applications`.

Dentro do diretório `$HOME/.biblia-offline` será criado um ambiente virtual Python para instalar a biblioteca pyQt5. Dessa forma nenhuma biblioteca python será instalada no Python do seu sistema principal, deixando assim a instalação e desisntalação da aplicação muito mais segura.

O script `install.sh` possui a opção para remover os arquivos da Bíblia Offline. Porém, se o usuário escolher excluir manualmente o diretório `$HOME/.biblia-offline` e o arquivo `$HOME/.local/share/applications/biblia-offline.desktop`, o efeito será o mesmo.
