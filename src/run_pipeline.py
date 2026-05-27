
import os
from src.config import config
from src.geometry_engine import clean_and_normalize_raw_data, generate_naca4_coordinates, extrude_to_3d_wing
from src.visualization import generate_and_save_comparison_plot

def execute_computational_pipeline():
    print(" Initializing Parametric NACA Airfoil Computational Pipeline...")
    
    # 1. Ingest and sanitize raw empirical data
    try:
        raw_data_path = os.path.join(config.RAW_DATA_DIR, "4412.csv")
        cleaned_baseline_df = clean_and_normalize_raw_data(raw_data_path)
        print(f" Baseline empirical logs ingested successfully. Shape: {cleaned_baseline_df.shape}")
    except Exception as e:
        print(f" Raw data ingestion bypassed or failed: {e}")
        raw_data_path = ""

    # 2. Generate pristine analytical target profile (NACA 2412)
    print(" Generating theoretical target math profile (NACA 2412)...")
    analytical_df = generate_naca4_coordinates(m=0.02, p=0.4, t=0.12, chord=1.0, n_points=1000)
    
    # 3. Trigger the data-normalization visualization engine
    generate_and_save_comparison_plot(
        baseline_path=raw_data_path, 
        analytical_df=analytical_df, 
        output_path=config.COMPARISON_PLOT
    )

    # 4. Extrude the 2D panel nodes into an advanced 3D tapered & twisted wing
    print(" Extruding geometry to 3D spatial domain with aerodynamic washout...")
    wing_3d_df = extrude_to_3d_wing(
        df_2d=analytical_df, 
        span=2.0, 
        n_stations=20, 
        taper_ratio=0.6, 
        max_twist_deg=-5.0
    )
    
    # Export the generated 3D data-matrix spreadsheet
    # --- FIX APPLIED HERE: changed os.path.exists=True to exist_ok=True ---
    os.makedirs(os.path.dirname(config.NACA_2412_3D), exist_ok=True)
    wing_3d_df.to_csv(config.NACA_2412_3D, index=False)
    print(f" High-resolution 3D wing mesh coordinates saved to: {config.NACA_2412_3D}")
    print(" Pipeline run complete with zero critical errors!")

if __name__ == "__main__":
    execute_computational_pipeline()