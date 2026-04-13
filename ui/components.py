"""Accessible UI components with text-based fallbacks and large typography."""

import streamlit as st
from core.models import SimulationOutput
from core.constants import COLOR_GO_NOW, COLOR_WAIT

def recommendation_card(title: str, status: str, wait_time: int, detail_label: str, detail_val: str) -> None:
    """Displays an accessible recommendation card.

    ACCESSIBILITY IMPROVEMENTS:
    - Status Badge: Uses text-only indicators (e.g., 'OPTIMAL') as fallback for color.
    - Large Primary Text: Focuses attention on the most critical action.
    - Contrast: Uses high-contrast WCAG-compliant colors.
    """
    is_go = "GO" in status
    color_class = "status-go" if is_go else "status-wait"
    badge_class = "badge-go" if is_go else "badge-wait"
    badge_text = "Optimal Status" if is_go else "Sub-optimal Status"
    helper_text = "Highly recommended to act now." if is_go else "You can save time by waiting."
    
    st.markdown(f"""
        <div class="recommendation-card {color_class}">
            <div class="status-badge {badge_class}">{badge_text}</div>
            <div style="font-size: 28px; font-weight: 700; color: #111;">{title}</div>
            <div class="big-text" style="color: {COLOR_GO_NOW if is_go else COLOR_WAIT};">{status}</div>
            <div class="sub-text">Estimated Wait: <b>{wait_time} minutes</b></div>
            <div style="color: #666; font-size: 16px; margin-top: 5px;">{helper_text}</div>
            <hr style="margin: 30px 0; border: 0; border-top: 2px solid #f8f8f8;">
            <div style="display: flex; justify-content: space-between; color: #333; font-size: 18px;">
                <span>{detail_label}</span>
                <b style="font-weight: 800;">{detail_val}</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

def summary_metrics(base: SimulationOutput, optimized: SimulationOutput) -> None:
    """Displays key comparative metrics with delta indicators."""
    col1, col2, col3, col4 = st.columns(4)
    
    def get_delta(b, o, inverse=True):
        val = ((b - o) / max(b, 1.0)) * 100
        return f"{val:.1f}%" if inverse else f"{-val:.1f}%"

    col1.metric("Avg Wait", f"{optimized.avg_wait:.1f}m", 
               delta=get_delta(base.avg_wait, optimized.avg_wait), delta_color="inverse")
    
    col2.metric("Max Queue", int(optimized.max_queue), 
               delta=get_delta(base.max_queue, optimized.max_queue), delta_color="inverse")
    
    col3.metric("Peak Time", f"t={optimized.peak_congestion_time}", 
               help="Minute of highest overall system congestion.")
    
    sat_delta = optimized.satisfaction_score - base.satisfaction_score
    col4.metric("Satisfaction", f"{int(optimized.satisfaction_score)}/100", 
               delta=f"{sat_delta:+.1f} pts")

def display_textual_summary(base: SimulationOutput, optimized: SimulationOutput) -> None:
    """Provides a plain-English performance executive summary."""
    st.markdown("#### 📝 Executive Summary")
    
    wait_reduction = ((base.avg_wait - optimized.avg_wait) / max(base.avg_wait, 1)) * 100
    satisfaction_gain = optimized.satisfaction_score - base.satisfaction_score
    
    summary = (
        f"FlowSync has reduced the average waiting time by **{wait_reduction:.1f}%**. "
        f"This resulted in a user satisfaction increase of **{satisfaction_gain:.1f} points**. "
        f"The peak congestion was shifted and smoothed, moving from minute {base.peak_congestion_time} "
        f"to minute {optimized.peak_congestion_time}, effectively reducing the maximum crowd size at any single point."
    )
    
    if wait_reduction > 30:
        st.success(f"🚀 **Highly Successful Optimization:** {summary}")
    elif wait_reduction > 10:
        st.info(f"📈 **Positive Optimization:** {summary}")
    else:
        st.warning(f"⚖️ **Marginal Gains:** {summary}")
