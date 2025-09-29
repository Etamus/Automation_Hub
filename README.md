#  Automation Hub (VBA/SAP)

Servidor web desenvolvido em Python com Flask, projetado para orquestrar a execução de tarefas de automação que envolvem macros VBA em planilhas Excel e interações com o sistema SAP.  
Através de uma interface web simples, o usuário pode realizar o login no SAP e executar macros pré-configuradas de forma segura e controlada.

---

## Funcionalidades

  - Servidor Web com Flask: Cria um servidor local para gerenciar as automações.
  - Execução Remota de Macros: Dispara a execução de macros VBA em planilhas Excel localizadas em um caminho de rede ou local, através de scripts PowerShell.
  - Controle de Login no SAP: O sistema mantém o estado de login, permitindo que as macros relacionadas ao SAP sejam executadas somente após a autenticação.
  - Fluxo de Login e Logout: Gerencia a autenticação no SAP de forma programática. O logout inclui a limpeza forçada de processos para garantir que o SAP não permaneça aberto.
  - Gerenciamento de Tarefas: Um dicionário de macros disponíveis mapeia nomes amigáveis a caminhos de arquivos e nomes de macros reais, facilitando a configuração.
  - Tratamento de Erros: O sistema lida com falhas de execução, timeouts e erros de login, retornando mensagens claras para o usuário.

- **Estrutura do Projeto**
  - servidor_unico.py: O coração da aplicação Flask, contendo todas as rotas e a lógica de execução.
  - runner.ps1: Script PowerShell para executar macros simples.
  - sap_login_runner.ps1: Script PowerShell específico para o login no SAP.
  - cleanup_processes.ps1: Script PowerShell para encerrar processos do Excel e SAP em caso de erros ou no logout.
  - templates/index.html: A interface web do usuário.

---

## Como Executar

### Pré-requisitos
- Python 3.X
- Acesse o endereço http://10.12.72.90:5000 em seu navegador para utilizar a aplicação.

### Instalação
1. Clone este repositório ou baixe os arquivos:
   ```bash
   git clone https://github.com/Etamus/Portal_Automation.git
   cd Portal_Automation
   ```

3.  Crie um ambiente virtual e instale as dependências:
    ```bash
    pip install flask
    ```

4.  Execução:
    ```bash
    python servidor_unico.py
    ```




