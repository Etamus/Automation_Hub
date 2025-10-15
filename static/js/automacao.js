document.addEventListener('DOMContentLoaded', () => {
    let isSapLoggedIn = false;
    let isBwLoggedIn = false;
    let lastUsedCredentials = {};
    let statusTimeout;

    // --- Seletores dos elementos da página ---
    const loginArea = document.getElementById('login-area');
    const loggedinArea = document.getElementById('loggedin-area');
    const subtitleText = document.getElementById('subtitle-text');
    const mainUser = document.getElementById('main-user');
    const mainPass = document.getElementById('main-pass');
    const statusBox = document.getElementById('status');
    const systemRadios = document.querySelectorAll('input[name="login_system"]');
    
    const mainLoginBtn = document.getElementById('main-toggle-btn');
    const mainLogoutBtn = document.getElementById('main-logout-btn');
    
    const bwExtractButton = document.getElementById('bw-extract-btn');
    const sapTasksSection = document.getElementById('sap-tasks-section');
    const bwTasksSection = document.getElementById('bw-tasks-section');
    const sapTaskButtons = document.querySelectorAll('.task-button[data-task-name]');

    const collapsibleHeaderSap = document.getElementById('collapsible-header-sap');
    const collapsibleContentSap = document.getElementById('collapsible-content-sap');
    const collapsibleHeaderBw = document.getElementById('collapsible-header-bw');
    const collapsibleContentBw = document.getElementById('collapsible-content-bw');

    // --- Funções de Controle da UI ---

    function showStatus(message, type = 'processing') {
        clearTimeout(statusTimeout);
        statusBox.className = `status-box ${type} visible`;
        statusBox.textContent = message;
        if (type === 'success' || type === 'error') {
            const delay = type === 'success' ? 5000 : 8000;
            statusTimeout = setTimeout(() => {
                statusBox.classList.remove('visible');
            }, delay);
        }
    }

    function setProcessing(message) {
        // Seleciona todos os botões, EXCETO o botão de logout
        document.querySelectorAll('.button:not(#main-logout-btn), .task-button').forEach(btn => {
            btn.disabled = true;
            btn.classList.add('disabled');
        });
        showStatus(message, 'processing');
    }

    function handleFetchError(error) {
        showStatus('Erro de comunicação com o servidor.', 'error');
        console.error('Erro de Fetch:', error);
        updateUiState();
    }
    
    function setResult(data, actionContext) {
        if (data.status === 'sucesso') {
            showStatus(data.mensagem, 'success');
            if (actionContext.type === 'login-sap') isSapLoggedIn = true;
            if (actionContext.type === 'logout-sap') isSapLoggedIn = false;
            if (actionContext.type === 'login-bw') isBwLoggedIn = true;
            if (actionContext.type === 'logout-bw') isBwLoggedIn = false;
            
            if (actionContext.type === 'macro' && data.download_file) {
                const downloadLink = document.querySelector('.task-button[data-task-name="Executar ZV62N"] .download-icon');
                if (downloadLink) {
                    downloadLink.href = '/download/' + data.download_file;
                    downloadLink.classList.remove('inactive');
                    downloadLink.title = `Baixar ${data.download_file}`;
                }
            }
        } else {
            showStatus('ERRO: ' + data.mensagem, 'error');
        }
        updateUiState();
    }

    function updateUiState() {
        document.querySelectorAll('.button, .task-button').forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('disabled');
        });
        
        const anySystemLoggedIn = isSapLoggedIn || isBwLoggedIn;
        
        loginArea.classList.toggle('hidden', anySystemLoggedIn);
        loggedinArea.classList.toggle('hidden', !anySystemLoggedIn);
        
        if (isSapLoggedIn) {
            subtitleText.textContent = "Selecione a tarefa de automatização disponível";
            sapTasksSection.classList.remove('hidden');
            bwTasksSection.classList.add('hidden');
            
            collapsibleHeaderSap.classList.add('open');
            collapsibleContentSap.style.maxHeight = collapsibleContentSap.scrollHeight + "px";
            
            collapsibleHeaderBw.classList.remove('open');
            collapsibleContentBw.style.maxHeight = null;
        } else if (isBwLoggedIn) {
            subtitleText.textContent = "Selecione a tarefa de extração disponível";
            sapTasksSection.classList.add('hidden');
            bwTasksSection.classList.remove('hidden');

            collapsibleHeaderSap.classList.remove('open');
            collapsibleContentSap.style.maxHeight = null;
            
            collapsibleHeaderBw.classList.add('open');
            collapsibleContentBw.style.maxHeight = collapsibleContentBw.scrollHeight + "px";
        } else {
            subtitleText.textContent = "Selecione a plataforma para acessar";
            sapTasksSection.classList.add('hidden');
            bwTasksSection.classList.add('hidden');
            
            collapsibleHeaderSap.classList.remove('open');
            collapsibleContentSap.style.maxHeight = null;
            
            collapsibleHeaderBw.classList.remove('open');
            collapsibleContentBw.style.maxHeight = null;
        }
    }
    
    // --- Listeners de Eventos ---
    
    mainLoginBtn.addEventListener('click', () => {
        const selectedSystem = document.querySelector('input[name="login_system"]:checked').value;
        if (!mainUser.value || !mainPass.value) { alert('Preencha Usuário e Senha.'); return; }
        lastUsedCredentials = { user: mainUser.value, pass: mainPass.value };

        let actionContext, endpoint, body = null;

        if (selectedSystem === 'sap') {
            actionContext = { type: 'login-sap' };
            endpoint = '/login-sap';
            setProcessing('Realizando login no SAP...');
            const formData = new URLSearchParams();
            formData.append('usuario', lastUsedCredentials.user);
            formData.append('senha', lastUsedCredentials.pass);
            body = formData;
        } else { // 'bw'
            actionContext = { type: 'login-bw', credentials: lastUsedCredentials };
            endpoint = '/login-bw-hana';
            setProcessing('Validando acesso ao BW HANA...');
        }
        fetch(endpoint, { method: 'POST', body: body }).then(r => r.json()).then(d => setResult(d, actionContext)).catch(handleFetchError);
    });

    mainLogoutBtn.addEventListener('click', () => {
         let actionContext, endpoint;
         if(isSapLoggedIn) {
            actionContext = { type: 'logout-sap' };
            endpoint = '/logout-sap';
            setProcessing('Realizando logout do SAP...');
         } else { // isBwLoggedIn
            actionContext = { type: 'logout-bw' };
            endpoint = '/logout-bw-hana';
            setProcessing('Realizando logout do BW HANA...');
         }
         fetch(endpoint, { method: 'POST' }).then(r => r.json()).then(d => setResult(d, actionContext)).catch(handleFetchError);
    });
    
    // Listener do "Extrair BW" precisa mirar no div de texto interno
    bwExtractButton.querySelector('.button-text').addEventListener('click', () => {
        if (bwExtractButton.classList.contains('disabled')) return;
        setProcessing('Executando extração BW HANA...');
        const formData = new URLSearchParams();
        formData.append('usuario', lastUsedCredentials.user);
        formData.append('senha', lastUsedCredentials.pass);
        fetch('/executar-bw-hana', { method: 'POST', body: formData }).then(r => r.json()).then(d => setResult(d, {type: 'bwhana_extract'})).catch(handleFetchError);
    });

    sapTaskButtons.forEach(taskButton => {
        const textPart = taskButton.querySelector('.button-text');
        const downloadPart = taskButton.querySelector('.download-icon');
        const taskName = taskButton.getAttribute('data-task-name');
        
        textPart.addEventListener('click', () => {
            if (taskButton.classList.contains('disabled')) return;
            setProcessing(`Executando '${taskName}'...`);
            const actionContext = { type: 'macro', button_name: taskName };
            const formData = new URLSearchParams();
            formData.append('macro', taskName);
            fetch('/executar-macro', { method: 'POST', body: formData }).then(r => r.json()).then(d => setResult(d, actionContext)).catch(handleFetchError);
        });

        if (downloadPart) {
            downloadPart.addEventListener('click', (event) => {
                if (taskButton.classList.contains('disabled')) { event.preventDefault(); return; }
                if (downloadPart.classList.contains('inactive')) {
                    event.preventDefault();
                    alert('Arquivo para download não encontrado.');
                }
            });
        }
    });

    collapsibleHeaderSap.addEventListener('click', () => {
        collapsibleHeaderSap.classList.toggle('open');
        if (collapsibleContentSap.style.maxHeight) {
            collapsibleContentSap.style.maxHeight = null;
        } else {
            collapsibleContentSap.style.maxHeight = collapsibleContentSap.scrollHeight + "px";
        }
    });
    
    collapsibleHeaderBw.addEventListener('click', () => {
        collapsibleHeaderBw.classList.toggle('open');
        if (collapsibleContentBw.style.maxHeight) {
            collapsibleContentBw.style.maxHeight = null;
        } else {
            collapsibleContentBw.style.maxHeight = collapsibleContentBw.scrollHeight + "px";
        }
    });
    
    updateUiState();
});