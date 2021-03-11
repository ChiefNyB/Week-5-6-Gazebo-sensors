#!/usr/bin/env python

import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance
    R = 6371.0088 # Radius of earth in km
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c * 1000 # in meters

    # Calculate heading
    y = math.sin(dLon) * math.cos(dLon)
    x = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos(dLon)
    bearing = -math.atan2(y,x)

    return d, bearing

# (lat, lon)
lyon = (45.7597, 4.8422) 
paris = (48.8567, 2.3508)
new_york = (40.7033962, -74.2351462)
london = (51.509865, -0.118092)

print(haversine(lyon[0],lyon[1],paris[0],paris[1]))
print(haversine(lyon[0],lyon[1],new_york[0],new_york[1]))