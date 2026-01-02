"""
F1 Telemetry Viewer - FastF1 Data Processor
Handles loading, processing, and caching of F1 telemetry data.
"""
import fastf1
import numpy as np
import pandas as pd
import os
from typing import Dict, List, Optional
from config import CACHE_DIR, FPS


class F1DataProcessor:
    """
    Processes F1 session data using FastF1 library.
    Handles track coordinates, driver positions, and telemetry.
    """
    
    def __init__(self):
        """Initialize the data processor and setup cache."""
        self._setup_cache()
        self.session = None
        self.frames = []
        self.driver_colors = {}
        self.track_coords = {}
        
    def _setup_cache(self):
        """Create and enable FastF1 cache directory."""
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        fastf1.Cache.enable_cache(CACHE_DIR)
    
    def get_race_schedule(self, year: int) -> List[Dict]:
        """
        Get all races for a specific year.
        
        Args:
            year: The F1 season year (e.g., 2024)
            
        Returns:
            List of race dictionaries with round, name, country, date
        """
        schedule = fastf1.get_event_schedule(year)
        races = []
        
        for _, event in schedule.iterrows():
            if 'Testing' not in str(event['EventName']):
                races.append({
                    'round': int(event['RoundNumber']),
                    'name': event['EventName'],
                    'country': event['Country'],
                    'date': str(event['EventDate'].date()),
                    'has_sprint': event['EventFormat'] == 'sprint_qualifying'
                })
        
        return races
    
    def load_and_process(self, year: int, round_num: int, session_type: str = 'R') -> Dict:
        """
        Load a session and process all data for replay.
        
        Args:
            year: Season year
            round_num: Race round number
            session_type: 'R' for Race, 'Q' for Qualifying, 'S' for Sprint
            
        Returns:
            Dictionary with total_frames, drivers, track, total_laps
        """
        # Load session
        self.session = fastf1.get_session(year, round_num, session_type)
        self.session.load(telemetry=True, weather=True)
        
        # Extract data
        self._extract_driver_colors()
        self._extract_track_coords()
        self._process_frames(fps=FPS)
        
        # Get total laps
        total_laps = int(self.session.laps['LapNumber'].max())
        
        return {
            'total_frames': len(self.frames),
            'drivers': list(self.driver_colors.keys()),
            'driver_colors': self.driver_colors,
            'track': self.track_coords,
            'total_laps': total_laps
        }
    
    def _extract_driver_colors(self):
        """Extract team colors for all drivers in the session."""
        try:
            color_mapping = fastf1.plotting.get_driver_color_mapping(self.session)
            
            self.driver_colors = {}
            for driver, hex_color in color_mapping.items():
                hex_color = hex_color.lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                self.driver_colors[driver] = {
                    'hex': f'#{hex_color}',
                    'rgb': [r, g, b]
                }
        except Exception as e:
            print(f"Error extracting driver colors: {e}")
            self.driver_colors = {}
    
    def _extract_track_coords(self):
        """
        Extract track boundary coordinates from the fastest lap.
        Normalizes coordinates for game rendering.
        """
        try:
            fastest_lap = self.session.laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            # Get circuit rotation
            circuit_info = self.session.get_circuit_info()
            rotation = circuit_info.rotation if hasattr(circuit_info, 'rotation') else 0
            
            x = telemetry['X'].values
            y = telemetry['Y'].values
            
            # Apply rotation
            if rotation:
                rad = np.deg2rad(rotation)
                x_rot = x * np.cos(rad) - y * np.sin(rad)
                y_rot = x * np.sin(rad) + y * np.cos(rad)
                x, y = x_rot, y_rot
            
            # Normalize to 0-1000 range for game rendering
            x_min, x_max = x.min(), x.max()
            y_min, y_max = y.min(), y.max()
            
            scale = 800 / max(x_max - x_min, y_max - y_min)
            
            x_norm = ((x - x_min) * scale + 100).tolist()
            y_norm = ((y - y_min) * scale + 100).tolist()
            
            self.track_coords = {
                'x': x_norm,
                'y': y_norm,
                'distance': telemetry['Distance'].values.tolist(),
                'width': 1000,
                'height': 1000,
                'scale': scale,
                'offset_x': float(x_min),
                'offset_y': float(y_min)
            }
            
        except Exception as e:
            print(f"Error extracting track coordinates: {e}")
            self.track_coords = {'x': [], 'y': []}
    
    def _process_frames(self, fps: int = 25):
        """
        Process telemetry data into frames for replay animation.
        
        Args:
            fps: Frames per second for the replay
        """
        drivers = self.session.drivers
        driver_codes = {num: self.session.get_driver(num)["Abbreviation"] for num in drivers}
        
        all_data = {}
        global_t_min, global_t_max = None, None
        
        # Collect telemetry for all drivers
        for driver_no in drivers:
            code = driver_codes[driver_no]
            laps = self.session.laps.pick_drivers(driver_no)
            
            if laps.empty:
                continue
            
            arrays = {
                't': [], 'x': [], 'y': [], 'dist': [],
                'speed': [], 'gear': [], 'throttle': [], 'brake': [],
                'drs': [], 'lap': [], 'tyre': []
            }
            
            for _, lap in laps.iterlaps():
                tel = lap.get_telemetry()
                if tel.empty:
                    continue
                
                t = tel["SessionTime"].dt.total_seconds().values
                arrays['t'].extend(t)
                arrays['x'].extend(tel["X"].values)
                arrays['y'].extend(tel["Y"].values)
                arrays['dist'].extend(tel["Distance"].values)
                arrays['speed'].extend(tel["Speed"].values)
                arrays['gear'].extend(tel["nGear"].values)
                arrays['throttle'].extend(tel["Throttle"].values)
                arrays['brake'].extend(tel["Brake"].values)
                arrays['drs'].extend(tel["DRS"].values)
                arrays['lap'].extend([lap.LapNumber] * len(t))
                arrays['tyre'].extend([str(lap.Compound)] * len(t))
            
            if not arrays['t']:
                continue
            
            # Convert to numpy arrays
            for key in arrays:
                if key != 'tyre':
                    arrays[key] = np.array(arrays[key])
            
            all_data[code] = arrays
            
            t_min, t_max = arrays['t'].min(), arrays['t'].max()
            global_t_min = t_min if global_t_min is None else min(global_t_min, t_min)
            global_t_max = t_max if global_t_max is None else max(global_t_max, t_max)
        
        # Create timeline
        dt = 1 / fps
        timeline = np.arange(global_t_min, global_t_max, dt)
        
        # Normalize coordinates
        scale = self.track_coords.get('scale', 1)
        offset_x = self.track_coords.get('offset_x', 0)
        offset_y = self.track_coords.get('offset_y', 0)
        
        self.frames = []
        
        # Build frames
        for i, t in enumerate(timeline):
            frame = {
                't': round(t - global_t_min, 3),
                'drivers': {}
            }
            
            for code, data in all_data.items():
                idx = np.searchsorted(data['t'], t)
                idx = min(idx, len(data['t']) - 1)
                
                # Normalize position
                x_norm = (data['x'][idx] - offset_x) * scale + 100
                y_norm = (data['y'][idx] - offset_y) * scale + 100
                
                frame['drivers'][code] = {
                    'x': round(float(x_norm), 1),
                    'y': round(float(y_norm), 1),
                    'dist': round(float(data['dist'][idx]), 1),
                    'speed': round(float(data['speed'][idx]), 1),
                    'gear': int(data['gear'][idx]),
                    'throttle': round(float(data['throttle'][idx]), 1),
                    'brake': round(float(data['brake'][idx]), 1),
                    'drs': int(data['drs'][idx]),
                    'lap': int(data['lap'][idx]),
                    'tyre': data['tyre'][idx] if idx < len(data['tyre']) else 'UNKNOWN'
                }
            
            self.frames.append(frame)
        
        # Add weather data
        self._add_weather_to_frames(timeline, global_t_min)
    
    def _add_weather_to_frames(self, timeline, t_offset):
        """Add weather information to each frame."""
        weather_df = getattr(self.session, 'weather_data', None)
        
        if weather_df is None or weather_df.empty:
            return
        
        try:
            weather_times = weather_df["Time"].dt.total_seconds().values
            
            for i, t in enumerate(timeline):
                idx = np.searchsorted(weather_times, t)
                idx = min(idx, len(weather_times) - 1)
                
                row = weather_df.iloc[idx]
                
                self.frames[i]['weather'] = {
                    'track_temp': round(float(row.get('TrackTemp', 0)), 1),
                    'air_temp': round(float(row.get('AirTemp', 0)), 1),
                    'humidity': round(float(row.get('Humidity', 0)), 1),
                    'wind_speed': round(float(row.get('WindSpeed', 0)), 1),
                    'rainfall': bool(row.get('Rainfall', False))
                }
        except Exception as e:
            print(f"Weather processing error: {e}")
    
    def get_frames(self, start: int, end: int) -> List[Dict]:
        """Get a range of frames for replay."""
        return self.frames[start:end]
    
    def get_frame(self, index: int) -> Dict:
        """Get a single frame by index."""
        if 0 <= index < len(self.frames):
            return self.frames[index]
        return {}
    
    def get_driver_telemetry(self, driver_code: str, lap: Optional[int] = None) -> Dict:
        """
        Get detailed telemetry for a specific driver.
        
        Args:
            driver_code: Three-letter driver code (e.g., 'VER')
            lap: Specific lap number, or None for fastest lap
            
        Returns:
            Dictionary with distance, speed, throttle, brake, gear, drs
        """
        laps = self.session.laps.pick_drivers(driver_code)
        
        if lap:
            lap_data = laps[laps['LapNumber'] == lap].iloc[0]
        else:
            lap_data = laps.pick_fastest()
        
        tel = lap_data.get_telemetry()
        
        return {
            'distance': tel['Distance'].values.tolist(),
            'speed': tel['Speed'].values.tolist(),
            'throttle': tel['Throttle'].values.tolist(),
            'brake': tel['Brake'].values.tolist(),
            'gear': tel['nGear'].values.tolist(),
            'drs': tel['DRS'].values.tolist(),
            'lap_time': str(lap_data['LapTime']),
            'compound': str(lap_data['Compound'])
        }
    
    def get_lap_time_analysis(self) -> Dict:
        """
        Get lap time analysis for all drivers.
        
        Returns:
            Dictionary with lap numbers, times, fastest, and average for each driver
        """
        laps = self.session.laps
        
        analysis = {}
        for driver in laps['Driver'].unique():
            driver_laps = laps[laps['Driver'] == driver]
            lap_times = driver_laps['LapTime'].dt.total_seconds().dropna().tolist()
            lap_numbers = driver_laps[driver_laps['LapTime'].notna()]['LapNumber'].tolist()
            
            analysis[driver] = {
                'lap_numbers': lap_numbers,
                'lap_times': lap_times,
                'fastest': min(lap_times) if lap_times else None,
                'average': sum(lap_times) / len(lap_times) if lap_times else None
            }
        
        return analysis
    
    def get_sector_analysis(self, driver_code: str) -> Dict:
        """
        Get sector time breakdown for a driver.
        
        Args:
            driver_code: Three-letter driver code
            
        Returns:
            Dictionary with sector times for each lap
        """
        laps = self.session.laps.pick_drivers(driver_code)
        
        sectors = {
            'lap_numbers': [],
            'sector1': [],
            'sector2': [],
            'sector3': []
        }
        
        for _, lap in laps.iterrows():
            if pd.notna(lap['Sector1Time']):
                sectors['lap_numbers'].append(int(lap['LapNumber']))
                sectors['sector1'].append(lap['Sector1Time'].total_seconds())
                sectors['sector2'].append(
                    lap['Sector2Time'].total_seconds() if pd.notna(lap['Sector2Time']) else None
                )
                sectors['sector3'].append(
                    lap['Sector3Time'].total_seconds() if pd.notna(lap['Sector3Time']) else None
                )
        
        return sectors
    
    def get_tyre_strategy(self) -> List[Dict]:
        """
        Get tyre strategy for all drivers.
        
        Returns:
            List of driver strategies with stint information
        """
        laps = self.session.laps
        strategies = []
        
        for driver in laps['Driver'].unique():
            driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
            
            stints = []
            current_compound = None
            stint_start = 1
            
            for _, lap in driver_laps.iterrows():
                compound = str(lap['Compound'])
                if compound != current_compound:
                    if current_compound:
                        stints.append({
                            'compound': current_compound,
                            'start_lap': stint_start,
                            'end_lap': int(lap['LapNumber']) - 1
                        })
                    current_compound = compound
                    stint_start = int(lap['LapNumber'])
            
            # Add final stint
            if current_compound:
                stints.append({
                    'compound': current_compound,
                    'start_lap': stint_start,
                    'end_lap': int(driver_laps['LapNumber'].max())
                })
            
            strategies.append({
                'driver': driver,
                'color': self.driver_colors.get(driver, {}).get('hex', '#ffffff'),
                'stints': stints
            })
        
        return strategies
    
    def get_weather_data(self) -> Dict:
        """
        Get weather data throughout the session.
        
        Returns:
            Dictionary with time series of weather conditions
        """
        weather_df = getattr(self.session, 'weather_data', None)
        
        if weather_df is None or weather_df.empty:
            return {'available': False}
        
        return {
            'available': True,
            'time': (weather_df['Time'].dt.total_seconds() / 60).tolist(),
            'track_temp': weather_df['TrackTemp'].tolist(),
            'air_temp': weather_df['AirTemp'].tolist(),
            'humidity': weather_df['Humidity'].tolist(),
            'wind_speed': weather_df['WindSpeed'].tolist()
        }
