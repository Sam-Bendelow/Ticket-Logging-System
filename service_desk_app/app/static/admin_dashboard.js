
async function fetchTicketStats() {
    const response = await fetch('/api/ticket-stats');
    const data = await response.json();

    const categoryLabels = data.categories.map(c => c.category);
    const categoryCounts = data.categories.map(c => c.count);

    const userLabels = data.users.map(u => u.user);
    const userCounts = data.users.map(u => u.count);

    new Chart(document.getElementById('categoryPieChart'), {
        type: 'pie',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryCounts,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Tickets by Category',
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    });

    new Chart(document.getElementById('userBarChart'), {
        type: 'bar',
        data: {
            labels: userLabels,
            datasets: [{
                label: 'Tickets per User',
                data: userCounts,
                backgroundColor: '#36A2EB'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Tickets Raised per User',
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', fetchTicketStats);
