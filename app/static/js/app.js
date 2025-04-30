// Função auxiliar para obter o token CSRF
function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    console.log('CSRF Token:', token);
    return token;
}

// Exemplo de requisição AJAX com CSRF
async function makeRequest(url, method, data = null) {
    const headers = {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/json'
    };

    const options = {
        method: method,
        headers: headers,
        credentials: 'same-origin'
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Função melhorada para fazer requisições com prevenção de cache
async function fetchWithCache(url, options = {}) {
    // Adicionar um parâmetro de timestamp para evitar cache
    const cacheBuster = `_t=${Date.now()}`;
    const urlWithCache = url.includes('?') ? `${url}&${cacheBuster}` : `${url}?${cacheBuster}`;
    
    try {
        const response = await fetch(urlWithCache, options);
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        throw error;
    }
}

// Exportar a função para que outros scripts possam usá-la
window.fetchWithCache = fetchWithCache;

// Função para verificar se o CSRF token está disponível
function checkCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (!token) {
        console.error('CSRF Token não encontrado! Adicione uma meta tag com o nome "csrf-token".');
        return false;
    }
    return token;
}

// Configurar CSRF para AJAX requests
document.addEventListener('DOMContentLoaded', function() {
    const token = checkCsrfToken();
    if (!token) return;

    console.log('CSRF Token configurado para requisições AJAX');
    
    // Aplicar a todas as requisições fetch
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        // Clonar options para não modificar o objeto original
        const newOptions = {...options};
        
        // Adicionar headers se não existirem
        if (!newOptions.headers) {
            newOptions.headers = {};
        } else if (!(newOptions.headers instanceof Object)) {
            // Se headers não for um objeto, converter para objeto
            newOptions.headers = {...newOptions.headers};
        }
        
        // Adicionar CSRF token para requisições não-GET
        if (!newOptions.method || newOptions.method.toUpperCase() !== 'GET') {
            newOptions.headers['X-CSRFToken'] = token;
        }
        
        // Adicionar credentials para enviar cookies
        newOptions.credentials = 'same-origin';
        
        return originalFetch(url, newOptions);
    };
    
    // Para jQuery (se você o utilizar)
    if (window.jQuery) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", token);
                }
            }
        });
    }
});