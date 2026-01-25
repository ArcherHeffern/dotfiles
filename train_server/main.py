import requests
import json

# --- CONFIGURATION ---
# IMPORTANT: Replace with your actual Google Maps Platform API key
API_KEY = 'YOUR_API_KEY'

# Starting location (latitude and longitude)
# Example: Googleplex in Mountain View, CA
USER_LOCATION = {
    "latitude": 37.4223878,
    "longitude": -122.0841877
}

# Search radius in meters (max 50000)
SEARCH_RADIUS = 5000
# ---------------------

PLACES_API_URL = 'https://places.googleapis.com/v1/places:searchNearby'
ROUTES_API_URL = 'https://routes.googleapis.com/v2:computeRoutes'

def find_nearby_train_stations():
    """Calls the Places API to find nearby train stations."""
    print("Finding nearby train stations...")
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.location,places.formattedAddress'
    }
    payload = {
        "includedTypes": ["train_station"],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": USER_LOCATION['latitude'],
                    "longitude": USER_LOCATION['longitude']
                },
                "radius": SEARCH_RADIUS
            }
        }
    }
    try:
        response = requests.post(PLACES_API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json().get('places', [])
    except requests.exceptions.RequestException as e:
        print(f"Error calling Places API: {e}")
        return []

def get_route_info(destination_location):
    """Calls the Routes API to get ETA and distance."""
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
    }
    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": USER_LOCATION['latitude'],
                    "longitude": USER_LOCATION['longitude']
                }
            }
        },
        "destination": {
            "location": {
                "latLng": destination_location
            }
        },
        "travelMode": "TRANSIT"
    }
    try:
        response = requests.post(ROUTES_API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        routes = response.json().get('routes', [])
        if routes:
            # Duration is in seconds, convert to minutes
            duration_seconds = int(routes[0].get('duration', '0s').replace('s', ''))
            duration_minutes = round(duration_seconds / 60)
            return {
                "duration": f"{duration_minutes} mins",
                "distance_meters": routes[0].get('distanceMeters', 0)
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Routes API for destination {destination_location}: {e}")
        return None

def main():
    import geocoder
    g = geocoder.ip('me')
    print(g.latlng)
def m():
    """Main function to orchestrate the process."""
    if API_KEY == 'YOUR_API_KEY':
        print("Error: Please replace 'YOUR_API_KEY' with your actual Google Maps Platform API key.")
        return

    stations = find_nearby_train_stations()
    if not stations:
        print("No nearby train stations found.")
        return

    results = []
    print(f"Found {len(stations)} stations. Calculating ETA for each...")

    for station in stations:
        station_info = {
            "displayName": station.get('displayName'),
            "address": station.get('formattedAddress'),
            "location": station.get('location')
        }
        
        route_info = get_route_info(station.get('location'))
        
        if route_info:
            station_info['transitInfo'] = route_info
        else:
            station_info['transitInfo'] = 'Not available'
        
        results.append(station_info)

    # Print the final results as a JSON object
    print("\n--- RESULTS ---")
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
# Find nearby trains
# Find distance from me to trains
# Find the ETA for said trains
# Compute when I should leave for the trains

# Optional: 
# - Account for weather
# - Rank relevent trains higher

