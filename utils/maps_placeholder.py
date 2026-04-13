"""Google Maps Platform Placeholder (Billing-Free).

PRODUCTION USAGE:
- In production, replace these functions with 'googlemaps' SDK calls.
- Requires: API Key with 'Distance Matrix' and 'Places' APIs enabled.
- Billing: This is a paid service (Google Maps Platform).
"""

def get_walking_time_to_facility(user_lat: float, user_lng: float, facility_name: str) -> int:
    """Placeholder for Google Maps Distance Matrix API.
    
    In production, this would return real-time walking durations based 
    on the current stadium layout and crowd flow.
    """
    # Returns a logical constant for prototype demonstration
    return 5 

def get_nearby_facilities(lat: float, lng: float) -> list:
    """Placeholder for Google Maps Places API."""
    return ["Food Stall North", "Restroom Section 102", "Exit Gate 4"]
