# Geodesy & Distance Engine Skill

Exact ellipsoidal and spherical great-circle geodesic solvers adhering strictly to WGS-84 ellipsoid parameters.

```mermaid
flowchart LR
    Coords["Coordinates (lat1, lon1) & (lat2, lon2)"] --> Hav["Haversine Formula (Spherical Earth)"]
    Coords --> Vinc["Vincenty Inverse Iteration (WGS-84 Ellipsoid)"]
    Hav --> Res1["Distance d (Spherical)"]
    Vinc --> Res2["Millimeter-Accurate Geodesic s"]
```

## Features
- **100% Python Standard Library**: WGS-84 constants.
- **Millimeter Precision**: Vincenty inverse iterative solver down to \(10^{-12}\) convergence.
