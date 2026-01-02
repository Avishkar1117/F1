from flask import Flask, request, jsonify
from flask_cors import CORS
from config import HOST, PORT, DEBUG
from f1_data_processor import F1DataProcessor

app = Flask(__name__)
CORS(app)
processor = F1DataProcessor()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/sessions/<int:year>', methods=['GET'])
def sessions(year):
    try:
        races = processor.get_race_schedule(year)
        return jsonify({'year': year, 'races': races})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load', methods=['POST'])
def load_session():
    body = request.get_json() or {}
    year = int(body.get('year', 2024))
    round_num = int(body.get('round', 1))
    session_type = body.get('session', 'R')

    try:
        meta = processor.load_and_process(year, round_num, session_type)
        return jsonify({'loaded': True, 'meta': meta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frames', methods=['GET'])
def frames():
    try:
        start = int(request.args.get('start', 0))
        end = int(request.args.get('end', start + 100))
        data = processor.get_frames(start, end)
        return jsonify({'start': start, 'end': end, 'frames': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/frame/<int:index>', methods=['GET'])
def frame(index):
    try:
        data = processor.get_frame(index)
        return jsonify({'index': index, 'frame': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telemetry/<string:driver_code>', methods=['GET'])
def telemetry(driver_code):
    lap = request.args.get('lap')
    try:
        data = processor.get_driver_telemetry(driver_code.upper(), int(lap) if lap else None)
        return jsonify({'driver': driver_code.upper(), 'telemetry': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/lap-times', methods=['GET'])
def lap_times():
    try:
        data = processor.get_lap_time_analysis()
        return jsonify({'analysis': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/tyre-strategy', methods=['GET'])
def tyre_strategy():
    try:
        data = processor.get_tyre_strategy()
        return jsonify({'strategies': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather', methods=['GET'])
def weather():
    try:
        data = processor.get_weather_data()
        return jsonify({'weather': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
