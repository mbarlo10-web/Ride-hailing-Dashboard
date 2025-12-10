# Ride-Hailing Dashboard Features

## Overview

This project has been enhanced with a **real-time web dashboard** designed for display at Sky Harbor Airport in Phoenix, Arizona. The dashboard provides passengers with live ride-hailing information while waiting.

## Two New Features

### Feature 1: Real-Time Parking Zone Status Grid

**Location**: Left side of dashboard

**Description**: 
- Displays an 8x6 grid (48 zones) showing parking/waiting area status
- Each zone shows:
  - Zone identifier (e.g., "Zone A1", "Zone B2")
  - Current occupancy count
  - Color-coded status:
    - 🟢 **Green**: Available (0 rides)
    - 🟡 **Yellow**: Moderate occupancy (1-2 rides)
    - 🔴 **Red**: Busy (3+ rides)
- Updates every 5 seconds with real-time data
- Zones are mapped from spatial coordinates (x, y) in the dataset

**API Endpoint**: `/api/parking-zones`

**Use Case**: Helps passengers identify available waiting areas and see which zones are currently busy.

---

### Feature 2: Active Ride Queue Display

**Location**: Right side of dashboard

**Description**:
- Shows a live list of active rides in the system
- Each ride entry displays:
  - 🚗 Car icon
  - License plate number (in monospace font for readability)
  - Service type (Uber, Lyft, etc.)
  - Estimated wait time (in minutes)
  - Timestamp of ride request
- Displays up to 20 most recent active rides
- Updates every 5 seconds
- Sorted by most recent first

**API Endpoint**: `/api/active-rides`

**Use Case**: Allows passengers to see which rides are currently active, check wait times, and identify their ride by license plate number.

---

## Additional Dashboard Features

### Real-Time Clock
- Large, prominent time display in header
- Updates every second
- Shows current date and time

### Dashboard Statistics
- Total rides today
- Active drivers count
- Occupied zones count
- Updates automatically

### Airport-Style Design
- Dark blue gradient background (matching airport display aesthetics)
- High contrast for visibility on large screens
- Responsive layout optimized for wall-mounted displays
- QR code placeholder for passenger information scanning

## Technical Implementation

- **Framework**: Flask web application
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Data Source**: Excel file (`assets/ride_hailing.xlsx`)
- **Update Frequency**: 5 seconds for data, 1 second for time
- **Real-time Simulation**: Uses most recent data from dataset with 30-minute activity window

## Running the Dashboard

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Launch dashboard
python src/main.py --dashboard
```

The dashboard will be available at: `http://localhost:5000`

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/current-time` - Current time and date
- `GET /api/parking-zones` - Parking zone grid status
- `GET /api/active-rides` - Active ride queue
- `GET /api/dashboard-stats` - Overall statistics
- `GET /api/qr-code` - QR code data

## Design Philosophy

The dashboard is designed to:
1. **Be highly visible** - Large fonts, high contrast, clear icons
2. **Update frequently** - Real-time feel with 5-second refresh
3. **Be intuitive** - Color coding, clear labels, organized layout
4. **Support airport use** - Optimized for large screens in waiting areas
5. **Provide actionable information** - Helps passengers make decisions about where to wait and when their ride will arrive

