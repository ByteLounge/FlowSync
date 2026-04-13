"""UI styles with accessibility-focused typography and colors."""

import streamlit as st
from core.constants import COLOR_GO_NOW, COLOR_WAIT

def inject_custom_styles() -> None:
    """Injects high-contrast CSS and large-text styling."""
    st.markdown(f"""
        <style>
        .main {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        
        /* Larger, accessible radio buttons */
        .stRadio [role=radiogroup] {{ 
            display: flex; 
            flex-direction: row; 
            justify-content: center; 
            gap: 20px;
            margin-bottom: 2.5rem;
        }}
        .stRadio div[role=radiogroup] > label {{
            background: white;
            padding: 16px 32px;
            border-radius: 30px;
            border: 2px solid #ddd;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 600;
        }}

        /* Enhanced Card Accessibility */
        .recommendation-card {{
            background-color: white;
            padding: 40px;
            border-radius: 32px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.06);
            text-align: center;
            margin-top: 15px;
            border-left: 12px solid; /* Vertical indicator for color blindness */
        }}
        .status-go {{ border-left-color: {COLOR_GO_NOW}; }}
        .status-wait {{ border-left-color: {COLOR_WAIT}; }}
        
        /* Accessible Typography */
        .big-text {{ font-size: 64px; font-weight: 800; margin: 10px 0; letter-spacing: -2px; }}
        .sub-text {{ color: #444; font-size: 22px; font-weight: 500; }}
        .status-badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 15px;
        }}
        .badge-go {{ background-color: #E8F5E9; color: {COLOR_GO_NOW}; }}
        .badge-wait {{ background-color: #FFFDE7; color: {COLOR_WAIT}; }}
        </style>
        """, unsafe_allow_html=True)
