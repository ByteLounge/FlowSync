"""FlowSync Assistant Application Entry Point.

GOOGLE SERVICES INTEGRATION (Billing-Free Spark Plan):
- Firebase Auth: Secure user session management.
- Firebase Realtime DB: Cloud storage for simulation logs.
- Maps Placeholder: Ready for Distance Matrix API integration.
- Vertex AI Placeholder: Ready for custom prediction endpoints.
"""

import streamlit as st
from core.constants import FACILITIES, DEFAULT_NUM_USERS, DEFAULT_SERVICE_RATE
from ui.styles import inject_custom_styles
from ui.views import render_user_mode, render_demo_mode
from core.firebase_manager import FirebaseManager
from utils.maps_placeholder import get_walking_time_to_facility

def main() -> None:
    """Configures and runs the Streamlit application."""
    st.set_page_config(
        page_title="FlowSync Assistant", 
        page_icon="⚡", 
        layout="centered"
    )

    inject_custom_styles()

    # --- SESSION MANAGEMENT (Firebase) ---
    if "user" not in st.session_state:
        st.session_state.user = None

    # Sidebar: Login/Signup UI
    with st.sidebar:
        st.header("👤 Account")
        if not st.session_state.user:
            auth_mode = st.radio("Access Mode", ["Anonymous", "Login", "Sign Up"])
            
            if auth_mode == "Anonymous":
                if st.button("Enter anonymously"):
                    user, error = FirebaseManager.sign_in_anonymous()
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error(f"Auth failed: {error}")
            
            elif auth_mode == "Login":
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    user, error = FirebaseManager.sign_in_email(email, password)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error(f"Login failed: {error}")
            
            elif auth_mode == "Sign Up":
                new_email = st.text_input("New Email")
                new_password = st.text_input("New Password", type="password")
                if st.button("Create Account"):
                    user, error = FirebaseManager.sign_up_email(new_email, new_password)
                    if user:
                        st.success("Account created! Logging in...")
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error(f"Signup failed: {error}")
        else:
            st.success(f"Signed in as: {st.session_state.user['localId'][:8]}...")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

    # --- MAIN UI ---
    st.title("⚡ FlowSync")
    st.markdown(
        "<p style='text-align: center; color: #777; font-size: 1.1rem;'>"
        "Powered by Predictive Intelligence</p>", 
        unsafe_allow_html=True
    )

    if not st.session_state.user:
        st.warning("Please sign in from the sidebar to access recommendations.")
        st.stop()

    selected_service = st.radio(
        label="Service Selector",
        options=FACILITIES,
        label_visibility="collapsed"
    )

    # Map Placeholder Logic
    travel_time = get_walking_time_to_facility(40.7128, -74.0060, selected_service)
    st.info(f"📍 Distance: Approximately {travel_time} min walk from your seat.")

    st.sidebar.header("🛠️ Simulation Controls")
    num_users = st.sidebar.slider("Population Count", 100, 500, DEFAULT_NUM_USERS)
    service_rate = st.sidebar.slider("Service Capacity", 0.1, 1.5, DEFAULT_SERVICE_RATE)
    
    is_demo = st.toggle("🔬 Enable Analytics Mode", value=False)

    if is_demo:
        render_demo_mode(num_users=num_users, service_rate=service_rate)
    else:
        render_user_mode(selected_service=selected_service)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("FlowSync v3.3 | Firebase Integrated | Billing-Free Version")

if __name__ == "__main__":
    main()
