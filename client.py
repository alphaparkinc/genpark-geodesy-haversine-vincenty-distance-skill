"""Geodesic Distance Engine: Haversine & Vincenty Inverse.
100% Python Standard Library.
"""

import math

class GeodesyEngine:
    WGS84_A = 6378137.0
    WGS84_F = 1.0 / 298.257223563
    WGS84_B = 6356752.314245

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2, radius=6371000.0):
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        
        a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(radius * c, 2)

    @staticmethod
    def vincenty_distance(lat1, lon1, lat2, lon2, max_iter=100, tol=1e-12):
        a = GeodesyEngine.WGS84_A
        b = GeodesyEngine.WGS84_B
        f = GeodesyEngine.WGS84_F
        
        L = math.radians(lon2 - lon1)
        U1 = math.atan((1.0 - f) * math.tan(math.radians(lat1)))
        U2 = math.atan((1.0 - f) * math.tan(math.radians(lat2)))
        sinU1, cosU1 = math.sin(U1), math.cos(U1)
        sinU2, cosU2 = math.sin(U2), math.cos(U2)
        
        lam = L
        for _ in range(max_iter):
            sin_lam = math.sin(lam)
            cos_lam = math.cos(lam)
            sin_sigma = math.sqrt((cosU2 * sin_lam)**2 + (cosU1 * sinU2 - sinU1 * cosU2 * cos_lam)**2)
            if sin_sigma == 0:
                return 0.0
            cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lam
            sigma = math.atan2(sin_sigma, cos_sigma)
            sin_alpha = (cosU1 * cosU2 * sin_lam) / sin_sigma
            cos2_alpha = 1.0 - sin_alpha**2
            cos_2sigma_m = cos_sigma - (2.0 * sinU1 * sinU2) / cos2_alpha if cos2_alpha != 0 else 0.0
            
            C = (f / 16.0) * cos2_alpha * (4.0 + f * (4.0 - 3.0 * cos2_alpha))
            lam_prev = lam
            lam = L + (1.0 - C) * f * sin_alpha * (
                sigma + C * sin_sigma * (cos_2sigma_m + C * cos_sigma * (-1.0 + 2.0 * cos_2sigma_m**2))
            )
            if abs(lam - lam_prev) < tol:
                break
                
        u_sq = cos2_alpha * (a**2 - b**2) / (b**2)
        A_val = 1.0 + (u_sq / 16384.0) * (4096.0 + u_sq * (-768.0 + u_sq * (320.0 - 175.0 * u_sq)))
        B_val = (u_sq / 1024.0) * (256.0 + u_sq * (-128.0 + u_sq * (74.0 - 47.0 * u_sq)))
        delta_sigma = B_val * sin_sigma * (
            cos_2sigma_m + 0.25 * B_val * (
                cos_sigma * (-1.0 + 2.0 * cos_2sigma_m**2) - (B_val / 6.0) * cos_2sigma_m * (-3.0 + 4.0 * sin_sigma**2) * (-3.0 + 4.0 * cos_2sigma_m**2)
            )
        )
        s = b * A_val * (sigma - delta_sigma)
        return round(s, 2)
