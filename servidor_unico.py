# ===================================================================
# == CÓDIGO CORRIGIDO: servidor_unico.py                           ==
# ===================================================================

import subprocess
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Variável de Estado Global ---
is_sap_logged_in = False

# --- Caminhos e Configurações ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_RUNNER_SIMPLES = os.path.join(BASE_DIR, "runner.ps1")
SCRIPT_RUNNER_SAP_LOGIN = os.path.join(BASE_DIR, "sap_login_runner.ps1")
SCRIPT_CLEANUP = os.path.join(BASE_DIR, "cleanup_processes.ps1")

# --- Dicionário de macros ---
macros_disponiveis = {
    "Executar ZV62N": {
        "arquivo": "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\Input diário PÇ's.xlsm",
        "macro": "Org_relatorio_diario" 
    },
    "Executar Cancelamento Aging": {
        "arquivo": "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\Criação Aging.xlsm",
        "macro": "cancelar_fora_prazo"
    }
}

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html', macros=macros_disponiveis)

@app.route('/executar-macro', methods=['POST'])
def executar_macro():
    if not is_sap_logged_in:
        return jsonify({"status": "erro", "mensagem": "Acesso negado. Por favor, faça o login no SAP antes de executar uma tarefa."}), 403

    nome_macro_selecionada = request.form['macro']
    config = macros_disponiveis.get(nome_macro_selecionada)
    if not config:
        return jsonify({"status": "erro", "mensagem": "Macro não encontrada!"}), 400

    comando = [
        "powershell.exe", "-ExecutionPolicy", "Bypass",
        "-File", SCRIPT_RUNNER_SIMPLES,
        "-CaminhoArquivo", config['arquivo'],
        "-NomeMacro", config['macro']
    ]
    
    contexto = f"tarefa '{nome_macro_selecionada}'"
    resultado = executar_comando_powershell(comando, contexto_tarefa=contexto)
    return jsonify(resultado)

@app.route('/login-sap', methods=['POST'])
def login_sap():
    global is_sap_logged_in
    usuario = request.form['usuario']
    senha = request.form['senha']
    
    comando = [
        "powershell.exe", "-ExecutionPolicy", "Bypass",
        "-File", SCRIPT_RUNNER_SAP_LOGIN,
        "-CaminhoArquivo", "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\LoginSAP.xlsm",
        # --- CORREÇÃO AQUI ---
        "-NomeMacro", "funcSAPOpen",
        "-Usuario", usuario,
        "-Senha", senha
    ]
    
    resultado = executar_comando_powershell(comando, contexto_tarefa="Login SAP", timeout_seconds=8)
    
    if resultado['status'] == 'erro' and 'excedeu o tempo limite' in resultado['mensagem']:
        resultado['mensagem'] = "Login ou senha incorreto, ou o SAP demorou para responder."
    
    if resultado['status'] == 'sucesso':
        is_sap_logged_in = True
    else:
        is_sap_logged_in = False
        
    return jsonify(resultado)

@app.route('/logout-sap', methods=['POST'])
def logout_sap():
    global is_sap_logged_in
    print("Iniciando limpeza forçada de processos para o logout...")
    comando_cleanup = [
        "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_CLEANUP
    ]
    resultado_cleanup = executar_comando_powershell(comando_cleanup, contexto_tarefa="Logout e Limpeza de Processos")
    is_sap_logged_in = False
    return jsonify(resultado_cleanup)

# --- Função Auxiliar ---
def executar_comando_powershell(comando, contexto_tarefa="Tarefa genérica", timeout_seconds=300):
    try:
        resultado = subprocess.run(comando, capture_output=True, check=True, text=False, timeout=timeout_seconds)
        output = resultado.stdout.decode('cp1252', errors='ignore').strip()
        return {"status": "sucesso", "mensagem": output}

    except subprocess.TimeoutExpired:
        print(f"ERRO: Timeout atingido na {contexto_tarefa}!")
        cleanup_command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_CLEANUP]
        subprocess.run(cleanup_command)
        return {"status": "erro", "mensagem": f"A {contexto_tarefa} excedeu o tempo limite de {timeout_seconds} segundos e foi finalizada."}
    
    except subprocess.CalledProcessError as e:
        erro_msg = e.stderr.decode('cp1252', errors='ignore').strip()
        return {"status": "erro", "mensagem": f"Erro crítico no PowerShell durante a {contexto_tarefa}: {erro_msg}"}
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro inesperado no Python durante a {contexto_tarefa}: {str(e)}"}

# --- Ponto de Entrada da Aplicação ---
if __name__ == '__main__':
    print("=====================================================")
    print("== Servidor de Automação Iniciado ==")
    print(f"== Acesse http://10.12.72.90:5000 no seu navegador ==")
    print("=====================================================")
    app.run(host='0.0.0.0', port=5000)