# ===================================================================
# == CÓDIGO FINAL E COMPLETO: servidor_unico.py                    ==
# ===================================================================

import subprocess
import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# --- Variáveis de Estado Globais ---
is_sap_logged_in = False
is_bw_hana_logged_in = False

# --- Caminhos e Configurações ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_RUNNER_SIMPLES = os.path.join(BASE_DIR, "runner.ps1")
SCRIPT_RUNNER_SAP_LOGIN = os.path.join(BASE_DIR, "sap_login_runner.ps1")
SCRIPT_CLEANUP = os.path.join(BASE_DIR, "cleanup_processes.ps1")
SCRIPT_BW_HANA = os.path.join(BASE_DIR, "bw_hana_extractor.py")
DOWNLOAD_DIR = "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros"

macros_disponiveis = {
    "Executar ZV62N": { "arquivo": "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\Input diário PÇ's.xlsm", "macro": "Org_relatorio_diario" },
    "Executar Outlook": { "arquivo": "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\Outlook_Macro.xlsm", "macro": "EnviarEmails" },
    "Executar Cancelamento Aging": { "arquivo": "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\Criação Aging.xlsm", "macro": "cancelar_fora_prazo" }
}

def find_file_by_prefix(directory, prefix):
    try:
        for filename in os.listdir(directory):
            if filename.startswith(prefix): return filename
    except FileNotFoundError: return None
    return None

# --- ROTAS DE PÁGINAS ---

@app.route('/')
def hub():
    return render_template('hub.html')

@app.route('/automacao')
def automacao():
    initial_zv62n_file = find_file_by_prefix(DOWNLOAD_DIR, "ZV62N")
    return render_template('automacao.html', macros=macros_disponiveis, initial_zv62n_file=initial_zv62n_file)

@app.route('/dashboards')
def dashboards():
    return render_template('dashboards.html')

@app.route('/drive')
def drive():
    return render_template('drive.html')


# --- ROTAS DE API (AÇÕES) ---

@app.route('/executar-macro', methods=['POST'])
def executar_macro():
    if not is_sap_logged_in: return jsonify({"status": "erro", "mensagem": "Acesso negado. Por favor, faça o login no SAP."}), 403
    nome_macro_selecionada = request.form['macro']
    config = macros_disponiveis.get(nome_macro_selecionada)
    if not config: return jsonify({"status": "erro", "mensagem": "Macro não encontrada!"}), 400
    comando = [ "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_RUNNER_SIMPLES, "-CaminhoArquivo", config['arquivo'], "-NomeMacro", config['macro'] ]
    contexto = f"tarefa '{nome_macro_selecionada}'"
    resultado = executar_comando_externo(comando, contexto_tarefa=contexto)
    if resultado['status'] == 'sucesso' and nome_macro_selecionada == "Executar ZV62N":
        nome_arquivo_download = find_file_by_prefix(DOWNLOAD_DIR, "ZV62N")
        if nome_arquivo_download: resultado['download_file'] = nome_arquivo_download
        else: resultado['mensagem'] += " (Aviso: arquivo de relatório não encontrado para download.)"
    return jsonify(resultado)

@app.route('/executar-bw-hana', methods=['POST'])
def executar_bw_hana():
    if not is_bw_hana_logged_in: return jsonify({"status": "erro", "mensagem": "Acesso negado. Por favor, faça o login no BW HANA."}), 403
    usuario = request.form['usuario']
    senha = request.form['senha']
    comando = [sys.executable, SCRIPT_BW_HANA, usuario, senha]
    resultado = executar_comando_externo(comando, contexto_tarefa="Extração BW HANA", timeout_seconds=600)
    if resultado['status'] == 'sucesso' and "ERRO:" in resultado['mensagem'].upper():
        resultado['status'] = 'erro'
    return jsonify(resultado)

@app.route('/download/<filename>')
def download_file(filename):
    try: return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)
    except FileNotFoundError: return "Arquivo não encontrado.", 404

@app.route('/login-sap', methods=['POST'])
def login_sap():
    global is_sap_logged_in, is_bw_hana_logged_in
    usuario = request.form['usuario']
    senha = request.form['senha']
    comando = [ "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_RUNNER_SAP_LOGIN, "-CaminhoArquivo", "C:\\Users\\Robo01\\Desktop\\Automacao_Final\\macros\\LoginSAP.xlsm", "-NomeMacro", "funcSAPOpen", "-Usuario", usuario, "-Senha", senha ]
    resultado = executar_comando_externo(comando, contexto_tarefa="Login SAP", timeout_seconds=20)
    if resultado['status'] == 'erro' and 'excedeu o tempo limite' in resultado['mensagem']:
        resultado['mensagem'] = "Login ou senha incorreto, ou o SAP demorou para responder."
    if resultado['status'] == 'sucesso':
        is_sap_logged_in = True
        is_bw_hana_logged_in = False
    else:
        is_sap_logged_in = False
    return jsonify(resultado)

@app.route('/logout-sap', methods=['POST'])
def logout_sap():
    global is_sap_logged_in
    is_sap_logged_in = False
    comando_cleanup = [ "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_CLEANUP ]
    resultado_cleanup = executar_comando_externo(comando_cleanup, contexto_tarefa="Logout SAP e Limpeza")
    return jsonify(resultado_cleanup)

@app.route('/login-bw-hana', methods=['POST'])
def login_bw_hana():
    global is_sap_logged_in, is_bw_hana_logged_in
    is_bw_hana_logged_in = True
    is_sap_logged_in = False
    return jsonify({"status": "sucesso", "mensagem": "Pronto para executar a extração BW HANA."})

@app.route('/logout-bw-hana', methods=['POST'])
def logout_bw_hana():
    global is_bw_hana_logged_in
    is_bw_hana_logged_in = False
    return jsonify({"status": "sucesso", "mensagem": "Estado de login BW HANA reiniciado."})

def executar_comando_externo(comando, contexto_tarefa="Tarefa genérica", timeout_seconds=300):
    try:
        resultado = subprocess.run(comando, capture_output=True, check=True, text=False, timeout=timeout_seconds)
        output = resultado.stdout.decode('cp1252', errors='ignore').strip()
        return {"status": "sucesso", "mensagem": output}
    except subprocess.TimeoutExpired:
        cleanup_command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_CLEANUP]
        subprocess.run(cleanup_command)
        return {"status": "erro", "mensagem": f"A {contexto_tarefa} excedeu o tempo limite e foi finalizada."}
    except subprocess.CalledProcessError as e:
        erro_msg = e.stdout.decode('cp1252', errors='ignore').strip() + "\n" + e.stderr.decode('cp1252', errors='ignore').strip()
        return {"status": "erro", "mensagem": f"Erro crítico durante a {contexto_tarefa}: {erro_msg.strip()}"}
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro inesperado no Python: {str(e)}"}


if __name__ == '__main__':
    print("Servidor Iniciado...")
    print(f"Acesse o Hub em http://10.12.72.90:5000")
    app.run(host='0.0.0.0', port=5000)
