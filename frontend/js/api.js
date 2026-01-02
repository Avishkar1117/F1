const API_BASE = '/api'

async function getSessions(year) {
  const res = await fetch(`${API_BASE}/sessions/${year}`)
  return await res.json()
}

async function loadSession(year, round, session) {
  const res = await fetch(`${API_BASE}/load`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ year, round, session })
  })
  return await res.json()
}

async function getFrames(start, end) {
  const res = await fetch(`${API_BASE}/frames?start=${start}&end=${end}`)
  return await res.json()
}

async function getDriverTelemetry(code, lap) {
  const url = lap ? `${API_BASE}/telemetry/${code}?lap=${lap}` : `${API_BASE}/telemetry/${code}`
  const res = await fetch(url)
  return await res.json()
}
