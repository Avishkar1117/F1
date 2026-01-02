let telemetryChart = null

function initTelemetryChart(ctx) {
  telemetryChart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Speed', data: [], borderColor: 'rgb(255,99,132)', tension: 0.2 }] },
    options: { responsive: true, maintainAspectRatio: false }
  })
}

function updateTelemetryChart(data) {
  if (!telemetryChart) return
  telemetryChart.data.labels = data.distance
  telemetryChart.data.datasets[0].data = data.speed
  telemetryChart.update()
}
