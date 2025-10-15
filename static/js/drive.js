document.addEventListener('DOMContentLoaded', () => {
    const fileList = document.getElementById('file-list');
    const breadcrumbs = document.getElementById('breadcrumbs');

    // Função principal para buscar e renderizar o conteúdo de uma pasta
    const fetchDirectory = async (path = '') => {
        try {
            const response = await fetch(`/api/browse?path=${encodeURIComponent(path)}`);
            if (!response.ok) {
                throw new Error('Falha ao carregar o diretório.');
            }
            const data = await response.json();
            render(data.path, data.content);
        } catch (error) {
            fileList.innerHTML = `<li class="file-item">${error.message}</li>`;
        }
    };

    // Função para renderizar os itens na tela
    const render = (currentPath, content) => {
        // Limpa a lista atual
        fileList.innerHTML = '';
        
        // Cria os breadcrumbs (navegação de caminho)
        renderBreadcrumbs(currentPath);

        // Adiciona um item para "voltar" se não estivermos na raiz
        if (currentPath) {
            const parentPath = currentPath.substring(0, currentPath.lastIndexOf('\\'));
            const upItem = document.createElement('li');
            upItem.className = 'file-item';
            upItem.innerHTML = `<i class="fas fa-arrow-up folder-icon"></i> <span>..</span>`;
            upItem.addEventListener('click', () => fetchDirectory(parentPath));
            fileList.appendChild(upItem);
        }

        // Renderiza as pastas e arquivos
        if (content.length === 0 && !currentPath) {
             fileList.innerHTML = `<li class="file-item">Nenhum item encontrado na pasta raiz.</li>`;
        } else {
            content.forEach(item => {
                const li = document.createElement('li');
                li.className = 'file-item';
                const itemPath = currentPath ? `${currentPath}\\${item.name}` : item.name;

                if (item.is_dir) {
                    li.innerHTML = `<i class="fas fa-folder folder-icon"></i> <span>${item.name}</span>`;
                    li.addEventListener('click', () => fetchDirectory(itemPath));
                } else {
                    li.innerHTML = `<i class="fas fa-file-alt file-icon"></i> <span>${item.name}</span>`;
                    li.addEventListener('click', () => {
                        // Inicia o download
                        window.location.href = `/api/download?path=${encodeURIComponent(itemPath)}`;
                    });
                }
                fileList.appendChild(li);
            });
        }
    };
    
    // Função para renderizar os breadcrumbs
    const renderBreadcrumbs = (path) => {
        breadcrumbs.innerHTML = '';
        const rootLink = document.createElement('a');
        rootLink.href = '#';
        rootLink.textContent = 'Raiz';
        rootLink.addEventListener('click', (e) => {
            e.preventDefault();
            fetchDirectory('');
        });
        breadcrumbs.appendChild(rootLink);

        if (path) {
            const parts = path.split('\\');
            let currentPath = '';
            parts.forEach((part, index) => {
                currentPath += (index > 0 ? '\\' : '') + part;
                const partLink = document.createElement('a');
                partLink.href = '#';
                partLink.textContent = part;
                const pathForLink = currentPath; // Captura o caminho atual
                partLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    fetchDirectory(pathForLink);
                });
                breadcrumbs.appendChild(document.createTextNode(' / '));
                breadcrumbs.appendChild(partLink);
            });
        }
    };

    // Carga inicial
    fetchDirectory('');
});