# ===================================================================
<<<<<<< HEAD
# == CÓDIGO CORRIGIDO: servidor_unico.py                           ==
=======
# == CÓDIGO ATUALIZADO: servidor_unico.py                          ==
# == (Adicionada a nova rota /drive)                               ==
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
# ===================================================================

import subprocess
import os
<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Variável de Estado Global ---
is_sap_logged_in = False

# --- Caminhos e Configurações ---
=======
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

is_sap_logged_in = False
is_bw_hana_logged_in = False
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_RUNNER_SIMPLES = os.path.join(BASE_DIR, "runner.ps1")
SCRIPT_RUNNER_SAP_LOGIN = os.path.join(BASE_DIR, "sap_login_runner.ps1")
SCRIPT_CLEANUP = os.path.join(BASE_DIR, "cleanup_processes.ps1")
<<<<<<< HEAD

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
        
=======
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

# --- NOVA ROTA PARA A PÁGINA "EM DESENVOLVIMENTO" ---
@app.route('/drive')
def drive():
    return render_template('drive.html')


# --- ROTAS DE API (O resto do código continua o mesmo) ---

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
        else: resultado['mensagem'] += " (Aviso: arquivo não encontrado.)"
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
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
    return jsonify(resultado)

@app.route('/logout-sap', methods=['POST'])
def logout_sap():
    global is_sap_logged_in
<<<<<<< HEAD
    print("Iniciando limpeza forçada de processos para o logout...")
    comando_cleanup = [
        "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_CLEANUP
    ]
    resultado_cleanup = executar_comando_powershell(comando_cleanup, contexto_tarefa="Logout e Limpeza de Processos")
    is_sap_logged_in = False
    return jsonify(resultado_cleanup)

# --- Função Auxiliar ---
def executar_comando_powershell(comando, contexto_tarefa="Tarefa genérica", timeout_seconds=300):
=======
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
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
    try:
        resultado = subprocess.run(comando, capture_output=True, check=True, text=False, timeout=timeout_seconds)
        output = resultado.stdout.decode('cp1252', errors='ignore').strip()
        return {"status": "sucesso", "mensagem": output}
<<<<<<< HEAD

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
=======
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
>>>>>>> 450f75c (Atualizações Gerais e Novos Aprimoramentos)
    app.run(host='0.0.0.0', port=5000)