# app.py - Main Streamlit Application Entry Point
import streamlit as st
from datetime import datetime
import os

# Import page modules
from pages import home, student_management, train_model, face_recognition, attendance_report, setup
from utils.database import init_supabase
from utils.ui_components import render_sidebar, apply_custom_css

# Page config
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Create data directory if not exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize Supabase
supabase = init_supabase()

# Render sidebar and get selected page
render_sidebar(supabase)

# Main Content Area
st.markdown('<h1 class="main-header">FACE RECOGNITION ATTENDANCE SYSTEM</h1>', unsafe_allow_html=True)

# Route to appropriate page based on session state
if st.session_state.page == 'Home':
    home.render_page(supabase)
elif st.session_state.page == 'Student Management':
    student_management.render_page(supabase)
elif st.session_state.page == 'Train Model':
    train_model.render_page(supabase)
elif st.session_state.page == 'Face Recognition':
    face_recognition.render_page(supabase)
elif st.session_state.page == 'Attendance Report':
    attendance_report.render_page(supabase)
elif st.session_state.page == 'Setup':
    setup.render_page()

# Footer
st.markdown("---")
st.markdown("© 2024 Face Recognition Attendance System - MMU | Powered by Supabase")