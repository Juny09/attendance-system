# app.py - Main Streamlit Application with Supabase
import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import time
import tempfile
import csv
from supabase import create_client, Client
import json
from typing import Optional
import uuid

# Page config
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("### 🔐 Supabase Configuration")
supabase_url = st.sidebar.text_input("Supabase URL", type="default")
supabase_key = st.sidebar.text_input("Supabase Anon Key", type="password")

# Store in session
if supabase_url and supabase_key:
    st.session_state['SUPABASE_URL'] = supabase_url
    st.session_state['SUPABASE_KEY'] = supabase_key


# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Supabase configuration
# @st.cache_resource
# def init_supabase() -> Optional[Client]:
#     """Initialize Supabase client"""
#     try:
#         # You should store these in Streamlit secrets or environment variables
#         url = st.secrets.get("SUPABASE_URL", "")
#         key = st.secrets.get("SUPABASE_ANON_KEY", "")
        
#         if not url or not key:
#             st.error("Please configure Supabase credentials in .streamlit/secrets.toml")
#             st.code("""
# # .streamlit/secrets.toml
# SUPABASE_URL = "your-project-url"
# SUPABASE_ANON_KEY = "your-anon-key"
#             """)
#             return None

@st.cache_resource
def init_supabase(url: str, key: str) -> Optional[Client]:
    try:
        if not url or not key:
            st.error("Please provide both Supabase URL and Anon Key.")
            return None
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {str(e)}")
        return None

            
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {str(e)}")
        return None

# Get Supabase client
# supabase = init_supabase()
supabase = None
if 'SUPABASE_URL' in st.session_state and 'SUPABASE_KEY' in st.session_state:
    supabase = init_supabase(st.session_state['SUPABASE_URL'], st.session_state['SUPABASE_KEY'])

# Create tables if they don't exist (run this once in Supabase SQL editor)
def show_create_tables_sql():
    sql = """
    -- Create students table
    CREATE TABLE IF NOT EXISTS students (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        student_id VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        department VARCHAR(255) NOT NULL,
        course VARCHAR(255) NOT NULL,
        year VARCHAR(255) NOT NULL,
        semester VARCHAR(255) NOT NULL,
        teacher VARCHAR(255) NOT NULL,
        gender VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        photo_status VARCHAR(255) DEFAULT 'No',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Create attendance table
    CREATE TABLE IF NOT EXISTS attendance (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        student_id VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        department VARCHAR(255) NOT NULL,
        check_in_time TIME NOT NULL,
        check_in_date DATE NOT NULL,
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_students_student_id ON students(student_id);
    CREATE INDEX IF NOT EXISTS idx_attendance_student_id ON attendance(student_id);
    CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(check_in_date);

    -- Enable Row Level Security
    ALTER TABLE students ENABLE ROW LEVEL SECURITY;
    ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;

    -- Create policies (adjust based on your auth needs)
    CREATE POLICY "Enable all access for authenticated users" ON students
        FOR ALL USING (true);
    
    CREATE POLICY "Enable all access for authenticated users" ON attendance
        FOR ALL USING (true);
    """
    return sql

# Create data directory if not exists
if not os.path.exists('data'):
    os.makedirs('data')

# Helper functions for Supabase operations
def get_all_students():
    """Fetch all students from Supabase"""
    if not supabase:
        return pd.DataFrame()
    
    try:
        response = supabase.table('students').select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching students: {str(e)}")
        return pd.DataFrame()

def add_student(student_data):
    """Add a new student to Supabase"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').insert(student_data).execute()
        return True, "Student added successfully"
    except Exception as e:
        return False, str(e)

def update_student(student_id, update_data):
    """Update student information"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').update(update_data).eq('student_id', student_id).execute()
        return True, "Student updated successfully"
    except Exception as e:
        return False, str(e)

def delete_student(student_id):
    """Delete a student"""
    if not supabase:
        return False, "Supabase not initialized"
    
    try:
        response = supabase.table('students').delete().eq('student_id', student_id).execute()
        return True, "Student deleted successfully"
    except Exception as e:
        return False, str(e)

