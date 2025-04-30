// Configuração do Tailwind
const tailwindConfig = {
    // ... mova a configuração do tailwind para um arquivo separado tailwind.config.js
};

// Função para renderizar o gráfico de Distribuição de Gastos
async function renderDonutChart() {
    try {
        console.log("Iniciando carregamento do gráfico de distribuição de gastos");
        const response = await fetch('/categories/data');
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const data = await response.json();
        console.log("Dados recebidos para o gráfico de distribuição:", data);
        
        // Verificar se há dados para mostrar
        if (!data.labels || data.labels.length === 0) {
            document.querySelector('[data-chart="chart_1"]').innerHTML = 
                '<div class="flex flex-col items-center justify-center h-full">' +
                '<p class="text-gray-500">Não há dados de despesas para exibir.</p>' +
                '</div>';
            return;
        }
        
        // Limpar o elemento antes de renderizar novo gráfico
        document.querySelector('[data-chart="chart_1"]').innerHTML = '';
        
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
            tooltip: { 
                y: {
                    formatter: (val) => `R$ ${val.toFixed(2)}`
                } 
            },
            plotOptions: { 
                pie: { 
                    donut: { 
                        size: "70%", 
                        labels: { 
                            show: true, 
                            total: { 
                                show: true, 
                                label: "Total",
                                formatter: function (w) {
                                    const total = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                                    return `R$ ${total.toFixed(2)}`;
                                }
                            } 
                        } 
                    } 
                } 
            },
            series: data.values
        };

        const chart = new ApexCharts(document.querySelector('[data-chart="chart_1"]'), chartOptions);
        chart.render();
        console.log("Gráfico de distribuição renderizado com sucesso");
    } catch (error) {
        console.error("Erro ao buscar dados para o gráfico de Distribuição de Gastos:", error);
        document.querySelector('[data-chart="chart_1"]').innerHTML = 
            '<div class="flex flex-col items-center justify-center h-full">' +
            `<p class="text-red-500">Erro ao carregar o gráfico: ${error.message}</p>` +
            '</div>';
    }
}

// Função para renderizar o gráfico Financeiro
async function renderFinancialChart() {
    try {
        console.log("Iniciando carregamento do gráfico financeiro");
        const response = await fetch('/dashboard/financial_data');
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const chartData = await response.json();
        console.log("Dados recebidos para o gráfico financeiro:", chartData);
        
        // Limpar o elemento antes de renderizar novo gráfico
        document.getElementById('financialChart').innerHTML = '';
        
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
            yaxis: { 
                labels: { 
                    style: { colors: "#64748b" },
                    formatter: (val) => `R$ ${val.toFixed(0)}`
                } 
            },
            tooltip: { 
                y: {
                    formatter: (val) => `R$ ${val.toFixed(2)}`
                }
            },
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

        const chart = new ApexCharts(document.getElementById('financialChart'), chartOptions);
        chart.render();
        console.log("Gráfico financeiro renderizado com sucesso");
    } catch (error) {
        console.error("Erro ao buscar dados para o gráfico financeiro:", error);
        document.getElementById('financialChart').innerHTML = 
            '<div class="flex flex-col items-center justify-center h-full">' +
            `<p class="text-red-500">Erro ao carregar o gráfico: ${error.message}</p>` +
            '</div>';
    }
}

// Função para atualizar os cards
async function updateCards() {
    try {
        console.log("Buscando dados para os cards do dashboard...");
        // Usar fetchWithCache para evitar problemas de cache
        const response = await fetch('/dashboard/summary?' + new Date().getTime());
        if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
        
        const summary = await response.json();
        console.log("Dados dos cards recebidos:", summary);
        
        const formatter = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 });

        // Atualizar os valores dos cards e aplicar classes condicionais para o saldo
        document.getElementById('cardBalance').textContent = `R$ ${formatter.format(summary.balance)}`;
        if (summary.balance > 0) {
            document.getElementById('cardBalance').classList.remove('text-red-600');
            document.getElementById('cardBalance').classList.add('text-blue-600');
        } else if (summary.balance < 0) {
            document.getElementById('cardBalance').classList.remove('text-blue-600');
            document.getElementById('cardBalance').classList.add('text-red-600');
        }

        document.getElementById('cardIncome').textContent = `R$ ${formatter.format(summary.total_income)}`;
        document.getElementById('cardExpense').textContent = `R$ ${formatter.format(summary.total_expense)}`;
    } catch (error) {
        console.error("Erro ao buscar dados dos cards:", error);
        document.getElementById('cardBalance').textContent = "Erro ao carregar";
        document.getElementById('cardIncome').textContent = "Erro ao carregar";
        document.getElementById('cardExpense').textContent = "Erro ao carregar";
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

// Função para forçar atualização de dados
function forceRefresh() {
    console.log("Forçando atualização de dados do dashboard");
    updateCards();
    renderFinancialChart();
    renderRecentTransactions();
    renderDonutChart();
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    console.log("Iniciando carregamento do dashboard");
    
    // Adicionar botão de atualização ao dashboard
    const header = document.querySelector('header');
    if (header) {
        const refreshButton = document.createElement('button');
        refreshButton.innerHTML = `
            <span class="material-symbols-outlined mr-2">refresh</span>
            Atualizar dados
        `;
        refreshButton.className = 'mt-2 bg-blue-100 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors duration-200 flex items-center text-sm';
        refreshButton.onclick = forceRefresh;
        header.appendChild(refreshButton);
    }
    
    // Inicialização dos dados
    updateCards();
    renderFinancialChart();
    renderRecentTransactions();
    renderDonutChart();
    
    // Adiciona refresh automático a cada 5 minutos
    setInterval(forceRefresh, 300000); // 5 minutos
});