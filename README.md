# Parametric 4-Digit NACA Airfoil Computational Geometry & API Framework 
[![Python CI](https://github.com/lightonly1/NACA-Airfoil-Comparison/actions/workflows/main.yml/badge.svg)](https://github.com/lightonly1/NACA-Airfoil-Comparison/actions/workflows/main.yml)

A high-fidelity computational geometry pipeline and enterprise REST API engineered to parse data-driven spatial profiles, execute numerical exploratory analytics and dynamically stream parametric 3D coordinate matrices. Built using functional vector math engines and wrapped in a high-performance FastAPI microservice layer, this framework serves CAD-ready spatial points on-demand for downstream aerodynamic design and engineering simulation workflows.

---

##  Visual Engineering Analytics

### 1. High-Resolution 3D Geometric Mesh Viewport
Below is the generation output from the linear mesh projection engine, showcasing a structured 3D wing profile configured with a **0.6 taper ratio** and a **-5.0° aerodynamic washout (twist)** around the leading edge.

<p align="center">
  <img src="data/processed/wing_3d_mesh_render.png" width="85%" alt="3D Airfoil Mesh Viewport">
</p>

### 2. Data-Driven vs. Analytical Profile Verification (2D)
The framework automatically maps empirical data-driven coordinates against theoretical parametric thickness distributions to audit camber line deviations, correcting coordinate scale distortions dynamically.

<p align="center">
  <img src="data/processed/airfoil_profile_comparison.png" width="85%" alt="2D Profile Comparison">
</p>

---

##  System Architecture & Layout

```text
├── data/
│   ├── raw/                   <- Primary target datasets (e.g., 4412.csv)
│   └── processed/             <- Dynamically generated assets & visualizations
├── src/
│   ├── config.py              <- Application parameter configurations
│   ├── geometry_engine.py     <- Core procedural math and 3D extrusion pipelines
│   ├── visualization.py       <- Automation plotting engine
│   ├── view_3d_mesh.py        <- Interactive 3D point cloud GUI viewer
│   ├── app.py                 <- FastAPI microservice backend engine
│   └── run_pipeline.py        <- Core batch-processing runner engine
├── notebooks/
│   └── aerodynamic_exploration.ipynb <- Historical exploratory R&D workspace
└── tests/
    └── test_geometry.py       <- Automated mathematical boundary test maps
