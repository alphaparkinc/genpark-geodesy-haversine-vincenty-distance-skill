"""Example evaluating geodesic distance."""
from client import GeodesyEngine

def main():
    # NY to London
    lat1, lon1 = 40.7128, -74.0060
    lat2, lon2 = 51.5074, -0.1278
    d_hav = GeodesyEngine.haversine_distance(lat1, lon1, lat2, lon2)
    d_vinc = GeodesyEngine.vincenty_distance(lat1, lon1, lat2, lon2)
    print(f"Haversine Spherical: {d_hav / 1000:.2f} km")
    print(f"Vincenty Ellipsoidal: {d_vinc / 1000:.2f} km")

if __name__ == "__main__":
    main()
