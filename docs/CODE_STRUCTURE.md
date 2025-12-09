# Code Structure Documentation

## Module Overview

### `data_loader.py`
**Purpose**: Load and preprocess ride-hailing data

**Key Classes**:
- `RideHailingDataLoader`: Main data loading and cleaning class

**Key Methods**:
- `load_data()`: Load data from Excel file
- `clean_data()`: Clean and preprocess data
- `get_summary_stats()`: Get dataset summary statistics
- `_add_derived_features()`: Add time-based and spatial features

### `analyzer.py`
**Purpose**: Perform comprehensive data analysis

**Key Classes**:
- `RideHailingAnalyzer`: Main analysis class

**Key Methods**:
- `analyze_temporal_patterns()`: Analyze time-based patterns
- `analyze_spatial_patterns()`: Analyze location-based patterns
- `analyze_service_patterns()`: Analyze service usage patterns
- `analyze_driver_performance()`: Analyze driver metrics
- `generate_insights()`: Generate human-readable insights

### `visualizer.py`
**Purpose**: Create visualizations

**Key Classes**:
- `RideHailingVisualizer`: Visualization generation class

**Key Methods**:
- `plot_temporal_analysis()`: Create temporal visualizations
- `plot_spatial_analysis()`: Create spatial visualizations
- `plot_service_analysis()`: Create service comparison charts
- `plot_driver_performance()`: Create driver performance charts
- `create_comprehensive_report()`: Generate all visualizations

### `plate_utils.py`
**Purpose**: Manage license plate images

**Key Classes**:
- `PlateImageManager`: License plate image management

**Key Methods**:
- `get_plate_image()`: Retrieve plate image
- `get_plate_info()`: Get image metadata
- `list_all_plates()`: List available plates
- `get_plates_in_data()`: Check plate availability in dataset

### `main.py`
**Purpose**: Application entry point

**Key Functions**:
- `main()`: Orchestrates the entire analysis pipeline

## Data Flow

1. **Data Loading**: `RideHailingDataLoader` loads raw data from Excel
2. **Data Cleaning**: Data is cleaned and features are engineered
3. **Analysis**: `RideHailingAnalyzer` performs various analyses
4. **Visualization**: `RideHailingVisualizer` creates charts
5. **Output**: Results saved to `data/output/`

## Extension Points

To add new analysis:
1. Add method to `RideHailingAnalyzer`
2. Call from `main.py`
3. Optionally add visualization in `RideHailingVisualizer`

To add new visualization:
1. Add method to `RideHailingVisualizer`
2. Call from `create_comprehensive_report()`
