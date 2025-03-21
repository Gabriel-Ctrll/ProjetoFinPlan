// Configuração do Tailwind
const tailwindConfig = {
    // ... mova a configuração do tailwind para um arquivo separado tailwind.config.js
};

// Função para renderizar o gráfico de Distribuição de Gastos
async function renderDonutChart() {
    try {
        const response = await fetch('/categories/data');
        const data = await response.json();
        
        const chartOptions = {
            chart: { 
                type: "donut", 
                width: "100%", 
                height: "320", 
                toolbar: { show: false } 
            },
            colors: ["#3b82f6", "#f97316", "#a855f7", "#ec4899", "#14b8a6", "#84cc16"],
            labels: data.labels,
            dataLabels: { enabled: false },
            legend: {
                position: "bottom",
                fontSize: "14px",
                labels: { colors: "#64748b" },
                markers: { width: 12, height: 12, radius: 6 },
                itemMargin: { horizontal: 10, vertical: 5 }
            },
            tooltip: { y: {} },
            plotOptions: { 
                pie: { 
                    donut: { 
                        size: "70%", 
                        labels: { 
                            show: true, 
                            total: { show: true, label: "Total" } 
                        } 
                    } 
                } 
            },
            series: data.values
        };

        new ApexCharts(document.querySelector('[data-chart="chart_1"]'), chartOptions).render();
    } catch (error) {
        console.error("Erro ao buscar dados para o gráfico de Distribuição de Gastos:", error);
    }
}

// Função para renderizar o gráfico Financeiro
async function renderFinancialChart() {
    try {
        const response = await fetch('/dashboard/financial_data');
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const chartData = await response.json();
        const chartOptions = {
            chart: {
                type: "bar",
                width: "100%",
                height: "320",
                stacked: false,
                toolbar: { show: false },
                zoom: { enabled: false }
            },
            colors: ["#22c55e", "#ef4444"],
            plotOptions: { 
                bar: { 
                    horizontal: false, 
                    columnWidth: "70%", 
                    borderRadius: 6 
                } 
            },
            dataLabels: { enabled: false },
            grid: { borderColor: "#f1f1f1" },
            xaxis: {
                categories: chartData.labels,
                labels: { style: { colors: "#64748b" } },
                axisBorder: { show: false }
            },
            yaxis: { labels: { style: { colors: "#64748b" } } },
            tooltip: { y: {} },
            legend: { 
                position: "top", 
                horizontalAlign: "right", 
                labels: { colors: "#64748b" } 
            },
            series: [
                { name: "Receitas", data: chartData.incomes },
                { name: "Despesas", data: chartData.expenses }
            ]
        };

        new ApexCharts(document.getElementById('financialChart'), chartOptions).render();
    } catch (error) {
        console.error("Erro ao buscar dados para o gráfico financeiro:", error);
    }
}

// Função para atualizar os cards
async function updateCards() {
    try {
        const response = await fetch('/dashboard/summary');
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const summary = await response.json();
        const formatter = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 });

        document.getElementById('cardBalance').textContent = `R$ ${formatter.format(summary.balance)}`;
        document.getElementById('cardIncome').textContent = `R$ ${formatter.format(summary.total_income)}`;
        document.getElementById('cardExpense').textContent = `R$ ${formatter.format(summary.total_expense)}`;
    } catch (error) {
        console.error("Erro ao buscar dados dos cards:", error);
    }
}

// Função para renderizar transações recentes
async function renderRecentTransactions() {
    try {
        const response = await fetch('/dashboard/transactions_data');
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const transactions = await response.json();
        const transactionsList = document.querySelector('#transactions-list');
        transactionsList.innerHTML = '';

        transactions.forEach(tx => {
            const isIncome = tx.is_income;
            const transactionItem = createTransactionElement(tx, isIncome);
            transactionsList.appendChild(transactionItem);
        });
    } catch (error) {
        console.error("Erro ao buscar transações recentes:", error);
    }
}

// Função auxiliar para criar elemento de transação
function createTransactionElement(tx, isIncome) {
    const element = document.createElement('li');
    element.className = 'py-3 flex justify-between items-center hover:bg-gray-50 rounded px-2 transition-colors duration-200';
    
    const formatter = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 });
    const formattedAmount = formatter.format(Math.abs(tx.amount));
    const date = new Date(tx.date).toLocaleDateString('pt-BR');

    element.innerHTML = `
        <div class="flex items-center">
            <span class="material-symbols-outlined ${isIncome ? 'text-green-500' : 'text-red-500'} mr-3 ${isIncome ? 'bg-green-100' : 'bg-red-100'} p-2 rounded-full">
                ${isIncome ? 'payments' : 'trending_down'}
            </span>
            <div>
                <p class="font-medium">${tx.description}</p>
                <p class="text-sm text-gray-500">${date} - ${tx.category}</p>
            </div>
        </div>
        <span class="${isIncome ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'} font-medium px-3 py-1 rounded-full">
            ${isIncome ? '+' : '-'}R$ ${formattedAmount}
        </span>
    `;

    return element;
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    updateCards();
    renderFinancialChart();
    renderRecentTransactions();
    renderDonutChart();
});