"""FlowSync Assistant Application Entry Point.

INTEGRATION POINTS:
- Firebase: Simulates 'Live Sync' for real-time crowd data.
- Google Maps: Displays 'Travel Time' to the selected facility.
- Vertex AI: Powers the simulation engine's prediction thresholds.
"""

import streamlit as st
import random
from core.constants import FACILITIES, DEFAULT_NUM_USERS, DEFAULT_SERVICE_RATE
from ui.styles import inject_custom_styles
from ui.views import render_user_mode, render_demo_mode

# [MOCK INTEGRATIONS]
from core.firebase_mock import sync_live_crowd_data
from utils.maps_placeholder import get_walking_time_to_facility

def main() -> None:
    """Configures and runs the Streamlit application."""
    st.set_page_config(
        page_title="FlowSync Assistant", 
        page_icon="⚡", 
        layout="centered"
    )

    inject_custom_styles()

    st.title("⚡ FlowSync")
    st.markdown(
        "<p style='text-align: center; color: #777; font-size: 1.1rem;'>"
        "Powered by Predictive Intelligence</p>", 
        unsafe_allow_html=True
    )

    # Simulation of Firebase 'Live Connection'
    live_status = sync_live_crowd_data("stadium_01")
    st.sidebar.caption(f"📡 Real-time Sync: {live_status['last_updated']} | Users: {live_status['current_users']}")

    selected_service = st.radio(
        label="Service Selector",
        options=FACILITIES,
        label_visibility="collapsed"
    )

    # Google Maps Integration: Personalizing the recommendation
    # In a real app, these coords would come from the browser's geolocation
    travel_time = get_walking_time_to_facility(40.7128, -74.0060, selected_service)
    st.info(f"📍 Distance: {travel_time} min walk from your seat.")

    st.sidebar.header("🛠️ Simulation Controls")
    num_users = st.sidebar.slider("Population Count", 100, 500, DEFAULT_NUM_USERS)
    service_rate = st.sidebar.slider("Service Capacity", 0.1, 1.5, DEFAULT_SERVICE_RATE)
    
    is_demo = st.toggle("🔬 Enable Analytics Mode", value=False)

    if is_demo:
        render_demo_mode(num_users=num_users, service_rate=service_rate)
    else:
        render_user_mode(selected_service=selected_service)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("FlowSync v3.2 | Google Services Ready | Modular Architecture")

if __name__ == "__main__":
    main()
