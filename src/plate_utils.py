"""
License Plate Utilities
Improved utilities for working with license plate images
"""

from pathlib import Path
from PIL import Image
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlateImageManager:
    """Manager for license plate images"""
    
    def __init__(self, plates_dir: str = "assets/plates"):
        """
        Initialize plate image manager
        
        Args:
            plates_dir: Directory containing license plate images
        """
        self.plates_dir = Path(plates_dir)
        self.plate_images: Dict[str, Path] = {}
        self._load_plate_images()
    
    def _load_plate_images(self) -> None:
        """Load all plate images from directory"""
        if not self.plates_dir.exists():
            logger.warning(f"Plates directory not found: {self.plates_dir}")
            return
        
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        for img_path in self.plates_dir.iterdir():
            if img_path.suffix.lower() in image_extensions:
                # Extract plate number from filename (remove extension)
                plate_number = img_path.stem
                self.plate_images[plate_number] = img_path
        
        logger.info(f"Loaded {len(self.plate_images)} plate images")
    
    def get_plate_image(self, plate_number: str) -> Optional[Image.Image]:
        """
        Get PIL Image for a given plate number
        
        Args:
            plate_number: License plate number
            
        Returns:
            PIL Image or None if not found
        """
        if plate_number in self.plate_images:
            try:
                return Image.open(self.plate_images[plate_number])
            except Exception as e:
                logger.error(f"Error loading image for {plate_number}: {e}")
                return None
        return None
    
    def get_plate_info(self, plate_number: str) -> Optional[Dict]:
        """
        Get information about a plate image
        
        Args:
            plate_number: License plate number
            
        Returns:
            Dictionary with image info or None
        """
        img = self.get_plate_image(plate_number)
        if img is None:
            return None
        
        return {
            'plate_number': plate_number,
            'size': img.size,
            'mode': img.mode,
            'format': img.format,
            'file_path': str(self.plate_images[plate_number])
        }
    
    def list_all_plates(self) -> List[str]:
        """
        Get list of all available plate numbers
        
        Returns:
            List of plate numbers
        """
        return list(self.plate_images.keys())
    
    def get_plates_in_data(self, df) -> Dict[str, bool]:
        """
        Check which plates from data have images
        
        Args:
            df: DataFrame with plate_number column
            
        Returns:
            Dictionary mapping plate numbers to availability status
        """
        if 'plate_number' not in df.columns:
            return {}
        
        unique_plates = df['plate_number'].unique()
        availability = {}
        
        for plate in unique_plates:
            availability[plate] = plate in self.plate_images
        
        return availability
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about plate images
        
        Returns:
            Dictionary with statistics
        """
        if not self.plate_images:
            return {'total_plates': 0}
        
        sizes = []
        for plate_number in self.plate_images.keys():
            img = self.get_plate_image(plate_number)
            if img:
                sizes.append(img.size)
        
        if sizes:
            widths = [s[0] for s in sizes]
            heights = [s[1] for s in sizes]
            
            return {
                'total_plates': len(self.plate_images),
                'average_width': sum(widths) / len(widths),
                'average_height': sum(heights) / len(heights),
                'min_width': min(widths),
                'max_width': max(widths),
                'min_height': min(heights),
                'max_height': max(heights)
            }
        
        return {'total_plates': len(self.plate_images)}