def mark_attendance(attendance_data):
    """Mark attendance in Supabase"""
    if not supabase:
        return False
    
    try:
        response = supabase.table('attendance').insert(attendance_data).execute()
        return True
    except Exception as e:
        st.error(f"Error marking attendance: {str(e)}")
        return False

def get_attendance_records(date_filter=None, department_filter=None):
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

# Sidebar Navigation
with st.sidebar:
    st.markdown("# Navigation")
    
    if st.button("🏠 Home", key="home"):
        st.session_state.page = 'Home'
    if st.button("👥 Student Management", key="student"):
        st.session_state.page = 'Student Management'
    if st.button("🎯 Train Model", key="train"):
        st.session_state.page = 'Train Model'
    if st.button("📸 Face Recognition", key="recognition"):
        st.session_state.page = 'Face Recognition'
    if st.button("📊 Attendance Report", key="attendance"):
        st.session_state.page = 'Attendance Report'
    if st.button("🔧 Setup", key="setup"):
        st.session_state.page = 'Setup'
    
    st.markdown("---")
    st.markdown("### System Info")
    st.info(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
    st.info(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    
    if supabase:
        st.success("✅ Connected to Supabase")
    else:
        st.error("❌ Supabase not connected")

# Main Content Area
st.markdown('<h1 class="main-header">FACE RECOGNITION ATTENDANCE SYSTEM</h1>', unsafe_allow_html=True)

# Home Page
if st.session_state.page == 'Home':
    st.markdown("## Welcome to Face Recognition Attendance System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👥 Student Management")
        st.write("Add, update, and manage student information")
        if st.button("Go to Student Management"):
            st.session_state.page = 'Student Management'
            st.rerun()
    
    with col2:
        st.markdown("### 📸 Face Recognition")
        st.write("Mark attendance using face recognition")
        if st.button("Go to Face Recognition"):
            st.session_state.page = 'Face Recognition'
            st.rerun()
    
    with col3:
        st.markdown("### 📊 Reports")
        st.write("View and export attendance reports")
        if st.button("Go to Reports"):
            st.session_state.page = 'Attendance Report'
            st.rerun()
    
    # Quick Stats
    if supabase:
        st.markdown("### 📊 Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        students_df = get_all_students()
        today_date = datetime.now().strftime('%Y-%m-%d')
        attendance_df = get_attendance_records(date_filter=today_date)
        
        with col1:
            st.metric("Total Students", len(students_df))
        with col2:
            if not attendance_df.empty and 'status' in attendance_df.columns:
                present_count = len(attendance_df[attendance_df['status'] == 'Present'])
                st.metric("Present Today", present_count)
            else:
                st.metric("Present Today", 0)

        with col3:
            st.metric("Departments", students_df['department'].nunique() if not students_df.empty else 0)
        with col4:
            if len(students_df) > 0 and len(attendance_df) > 0:
                attendance_rate = (len(attendance_df[attendance_df['status'] == 'Present']) / len(students_df)) * 100
                st.metric("Today's Attendance", f"{attendance_rate:.1f}%")
            else:
                st.metric("Today's Attendance", "0%")

# Setup Page
elif st.session_state.page == 'Setup':
    st.markdown("## Database Setup")
    
    st.markdown("### Supabase Configuration")
    st.info("Make sure you have created a Supabase project and have your URL and Anon Key ready.")
    
    st.markdown("### Create Tables")
    st.markdown("Run the following SQL in your Supabase SQL editor to create the required tables:")
    
    sql_code = show_create_tables_sql()
    st.code(sql_code, language='sql')
    
    st.markdown("### Configuration File")
    st.markdown("Create a `.streamlit/secrets.toml` file in your project directory with:")
    st.code("""
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
    """)

# Student Management Page
elif st.session_state.page == 'Student Management':
    st.markdown("## Student Management System")
    
    if not supabase:
        st.error("Please configure Supabase connection first!")
        if st.button("Go to Setup"):
            st.session_state.page = 'Setup'
            st.rerun()
    else:
        tab1, tab2, tab3 = st.tabs(["Add Student", "View/Update Students", "Capture Photos"])
        
        with tab1:
            st.markdown("### Add New Student")
            
            col1, col2 = st.columns(2)
            
            with col1:
                department = st.selectbox("Department", ["Select Department", "FCI", "FIST", "FOB", "FOM", "FOE", "FET", "FCM", "FCL"])
                course = st.selectbox("Course", ["Select Course", "TSE", "TML"])
                year = st.selectbox("Year", ["Select Year", "2023-24", "2024-25"])
                semester = st.selectbox("Semester", ["Select Semester", "Semester-1", "Semester-2", "Semester-3"])
                student_id = st.text_input("Student ID")
            
            with col2:
                student_name = st.text_input("Student Name")
                teacher_name = st.text_input("Teacher Name")
                gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other"])
                email = st.text_input("Email")
            
            if st.button("Save Student", type="primary"):
                if all([department != "Select Department", course != "Select Course", 
                       year != "Select Year", semester != "Select Semester",
                       student_id, student_name, teacher_name, gender != "Select Gender", email]):
                    
                    student_data = {
                        'student_id': student_id,
                        'name': student_name,
                        'department': department,
                        'course': course,
                        'year': year,
                        'semester': semester,
                        'teacher': teacher_name,
                        'gender': gender,
                        'email': email,
                        'photo_status': 'No'
                    }
                    
                    success, message = add_student(student_data)
                    if success:
                        st.success(message + " Please capture photos in the 'Capture Photos' tab.")
                    else:
                        st.error(f"Error: {message}")
                else:
                    st.error("All fields are required!")
        
        with tab2:
            st.markdown("### View and Update Students")
            
            students_df = get_all_students()
            
            if not students_df.empty:
                # Display students in a table
                st.dataframe(students_df, use_container_width=True)
                
                # Update/Delete section
                st.markdown("### Update or Delete Student")
                student_ids = students_df['student_id'].tolist()
                selected_id = st.selectbox("Select Student ID", student_ids)
                
                if selected_id:
                    student_data = students_df[students_df['student_id'] == selected_id].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Name", value=student_data['name'])
                        new_email = st.text_input("Email", value=student_data['email'])
                    with col2:
                        new_teacher = st.text_input("Teacher", value=student_data['teacher'])
                        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                                index=["Male", "Female", "Other"].index(student_data['gender']) if student_data['gender'] in ["Male", "Female", "Other"] else 0)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update Student", type="primary"):
                            update_data = {
                                'name': new_name,
                                'email': new_email,
                                'teacher': new_teacher,
                                'gender': new_gender,
                                'updated_at': datetime.now().isoformat()
                            }
                            
                            success, message = update_student(selected_id, update_data)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(f"Error: {message}")
                    
                    with col2:
                        if st.button("Delete Student", type="secondary"):
                            if st.checkbox("Confirm deletion"):
                                success, message = delete_student(selected_id)
                                if success:
                                    # Delete photos
                                    for i in range(1, 101):
                                        photo_path = f"data/user.{selected_id}.{i}.jpg"
                                        if os.path.exists(photo_path):
                                            os.remove(photo_path)
                                    
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(f"Error: {message}")
            else:
                st.info("No students found in the database.")
        
        with tab3:
            st.markdown("### Capture Student Photos")
            
            students_df = get_all_students()
            
            if not students_df.empty:
                student_options = [f"{row['student_id']} - {row['name']}" for _, row in students_df.iterrows()]
                selected_student = st.selectbox("Select Student", student_options)
                
                if selected_student:
                    student_id = selected_student.split(" - ")[0]
                    
                    # Camera input
                    st.markdown("### Capture Photos")
                    st.info("Click 'Start Capture' and the system will automatically capture 100 photos")
                    
                    # if st.button("Start Photo Capture"):
                    #     face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                    #     cap = cv2.VideoCapture(0)

                    #     img_counter = 0
                    #     max_images = 100
                    #     capture_interval = 1  # in seconds

                    #     progress_bar = st.progress(0)
                    #     status_text = st.empty()
                    #     photo_placeholder = st.empty()

                    #     start_time = time.time()

                    #     while img_counter < max_images:
                    #         ret, frame = cap.read()
                    #         if not ret:
                    #             break

                    #         elapsed_time = time.time() - start_time
                    #         if elapsed_time >= capture_interval:
                    #             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    #             faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                    #             if len(faces) > 0:
                    #                 (x, y, w, h) = faces[0]  # capture the first detected face
                    #                 face_img = frame[y:y+h, x:x+w]
                    #                 face_img = cv2.resize(face_img, (450, 450))

                    #                 file_path = f"data/user.{student_id}.{img_counter+1}.jpg"
                    #                 cv2.imwrite(file_path, face_img)

                    #                 img_counter += 1
                    #                 progress_bar.progress(img_counter / max_images)
                    #                 status_text.text(f"Captured {img_counter}/{max_images} photos")
                    #                 photo_placeholder.image(face_img, channels="BGR", width=200)

                    #                 start_time = time.time()  # reset timer

                    #     cap.release()
            #         if st.button("Start Photo Capture"):
            #             cap = cv2.VideoCapture(0)

            #             img_counter = 0
            #             max_images = 50
            #             capture_interval = 0.1  # in seconds

            #             progress_bar = st.progress(0)
            #             status_text = st.empty()
            #             photo_placeholder = st.empty()

            #             start_time = time.time()

            #             while img_counter < max_images:
            #                 ret, frame = cap.read()
            #                 if not ret:
            #                     break

            #                 elapsed_time = time.time() - start_time
            #                 if elapsed_time >= capture_interval:
            #                     # Resize full frame to 450x450 if needed
            #                     resized_frame = cv2.resize(frame, (450, 450))

            #                     file_path = f"data/user.{student_id}.{img_counter+1}.jpg"
            #                     cv2.imwrite(file_path, resized_frame)

            #                     img_counter += 1
            #                     progress_bar.progress(img_counter / max_images)
            #                     status_text.text(f"Captured {img_counter}/{max_images} photos")
            #                     photo_placeholder.image(resized_frame, channels="BGR", width=200)

            #                     start_time = time.time()

            #             cap.release()
                    
            #             # Update photo status in database
            #             update_data = {
            #                 'photo_status': 'Yes',
            #                 'updated_at': datetime.now().isoformat()
            #             }
            #             success, message = update_student(student_id, update_data)
                        
            #             if success:
            #                 st.success("Photo capture completed! 100 photos saved.")
            #             else:
            #                 st.error(f"Photos saved but failed to update database: {message}")
            # else:
            #     st.info("No students found. Please add students first.")

    # Let user choose capture method
    capture_method = st.radio("Select Method to Add Photos", ["Upload Images", "Use Webcam (local only)"])

    if capture_method == "Upload Images":
        uploaded_files = st.file_uploader(
            "Upload up to 50 student face images (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            for idx, uploaded_file in enumerate(uploaded_files[:50]):
                image = Image.open(uploaded_file).convert("RGB")
                image = image.resize((450, 450))
                file_path = f"data/user.{student_id}.{idx+1}.jpg"
                image.save(file_path)

            update_data = {
                'photo_status': 'Yes',
                'updated_at': datetime.now().isoformat()
            }
            success, message = update_student(student_id, update_data)

            if success:
                st.success(f"{len(uploaded_files)} photos uploaded and saved successfully.")
            else:
                st.error(f"Failed to update database: {message}")

        elif capture_method == "Use Webcam (local only)":
            if st.button("Start Photo Capture"):
                cap = cv2.VideoCapture(0)

                img_counter = 0
                max_images = 50
                capture_interval = 0.1  # seconds

                progress_bar = st.progress(0)
                status_text = st.empty()
                photo_placeholder = st.empty()

                start_time = time.time()

                while img_counter < max_images:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    elapsed_time = time.time() - start_time
                    if elapsed_time >= capture_interval:
                        resized_frame = cv2.resize(frame, (450, 450))

                        file_path = f"data/user.{student_id}.{img_counter+1}.jpg"
                        cv2.imwrite(file_path, resized_frame)

                        img_counter += 1
                        progress_bar.progress(img_counter / max_images)
                        status_text.text(f"Captured {img_counter}/{max_images} photos")
                        photo_placeholder.image(resized_frame, channels="BGR", width=200)

                        start_time = time.time()

                cap.release()

                update_data = {
                    'photo_status': 'Yes',
                    'updated_at': datetime.now().isoformat()
                }
                success, message = update_student(student_id, update_data)

                if success:
                    st.success("Photo capture completed! Photos saved successfully.")
                else:
                    st.error(f"Photos saved but failed to update database: {message}")

# Train Model Page
elif st.session_state.page == 'Train Model':
    st.markdown("## Train Face Recognition Model")
    
    # Check if photos exist
    if os.path.exists('data') and len(os.listdir('data')) > 0:
        st.info(f"Found {len(os.listdir('data'))} photos in the dataset")
        
        if st.button("Start Training", type="primary"):
            with st.spinner("Training in progress..."):
                try:
                    faces = []
                    ids = []
                    
                    # Get student mapping
                    students_df = get_all_students()
                    student_mapping = {}
                    for idx, row in students_df.iterrows():
                        # Use index as numeric ID for face recognizer
                        student_mapping[idx] = row['student_id']
                    
                    # Save mapping for later use
                    with open('student_mapping.json', 'w') as f:
                        json.dump(student_mapping, f)
                    
                    for image_file in os.listdir('data'):
                        if image_file.endswith('.jpg'):
                            img_path = os.path.join('data', image_file)
                            img = Image.open(img_path).convert('L')
                            img_np = np.array(img, 'uint8')
                            
                            # Extract student_id from filename
                            student_id = image_file.split('.')[1]
                            
                            # Find numeric ID for this student
                            numeric_id = None
                            for num_id, stu_id in student_mapping.items():
                                if stu_id == student_id:
                                    numeric_id = int(num_id)
                                    break
                            
                            if numeric_id is not None:
                                faces.append(img_np)
                                ids.append(numeric_id)
                    
                    if len(faces) > 0:
                        # Train the recognizer
                        recognizer = cv2.face.LBPHFaceRecognizer_create()
                        recognizer.train(faces, np.array(ids))
                        recognizer.write('classifier.xml')
                        
                        st.success(f"Training completed! Trained with {len(faces)} images from {len(set(ids))} students.")
                    else:
                        st.error("No valid face data found for training!")
                except Exception as e:
                    st.error(f"Training failed: {str(e)}")
    else:
        st.warning("No photos found for training. Please capture student photos first.")

# Face Recognition Page
elif st.session_state.page == 'Face Recognition':
    st.markdown("## Face Recognition Attendance")
    
    if not supabase:
        st.error("Please configure Supabase connection first!")
    elif not os.path.exists('classifier.xml'):
        st.error("No trained model found. Please train the model first.")
    elif not os.path.exists('student_mapping.json'):
        st.error("Student mapping not found. Please train the model again.")
    else:
        st.info("Click 'Start Recognition' to begin marking attendance")
        
        # Load student mapping
        with open('student_mapping.json', 'r') as f:
            student_mapping = json.load(f)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Face Recognition", type="primary"):
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read('classifier.xml')
                
                # Video capture placeholder
                video_placeholder = st.empty()
                status_placeholder = st.empty()
                stop_button_placeholder = st.empty()
                
                cap = cv2.VideoCapture(0)
                attendance_marked = set()
                
                # Create stop button
                stop_clicked = stop_button_placeholder.button("Stop Recognition")
                
                while cap.isOpened() and not stop_clicked:
                    ret, frame = cap.read()
                    if ret:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.1, 10)
                        
                        for (x, y, w, h) in faces:
                            face_roi = gray[y:y+h, x:x+w]
                            id, confidence = recognizer.predict(face_roi)
                            
                            if confidence < 50:  # Good match
                                # Get student_id from mapping
                                student_id = student_mapping.get(str(id))
                                
                                if student_id:
                                    # Get student details
                                    students_df = get_all_students()
                                    student = students_df[students_df['student_id'] == student_id]
                                    
                                    if not student.empty:
                                        student_data = student.iloc[0]
                                        name = student_data['name']
                                        dept = student_data['department']
                                        
                                        # Draw rectangle and text
                                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                                        cv2.putText(frame, f"ID: {student_id}", (x, y-75), 
                                                   cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                                        cv2.putText(frame, f"Name: {name}", (x, y-30), 
                                                   cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                                        
                                        # Mark attendance
                                        if student_id not in attendance_marked:
                                            now = datetime.now()
                                            attendance_data = {
                                                'student_id': student_id,
                                                'name': name,
                                                'department': dept,
                                                'check_in_time': now.strftime("%H:%M:%S"),
                                                'check_in_date': now.strftime("%Y-%m-%d"),
                                                'status': 'Present'
                                            }
                                            
                                            if mark_attendance(attendance_data):
                                                attendance_marked.add(student_id)
                                                status_placeholder.success(f"✅ Attendance marked for {name}")
                            else:
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                                cv2.putText(frame, "Unknown", (x, y-5), 
                                           cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)
                        
                        # Display frame
                        video_placeholder.image(frame, channels="BGR", use_column_width=True)
                    
                    # Check if stop button was clicked
                    stop_clicked = stop_button_placeholder.button("Stop Recognition", key=f"stop_{time.time()}")
                
                cap.release()
                video_placeholder.empty()
                status_placeholder.success("Face recognition session ended.")
                stop_button_placeholder.empty()

# Attendance Report Page
elif st.session_state.page == 'Attendance Report':
    st.markdown("## Attendance Report")
    
    if not supabase:
        st.error("Please configure Supabase connection first!")
    else:
        tab1, tab2 = st.tabs(["View Attendance", "Export Report"])
        
        with tab1:
            st.markdown("### Attendance Records")
            
            # Get all students and attendance records
            students_df = get_all_students()
            attendance_df = get_attendance_records()
            
            if not attendance_df.empty:
                # Display filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    departments = ["All"] + students_df['department'].unique().tolist() if not students_df.empty else ["All"]
                    dept_filter = st.selectbox("Filter by Department", departments)
                with col2:
                    dates = ["All"] + attendance_df['check_in_date'].unique().tolist()
                    date_filter = st.selectbox("Filter by Date", dates)
                with col3:
                    status_filter = st.selectbox("Filter by Status", ["All", "Present", "Absent"])
                
                # Apply filters
                filtered_df = attendance_df.copy()
                
                if dept_filter != "All":
                    filtered_df = filtered_df[filtered_df['department'] == dept_filter]
                
                if date_filter != "All":
                    filtered_df = filtered_df[filtered_df['check_in_date'] == date_filter]
                
                # For showing absent students
                if status_filter == "Absent" and date_filter != "All":
                    # Get students who were absent on selected date
                    present_students = filtered_df['student_id'].unique()
                    all_student_ids = students_df['student_id'].unique()
                    absent_students = [sid for sid in all_student_ids if sid not in present_students]
                    
                    # Create absent records
                    absent_records = []
                    for sid in absent_students:
                        student = students_df[students_df['student_id'] == sid].iloc[0]
                        if dept_filter == "All" or student['department'] == dept_filter:
                            absent_records.append({
                                'student_id': sid,
                                'name': student['name'],
                                'department': student['department'],
                                'check_in_time': 'N/A',
                                'check_in_date': date_filter,
                                'status': 'Absent'
                            })
                    
                    if absent_records:
                        absent_df = pd.DataFrame(absent_records)
                        filtered_df = absent_df
                    else:
                        filtered_df = pd.DataFrame()
                
                elif status_filter == "Present":
                    filtered_df = filtered_df[filtered_df['status'] == 'Present']
                
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Records", len(filtered_df))
                with col2:
                    present_count = len(filtered_df[filtered_df['status'] == 'Present'])
                    st.metric("Present", present_count)
                with col3:
                    absent_count = len(filtered_df[filtered_df['status'] == 'Absent'])
                    st.metric("Absent", absent_count)
                with col4:
                    if len(filtered_df) > 0:
                        attendance_rate = (present_count / (present_count + absent_count)) * 100 if (present_count + absent_count) > 0 else 0
                        st.metric("Attendance Rate", f"{attendance_rate:.1f}%")
                
                # Display table
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.info("No records found with the selected filters.")
            else:
                st.info("No attendance records found.")
        
        with tab2:
            st.markdown("### Export Attendance Report")
            
            # Date range selection
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", datetime.now().date())
            with col2:
                end_date = st.date_input("End Date", datetime.now().date())
            
            # Department filter for export
            departments = ["All"] + students_df['department'].unique().tolist() if not students_df.empty else ["All"]
            export_dept = st.selectbox("Department", departments, key="export_dept")
            
            # Export options
            include_absent = st.checkbox("Include absent students", value=True)
            
            if st.button("Generate Report", type="primary"):
                # Fetch attendance data for date range
                all_attendance = []
                current_date = start_date
                
                while current_date <= end_date:
                    date_str = current_date.strftime('%Y-%m-%d')
                    day_attendance = get_attendance_records(date_filter=date_str)
                    
                    if not day_attendance.empty:
                        all_attendance.append(day_attendance)
                    
                    # Add absent students if requested
                    if include_absent:
                        present_ids = day_attendance['student_id'].unique() if not day_attendance.empty else []
                        
                        for _, student in students_df.iterrows():
                            if student['student_id'] not in present_ids:
                                if export_dept == "All" or student['department'] == export_dept:
                                    absent_record = pd.DataFrame([{
                                        'student_id': student['student_id'],
                                        'name': student['name'],
                                        'department': student['department'],
                                        'check_in_time': 'N/A',
                                        'check_in_date': date_str,
                                        'status': 'Absent'
                                    }])
                                    all_attendance.append(absent_record)
                    
                    current_date += pd.Timedelta(days=1)
                
                if all_attendance:
                    # Combine all data
                    export_df = pd.concat(all_attendance, ignore_index=True)
                    
                    # Apply department filter
                    if export_dept != "All":
                        export_df = export_df[export_df['department'] == export_dept]
                    
                    # Sort by date and student ID
                    export_df = export_df.sort_values(['check_in_date', 'student_id'])
                    
                    # Generate CSV
                    csv = export_df.to_csv(index=False)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Attendance Report",
                        data=csv,
                        file_name=f'attendance_report_{start_date}_{end_date}.csv',
                        mime='text/csv'
                    )
                    
                    # Show preview
                    st.markdown("### Report Preview")
                    st.dataframe(export_df, use_container_width=True)
                    
                    # Summary statistics
                    st.markdown("### Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Days", (end_date - start_date).days + 1)
                    with col2:
                        st.metric("Total Students", export_df['student_id'].nunique())
                    with col3:
                        total_present = len(export_df[export_df['status'] == 'Present'])
                        total_records = len(export_df)
                        avg_attendance = (total_present / total_records * 100) if total_records > 0 else 0
                        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
                else:
                    st.info("No data found for the selected date range.")

# Footer
st.markdown("---")
st.markdown("© 2024 Face Recognition Attendance System")