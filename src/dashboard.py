"""
Ride-Hailing Dashboard Application
Real-time dashboard for Sky Harbor Airport ride-hailing display
"""

import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, send_file
from datetime import datetime, timedelta
import pandas as pd
import json
import logging
import qrcode
from io import BytesIO
import base64

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import RideHailingDataLoader
from analyzer import RideHailingAnalyzer
from plate_utils import PlateImageManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set template folder explicitly
template_dir = Path(__file__).parent / 'templates'
app = Flask(__name__, template_folder=str(template_dir))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for real-time updates

# Global data storage
data_loader = None
analyzer = None
plate_manager = None
df = None


def initialize_data():
    """Initialize data components"""
    global data_loader, analyzer, plate_manager, df
    
    try:
        logger.info("Initializing dashboard data...")
        data_loader = RideHailingDataLoader("assets/ride_hailing.xlsx")
        df = data_loader.clean_data()
        analyzer = RideHailingAnalyzer(data_loader)
        plate_manager = PlateImageManager("assets/plates")
        logger.info("Dashboard data initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing dashboard data: {e}")
        raise


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/current-time')
def get_current_time():
    """Get current time for display"""
    now = datetime.now()
    return jsonify({
        'time': now.strftime('%H:%M'),
        'date': now.strftime('%A, %B %d, %Y'),
        'timestamp': now.isoformat()
    })


