document.addEventListener("DOMContentLoaded", async function () {
    const categorySelect = document.getElementById("category");
    const form = document.getElementById("transactionForm");
    const statusMessage = document.getElementById("statusMessage");

    // 🔹 Função para buscar categorias
    async function loadCategories() {
        try {
            const response = await fetch("/categories/data");
            if (!response.ok) throw new Error("Erro ao carregar categorias");

            const data = await response.json();

            // Limpa as opções antes de inserir novas
            categorySelect.innerHTML = '<option value="" disabled selected>Selecione uma categoria</option>';

            // Adiciona as categorias vindas do backend
            data.values.forEach((id, index) => {
                const option = document.createElement("option");
                option.value = id;
                option.textContent = data.labels[index];
                categorySelect.appendChild(option);
            });

        } catch (error) {
            console.error("Erro ao buscar categorias:", error);
            categorySelect.innerHTML = '<option value="" disabled>Erro ao carregar categorias</option>';
        }
    }

    // 🔹 Carrega as categorias ao abrir a página
    await loadCategories();

    // 🔹 Envio do formulário
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const transactionData = Object.fromEntries(formData);

        try {
            const response = await fetch("/transactions", {
                method: "POST",
                body: new URLSearchParams(transactionData),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });

            if (response.ok) {
                statusMessage.textContent = "✅ Transação cadastrada com sucesso!";
                statusMessage.classList.add("text-green-600");
                form.reset();
                await loadCategories();
            } else {
                statusMessage.textContent = "❌ Erro ao cadastrar transação.";
                statusMessage.classList.add("text-red-600");
            }
        } catch (error) {
            console.error("Erro ao cadastrar transação:", error);
            statusMessage.textContent = "❌ Erro inesperado.";
            statusMessage.classList.add("text-red-600");
        }
    });
});

// Função para buscar e renderizar as últimas transações
async function renderRecentTransactions() {
    try {
        const response = await fetch('/dashboard/transactions_data');
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        const transactions = await response.json();
        const transactionsList = document.querySelector('#transactions-list');
        transactionsList.innerHTML = '';

        transactions.forEach(tx => {
            const isIncome = tx.is_income;
            const amountSign = isIncome ? '+' : '-';

            const transactionItem = document.createElement('li');
            transactionItem.className = 'py-3 flex justify-between items-center hover:bg-gray-50 rounded px-2 transition-colors duration-200';
            transactionItem.innerHTML = `
                <div class="flex items-center">
                    <div>
                        <p class="font-medium">${tx.description}</p>
                        <p class="text-sm text-gray-500">${new Date(tx.date).toLocaleDateString('pt-BR')} - ${tx.category}</p>
                    </div>
                </div>
                <span class="font-medium px-3 py-1 rounded-full">${amountSign}R$ ${Math.abs(tx.amount).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</span>
            `;
            transactionsList.appendChild(transactionItem);
        });
    } catch (error) {
        console.error("Erro ao buscar transações recentes:", error);
    }
}

// Chama a função para carregar as transações recentes quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", () => {
    renderRecentTransactions();
});