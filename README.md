# Mini Project 3 - Ride-Hailing Data Analysis

## 🚀 Project Overview

This is an improved Python-based data analysis application for ride-hailing data. The project provides comprehensive analytics, visualization, and insights generation capabilities.

## ✨ Features

- **Data Loading & Processing**: Robust data loading with cleaning and feature engineering
- **Temporal Analysis**: Hourly, daily, and weekly pattern analysis
- **Spatial Analysis**: Location-based insights and hotspot identification
- **Service Analysis**: Multi-service comparison and usage patterns
- **Driver Performance**: Driver efficiency and performance metrics
- **Visualization**: Comprehensive charts and graphs
- **License Plate Management**: Utilities for working with plate images
- **🆕 Real-Time Dashboard**: Web-based dashboard for Sky Harbor Airport display
  - **Feature 1: Parking Zone Status Grid**: Real-time visualization of parking zones with occupancy status
  - **Feature 2: Active Ride Queue**: Live display of active rides with license plates, wait times, and timestamps

## 📁 Project Structure

```
mini-project-3-mark-barlow/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── dashboard.py          # Web dashboard application
│   ├── data_loader.py       # Data loading and preprocessing
│   ├── analyzer.py          # Data analysis and insights
│   ├── visualizer.py        # Visualization generation
│   ├── plate_utils.py       # License plate image utilities
│   └── templates/
│       └── dashboard.html   # Dashboard HTML template
├── assets/
│   ├── ride_hailing.xlsx    # Main dataset
│   ├── map.png              # Map image
│   └── plates/              # License plate images
├── data/
│   ├── raw/                 # Raw data storage
│   ├── processed/           # Processed data
│   └── output/              # Analysis results and visualizations
├── tests/                   # Test files
├── docs/                    # Documentation
├── config/                  # Configuration files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

**Option A: Run Data Analysis**
```bash
python src/main.py
```

**Option B: Launch Web Dashboard**
```bash
python src/main.py --dashboard
```

The dashboard will be available at `http://localhost:5000` (or specify a different port with `--port`)

## 📊 Usage

### Basic Analysis

Run the main application to perform comprehensive analysis:

```bash
python src/main.py
```

This will:
- Load and clean the data
- Perform temporal, spatial, service, and driver analyses
- Generate insights
- Create visualizations
- Save results to `data/output/`

### Web Dashboard

Launch the real-time ride-hailing dashboard for airport display:

```bash
python src/main.py --dashboard
```

The dashboard provides:
- **Real-time updates** every 5 seconds
- **Parking Zone Status Grid**: 8x6 grid showing zone occupancy (green=available, yellow=moderate, red=busy)
- **Active Ride Queue**: List of current rides with license plates, service types, wait times, and timestamps
- **Live Statistics**: Total rides, active drivers, and occupied zones
- **Current Time Display**: Real-time clock synchronized with server
- **Airport-Style Design**: Dark blue theme optimized for large-screen displays

Perfect for displaying at Sky Harbor Airport waiting areas!

### Programmatic Usage

```python
from src.data_loader import RideHailingDataLoader
from src.analyzer import RideHailingAnalyzer
from src.visualizer import RideHailingVisualizer

# Load data
loader = RideHailingDataLoader("assets/ride_hailing.xlsx")
df = loader.clean_data()

# Analyze
analyzer = RideHailingAnalyzer(loader)
insights = analyzer.generate_insights()

# Visualize
visualizer = RideHailingVisualizer(analyzer)
visualizer.create_comprehensive_report()
```

## 📈 Output

The application generates:

1. **Visualizations** (saved to `data/output/`):
   - `temporal_analysis.png` - Time-based patterns
   - `spatial_analysis.png` - Location-based patterns
   - `service_analysis.png` - Service comparison
   - `driver_performance.png` - Driver metrics

2. **Analysis Results** (saved to `data/output/analysis_results.json`):
   - Summary statistics
   - Temporal analysis results
   - Spatial analysis results
   - Service analysis results
   - Driver performance metrics
   - Generated insights

## 🔍 Key Improvements

This version improves upon previous implementations by:

1. **Modular Architecture**: Clean separation of concerns with dedicated modules
2. **Comprehensive Analysis**: Multiple analysis dimensions (temporal, spatial, service, driver)
3. **Automated Insights**: Automatic generation of human-readable insights
4. **Enhanced Visualizations**: Professional, publication-ready charts
5. **Error Handling**: Robust error handling and logging
6. **Extensibility**: Easy to extend with new analysis methods
7. **Documentation**: Comprehensive code documentation

## 📝 Data Format

The application expects an Excel file with the following columns:
- `current_time`: Timestamp of the ride
- `slot_id`: Time slot identifier
- `x`, `y`: Spatial coordinates
- `reservation_id`: Unique reservation identifier
- `rider_id`: Rider identifier
- `driver_id`: Driver identifier
- `plate_number`: License plate number
- `service`: Service type (e.g., "Uber", "Lyft")

## 🧪 Testing

Run tests (when implemented):

```bash
pytest tests/
```

## 📚 Dependencies

See `requirements.txt` for full list. Key dependencies:
- pandas: Data manipulation
- numpy: Numerical computing
- matplotlib: Basic plotting
- seaborn: Statistical visualizations
- Pillow: Image processing
- openpyxl: Excel file handling
- flask: Web framework for dashboard
- qrcode: QR code generation

## 👤 Author

Mark Barlow

## 📄 License

ISC
