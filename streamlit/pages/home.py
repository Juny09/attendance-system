# pages/home.py - Home page
import streamlit as st
from datetime import datetime
from utils.database import get_attendance_statistics, get_department_statistics, get_all_students, get_attendance_records
from utils.ui_components import create_metric_card, show_info_message

def render_page(supabase):
    """Render the home page"""
    st.markdown("## Welcome to Face Recognition Attendance System")
    
    # Quick action cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="info-card">
                <h3>👥 Student Management</h3>
                <p>Add, update, and manage student information in the system.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Student Management", key="home_student_btn"):
                st.session_state.page = 'Student Management'
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="info-card">
                <h3>📸 Face Recognition</h3>
                <p>Mark attendance automatically using face recognition technology.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Face Recognition", key="home_recognition_btn"):
                st.session_state.page = 'Face Recognition'
                st.rerun()
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="info-card">
                <h3>📊 Reports</h3>
                <p>View attendance reports and export data for analysis.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Reports", key="home_reports_btn"):
                st.session_state.page = 'Attendance Report'
                st.rerun()
    
    # Statistics Section
    if supabase:
        st.markdown("---")
        st.markdown("### 📊 Today's Statistics")
        
        # Get today's stats
        today_date = datetime.now().strftime('%Y-%m-%d')
        stats = get_attendance_statistics(supabase, date=today_date)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Students", 
                stats.get('total_students', 0),
                help="Total number of registered students"
            )
        
        with col2:
            st.metric(
                "Present Today", 
                stats.get('present', 0),
                delta=f"{stats.get('attendance_rate', 0):.1f}% attendance",
                help="Students marked present today"
            )
        
        with col3:
            st.metric(
                "Absent Today", 
                stats.get('absent', 0),
                help="Students not yet marked present"
            )
        
        with col4:
            # Get department count
            dept_stats = get_department_statistics(supabase)
            st.metric(
                "Departments", 
                len(dept_stats) if not dept_stats.empty else 0,
                help="Number of active departments"
            )
        
        # Recent Activity
        st.markdown("### 🕐 Recent Attendance")
        recent_attendance = get_attendance_records(supabase, date_filter=today_date)
        
        if not recent_attendance.empty:
            # Show last 5 attendance records
            recent_attendance = recent_attendance.sort_values('created_at', ascending=False).head(5)
            
            for _, record in recent_attendance.iterrows():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.text(f"👤 {record['name']}")
                with col2:
                    st.text(f"🏢 {record['department']}")
                with col3:
                    st.text(f"🕐 {record['check_in_time']}")
        else:
            show_info_message("No attendance records for today yet.", "info")
        
        # Department Statistics
        st.markdown("### 🏢 Department Overview")
        dept_stats = get_department_statistics(supabase)
        
        if not dept_stats.empty:
            # Create a bar chart
            st.bar_chart(
                dept_stats.set_index('department')['count'],
                use_container_width=True,
                height=300
            )
        else:
            show_info_message("No department data available.", "info")
        
        # Quick Links
        st.markdown("### 🔗 Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("➕ Add Student", use_container_width=True):
                st.session_state.page = 'Student Management'
                st.rerun()
        
        with col2:
            if st.button("📷 Capture Photos", use_container_width=True):
                st.session_state.page = 'Student Management'
                st.rerun()
        
        with col3:
            if st.button("🎯 Train Model", use_container_width=True):
                st.session_state.page = 'Train Model'
                st.rerun()
        
        with col4:
            if st.button("📥 Export Report", use_container_width=True):
                st.session_state.page = 'Attendance Report'
                st.rerun()
    
    else:
        # No database connection
        st.markdown("---")
        show_info_message(
            "Database not connected. Please configure Supabase connection in the Setup page.",
            "warning"
        )
        
        if st.button("Go to Setup", type="primary", use_container_width=True):
            st.session_state.page = 'Setup'
            st.rerun()