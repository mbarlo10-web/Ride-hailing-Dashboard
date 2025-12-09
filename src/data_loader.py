"""
Data Loading and Processing Module
Improved version for ride-hailing data analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RideHailingDataLoader:
    """Enhanced data loader for ride-hailing datasets"""
    
    def __init__(self, data_path: str = "assets/ride_hailing.xlsx"):
        """
        Initialize the data loader
        
        Args:
            data_path: Path to the Excel file containing ride-hailing data
        """
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        self.processed_df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from Excel file
        
        Returns:
            DataFrame with ride-hailing data
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_excel(self.data_path)
            logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data
        
        Returns:
            Cleaned DataFrame
        """
        if self.df is None:
            self.load_data()
        
        logger.info("Cleaning data...")
        df = self.df.copy()
        
        # Convert time column to datetime if not already
        if 'current_time' in df.columns:
            df['current_time'] = pd.to_datetime(df['current_time'])
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate records")
        
        # Handle missing values
        missing_before = df.isnull().sum().sum()
        df = df.dropna(subset=['current_time', 'slot_id', 'x', 'y'])
        logger.info(f"Removed {missing_before - df.isnull().sum().sum()} records with missing critical data")
        
        # Add derived features
        df = self._add_derived_features(df)
        
        self.processed_df = df
        logger.info(f"Data cleaning complete. Final dataset: {len(df)} records")
        return df
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived features for analysis
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional features
        """
        df = df.copy()
        
        # Extract time features
        if 'current_time' in df.columns:
            df['hour'] = df['current_time'].dt.hour
            df['day_of_week'] = df['current_time'].dt.dayofweek
            df['date'] = df['current_time'].dt.date
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Calculate distance from origin (0, 0) if needed
        if 'x' in df.columns and 'y' in df.columns:
            df['distance_from_origin'] = np.sqrt(df['x']**2 + df['y']**2)
        
        # Add service type encoding if needed
        if 'service' in df.columns:
            df['service_encoded'] = pd.Categorical(df['service']).codes
        
        return df
    
    def get_summary_stats(self) -> Dict:
        """
        Get summary statistics for the dataset
        
        Returns:
            Dictionary with summary statistics
        """
        if self.processed_df is None:
            self.clean_data()
        
        df = self.processed_df
        
        stats = {
            'total_records': len(df),
            'unique_drivers': df['driver_id'].nunique() if 'driver_id' in df.columns else 0,
            'unique_riders': df['rider_id'].nunique() if 'rider_id' in df.columns else 0,
            'unique_plates': df['plate_number'].nunique() if 'plate_number' in df.columns else 0,
            'date_range': {
                'start': str(df['current_time'].min()) if 'current_time' in df.columns else None,
                'end': str(df['current_time'].max()) if 'current_time' in df.columns else None
            },
            'services': df['service'].value_counts().to_dict() if 'service' in df.columns else {},
            'spatial_range': {
                'x_min': float(df['x'].min()) if 'x' in df.columns else None,
                'x_max': float(df['x'].max()) if 'x' in df.columns else None,
                'y_min': float(df['y'].min()) if 'y' in df.columns else None,
                'y_max': float(df['y'].max()) if 'y' in df.columns else None
            }
        }
        
        return stats
    
    def get_dataframe(self, processed: bool = True) -> pd.DataFrame:
        """
        Get the DataFrame (raw or processed)
        
        Args:
            processed: If True, return processed data; otherwise raw
            
        Returns:
            DataFrame
        """
        if processed:
            if self.processed_df is None:
                self.clean_data()
            return self.processed_df
        else:
            if self.df is None:
                self.load_data()
            return self.df