@app.route('/api/parking-zones')
def get_parking_zones():
    """
    Feature 1: Real-time parking zone status grid
    Returns grid of parking zones with occupancy status
    """
    if df is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Create a grid of parking zones (e.g., 8x6 grid)
    grid_rows = 8
    grid_cols = 6
    
    # Get recent rides (last 30 minutes simulated as "active")
    now = datetime.now()
    # Use the most recent data from the dataset
    latest_time = df['current_time'].max()
    
    # Get rides that would be "active" (within last 30 min of latest data)
    active_window = latest_time - timedelta(minutes=30)
    recent_rides = df[df['current_time'] >= active_window].copy()
    
    # Map spatial coordinates to grid zones
    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()
    
    # Create grid
    zones = []
    zone_occupancy = {}
    
    # Calculate occupancy per zone
    for idx, ride in recent_rides.iterrows():
        # Map x, y to grid coordinates
        x_norm = (ride['x'] - x_min) / (x_max - x_min) if (x_max - x_min) > 0 else 0.5
        y_norm = (ride['y'] - y_min) / (y_max - y_min) if (y_max - y_min) > 0 else 0.5
        
        grid_x = min(int(x_norm * grid_cols), grid_cols - 1)
        grid_y = min(int(y_norm * grid_rows), grid_rows - 1)
        
        zone_id = f"{grid_y}-{grid_x}"
        if zone_id not in zone_occupancy:
            zone_occupancy[zone_id] = []
        
        zone_occupancy[zone_id].append({
            'plate': ride.get('plate_number', 'N/A'),
            'service': ride.get('service', 'N/A'),
            'time': ride['current_time'].strftime('%H:%M')
        })
    
    # Build grid response
    grid = []
    for row in range(grid_rows):
        grid_row = []
        for col in range(grid_cols):
            zone_id = f"{row}-{col}"
            rides = zone_occupancy.get(zone_id, [])
            occupancy = len(rides)
            
            # Determine status: green (available), yellow (moderate), red (busy)
            # Thresholds: 0 = available, 1-2 = moderate, 3+ = busy
            if occupancy == 0:
                status = 'available'
                color = 'green'
            elif occupancy >= 1 and occupancy <= 2:
                status = 'moderate'
                color = 'yellow'
            else:  # occupancy >= 3
                status = 'busy'
                color = 'red'
            
            grid_row.append({
                'zone_id': f"Zone {chr(65 + row)}{col + 1}",
                'occupancy': occupancy,
                'status': status,
                'color': color,
                'rides': rides[:3]  # Show up to 3 rides
            })
        grid.append(grid_row)
    
    return jsonify({
        'grid': grid,
        'total_zones': grid_rows * grid_cols,
        'occupied_zones': sum(1 for row in grid for cell in row if cell['occupancy'] > 0),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/active-rides')
def get_active_rides():
    """
    Feature 2: Active ride queue display
    Returns list of active rides with license plates, wait times, and timestamps
    """
    if df is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get recent rides (simulating "active" rides)
    latest_time = df['current_time'].max()
    active_window = latest_time - timedelta(minutes=30)
    recent_rides = df[df['current_time'] >= active_window].copy()
    
    # Sort by time (most recent first)
    recent_rides = recent_rides.sort_values('current_time', ascending=False)
    
    # Limit to top 20 active rides
    active_rides = recent_rides.head(20).copy()
    
    # Calculate wait times (simulated - difference from latest time)
    active_rides['wait_time'] = (latest_time - active_rides['current_time']).dt.total_seconds() / 60
    
    # Build ride list
    rides = []
    for idx, ride in active_rides.iterrows():
        plate = ride.get('plate_number', 'N/A')
        
        # Check if plate image exists
        has_image = plate_manager.get_plate_image(plate) is not None if plate_manager else False
        
        # Get service type
        service = ride.get('service', 'N/A')
        
        # Calculate passenger count and wait time (simulated metrics)
        # Using reservation_id and rider_id to simulate passenger info
        passenger_count = 1  # Default
        estimated_wait = max(1, int(ride['wait_time']))
        
        rides.append({
            'plate_number': plate,
            'service': service,
            'time': ride['current_time'].strftime('%H:%M'),
            'wait_time': estimated_wait,
            'passenger_count': passenger_count,
            'has_image': has_image,
            'zone': f"Zone {chr(65 + (idx % 8))}{(idx % 6) + 1}",  # Simulated zone
            'status': 'arriving' if estimated_wait < 5 else 'waiting'
        })
    
    return jsonify({
        'rides': rides,
        'total_active': len(rides),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    if df is None or analyzer is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get summary stats
    summary = data_loader.get_summary_stats()
    
    # Get recent activity
    latest_time = df['current_time'].max()
    recent_window = latest_time - timedelta(hours=1)
    recent_count = len(df[df['current_time'] >= recent_window])
    
    return jsonify({
        'total_rides_today': recent_count,
        'active_drivers': df['driver_id'].nunique(),
        'services_available': list(df['service'].unique()) if 'service' in df.columns else [],
        'last_update': latest_time.isoformat(),
        'airport': 'Sky Harbor Airport - Phoenix, AZ'
    })


@app.route('/info')
def info_page():
    """Information page for passengers scanning QR code - explains how to use the ride-hailing display"""
    return render_template('info.html')


@app.route('/api/qr-code')
def get_qr_code_data():
    """Generate QR code data for passenger scanning"""
    # QR code links to info page that explains how to use the ride-hailing display
    from flask import request
    host = request.host  # Gets the host from the request (works for localhost or actual domain)
    qr_url = f'http://{host}/info'
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return jsonify({
        'url': qr_url,
        'image': f'data:image/png;base64,{img_base64}',
        'message': 'Scan for ride-hailing information at Sky Harbor Airport'
    })


@app.route('/api/qr-code-image')
def get_qr_code_image():
    """Serve QR code as PNG image"""
    # Generate QR code with info page URL
    # Use the actual IP address so phones can access it when scanning QR code
    from flask import request
    # Get the host from request, but replace localhost with actual IP for QR codes
    host = request.host
    # If accessing via localhost, use the network IP for QR code (so phones can connect)
    if 'localhost' in host or '127.0.0.1' in host:
        # Try to get the actual network IP
        import socket
        try:
            # Connect to a remote address to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            port = request.environ.get('SERVER_PORT', '5003')
            qr_url = f'http://{local_ip}:{port}/info'
        except:
            # Fallback to request host
            qr_url = f'http://{host}/info'
    else:
        qr_url = f'http://{host}/info'
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(img_buffer, mimetype='image/png')


if __name__ == '__main__':
    initialize_data()
    logger.info("Starting Ride-Hailing Dashboard Server...")
    logger.info("Dashboard available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

