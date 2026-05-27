import os
import pandas as pd
import numpy as np
import open3d as o3d
from src.config import config

def launch_point_cloud_gui(file_path: str, window_title: str):
    print(f" Ingesting 3D geometry matrix from: {file_path}")
    if not os.path.exists(file_path):
        print(f" Error: Target file missing at {file_path}. Run the pipeline first!")
        return
        
    # Read the data coordinates from your spreadsheet
    df = pd.read_csv(file_path)
    xyz = df[['x', 'y', 'z']].values
    
    # Initialize Open3D structural PointCloud matrices
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    
    # Estimate surface normals so it reacts realistically to digital lighting structures
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Color the point cloud dynamically based on thickness positions (Y-Axis distribution tracking)
    y_coords = xyz[:, 1]
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    normalized_y = (y_coords - y_min) / (y_max - y_min if (y_max - y_min) > 0 else 1.0)
    
    # Map a smooth programmatic blue-to-red aerodynamic gradient spectrum
    colors = np.zeros((len(xyz), 3))
    colors[:, 0] = normalized_y        # Red channel (camber/thickness peaks)
    colors[:, 2] = 1.0 - normalized_y  # Blue channel (chord line baselines)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # Fire up the interactive graphics rendering UI window loop
    print(" Launching interactive 3D UI viewport. Use your mouse left-click to rotate, right-click to pan.")
    o3d.visualization.draw_geometries([pcd], window_name=window_title, width=1280, height=720, left=50, top=50)

if __name__ == "__main__":
    # Select which 3D model cloud profile you want to inspect inside the viewport
    # Toggle between config.NACA_2412_3D or config.NACA_4412_3D
    target_mesh = config.NACA_2412_3D  
    launch_point_cloud_gui(target_mesh, "NACA Airfoil Physics Surrogate - High-Resolution 3D Render Viewport")