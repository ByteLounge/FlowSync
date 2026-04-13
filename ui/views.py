"""High-level UI views with security-focused error handling."""

import streamlit as st
import numpy as np
from ui.components import recommendation_card, summary_metrics, display_textual_summary
from core.engine import CrowdSimulationEngine
from utils.plotting import create_performance_charts
from core.constants import FOOD, RESTROOM, EXIT

def render_user_mode(selected_service: str) -> None:
    """Renders the user interface with error safeguards."""
    try:
        st.markdown("---")
        
        # MOCK INTEGRATION: In production, we query Firebase for live wait times
        # and Vertex AI for predictive thresholds.
        # Here we mock the live state based on the selected facility.
        engine_mock = CrowdSimulationEngine(num_users=200)
        
        if FOOD in selected_service:
            wait = np.random.randint(2, 12)
            recommendation_card(FOOD, "GO NOW" if wait < 5 else "WAIT 10 mins", wait, "Queue Flow", "Steady")
        elif RESTROOM in selected_service:
            wait = np.random.randint(1, 8)
            recommendation_card(RESTROOM, "GO NOW" if wait < 3 else "WAIT 5 mins", wait, "Availability", "High")
        elif EXIT in selected_service:
            wait = np.random.randint(5, 20)
            recommendation_card(EXIT, "GO NOW" if wait < 8 else "WAIT 15 mins", wait, "Road Traffic", "Medium")
        else:
            st.warning("⚠️ Unknown service selected. Please use the selector above.")
    except Exception as e:
        st.error(f"❌ An error occurred while loading the recommendation: {str(e)}")

def render_demo_mode(num_users: int, service_rate: float) -> None:
    """Renders analytics mode with comprehensive error handling."""
    st.divider()
    st.write("### 📊 Performance Analysis")
    
    try:
        # Input validation occurs within the engine's constructor
        engine = CrowdSimulationEngine(num_users=num_users, service_rate=service_rate)
        
        with st.spinner("Analyzing crowd dynamics..."):
            base_res = engine.run_baseline()
            opt_res = engine.run_optimized()

        summary_metrics(base_res, opt_res)
        display_textual_summary(base_res, opt_res)
        
        # Visualization Section
        try:
            fig_line, fig_bar = create_performance_charts(base_res, opt_res)
            
            st.markdown("#### 📈 Efficiency Trends")
            st.pyplot(fig_line)
            
            st.markdown("#### 🏆 Performance Comparison")
            st.pyplot(fig_bar)
            
        except Exception as plot_error:
            st.error(f"⚠️ Visualization error: {str(plot_error)}")

        # Data Display
        st.markdown("#### Quantitative Comparison")
        comparison_data = {
            "Scenario": ["Baseline (Random)", "FlowSync (Predictive)"],
            "Avg Wait Time": [f"{base_res.avg_wait:.2f} min", f"{opt_res.avg_wait:.2f} min"],
            "Max Queue Size": [int(base_res.max_queue), int(opt_res.max_queue)],
            "Peak Status": ["High Congestion", "Optimized Flow"]
        }
        st.table(comparison_data)

    except RuntimeError as re:
        st.error(f"🔄 Simulation Error: {str(re)}")
    except Exception as e:
        st.error(f"🚨 A critical error occurred: {str(e)}")
