# 🏎️ F1 Telemetry Viewer

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![FastF1](https://img.shields.io/badge/FastF1-Powered-red.svg)](https://github.com/theOehrly/Fast-F1)

An interactive Formula 1 race visualization and telemetry analysis dashboard built with Python Flask backend and Phaser.js frontend.

![Dashboard Preview](docs/screenshots/dashboard-preview.png)

## ✨ Features

- **🗺️ Real-time Track Visualization** - Watch races unfold with smooth car animations on accurately rendered circuits
- **▶️ Interactive Race Replay** - Play, pause, rewind, fast-forward with adjustable speed (0.5x - 8x)
- **🏆 Live Leaderboard** - Real-time positions sorted by race distance with tyre compounds
- **📊 Driver Telemetry** - Speed, gear, throttle, brake, and DRS status for any driver
- **📈 Lap Time Analysis** - Compare lap times across all drivers with interactive charts
- **🛞 Tyre Strategy View** - Visualize pit stop strategies and compound choices
- **🌤️ Weather Data** - Track temperature, air temperature, humidity, and wind conditions
- **🎨 Team Colors** - Authentic F1 team colors for easy driver identification

## 🖼️ Screenshots

<details>
<summary>Click to view screenshots</summary>

### Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)

### Telemetry Analysis
![Telemetry](docs/screenshots/telemetry.png)

### Tyre Strategy
![Strategy](docs/screenshots/strategy.png)

</details>

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+, Flask, FastF1 |
| **Frontend** | Phaser.js 3.70, Chart.js, Vanilla JS |
| **Data** | FastF1 (Official F1 Telemetry) |
| **Deployment** | Docker, Docker Compose |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Avishkar1117/F1.git
cd F1

# Start with Docker Compose
docker-compose up

# Open http://localhost:8080 in your browser
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/Avishkar1117/F1.git
cd F1

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Open frontend/index.html in your browser
# Or serve with: python -m http.server 8080 --directory ../frontend
```

## 📁 Project Structure

```
F1/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Docker orchestration
│
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── f1_data_processor.py # FastF1 data processing
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
│
├── frontend/               # Web UI
│   ├── index.html         # Dashboard HTML
│   ├── css/
│   │   └── style.css      # Dark theme styles
│   ├── js/
│   │   ├── api.js         # API client
│   │   ├── game.js        # Phaser.js track scene
│   │   ├── telemetry.js   # Chart.js charts
│   │   └── main.js        # Main controller
│   └── assets/            # Static assets
│
├── docs/                   # Documentation
│   ├── SETUP.md           # Detailed setup guide
│   ├── API.md             # API documentation
│   └── screenshots/       # App screenshots
│
└── scripts/
    └── setup.sh           # Quick setup script
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sessions/<year>` | Get race schedule for a year |
| POST | `/api/load` | Load a session (year, round, type) |
| GET | `/api/frames?start=0&end=100` | Get frame range |
| GET | `/api/frame/<index>` | Get single frame |
| GET | `/api/telemetry/<driver>` | Get driver telemetry |
| GET | `/api/analysis/lap-times` | Lap time analysis |
| GET | `/api/analysis/tyre-strategy` | Tyre strategies |
| GET | `/api/weather` | Weather data |

See [API Documentation](docs/API.md) for full details.

## 🎮 Usage Guide

### 1. Select a Session
- Choose **Year** (2018-2024)
- Select **Race** from dropdown
- Pick **Session Type** (Race, Qualifying, Sprint)
- Click **Load Session**

### 2. Playback Controls
| Control | Action |
|---------|--------|
| ▶️ | Play |
| ⏸️ | Pause |
| ⏮️ | Go to start |
| ⏭️ | Go to end |
| ⏪ / ⏩ | Skip back/forward |
| Slider | Adjust speed (0.5x - 8x) |

### 3. Analyze Telemetry
- Click a driver in the leaderboard to see their telemetry
- View speed, gear, throttle, brake, DRS in real-time
- Switch to Analysis tabs for detailed charts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- [FastF1](https://github.com/theOehrly/Fast-F1) - F1 telemetry data access
- [Phaser.js](https://phaser.io/) - Game framework for track visualization
- [Chart.js](https://www.chartjs.org/) - Beautiful charts
- [IAmTomShaw/f1-race-replay](https://github.com/IAmTomShaw/f1-race-replay) - Inspiration

## ⚠️ Disclaimer

This project is not affiliated with Formula 1. All F1-related trademarks belong to their respective owners. Data is sourced from publicly available APIs for educational purposes.

---

Built with ❤️ for F1 fans