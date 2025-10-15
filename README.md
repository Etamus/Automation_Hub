# Hub Spare Parts

Servidor web desenvolvido em **Python** com **Flask**, projetado como um portal centralizado (Hub) para orquestrar, acessar e interagir com diversas ferramentas de automação e Business Intelligence. 

A aplicação oferece uma interface web unificada para executar tarefas, visualizar dashboards, planilhas e interagir com sistemas legados como **SAP** e portais web como o **BW HANA** em uma interface web única, limpa e moderna, eliminando a necessidade de múltiplos logins ou acesso a sistemas legados.

---

https://github.com/user-attachments/assets/595761ac-e15c-4739-b1a0-6acbfee3f8f3

---

## Funcionalidades
- **Hub de Aplicações:**  
  Página inicial (gateway) que direciona o usuário para as diferentes ferramentas disponíveis: *Automações*, *Dashboards*, *Drive online* e futuras integrações.
- **Painel de Automação Unificado:**  
  Interface de login única que gerencia o acesso a múltiplos sistemas (SAP e BW HANA).  
  O sistema controla o estado de login, habilitando as automações correspondentes apenas após autenticação bem-sucedida.
- **Execução de Macros (VBA):**  
  Dispara a execução de macros VBA em planilhas Excel através de scripts PowerShell, automatizando tarefas em sistemas desktop.
- **Automação Web (Playwright):**  
  Realiza automações complexas em portais web (como o BW HANA) utilizando a biblioteca **Playwright** — sem depender de executáveis como *chromedriver.exe*.
- **Portal de Dashboards:**  
  Integra relatórios de BI como **Looker Studio** e **Tableau** diretamente na interface, usando *iframes* para experiência unificada.
  - **Navegação Hierárquica (`v1.0.3`):** Organiza os dashboards em "Áreas" e "Setores", com um sistema de scrollbar para listas longas.
  - **Preview Lateral Interativo (`v1.0.4`):** Ao passar o mouse sobre um botão de dashboard, um painel lateral aparece exibindo um GIF de preview e uma descrição detalhada do relatório. O painel de preview exibe etiquetas coloridas que fornecem informações rápidas sobre o dashboard, como Frequência (`Daily`, `Weekly`), Fonte de Dados (`GCP`, `Sheets`) e Foco Principal (`Revenue`, `Costs`).

  https://github.com/user-attachments/assets/be147209-a071-4daf-aa87-2e8ba253e36c 

- **Download de Relatórios:**  
  Permite baixar arquivos gerados pelas automações (como relatórios do Excel) diretamente pela interface web.
- **Componente de Feedback (FAQ):**  
  Botão flutuante disponível em todas as telas, abrindo um *popup* com formulários do **Google Forms** para novas demandas ou sugestões.
- **Gerenciamento de Processos:**  
  Inclui script de limpeza forçada de processos (SAP, Excel, navegadores) para resetar o ambiente após logout ou erros — evitando travamentos.
- **Tratamento de Erros e Timeouts:**  
  Sistema robusto, lida com falhas de execução, macros travadas (janela de depuração) e timeouts, retornando mensagens claras e executando limpeza automática.
- **Navegador de Arquivos (Drive Online) (`v1.0.1`):**
  Uma interface web que permite navegar por uma estrutura de pastas no local da VM que hospeda o servidor e executar consultas & downloads de arquivos diretamente, sem a necessidade de VPN ou acesso a drives de rede.
- **Assistente Virtual Interativo: (`v1.0.2`)**
  Componente de chatbot flutuante que interpreta a necessidade do usuário através de palavras-chave para direcioná-lo ao formulário correto de **Demandas** ou **Sugestões** (Google Forms).    
---

## Como Executar

### Pré-requisitos
- Python 3.x  
- Navegador moderno (Chrome, Edge, etc.)  
- Ambiente Windows (necessário para os scripts PowerShell e automação de macros)

### Instalação
1. Clone o repositório ou baixe os arquivos:  
   git clone https://github.com/Etamus/Hub_Spare_Parts.git  
   cd Hub_Spare_Parts

2. Crie um arquivo chamado requirements.txt na pasta principal e adicione:  
   Flask  
   playwright  

3. Instale as dependências:  
   pip install -r requirements.txt  

---

## Execução

1. Inicie o servidor Flask:  
   python servidor_unico.py  

2. Acesse no navegador:  
   http://localhost:5000  

3. Para executar toda a automação de uma vez (Windows):  
   INICIAR_TUDO.bat  

---

## Scripts Importantes

| Script | Função |
|--------|--------|
| runner.ps1 | Executa a sequência de automações em ordem |
| cleanup_processes.ps1 | Finaliza processos abertos após a execução |
| sap_login_runner.ps1 | Faz login automático no SAP |
| bw_hana_extractor.py | Extrai dados do BW HANA |
| servidor_unico.py | Inicia o servidor Flask principal |

---

## Tecnologias

- Python + Flask → Backend e servidor local  
- Playwright → Automação de navegador  
- PowerShell → Scripts de integração no Windows  

- HTML/CSS/JS → Interface web