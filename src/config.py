import os

class AirfoilConfig:
    # Source Ingestion File
    RAW_DATA_PATH = os.path.join("data", "raw", "4412.csv")
    PROCESSED_DIR = os.path.join("data", "processed")
    
    # 2D Target Artifact Paths
    NACA_4412_2D = os.path.join(PROCESSED_DIR, "naca4412_cleaned_coordinates.csv")
    NACA_2412_2D = os.path.join(PROCESSED_DIR, "naca2412_formula_coordinates.csv")
    
    # 3D Extrusion Target Artifact Paths
    NACA_4412_3D = os.path.join(PROCESSED_DIR, "naca4412_3d_from_dataset.csv")
    NACA_2412_3D = os.path.join(PROCESSED_DIR, "naca2412_3d_formula.csv")
    
    # Static Computational Hyperparameters
    N_POINTS = 1000
    CHORD = 1.0
    SPAN = 2.0
    N_SPAN_STATIONS = 20

config = AirfoilConfig()