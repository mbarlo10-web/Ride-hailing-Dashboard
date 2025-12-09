"""
Data Visualization Module
Improved visualization capabilities for ride-hailing data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class RideHailingVisualizer:
    """Enhanced visualizer for ride-hailing data"""
    
    def __init__(self, analyzer, output_dir: str = "data/output"):
        """
        Initialize visualizer
        
        Args:
            analyzer: RideHailingAnalyzer instance
            output_dir: Directory to save visualizations
        """
        self.analyzer = analyzer
        self.df = analyzer.df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_temporal_analysis(self, save: bool = True) -> None:
        """Create temporal analysis visualizations"""
        logger.info("Creating temporal analysis plots...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Temporal Analysis of Ride-Hailing Data', fontsize=16, fontweight='bold')
        
        # Hourly distribution
        hourly = self.df.groupby('hour').size()
        axes[0, 0].plot(hourly.index, hourly.values, marker='o', linewidth=2, markersize=8)
        axes[0, 0].set_title('Ride Distribution by Hour', fontweight='bold')
        axes[0, 0].set_xlabel('Hour of Day')
        axes[0, 0].set_ylabel('Number of Rides')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Day of week distribution
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_counts = self.df.groupby('day_of_week').size()
        axes[0, 1].bar(day_names, [day_counts.get(i, 0) for i in range(7)], color='steelblue')
        axes[0, 1].set_title('Ride Distribution by Day of Week', fontweight='bold')
        axes[0, 1].set_xlabel('Day of Week')
        axes[0, 1].set_ylabel('Number of Rides')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Weekend vs Weekday
        weekend_counts = self.df.groupby('is_weekend').size()
        # Ensure we have both weekday and weekend values
        weekday_count = weekend_counts.get(0, 0)
        weekend_count = weekend_counts.get(1, 0)
        values = [weekday_count, weekend_count]
        labels = ['Weekday', 'Weekend']
        # Only show pie chart if we have data
        if sum(values) > 0:
            axes[1, 0].pie(values, labels=labels, 
                          autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
        else:
            axes[1, 0].text(0.5, 0.5, 'No data available', 
                          ha='center', va='center', transform=axes[1, 0].transAxes)
        axes[1, 0].set_title('Weekend vs Weekday Distribution', fontweight='bold')
        
        # Daily trends
        daily = self.df.groupby('date').size()
        axes[1, 1].plot(daily.index, daily.values, marker='o', linewidth=2, markersize=4)
        axes[1, 1].set_title('Daily Ride Trends', fontweight='bold')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Number of Rides')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / 'temporal_analysis.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved temporal analysis to {output_path}")
        
        plt.show()
    
    def plot_spatial_analysis(self, save: bool = True) -> None:
        """Create spatial analysis visualizations"""
        logger.info("Creating spatial analysis plots...")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Spatial Analysis of Ride-Hailing Data', fontsize=16, fontweight='bold')
        
        # Scatter plot of ride locations
        scatter = axes[0].scatter(self.df['x'], self.df['y'], 
                                 c=self.df['hour'], cmap='viridis', 
                                 alpha=0.5, s=20)
        axes[0].set_title('Ride Locations (colored by hour)', fontweight='bold')
        axes[0].set_xlabel('X Coordinate')
        axes[0].set_ylabel('Y Coordinate')
        axes[0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[0], label='Hour of Day')
        
        # Heatmap of ride density
        # Create 2D histogram
        heatmap, xedges, yedges = np.histogram2d(
            self.df['x'], self.df['y'], bins=20
        )
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        im = axes[1].imshow(heatmap.T, origin='lower', extent=extent, 
                           cmap='YlOrRd', aspect='auto')
        axes[1].set_title('Ride Density Heatmap', fontweight='bold')
        axes[1].set_xlabel('X Coordinate')
        axes[1].set_ylabel('Y Coordinate')
        plt.colorbar(im, ax=axes[1], label='Ride Count')
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / 'spatial_analysis.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved spatial analysis to {output_path}")
        
        plt.show()
    
    def plot_service_analysis(self, save: bool = True) -> None:
        """Create service analysis visualizations"""
        logger.info("Creating service analysis plots...")
        
        if 'service' not in self.df.columns:
            logger.warning("Service column not found, skipping service analysis")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Service Analysis', fontsize=16, fontweight='bold')
        
        # Service distribution
        service_counts = self.df['service'].value_counts()
        axes[0, 0].bar(service_counts.index, service_counts.values, color='steelblue')
        axes[0, 0].set_title('Ride Distribution by Service', fontweight='bold')
        axes[0, 0].set_xlabel('Service')
        axes[0, 0].set_ylabel('Number of Rides')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Service by hour
        service_hour = self.df.groupby(['service', 'hour']).size().unstack(fill_value=0)
        for service in service_hour.index:
            axes[0, 1].plot(service_hour.columns, service_hour.loc[service], 
                           marker='o', label=service, linewidth=2)
        axes[0, 1].set_title('Service Usage by Hour', fontweight='bold')
        axes[0, 1].set_xlabel('Hour of Day')
        axes[0, 1].set_ylabel('Number of Rides')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Service by day of week
        service_day = self.df.groupby(['service', 'day_of_week']).size().unstack(fill_value=0)
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        x = np.arange(len(service_day.columns))
        width = 0.35
        for i, service in enumerate(service_day.index):
            offset = (i - len(service_day.index)/2 + 0.5) * width / len(service_day.index)
            axes[1, 0].bar(x + offset, service_day.loc[service], width/len(service_day.index), 
                          label=service)
        axes[1, 0].set_title('Service Usage by Day of Week', fontweight='bold')
        axes[1, 0].set_xlabel('Day of Week')
        axes[1, 0].set_xticks(x)
        # Use actual day names for the days present in data
        actual_day_labels = [day_names[int(col)] if int(col) < len(day_names) else str(int(col)) 
                            for col in service_day.columns]
        axes[1, 0].set_xticklabels(actual_day_labels)
        axes[1, 0].set_ylabel('Number of Rides')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Service pie chart
        axes[1, 1].pie(service_counts.values, labels=service_counts.index, 
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Service Distribution', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / 'service_analysis.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved service analysis to {output_path}")
        
        plt.show()
    
    def plot_driver_performance(self, save: bool = True, top_n: int = 10) -> None:
        """Create driver performance visualizations"""
        logger.info("Creating driver performance plots...")
        
        driver_stats = self.df.groupby('driver_id').agg({
            'reservation_id': 'count',
            'rider_id': 'nunique'
        }).rename(columns={
            'reservation_id': 'total_rides',
            'rider_id': 'unique_riders'
        })
        
        top_drivers = driver_stats.nlargest(top_n, 'total_rides')
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'Top {top_n} Driver Performance', fontsize=16, fontweight='bold')
        
        # Total rides
        axes[0].barh(range(len(top_drivers)), top_drivers['total_rides'], color='steelblue')
        axes[0].set_yticks(range(len(top_drivers)))
        axes[0].set_yticklabels(top_drivers.index)
        axes[0].set_title('Total Rides by Driver', fontweight='bold')
        axes[0].set_xlabel('Number of Rides')
        axes[0].grid(True, alpha=0.3, axis='x')
        
        # Unique riders
        axes[1].barh(range(len(top_drivers)), top_drivers['unique_riders'], color='coral')
        axes[1].set_yticks(range(len(top_drivers)))
        axes[1].set_yticklabels(top_drivers.index)
        axes[1].set_title('Unique Riders Served', fontweight='bold')
        axes[1].set_xlabel('Number of Unique Riders')
        axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save:
            output_path = self.output_dir / 'driver_performance.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved driver performance to {output_path}")
        
        plt.show()
    
    def create_comprehensive_report(self) -> None:
        """Create all visualizations and save as comprehensive report"""
        logger.info("Creating comprehensive visualization report...")
        
        self.plot_temporal_analysis(save=True)
        self.plot_spatial_analysis(save=True)
        self.plot_service_analysis(save=True)
        self.plot_driver_performance(save=True)
        
        logger.info(f"All visualizations saved to {self.output_dir}")
