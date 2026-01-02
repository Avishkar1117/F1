import { renderLeaderboard } from './leaderboard.js'

document.addEventListener('DOMContentLoaded', async () => {
  const game = createGame('game-container')
  const ctx = document.getElementById('telemetryChart').getContext('2d')
  initTelemetryChart(ctx)

  document.getElementById('loadSchedule').addEventListener('click', async () => {
    const year = document.getElementById('year').value
    let res
    try {
      res = await getSessions(year)
    } catch (e) {
      alert('Failed to fetch sessions: ' + e.message)
      return
    }

    const select = document.getElementById('races')
    select.innerHTML = ''
    (res.races || []).forEach(r => {
      const opt = document.createElement('option')
      opt.value = r.round
      opt.textContent = `${r.round} - ${r.name} (${r.country})`
      select.appendChild(opt)
    })
  })

  document.getElementById('loadSession').addEventListener('click', async () => {
    const year = parseInt(document.getElementById('year').value)
    const round = parseInt(document.getElementById('races').value)
    const session = document.getElementById('sessionType').value

    let res
    try {
      res = await loadSession(year, round, session)
    } catch (e) {
      alert('Failed to load session: ' + e.message)
      return
    }

    if (res.loaded) {
      const meta = res.meta
      // draw track
      const scene = game.scene.keys['F1Game']
      scene.drawTrack(meta.track)

      // fetch frames
      let framesRes
      try {
        framesRes = await getFrames(0, 500)
      } catch (e) {
        alert('Failed to fetch frames: ' + e.message)
        return
      }

      const frames = framesRes.frames || []
      let idx = 0
      const loop = setInterval(() => {
        if (idx >= frames.length) { clearInterval(loop); return }
        scene.updateFrame(frames[idx])
        idx++
      }, 40)

      // populate leaderboard using shared renderer
      const lb = document.getElementById('leaderboard')
      renderLeaderboard(lb, meta.drivers || [])

    } else {
      alert('Failed to load session: ' + (res.error || 'unknown'))
    }
  })
})
