import os

class AirfoilConfig:
    def __init__(self):
        # Base directory paths
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.RAW_DATA_DIR = os.path.join(self.BASE_DIR, "data", "raw")
        self.PROCESSED_DATA_DIR = os.path.join(self.BASE_DIR, "data", "processed")
        
        # Ensure directories exist right away
        os.makedirs(self.RAW_DATA_DIR, exist_ok=True)
        os.makedirs(self.PROCESSED_DATA_DIR, exist_ok=True)
        
        # Target file destination assets
        self.COMPARISON_PLOT = os.path.join(self.PROCESSED_DATA_DIR, "airfoil_profile_comparison.png")
        self.NACA_2412_3D = os.path.join(self.PROCESSED_DATA_DIR, "naca2412_3d_formula.csv")
        self.NACA_4412_3D = os.path.join(self.PROCESSED_DATA_DIR, "naca4412_3d_data.csv")

# Instantiate a single configuration context instance
config = AirfoilConfig()