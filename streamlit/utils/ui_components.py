# utils/ui_components.py - Reusable UI components
import streamlit as st
from datetime import datetime
from supabase import Client

def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #FF0000;
            padding: 1rem;
            background-color: #f0f0f0;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            height: 50px;
            font-size: 18px;
        }
        .success-msg {
            padding: 1rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            color: #155724;
        }
        .error-msg {
            padding: 1rem;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            color: #721c24;
        }
        .info-card {
            padding: 1.5rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(supabase: Client):
    """Render the sidebar navigation"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=MMU+Logo", use_column_width=True)
        st.markdown("# Navigation")
        
        # Navigation buttons
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.page = 'Home'
            st.rerun()
            
        if st.button("👥 Student Management", key="nav_student", use_container_width=True):
            st.session_state.page = 'Student Management'
            st.rerun()
            
        if st.button("🎯 Train Model", key="nav_train", use_container_width=True):
            st.session_state.page = 'Train Model'
            st.rerun()
            
        if st.button("📸 Face Recognition", key="nav_recognition", use_container_width=True):
            st.session_state.page = 'Face Recognition'
            st.rerun()
            
        if st.button("📊 Attendance Report", key="nav_attendance", use_container_width=True):
            st.session_state.page = 'Attendance Report'
            st.rerun()
            
        if st.button("🔧 Setup", key="nav_setup", use_container_width=True):
            st.session_state.page = 'Setup'
            st.rerun()
        
        st.markdown("---")
        
        # System Info
        st.markdown("### System Info")
        st.info(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
        
        # Connection Status
        if supabase:
            st.success("✅ Connected to Supabase")
        else:
            st.error("❌ Supabase not connected")

def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Create a custom metric card"""
    delta_html = ""
    if delta:
        color = "green" if delta_color == "normal" else "red"
        delta_html = f'<p style="color: {color}; font-size: 14px; margin: 0;">{delta}</p>'
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0; color: #666;">{title}</h4>
        <h2 style="margin: 0.5rem 0; color: #333;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def show_info_message(message: str, msg_type: str = "info"):
    """Display formatted info messages"""
    icon = "ℹ️" if msg_type == "info" else "✅" if msg_type == "success" else "⚠️" if msg_type == "warning" else "❌"
    color = "#d1ecf1" if msg_type == "info" else "#d4edda" if msg_type == "success" else "#fff3cd" if msg_type == "warning" else "#f8d7da"
    
    st.markdown(f"""
    <div style="padding: 1rem; background-color: {color}; border-radius: 5px; margin: 1rem 0;">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
        {message}
    </div>
    """, unsafe_allow_html=True)

def create_download_button(label: str, data: str, filename: str, mime: str = 'text/csv'):
    """Create a styled download button"""
    return st.download_button(
        label=f"📥 {label}",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True
    )

def confirm_dialog(message: str) -> bool:
    """Show a confirmation dialog"""
    return st.checkbox(f"⚠️ {message}")

def render_data_table(dataframe, key=None):
    """Render a styled data table"""
    if not dataframe.empty:
        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
            key=key
        )
    else:
        show_info_message("No data available", "warning")