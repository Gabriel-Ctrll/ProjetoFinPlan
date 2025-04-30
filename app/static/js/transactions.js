document.addEventListener("DOMContentLoaded", function() {
    console.log("Inicializando página de transações");
    const categorySelect = document.getElementById("category");
    const form = document.getElementById("transactionForm");
    const statusMessage = document.getElementById("statusMessage");

    // Remover a classe hidden do statusMessage
    if (statusMessage) {
        statusMessage.classList.remove("hidden");
        statusMessage.classList.add("invisible"); // Invisível mas ocupa espaço
    }

    // 🔹 Função para buscar categorias
    async function loadCategories() {
        try {
            console.log("Carregando categorias...");
            // Usar a nova rota que retorna todas as categorias
            const response = await fetch("/categories/all");
            if (!response.ok) throw new Error("Erro ao carregar categorias");

            const categories = await response.json();
            console.log("Categorias carregadas:", categories);

            if (!categorySelect) {
                console.error("Elemento select de categoria não encontrado!");
                return;
            }

            // Limpa as opções antes de inserir novas
            categorySelect.innerHTML = '<option value="" disabled selected>Selecione uma categoria</option>';

            // Adiciona as categorias vindas do backend
            categories.forEach(category => {
                const option = document.createElement("option");
                option.value = category.id;
                // Adiciona um indicador visual para diferenciar receitas de despesas
                const prefix = category.is_income ? "📈 " : "📉 ";
                option.textContent = prefix + category.name;
                categorySelect.appendChild(option);
            });

        } catch (error) {
            console.error("Erro ao buscar categorias:", error);
            if (categorySelect) {
                categorySelect.innerHTML = '<option value="" disabled>Erro ao carregar categorias</option>';
            }
        }
    }

    // 🔹 Carrega as categorias ao abrir a página
    loadCategories();

    // Função para atualizar a tabela completa de transações
    async function updateTransactionsTable() {
        try {
            console.log("Atualizando tabela de transações...");
            // Buscar as últimas transações do servidor
            const response = await fetch('/transactions/data?' + new Date().getTime());
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            
            const transactions = await response.json();
            console.log("Dados de transações recebidos:", transactions);
            
            // Referência para o corpo da tabela
            const transactionsTable = document.querySelector('#transactions-table');
            if (!transactionsTable) {
                console.error("Tabela de transações não encontrada!");
                return;
            }
            
            // Limpar a tabela atual
            transactionsTable.innerHTML = '';
            
            if (transactions.length === 0) {
                const emptyRow = document.createElement('tr');
                emptyRow.innerHTML = `
                    <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                        Nenhuma transação encontrada
                    </td>
                `;
                transactionsTable.appendChild(emptyRow);
                return;
            }
            
            // Preencher a tabela com os dados atualizados
            transactions.forEach(tx => {
                const row = document.createElement('tr');
                row.className = 'hover:bg-gray-50';
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="font-medium text-gray-900">${tx.description}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500">${new Date(tx.date).toLocaleDateString('pt-BR')}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                            ${tx.is_income ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                            ${tx.category_name}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm 
                        ${tx.is_income ? 'text-green-600' : 'text-red-600'}">
                        ${tx.is_income ? '+' : '-'}R$ ${Math.abs(tx.amount).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-center text-sm">
                        <button onclick="deleteTransaction(${tx.id}, '${tx.description.replace(/'/g, "\\'")}')" 
                            class="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-100 transition-colors duration-200"
                            title="Excluir transação">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </td>
                `;
                transactionsTable.appendChild(row);
            });
            
            // Atualizar também as transações recentes na sidebar
            renderRecentTransactions();
            
        } catch (error) {
            console.error("Erro ao atualizar tabela de transações:", error);
        }
    }

    // 🔹 Envio do formulário
    if (form) {
        form.addEventListener("submit", async function(event) {
            event.preventDefault();
            console.log("Formulário enviado");

            if (statusMessage) {
                statusMessage.textContent = "⏳ Processando...";
                statusMessage.classList.remove("invisible", "text-green-600", "text-red-600");
                statusMessage.classList.add("text-blue-600", "block");
            }

            const formData = new FormData(form);
            const transactionData = Object.fromEntries(formData);
            console.log("Dados da transação:", transactionData);

            try {
                const response = await fetch("/transactions", {
                    method: "POST",
                    body: new URLSearchParams(formData),
                    headers: { 
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    }
                });

                if (response.ok) {
                    console.log("Transação cadastrada com sucesso");
                    if (statusMessage) {
                        statusMessage.textContent = "✅ Transação cadastrada com sucesso!";
                        statusMessage.classList.remove("text-blue-600", "text-red-600", "invisible");
                        statusMessage.classList.add("text-green-600", "block");
                        
                        // Esconder o status após 3 segundos
                        setTimeout(() => {
                            statusMessage.classList.add("invisible");
                            statusMessage.classList.remove("block");
                        }, 3000);
                    }
                    form.reset();
                    await loadCategories(); // Recarregar as categorias
                    
                    // Pequeno atraso para garantir que o banco de dados já foi atualizado
                    setTimeout(() => {
                        // Atualizar a tabela de transações
                        updateTransactionsTable();
                    }, 300);
                } else {
                    console.error("Erro ao cadastrar transação:", response.status);
                    if (statusMessage) {
                        statusMessage.textContent = "❌ Erro ao cadastrar transação.";
                        statusMessage.classList.remove("text-blue-600", "text-green-600", "invisible");
                        statusMessage.classList.add("text-red-600", "block");
                    }
                }
            } catch (error) {
                console.error("Erro ao cadastrar transação:", error);
                if (statusMessage) {
                    statusMessage.textContent = `❌ Erro inesperado: ${error.message}`;
                    statusMessage.classList.remove("text-blue-600", "text-green-600", "invisible");
                    statusMessage.classList.add("text-red-600", "block");
                }
            }
        });
    } else {
        console.error("Formulário de transação não encontrado!");
    }

    // Função para buscar e renderizar as últimas transações
    async function renderRecentTransactions() {
        try {
            console.log("Carregando transações recentes...");
            const response = await fetch('/dashboard/transactions_data');
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            const transactions = await response.json();
            console.log("Transações carregadas:", transactions);
            
            const transactionsList = document.querySelector('#transactions-list');
            if (!transactionsList) {
                console.error("Lista de transações não encontrada!");
                return;
            }

            transactionsList.innerHTML = '';

            if (transactions.length === 0) {
                transactionsList.innerHTML = '<li class="py-3 text-center text-gray-500">Nenhuma transação encontrada</li>';
                return;
            }

            transactions.forEach(tx => {
                const isIncome = tx.is_income;
                const amountSign = isIncome ? '+' : '-';
                const colorClass = isIncome ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100';

                const transactionItem = document.createElement('li');
                transactionItem.className = 'py-3 flex justify-between items-center hover:bg-gray-50 rounded px-2 transition-colors duration-200';
                transactionItem.innerHTML = `
                    <div class="flex items-center">
                        <span class="material-symbols-outlined ${isIncome ? 'text-green-500' : 'text-red-500'} mr-3 ${isIncome ? 'bg-green-100' : 'bg-red-100'} p-2 rounded-full">
                            ${isIncome ? 'payments' : 'trending_down'}
                        </span>
                        <div>
                            <p class="font-medium">${tx.description}</p>
                            <p class="text-sm text-gray-500">${new Date(tx.date).toLocaleDateString('pt-BR')} - ${tx.category}</p>
                        </div>
                    </div>
                    <div class="flex items-center">
                        <span class="${colorClass} font-medium px-3 py-1 rounded-full mr-2">
                            ${amountSign}R$ ${Math.abs(tx.amount).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
                        </span>
                        <button 
                            onclick="deleteTransaction(${tx.id}, '${tx.description}')" 
                            class="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-100 transition-colors duration-200" 
                            title="Excluir transação">
                            <span class="material-symbols-outlined text-sm">delete</span>
                        </button>
                    </div>
                `;
                transactionsList.appendChild(transactionItem);
            });
        } catch (error) {
            console.error("Erro ao buscar transações recentes:", error);
            const transactionsList = document.querySelector('#transactions-list');
            if (transactionsList) {
                transactionsList.innerHTML = `<li class="py-3 text-center text-red-500">Erro ao carregar transações: ${error.message}</li>`;
            }
        }
    }

    // Função para excluir uma transação
    window.deleteTransaction = async function(id, description) {
        if (!confirm(`Tem certeza que deseja excluir a transação "${description}"?`)) {
            return;
        }
        
        try {
            const response = await fetch(`/transactions/${id}/delete`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    // Exibir feedback visual
                    if (statusMessage) {
                        statusMessage.textContent = `✅ Transação "${description}" excluída com sucesso!`;
                        statusMessage.classList.remove("invisible", "text-red-600", "text-blue-600");
                        statusMessage.classList.add("text-green-600", "block");
                        
                        // Esconder após 3 segundos
                        setTimeout(() => {
                            statusMessage.classList.add("invisible");
                            statusMessage.classList.remove("block");
                        }, 3000);
                    }
                    
                    // Pequeno atraso para garantir que o banco de dados já foi atualizado
                    setTimeout(() => {
                        // Atualizar a tabela de transações
                        updateTransactionsTable();
                        
                        // Se estiver na página do dashboard, atualizar os gráficos
                        if (typeof forceRefresh === 'function') {
                            forceRefresh();
                        }
                    }, 300);
                }
            } else {
                throw new Error('Falha ao excluir transação');
            }
        } catch (error) {
            console.error("Erro ao excluir transação:", error);
            if (statusMessage) {
                statusMessage.textContent = `❌ Erro ao excluir transação: ${error.message}`;
                statusMessage.classList.remove("invisible", "text-green-600", "text-blue-600");
                statusMessage.classList.add("text-red-600", "block");
            }
        }
    };

    // Inicializar a página
    loadCategories();
    updateTransactionsTable();
});