# src/geometry_engine.py
import os
import numpy as np
import pandas as pd

def clean_and_normalize_raw_data(file_path: str) -> pd.DataFrame:
    """
    Ingests raw 4412 csv logs, sanitizes whitespace, maps trailing 
    delimiters, and forces high-precision numeric compliance.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target data missing at {file_path}. Place your 4412.csv there.")
        
    df = pd.read_csv(file_path)
    
    # Clean headers: remove spaces, lowercase everything, strip delimiters
    df.columns = [c.strip().lower().replace(':', '_').replace(' ', '_') for c in df.columns]
    
    # If the file uses capital labels like 'X' or 'Y', the line above forced them to 'x' and 'y'
    # Let's verify standard column references exist
    if 'x' not in df.columns and len(df.columns) >= 2:
        # Fallback: rename the first two columns to x and y explicitly if not matching
        df = df.rename(columns={df.columns[0]: 'x', df.columns[1]: 'y'})
    
    # Coerce columns to continuous floats
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    cleaned_df = df.dropna().reset_index(drop=True)
    
    # Sort coordinate points sequentially by X station to isolate upper/lower curves safely
    if 'x' in cleaned_df.columns:
        cleaned_df = cleaned_df.sort_values(by='x').reset_index(drop=True)
        
    return cleaned_df

def generate_naca4_coordinates(m: float, p: float, t: float, chord: float = 1.0, n_points: int = 1000) -> pd.DataFrame:
    """
    Analytically evaluates a 4-Digit NACA envelope using thickness distributions 
    and mean camber line piecewise derivatives.
    """
    x = np.linspace(0, chord, n_points)
    
    # Standard 4-digit thickness profile
    yt = 5 * t * chord * (0.2969 * np.sqrt(x/chord) - 0.1260*(x/chord) - 0.3516*(x/chord)**2 + 0.2843*(x/chord)**3 - 0.1015*(x/chord)**4)
    
    # Guard against division by zero at boundary points
    p_eps = max(p, 1e-5)
    
    # Vectorized piecewise camber line tracking
    yc = np.where(x <= p_eps * chord,
                 (m / (p_eps**2)) * (2 * p_eps * (x / chord) - (x / chord)**2) * chord,
                 (m / ((1 - p_eps)**2)) * ((1 - 2 * p_eps) + 2 * p_eps * (x / chord) - (x / chord)**2) * chord)
    
    # Spatial gradient derivations
    dyc_dx = np.where(x <= p_eps * chord,
                     (2 * m / (p_eps**2)) * (p_eps - (x / chord)),
                     (2 * m / ((1 - p_eps)**2)) * (p_eps - (x / chord)))
    
    theta = np.arctan(dyc_dx)
    
    # Map upper and lower geometric panels
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    # Consolidate trailing edge to leading edge to trailing edge coordinates
    x_coords = np.concatenate([xu[::-1], xl[1:]])
    y_coords = np.concatenate([yu[::-1], yl[1:]])
    
    return pd.DataFrame({'x': x_coords, 'y': y_coords})

def extrude_to_3d_wing(df_2d: pd.DataFrame, span: float = 2.0, n_stations: int = 20) -> pd.DataFrame:
    """
    Extrudes 2D profiles along the orthogonal Z-axis to build structured 3D CAD meshes.
    """
    z_stations = np.linspace(0, span, n_stations)
    x_3d, y_3d, z_3d = [], [], []
    
    for z in z_stations:
        x_3d.extend(df_2d['x'].values)
        y_3d.extend(df_2d['y'].values)
        z_3d.extend([z] * len(df_2d))
        
    return pd.DataFrame({'x': x_3d, 'y': y_3d, 'z': z_3d})