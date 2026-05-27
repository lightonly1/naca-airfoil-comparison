import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_aerodynamic_plots(df_4412: pd.DataFrame, df_2412: pd.DataFrame, output_dir: str):
    """
    Generates and saves high-resolution overlay comparisons to showcase your work visually.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    # 2D Profile Comparison Overlay Plot
    plt.figure(figsize=(12, 5))
    plt.plot(df_4412['x'], df_4412['y'], 'b-', linewidth=2.5, label='NACA 4412 (Dataset Baseline)')
    plt.plot(df_2412['x'], df_2412['y'], 'r--', linewidth=2, label='NACA 2412 (Analytical Target)')
    plt.title('Aerodynamic Geometric Comparison: NACA 4412 vs NACA 2412', fontsize=14, fontweight='bold')
    plt.xlabel('Chord Station (x/c)', fontsize=12)
    plt.ylabel('Profile Thickness (y/c)', fontsize=12)
    plt.axis('equal')
    plt.legend(loc='upper right')
    
    plot_path = os.path.join(output_dir, "airfoil_profile_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f" High-resolution visual analysis written to: {plot_path}")