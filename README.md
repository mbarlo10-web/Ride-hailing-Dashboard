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
  - **Feature 1: Parking Zone Status Grid**: Real-time visualization of parking zones with dynamic occupancy status
  - **Feature 2: Active Ride Queue**: Live display of active rides with license plates, wait times, and timestamps
  - **Feature 3: Interactive Portfolio Demo Mode (Streamlit)**: Includes a live simulation engine with an adjustable speed slider, allowing users to fast-forward through historical data to observe real-time system behavior and zone volatility.

## 📁 Project Structure

```
mini-project-3-mark-barlow/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── dashboard.py         # Flask web dashboard
│   ├── streamlit_app.py     # Streamlit dashboard (deploy to share.streamlit.io)
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
└── README.md                # This file
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

**Option B: Launch Web Dashboard (Flask)**
```bash
python src/main.py --dashboard
```

The dashboard will be available at `http://localhost:5000` (or specify a different port with `--port`)

**Option C: Launch Streamlit Dashboard (Recommended for Portfolio Review)**
```bash
streamlit run src/streamlit_app.py
```

Opens at `http://localhost:8501`. Deploy to [Streamlit Community Cloud](https://share.streamlit.io) by connecting this repo and setting the main file to `src/streamlit_app.py`.

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
- **Parking Zone Status Grid**: 8x6 grid showing zone occupancy (green=available, yellow=moderate, red=busy)
- **Active Ride Queue**: List of current rides with license plates, service types, wait times, and timestamps
- **Live Statistics**: Total rides, active drivers, and occupied zones
- **Airport-Style Design**: Dark blue theme optimized for large-screen displays

Perfect for displaying at Sky Harbor Airport waiting areas!

### Streamlit Dashboard (Simulation & Portfolio Demo)

When run via `streamlit_app.py` (locally or on Streamlit Community Cloud), the dashboard acts as an interactive simulation engine:

- **Portfolio Demo Controls**: A sidebar slider allows you to adjust the simulation speed on the fly (for example, fast-forwarding so 1 real second equals many simulated minutes).
- **Time-Series Playback**: Replays the dataset in accelerated time, demonstrating dynamic UI updates as parking zones fill/empty and active rides cycle through the queue.
- **Analysis Highlights charts**:
  - Rides by hour of day
  - Rides by service
- Includes a **QR code sidebar** with instructions so passengers can quickly access Sky Harbor information on their phones.

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

1. **Interactive Simulation Engine**: Dynamic time-series playback and adjustable simulation speed for engaging portfolio demonstrations.
2. **Modular Architecture**: Clean separation of concerns with dedicated modules.
3. **Comprehensive Analysis**: Multiple analysis dimensions (temporal, spatial, service, driver).
4. **Automated Insights**: Automatic generation of human-readable insights.
5. **Enhanced Visualizations**: Professional, publication-ready charts.
6. **Error Handling**: Robust error handling and logging.
7. **Extensibility**: Easy to extend with new analysis methods.
8. **Documentation**: Comprehensive code documentation.

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

- `pandas`: Data manipulation  
- `numpy`: Numerical computing  
- `matplotlib`: Basic plotting  
- `seaborn`: Statistical visualizations  
- `Pillow`: Image processing  
- `openpyxl`: Excel file handling  
- `flask`: Web framework for dashboard  
- `streamlit`: Interactive web application framework  
- `qrcode`: QR code generation

## 👤 Author

Mark Barlow

## 📄 License

ISC
