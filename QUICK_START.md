# Quick Start Guide

## Setup

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

**Launch the web dashboard:**
```bash
python src/main.py --dashboard
```

The dashboard will start on `http://localhost:5000`

Open your browser and navigate to:
- **http://localhost:5000** - View the dashboard

The dashboard will automatically:
- Load ride-hailing data from `assets/ride_hailing.xlsx`
- Display real-time parking zone status (updates every 5 seconds)
- Show active ride queue (updates every 5 seconds)
- Update the clock every second

## Running Data Analysis

**Run the standard analysis:**
```bash
python src/main.py
```

This will:
- Perform comprehensive data analysis
- Generate visualizations
- Save results to `data/output/`

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, specify a different port:
```bash
python src/main.py --dashboard --port 5001
```

### Data File Not Found
Make sure `assets/ride_hailing.xlsx` exists in the project root.

### Template Not Found
Make sure `src/templates/dashboard.html` exists. If not, the templates directory may need to be created.

## Dashboard Features

- **Parking Zone Grid**: 8x6 grid showing zone occupancy
- **Active Rides**: Live list of rides with license plates and wait times
- **Real-time Updates**: Automatic refresh every 5 seconds
- **Airport Design**: Optimized for large-screen displays

## Stopping the Dashboard

Press `Ctrl+C` in the terminal where the dashboard is running.

