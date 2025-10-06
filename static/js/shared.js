// Este script controla o componente de feedback (botão flutuante e pop-up)

document.addEventListener('DOMContentLoaded', () => {
    const fab = document.getElementById('feedback-fab');
    const popup = document.getElementById('feedback-popup');
    // Verifica se os elementos existem na página antes de adicionar os listeners
    if (!fab || !popup) return;

    const closeBtn = document.getElementById('modal-close-btn');
    const optionButtons = document.querySelectorAll('.option-button');
    const modalOptions = document.getElementById('modal-options');
    const iframeContainer = document.getElementById('iframe-container');
    const iframe = iframeContainer.querySelector('iframe');
    const modalTitle = document.getElementById('modal-title');

    const forms = {
        demanda: { title: "Solicitação de Demanda", url: "https://docs.google.com/forms/d/e/1FAIpQLSdBvCg6jU3XjXn-dFLfwRZU-fj80fMbAT1vv6J6hg9yUIH1Jg/viewform?embedded=true" },
        sugestao: { title: "Sugestões de Melhoria", url: "https://docs.google.com/forms/d/e/1FAIpQLScIp_mkk0kMZuJgjchiq5O2fHGTkPSjXYpsi4G5Xw2e297C6w/viewform?embedded=true" }
    };

    const togglePopup = () => {
        // Reseta para a tela de opções sempre que abrir/fechar
        modalOptions.style.display = 'flex';
        iframeContainer.style.display = 'none';
        modalTitle.textContent = "FAQ";
        popup.classList.toggle('visible');
    };

    fab.addEventListener('click', togglePopup);
    closeBtn.addEventListener('click', togglePopup);

    // Adiciona um listener para fechar o popup se clicar fora dele
    // Usamos um overlay separado para isso (adicionado no HTML)
    const overlay = document.getElementById('feedback-modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            // Garante que o clique foi no overlay e não no conteúdo do popup
            if (e.target === overlay) {
                popup.classList.remove('visible');
            }
        });
    }


    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const formType = button.getAttribute('data-form');
            const formData = forms[formType];
            modalTitle.textContent = formData.title;
            iframe.src = formData.url;
            modalOptions.style.display = 'none';
            iframeContainer.style.display = 'block';
        });
    });
});