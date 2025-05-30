# utils/database.py - Database connection and operations
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from typing import Optional, Tuple, Dict, List
from datetime import datetime

@st.cache_resource
def init_supabase() -> Optional[Client]:
    """Initialize Supabase client"""
    try:
        # You should store these in Streamlit secrets or environment variables
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_ANON_KEY", "")
        
        if not url or not key:
            st.error("Please configure Supabase credentials in .streamlit/secrets.toml")
            st.code("""
# .streamlit/secrets.toml
SUPABASE_URL = "https://zxbgxcfknbwedlvhqdru.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4Ymd4Y2ZrbmJ3ZWRsdmhxZHJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0MTg1ODIsImV4cCI6MjA2Mzk5NDU4Mn0.o_Uv9mc2tvmcSzGcA0lPO7DPmyaMO7yjxP1osWDV4y4"
            """)
            return None
            
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {str(e)}")
        return None

# Student Operations
def get_all_students(supabase: Client) -> pd.DataFrame:
    """Fetch all students from Supabase"""
    if not supabase:
        return pd.DataFrame()
    
    try:
        response = supabase.table('students').select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching students: {str(e)}")
        return pd.DataFrame()

def add_student(supabase: Client, student_data: Dict) -> Tuple[bool, str]:
    """Add a new student to Supabase"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').insert(student_data).execute()
        return True, "Student added successfully"
    except Exception as e:
        return False, str(e)

def update_student(supabase: Client, student_id: str, update_data: Dict) -> Tuple[bool, str]:
    """Update student information"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').update(update_data).eq('student_id', student_id).execute()
        return True, "Student updated successfully"
    except Exception as e:
        return False, str(e)

def delete_student(supabase: Client, student_id: str) -> Tuple[bool, str]:
    """Delete a student"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').delete().eq('student_id', student_id).execute()
        return True, "Student deleted successfully"
    except Exception as e:
        return False, str(e)

def get_student_by_id(supabase: Client, student_id: str) -> Optional[Dict]:
    """Get a specific student by ID"""
    if not supabase:
        return None
    
    try:
        response = supabase.table('students').select("*").eq('student_id', student_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error fetching student: {str(e)}")
        return None

# Attendance Operations
def mark_attendance(supabase: Client, attendance_data: Dict) -> bool:
    """Mark attendance in Supabase"""
    if not supabase:
        return False
    
    try:
        response = supabase.table('attendance').insert(attendance_data).execute()
        return True
    except Exception as e:
        st.error(f"Error marking attendance: {str(e)}")
        return False

def get_attendance_records(supabase: Client, date_filter: str = None, department_filter: str = None) -> pd.DataFrame:
    """Fetch attendance records with optional filters"""
    if not supabase:
        return pd.DataFrame()
    
    try:
        query = supabase.table('attendance').select("*")
        
        if date_filter:
            query = query.eq('check_in_date', date_filter)
        
        if department_filter:
            query = query.eq('department', department_filter)
        
        response = query.execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching attendance: {str(e)}")
        return pd.DataFrame()

def get_attendance_by_date_range(supabase: Client, start_date: str, end_date: str, department: str = None) -> pd.DataFrame:
    """Fetch attendance records for a date range"""
    if not supabase:
        return pd.DataFrame()
    
    try:
        query = supabase.table('attendance').select("*")\
            .gte('check_in_date', start_date)\
            .lte('check_in_date', end_date)
        
        if department and department != "All":
            query = query.eq('department', department)
        
        response = query.execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching attendance: {str(e)}")
        return pd.DataFrame()

def check_attendance_exists(supabase: Client, student_id: str, date: str) -> bool:
    """Check if attendance already exists for a student on a specific date"""
    if not supabase:
        return False
    
    try:
        response = supabase.table('attendance')\
            .select("id")\
            .eq('student_id', student_id)\
            .eq('check_in_date', date)\
            .execute()
        
        return len(response.data) > 0
    except Exception:
        return False

# Statistics Operations
def get_attendance_statistics(supabase: Client, date: str = None) -> Dict:
    """Get attendance statistics"""
    if not supabase:
        return {}
    
    try:
        students_df = get_all_students(supabase)
        total_students = len(students_df)
        
        if date:
            attendance_df = get_attendance_records(supabase, date_filter=date)
        else:
            attendance_df = get_attendance_records(supabase)
        
        present_count = len(attendance_df[attendance_df['status'] == 'Present']) if not attendance_df.empty else 0
        
        return {
            'total_students': total_students,
            'present': present_count,
            'absent': total_students - present_count,
            'attendance_rate': (present_count / total_students * 100) if total_students > 0 else 0
        }
    except Exception as e:
        st.error(f"Error calculating statistics: {str(e)}")
        return {}

def get_department_statistics(supabase: Client) -> pd.DataFrame:
    """Get statistics by department"""
    if not supabase:
        return pd.DataFrame()
    
    try:
        students_df = get_all_students(supabase)
        if students_df.empty:
            return pd.DataFrame()
        
        return students_df.groupby('department').size().reset_index(name='count')
    except Exception as e:
        st.error(f"Error calculating department statistics: {str(e)}")
        return pd.DataFrame()