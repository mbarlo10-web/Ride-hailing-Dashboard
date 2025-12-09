"""
Ride-Hailing Data Analysis Module
Improved analytics and insights generation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RideHailingAnalyzer:
    """Enhanced analyzer for ride-hailing data"""
    
    def __init__(self, data_loader):
        """
        Initialize analyzer with data loader
        
        Args:
            data_loader: RideHailingDataLoader instance
        """
        self.data_loader = data_loader
        self.df = data_loader.get_dataframe(processed=True)
    
    def analyze_temporal_patterns(self) -> Dict:
        """
        Analyze temporal patterns in ride data
        
        Returns:
            Dictionary with temporal analysis results
        """
        logger.info("Analyzing temporal patterns...")
        
        results = {
            'hourly_distribution': self.df.groupby('hour').size().to_dict(),
            'day_of_week_distribution': self.df.groupby('day_of_week').size().to_dict(),
            'weekend_vs_weekday': {
                'weekend': int(self.df[self.df['is_weekend'] == 1].shape[0]),
                'weekday': int(self.df[self.df['is_weekend'] == 0].shape[0])
            },
            'peak_hours': self._identify_peak_hours(),
            'daily_trends': self._calculate_daily_trends()
        }
        
        return results
    
    def _identify_peak_hours(self) -> List[int]:
        """Identify peak hours based on ride volume"""
        hourly_counts = self.df.groupby('hour').size()
        threshold = hourly_counts.quantile(0.75)
        peak_hours = hourly_counts[hourly_counts >= threshold].index.tolist()
        return sorted(peak_hours)
    
    def _calculate_daily_trends(self) -> Dict:
        """Calculate daily trends"""
        daily_counts = self.df.groupby('date').size()
        return {
            'average_daily_rides': float(daily_counts.mean()),
            'max_daily_rides': int(daily_counts.max()),
            'min_daily_rides': int(daily_counts.min()),
            'std_daily_rides': float(daily_counts.std())
        }
    
    def analyze_spatial_patterns(self) -> Dict:
        """
        Analyze spatial patterns in ride data
        
        Returns:
            Dictionary with spatial analysis results
        """
        logger.info("Analyzing spatial patterns...")
        
        results = {
            'hotspots': self._identify_hotspots(),
            'spatial_distribution': {
                'x_mean': float(self.df['x'].mean()),
                'x_std': float(self.df['x'].std()),
                'y_mean': float(self.df['y'].mean()),
                'y_std': float(self.df['y'].std())
            },
            'coverage_area': self._calculate_coverage_area()
        }
        
        return results
    
    def _identify_hotspots(self, grid_size: int = 10) -> List[Dict]:
        """Identify high-activity hotspots"""
        # Create grid
        x_bins = pd.cut(self.df['x'], bins=grid_size, labels=False)
        y_bins = pd.cut(self.df['y'], bins=grid_size, labels=False)
        
        # Count rides per grid cell
        grid_counts = pd.DataFrame({
            'x_bin': x_bins,
            'y_bin': y_bins
        }).groupby(['x_bin', 'y_bin']).size().reset_index(name='count')
        
        # Get top hotspots
        top_hotspots = grid_counts.nlargest(5, 'count')
        
        hotspots = []
        for _, row in top_hotspots.iterrows():
            x_range = pd.cut(self.df['x'], bins=grid_size).cat.categories[int(row['x_bin'])]
            y_range = pd.cut(self.df['y'], bins=grid_size).cat.categories[int(row['y_bin'])]
            hotspots.append({
                'x_range': str(x_range),
                'y_range': str(y_range),
                'ride_count': int(row['count'])
            })
        
        return hotspots
    
    def _calculate_coverage_area(self) -> Dict:
        """Calculate spatial coverage area"""
        x_range = self.df['x'].max() - self.df['x'].min()
        y_range = self.df['y'].max() - self.df['y'].min()
        
        return {
            'x_range': float(x_range),
            'y_range': float(y_range),
            'estimated_area': float(x_range * y_range)
        }
    
    def analyze_service_patterns(self) -> Dict:
        """
        Analyze patterns by service type
        
        Returns:
            Dictionary with service analysis results
        """
        logger.info("Analyzing service patterns...")
        
        if 'service' not in self.df.columns:
            return {}
        
        results = {
            'service_distribution': self.df['service'].value_counts().to_dict(),
            'service_by_hour': self.df.groupby(['service', 'hour']).size().unstack(fill_value=0).to_dict(),
            'service_by_day': self.df.groupby(['service', 'day_of_week']).size().unstack(fill_value=0).to_dict(),
            'top_drivers_by_service': self._get_top_drivers_by_service()
        }
        
        return results
    
    def _get_top_drivers_by_service(self, top_n: int = 5) -> Dict:
        """Get top drivers by service type"""
        top_drivers = {}
        for service in self.df['service'].unique():
            service_df = self.df[self.df['service'] == service]
            driver_counts = service_df['driver_id'].value_counts().head(top_n)
            top_drivers[service] = driver_counts.to_dict()
        return top_drivers
    
    def analyze_driver_performance(self) -> Dict:
        """
        Analyze driver performance metrics
        
        Returns:
            Dictionary with driver performance analysis
        """
        logger.info("Analyzing driver performance...")
        
        driver_stats = self.df.groupby('driver_id').agg({
            'reservation_id': 'count',
            'rider_id': 'nunique',
            'plate_number': 'first',
            'service': lambda x: x.mode()[0] if len(x.mode()) > 0 else None
        }).rename(columns={
            'reservation_id': 'total_rides',
            'rider_id': 'unique_riders'
        })
        
        results = {
            'top_drivers': driver_stats.nlargest(10, 'total_rides').to_dict('index'),
            'average_rides_per_driver': float(driver_stats['total_rides'].mean()),
            'driver_efficiency': self._calculate_driver_efficiency(driver_stats)
        }
        
        return results
    
    def _calculate_driver_efficiency(self, driver_stats: pd.DataFrame) -> Dict:
        """Calculate driver efficiency metrics"""
        return {
            'most_versatile_driver': driver_stats.nlargest(1, 'unique_riders').index[0],
            'most_active_driver': driver_stats.nlargest(1, 'total_rides').index[0],
            'rides_per_rider_ratio': float(
                driver_stats['total_rides'].sum() / driver_stats['unique_riders'].sum()
            )
        }
    
    def generate_insights(self) -> List[str]:
        """
        Generate human-readable insights from the analysis
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Temporal insights
        temporal = self.analyze_temporal_patterns()
        peak_hours = temporal['peak_hours']
        insights.append(f"Peak hours: {', '.join(map(str, peak_hours))}")
        
        weekend_ratio = temporal['weekend_vs_weekday']['weekend'] / (
            temporal['weekend_vs_weekday']['weekend'] + temporal['weekend_vs_weekday']['weekday']
        )
        insights.append(f"Weekend rides account for {weekend_ratio:.1%} of total rides")
        
        # Service insights
        service = self.analyze_service_patterns()
        if service:
            top_service = max(service['service_distribution'].items(), key=lambda x: x[1])
            insights.append(f"Most popular service: {top_service[0]} with {top_service[1]} rides")
        
        # Driver insights
        driver = self.analyze_driver_performance()
        insights.append(f"Average rides per driver: {driver['average_rides_per_driver']:.1f}")
        
        # Spatial insights
        spatial = self.analyze_spatial_patterns()
        insights.append(f"Service coverage area: {spatial['coverage_area']['estimated_area']:.0f} square units")
        
        return insights
