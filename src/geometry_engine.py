import os
import numpy as np
import pandas as pd

def clean_and_normalize_raw_data(file_path: str) -> pd.DataFrame:
    """Ingests raw 4412 csv logs, sanitizes whitespace, and standardizes columns."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target data missing at {file_path}.")
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower().replace(':', '_').replace(' ', '_') for c in df.columns]
    if 'x' not in df.columns and len(df.columns) >= 2:
        df = df.rename(columns={df.columns[0]: 'x', df.columns[1]: 'y'})
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    cleaned_df = df.dropna().reset_index(drop=True)
    if 'x' in cleaned_df.columns:
        cleaned_df = cleaned_df.sort_values(by='x').reset_index(drop=True)
    return cleaned_df

def generate_naca4_coordinates(m: float, p: float, t: float, chord: float = 1.0, n_points: int = 1000) -> pd.DataFrame:
    """Analytically evaluates a 4-Digit NACA envelope using thickness distributions."""
    x = np.linspace(0, chord, n_points)
    yt = 5 * t * chord * (0.2969 * np.sqrt(x/chord) - 0.1260*(x/chord) - 0.3516*(x/chord)**2 + 0.2843*(x/chord)**3 - 0.1015*(x/chord)**4)
    p_eps = max(p, 1e-5)
    yc = np.where(x <= p_eps * chord,
                 (m / (p_eps**2)) * (2 * p_eps * (x / chord) - (x / chord)**2) * chord,
                 (m / ((1 - p_eps)**2)) * ((1 - 2 * p_eps) + 2 * p_eps * (x / chord) - (x / chord)**2) * chord)
    dyc_dx = np.where(x <= p_eps * chord,
                     (2 * m / (p_eps**2)) * (p_eps - (x / chord)),
                     (2 * m / ((1 - p_eps)**2)) * (p_eps - (x / chord)))
    theta = np.arctan(dyc_dx)
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    return pd.DataFrame({'x': np.concatenate([xu[::-1], xl[1:]]), 'y': np.concatenate([yu[::-1], yl[1:]])})

def extrude_to_3d_wing(df_2d: pd.DataFrame, span: float = 2.0, n_stations: int = 20, 
                       taper_ratio: float = 0.6, max_twist_deg: float = -5.0) -> pd.DataFrame:
    """
    Extrudes 2D profiles along the Z-axis, applying linear taper scaling 
    and aerodynamic washout twist transformations.
    """
    z_stations = np.linspace(0, span, n_stations)
    x_3d, y_3d, z_3d = [], [], []
    
    # Extract raw 2D normalized coordinates
    x_raw = df_2d['x'].values
    y_raw = df_2d['y'].values
    
    for z in z_stations:
        # 1. Linear Taper Calculation (scales from 1.0 down to taper_ratio at the tip)
        fraction = z / span
        chord_scale = 1.0 - (1.0 - taper_ratio) * fraction
        
        x_scaled = x_raw * chord_scale
        y_scaled = y_raw * chord_scale
        
        # 2. Aerodynamic Twist (Rotation around leading edge [0,0])
        twist_rad = np.radians(max_twist_deg * fraction)
        cos_t, sin_t = np.cos(twist_rad), np.sin(twist_rad)
        
        # Standard 2D rotation matrix math transformation
        x_twisted = x_scaled * cos_t - y_scaled * sin_t
        y_twisted = x_scaled * sin_t + y_scaled * cos_t
        
        # Append spatial points
        x_3d.extend(x_twisted)
        y_3d.extend(y_twisted)
        z_3d.extend([z] * len(df_2d))
        
    return pd.DataFrame({'x': x_3d, 'y': y_3d, 'z': z_3d})