from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
# Import your functional math pipeline modules directly
from src.geometry_engine import generate_naca4_coordinates, extrude_to_3d_wing

app = FastAPI(
    title="Parametric 4-Digit NACA Airfoil Computational Engine API",
    description="Production-grade REST API streaming 3D spatial wing mesh coordinate matrices.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """System health check endpoint."""
    return {
        "status": "operational",
        "framework": "FastAPI",
        "engine": "NACA 4-Digit Functional Geometry Engine"
    }

@app.get("/api/generate")
def generate_airfoil_mesh(
    naca: str = Query("2412", description="4-Digit NACA string code (e.g., 2412, 4412)"),
    taper: float = Query(0.6, description="Wing tip taper ratio between 0.1 and 1.0"),
    twist: float = Query(-5.0, description="Aerodynamic washout twist in degrees (-15.0 to 15.0)")
):
    """
    Dynamically processes engineering inputs using functional math pipelines 
    and streams back a structured 3D spatial coordinate matrix array.
    """
    # 1. Input Format Validation
    if len(naca) != 4 or not naca.isdigit():
        raise HTTPException(status_code=400, detail="Invalid NACA code format. Must be exactly 4 digits.")
    
    if not (0.1 <= taper <= 1.0):
        raise HTTPException(status_code=400, detail="Taper ratio out of reliable engineering limits (0.1 to 1.0).")
        
    if not (-15.0 <= twist <= 15.0):
        raise HTTPException(status_code=400, detail="Washout twist limits exceeded (-15.0° to 15.0°).")

    try:
        print(f" API Request Received - NACA: {naca}, Taper: {taper}, Twist: {twist}°")
        
        # 2. Parse NACA characteristics from the 4-digit string
        # Digit 1: Maximum camber (m) in % of chord
        m = float(naca[0]) / 100.0
        # Digit 2: Position of maximum camber (p) in tenths of chord
        p = float(naca[1]) / 10.0
        # Digits 3-4: Maximum thickness (t) in % of chord
        t = float(naca[2:]) / 100.0
        
        # 3. Generate the analytical 2D profile coordinates
        df_2d = generate_naca4_coordinates(m=m, p=p, t=t, chord=1.0, n_points=500)
        
        # 4. Extrude the 2D profile to a structural 3D wing matrix
        df_3d = extrude_to_3d_wing(df_2d=df_2d, span=2.0, n_stations=20, taper_ratio=taper, max_twist_deg=twist)
        
        # 5. Serialize DataFrame records to dictionary layout format
        coordinates_list = df_3d.to_dict(orient="records")
        
        response_payload = {
            "metadata": {
                "naca_profile": naca,
                "parsed_parameters": {"max_camber_m": m, "camber_position_p": p, "thickness_t": t},
                "taper_ratio": taper,
                "washout_twist_deg": twist,
                "total_nodes_generated": len(coordinates_list)
            },
            "coordinates": coordinates_list
        }
        
        return JSONResponse(content=response_payload, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Core execution engine mathematical fault: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Launch server locally on port 8000
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)