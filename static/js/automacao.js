document.addEventListener('DOMContentLoaded', () => {
    let isSapLoggedIn = false;
    let isBwLoggedIn = false;
    let lastUsedCredentials = {};
    let statusTimeout; // Variável para controlar o auto-hide da notificação

    const loginArea = document.getElementById('login-area');
    const loggedinArea = document.getElementById('loggedin-area');
    const mainSubtitle = document.getElementById('main-subtitle');
    const mainUser = document.getElementById('main-user');
    const mainPass = document.getElementById('main-pass');
    const statusBox = document.getElementById('status');
    const systemRadios = document.querySelectorAll('input[name="login_system"]');
    const mainLoginBtn = document.getElementById('main-toggle-btn');
    const mainLogoutBtn = document.getElementById('main-logout-btn');
    const bwExtractButton = document.getElementById('bw-extract-btn');
    const sapTasksSection = document.getElementById('sap-tasks-section');
    const sapTaskButtons = document.querySelectorAll('.task-button');
    const collapsibleHeader = document.getElementById('collapsible-header');
    const collapsibleContent = document.getElementById('collapsible-content');

    // LÓGICA DE NOTIFICAÇÃO RESTAURADA
    function showStatus(message, type = 'processing') {
        clearTimeout(statusTimeout); // Limpa qualquer notificação anterior
        statusBox.className = `status-box ${type} visible`;
        statusBox.textContent = message;

        // A notificação de "processando" não some sozinha
        if (type === 'success' || type === 'error') {
            const delay = type === 'success' ? 5000 : 8000; // Sucesso: 5s, Erro: 8s
            statusTimeout = setTimeout(() => {
                statusBox.classList.remove('visible');
            }, delay);
        }
    }

    function setProcessing(message) {
        document.querySelectorAll('.button, .task-button').forEach(btn => btn.disabled = true);
        showStatus(message, 'processing');
    }

    function handleFetchError(error) {
        showStatus('Erro de comunicação com o servidor.', 'error');
        console.error('Erro de Fetch:', error);
        updateUiState();
    }
    
    function setResult(data, actionContext) {
        if (data.status === 'sucesso') {
            showStatus(data.mensagem, 'success'); // Usa a nova função de notificação
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
            showStatus('ERRO: ' + data.mensagem, 'error'); // Usa a nova função de notificação
        }
        updateUiState();
    }

    function updateUiState() {
        // ... (o resto do seu arquivo JavaScript continua exatamente o mesmo)
        document.querySelectorAll('.button, .task-button').forEach(btn => btn.disabled = false);
        const anySystemLoggedIn = isSapLoggedIn || isBwLoggedIn;
        loginArea.classList.toggle('hidden', anySystemLoggedIn);
        loggedinArea.classList.toggle('hidden', !anySystemLoggedIn);
        if (isSapLoggedIn) {
            mainSubtitle.textContent = "Selecione a tarefa de automatização disponível";
            sapTasksSection.classList.remove('hidden');
            bwExtractButton.classList.add('hidden');
            collapsibleHeader.classList.add('open');
            collapsibleContent.style.maxHeight = collapsibleContent.scrollHeight + "px";
        } else if (isBwLoggedIn) {
            mainSubtitle.textContent = "Selecione a tarefa de extração disponível";
            sapTasksSection.classList.add('hidden');
            bwExtractButton.classList.remove('hidden');
            bwExtractButton.style.width = '75%';
        } else {
            mainSubtitle.textContent = "Selecione a plataforma para acessar";
            sapTasksSection.classList.add('hidden');
            bwExtractButton.classList.add('hidden');
            collapsibleHeader.classList.remove('open');
            collapsibleContent.style.maxHeight = null;
        }
    }
    
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
        } else {
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
         } else {
            actionContext = { type: 'logout-bw' };
            endpoint = '/logout-bw-hana';
            setProcessing('Realizando logout do BW HANA...');
         }
         fetch(endpoint, { method: 'POST' }).then(r => r.json()).then(d => setResult(d, actionContext)).catch(handleFetchError);
    });
    bwExtractButton.addEventListener('click', () => {
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
    collapsibleHeader.addEventListener('click', () => {
        collapsibleHeader.classList.toggle('open');
        if (collapsibleContent.style.maxHeight) {
            collapsibleContent.style.maxHeight = null;
        } else {
            collapsibleContent.style.maxHeight = collapsibleContent.scrollHeight + "px";
        }
    });
    updateUiState();
});