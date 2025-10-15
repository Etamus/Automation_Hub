// Este script controla o componente de chatbot de feedback com análise de palavras-chave e botões de ação
document.addEventListener('DOMContentLoaded', () => {
    const fab = document.getElementById('feedback-fab');
    const popup = document.getElementById('feedback-popup');
    if (!fab || !popup) return;

    const closeBtn = document.getElementById('modal-close-btn');
    const chatMessages = document.getElementById('chat-messages');
    const iframeContainer = document.getElementById('iframe-container');
    const iframe = iframeContainer.querySelector('iframe');
    const modalTitle = document.getElementById('modal-title');
    const chatInputArea = document.getElementById('chat-input-area');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    const forms = {
        demanda: { title: "Solicitação de Demanda", url: "https://docs.google.com/forms/d/e/1FAIpQLSdBvCg6jU3XjXn-dFLfwRZU-fj80fMbAT1vv6J6hg9yUIH1Jg/viewform?embedded=true" },
        sugestao: { title: "Sugestões de Melhoria", url: "https://docs.google.com/forms/d/e/1FAIpQLScIp_mkk0kMZuJgjchiq5O2fHGTkPSjXYpsi4G5Xw2e297C6w/viewform?embedded=true" }
    };

    const keywords = {
        demanda: ['solicitar', 'demanda', 'automação', 'automatizar', 'robô', 'processo', 'tarefa', 'criar', 'quero', 'preciso', 'gostaria'],
        sugestao: ['sugestão', 'feedback', 'ideia', 'melhoria', 'mudar', 'ajustar', 'sugiro', 'poderia', 'poderiam']
    };

    const addMessage = (text, type, containsHtml = false, extraClass = '') => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type} ${extraClass}`;
        if (containsHtml) {
            messageDiv.innerHTML = text;
        } else {
            messageDiv.textContent = text;
        }
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const showForm = (formType) => {
        const formData = forms[formType];
        modalTitle.textContent = formData.title;
        iframe.src = formData.url;
        chatMessages.style.display = 'none';
        chatInputArea.style.display = 'none';
        iframeContainer.style.display = 'block';
    };

    const presentFormOption = (formType, introText) => {
        const formData = forms[formType];
        
        // 1. Envia a mensagem de texto
        addMessage(introText, 'bot-message');

        // 2. Com um pequeno delay, envia o balão com o botão
        setTimeout(() => {
            const buttonHtml = `<button class="chat-action-button" data-form="${formType}">${formData.title}</button>`;
            addMessage(buttonHtml, 'bot-message', true, 'button-bubble');

            // Adiciona o listener para o botão que acabamos de criar
            const newButton = chatMessages.querySelector(`button[data-form="${formType}"]`);
            if (newButton) {
                newButton.addEventListener('click', () => {
                    chatInput.disabled = true;
                    sendBtn.disabled = true;
                    showForm(formType);
                });
            }
        }, 800); // 800ms de delay
    };
    
    const resetChat = () => {
        popup.classList.remove('visible');
        setTimeout(() => {
            chatMessages.innerHTML = '';
            chatMessages.style.display = 'flex';
            chatInputArea.style.display = 'flex';
            chatInput.disabled = false;
            sendBtn.disabled = false;
            iframeContainer.style.display = 'none';
            iframe.src = 'about:blank';
            modalTitle.textContent = 'Assistente Virtual';
        }, 300);
    };
    
    const startConversation = () => {
        addMessage("Olá! Sou o assistente virtual.", 'bot-message');
        setTimeout(() => {
            addMessage("Por gentileza, descreva em poucas palavras o que deseja.", 'bot-message');
        }, 1200);
    };

    const toggleChat = () => {
        const isVisible = popup.classList.contains('visible');
        if (isVisible) {
            resetChat();
        } else {
            popup.classList.add('visible');
            if (chatMessages.children.length === 0) {
                startConversation();
            }
        }
    };
    
    const processUserInput = (userInput) => {
        const text = userInput.toLowerCase();
        
        const isDemanda = keywords.demanda.some(keyword => text.includes(keyword));
        const isSugestao = keywords.sugestao.some(keyword => text.includes(keyword));

        if (isDemanda && isSugestao) {
             addMessage("Não entendi muito bem. Sua mensagem parece ser tanto uma demanda quanto uma sugestão. Poderia esclarecer?", 'bot-message');
             chatInput.disabled = false;
             sendBtn.disabled = false;
        } else if (isDemanda) {
            presentFormOption('demanda', 'Para demandas, siga esse formulário:');
            chatInput.disabled = false;
            sendBtn.disabled = false;
        } else if (isSugestao) {
            presentFormOption('sugestao', 'Para sugestões, siga esse formulário:');
            chatInput.disabled = false;
            sendBtn.disabled = false;
        } else { 
            addMessage("Desculpe, não consegui identificar sua necessidade. Por favor, escreva novamente o que deseja em poucas palavras.", 'bot-message');
            chatInput.disabled = false;
            sendBtn.disabled = false;
        }
    };

    const handleUserInput = () => {
        const userInput = chatInput.value.trim();
        if (!userInput) return;

        addMessage(userInput, 'user-reply');
        chatInput.value = '';
        chatInput.disabled = true;
        sendBtn.disabled = true;

        setTimeout(() => {
            processUserInput(userInput);
        }, 1000);
    };

    fab.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', resetChat);
    sendBtn.addEventListener('click', handleUserInput);
    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleUserInput();
        }
    });
});