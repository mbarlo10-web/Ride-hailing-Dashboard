"""
Main Application Entry Point
Improved ride-hailing data analysis application
"""

import sys
import logging
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import RideHailingDataLoader
from analyzer import RideHailingAnalyzer
from visualizer import RideHailingVisualizer
from plate_utils import PlateImageManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application function"""
    logger.info("=" * 60)
    logger.info("Ride-Hailing Data Analysis Application")
    logger.info("=" * 60)
    
    # Initialize components
    logger.info("\n1. Initializing data loader...")
    data_loader = RideHailingDataLoader("assets/ride_hailing.xlsx")
    
    logger.info("\n2. Loading and cleaning data...")
    df = data_loader.clean_data()
    
    logger.info("\n3. Getting summary statistics...")
    summary = data_loader.get_summary_stats()
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Records: {summary['total_records']:,}")
    print(f"Unique Drivers: {summary['unique_drivers']}")
    print(f"Unique Riders: {summary['unique_riders']}")
    print(f"Unique License Plates: {summary['unique_plates']}")
    print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Services: {summary['services']}")
    print("=" * 60)
    
    # Initialize analyzer
    logger.info("\n4. Initializing analyzer...")
    analyzer = RideHailingAnalyzer(data_loader)
    
    # Perform analyses
    logger.info("\n5. Performing temporal analysis...")
    temporal_results = analyzer.analyze_temporal_patterns()
    
    logger.info("\n6. Performing spatial analysis...")
    spatial_results = analyzer.analyze_spatial_patterns()
    
    logger.info("\n7. Performing service analysis...")
    service_results = analyzer.analyze_service_patterns()
    
    logger.info("\n8. Analyzing driver performance...")
    driver_results = analyzer.analyze_driver_performance()
    
    # Generate insights
    logger.info("\n9. Generating insights...")
    insights = analyzer.generate_insights()
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    print("=" * 60)
    
    # Initialize plate manager
    logger.info("\n10. Initializing plate image manager...")
    plate_manager = PlateImageManager("assets/plates")
    plate_stats = plate_manager.get_statistics()
    print(f"\nPlate Images Available: {plate_stats.get('total_plates', 0)}")
    
    # Check plate availability in data
    plate_availability = plate_manager.get_plates_in_data(df)
    available_count = sum(1 for v in plate_availability.values() if v)
    print(f"Plates with Images in Data: {available_count} / {len(plate_availability)}")
    
    # Create visualizations
    logger.info("\n11. Creating visualizations...")
    visualizer = RideHailingVisualizer(analyzer, output_dir="data/output")
    visualizer.create_comprehensive_report()
    
    # Save analysis results
    logger.info("\n12. Saving analysis results...")
    results = {
        'summary': summary,
        'temporal_analysis': temporal_results,
        'spatial_analysis': spatial_results,
        'service_analysis': service_results,
        'driver_performance': driver_results,
        'insights': insights,
        'plate_statistics': plate_stats
    }
    
    output_path = Path("data/output/analysis_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)
    
    serializable_results = convert_to_serializable(results)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    logger.info(f"Analysis results saved to {output_path}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"Visualizations saved to: data/output/")
    print(f"Analysis results saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Ride-Hailing Data Analysis Application')
    parser.add_argument('--dashboard', action='store_true', 
                       help='Launch web dashboard instead of running analysis')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for dashboard server (default: 5000)')
    
    args = parser.parse_args()
    
    if args.dashboard:
        # Launch dashboard
        from dashboard import app, initialize_data
        initialize_data()
        logger.info("=" * 60)
        logger.info("Starting Ride-Hailing Dashboard Server...")
        logger.info(f"Dashboard available at: http://localhost:{args.port}")
        logger.info("Press Ctrl+C to stop the server")
        logger.info("=" * 60)
        app.run(debug=True, host='0.0.0.0', port=args.port)
    else:
        # Run analysis
        try:
            main()
        except KeyboardInterrupt:
            logger.info("\nAnalysis interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
            sys.exit(1)
