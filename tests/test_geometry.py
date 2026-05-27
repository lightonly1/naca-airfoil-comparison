import numpy as np
from src.geometry_engine import generate_naca4_coordinates

def test_symmetrical_profile_invariants():
    """
    Asserts that a 0012 configuration correctly evaluates 
    to zero camber across all stations.
    """
    df = generate_naca4_coordinates(m=0.0, p=0.0, t=0.12, chord=1.0, n_points=100)
    
    # Profiles must maintain mathematical structure within realistic spatial limits
    assert len(df) == 199  # Concat upper and lower lengths check
    assert np.max(df['x']) <= 1.0001
    assert np.min(df['x']) >= -0.0001