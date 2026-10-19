const ctx = document.getElementById('entropyChart');

const labels = Array.from({ length: 50 }, (_, i) => `t${i + 1}`);
const data = {
  labels,
  datasets: [{
    label: 'Entropy Score',
    data: Array(50).fill(0),
    borderColor: '#38bdf8',
    backgroundColor: 'rgba(56, 189, 248, 0.2)',
    fill: true,
    tension: 0.3,
  }]
};

const chart = new Chart(ctx, {
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

// WebSocket client to receive diagnostics and update chart
(function connectWS(){
  const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  const host = location.hostname || '127.0.0.1';
  const port = '8000';
  const wsUrl = `${protocol}://${host}:${port}/ws`;
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('WS connected to', wsUrl);
    // send a heartbeat to keep connection alive
    setInterval(() => { try { ws.send('ping') } catch(e){} }, 15000);
  };

  ws.onmessage = (evt) => {
    try {
      const msg = JSON.parse(evt.data);
      if(msg && msg.event === 'diagnostic' && msg.payload){
        const score = msg.payload.diagnosis ? msg.payload.diagnosis.entropy_score : null;
        if(typeof score === 'number'){
          // push to chart
          data.datasets[0].data.push(score);
          if(data.datasets[0].data.length > 50) data.datasets[0].data.shift();
          chart.update();
        }
      }
    } catch(e){
      console.warn('WS parse error', e);
    }
  };

  ws.onclose = () => {
    console.log('WS closed, retry in 3s');
    setTimeout(connectWS, 3000);
  };

  ws.onerror = (e) => {
    console.error('WS error', e);
    ws.close();
  };
})();
