class F1Game extends Phaser.Scene {
  constructor() {
    super({ key: 'F1Game' })
    this.trackGraphics = null
    this.carSprites = {}
  }

  preload() {}

  create() {
    this.cameras.main.setBackgroundColor('#071029')
    this.trackGraphics = this.add.graphics()
  }

  drawTrack(track) {
    this.trackGraphics.clear()
    this.trackGraphics.lineStyle(2, 0xffffff, 0.2)

    const x = track.x
    const y = track.y
    this.trackGraphics.beginPath()
    this.trackGraphics.moveTo(x[0], y[0])
    for (let i = 1; i < x.length; i++) {
      this.trackGraphics.lineTo(x[i], y[i])
    }
    this.trackGraphics.strokePath()
  }

  updateFrame(frame) {
    const drivers = frame.drivers
    for (const code in drivers) {
      const d = drivers[code]
      if (!this.carSprites[code]) {
        const g = this.add.circle(d.x, d.y, 6, 0xff0000)
        this.carSprites[code] = g
      } else {
        this.carSprites[code].x = d.x
        this.carSprites[code].y = d.y
      }
    }
  }
}

function createGame(container) {
  const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: container,
    scene: [F1Game]
  }

  const game = new Phaser.Game(config)
  return game
}
