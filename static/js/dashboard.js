    const tempCtx = document.getElementById('chartTemp').getContext('2d');
    const humCtx = document.getElementById('chartHum').getContext('2d');
    const mCtx = document.getElementById('chartM').getContext('2d');

    const chartTemp = new Chart(tempCtx, {
      type: 'line',
      data: { labels: [], datasets: [{ label: 'Temperature', data: [], borderColor: 'red', fill: false }] }
    });

    const chartHum = new Chart(humCtx, {
      type: 'line',
      data: { labels: [], datasets: [{ label: 'Humidity', data: [], borderColor: 'blue', fill: false }] }
    });

    const chartM = new Chart(mCtx, {
      type: 'line',
      data: { labels: [], datasets: [{ label: 'Internal CPU', data: [], borderColor: 'green', fill: false }] }
    });

    async function fetchData() {
      const response = await fetch('/data');
      const result = await response.json();

      const labels = result.map(r => r.ts);
      const temps = result.map(r => r.t);
      const hums = result.map(r => r.h);
      const ms = result.map(r => r.m);

      chartTemp.data.labels = labels;
      chartTemp.data.datasets[0].data = temps;
      chartTemp.update();

      chartHum.data.labels = labels;
      chartHum.data.datasets[0].data = hums;
      chartHum.update();

      chartM.data.labels = labels;
      chartM.data.datasets[0].data = ms;
      chartM.update();
    }

    setInterval(fetchData, 3000); 