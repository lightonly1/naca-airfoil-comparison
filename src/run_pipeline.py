import os
from src.config import config
from src.geometry_engine import (
    clean_and_normalize_raw_data,
    generate_naca4_coordinates,
    extrude_to_3d_wing
)
from src.visualization import generate_aerodynamic_plots

def run():
    print(" Initializing Physics-Informed Aerodynamic Processing Pipeline...")
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    
    # Step 1: Clean raw measurements
    print(f" Parsing data-driven target dataset from: {config.RAW_DATA_PATH}")
    df_4412_clean = clean_and_normalize_raw_data(config.RAW_DATA_PATH)
    df_4412_clean.to_csv(config.NACA_4412_2D, index=False)
    
    # Step 2: Evaluate high-fidelity formula reference maps
    print(" Running 4-digit camber distribution algorithms for NACA 2412...")
    df_2412_analytical = generate_naca4_coordinates(m=0.02, p=0.4, t=0.12, chord=config.CHORD, n_points=config.N_POINTS)
    df_2412_analytical.to_csv(config.NACA_2412_2D, index=False)
    
    # Step 3: Perform multi-station 3D space wing extrusions
    print(" Projecting 2D coordinate paths into 3D Wing Space Point Clouds...")
    df_4412_3d = extrude_to_3d_wing(df_4412_clean, span=config.SPAN, n_stations=config.N_SPAN_STATIONS)
    df_2412_3d = extrude_to_3d_wing(df_2412_analytical, span=config.SPAN, n_stations=config.N_SPAN_STATIONS)
    
    df_4412_3d.to_csv(config.NACA_4412_3D, index=False)
    df_2412_3d.to_csv(config.NACA_2412_3D, index=False)
    
    # Step 4: Run visual diagnostic reports
    generate_aerodynamic_plots(df_4412_clean, df_2412_analytical, config.PROCESSED_DIR)
    
    print("\n" + "="*50)
    print(" PIPELINE EXECUTION SUCCESSFUL")
    print(f" Total Data-Driven 3D Nodes: {len(df_4412_3d)}")
    print(f" Total Analytical 3D Nodes: {len(df_2412_3d)}")
    print("="*50)

if __name__ == "__main__":
    run()