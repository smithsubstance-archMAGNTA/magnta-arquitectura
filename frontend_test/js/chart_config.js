const ctx = document.getElementById('entropyChart');

const labels = Array.from({ length: 10 }, (_, i) => `t${i + 1}`);
const data = {
  labels,
  datasets: [{
    label: 'Entropy Score',
    data: [0.12, 0.18, 0.25, 0.38, 0.44, 0.60, 0.72, 0.68, 0.48, 0.33],
    borderColor: '#38bdf8',
    backgroundColor: 'rgba(56, 189, 248, 0.2)',
    fill: true,
    tension: 0.3,
  }]
};

new Chart(ctx, {
  type: 'line',
  data,
  options: {
    responsive: true,
    scales: {
      y: {
        min: 0,
        max: 1,
        ticks: { color: '#cbd5e1' },
        grid: { color: '#334155' }
      },
      x: {
        ticks: { color: '#cbd5e1' },
        grid: { color: '#334155' }
      }
    },
    plugins: {
      legend: { labels: { color: '#e2e8f0' } }
    }
  }
});
