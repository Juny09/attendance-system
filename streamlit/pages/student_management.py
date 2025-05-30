# pages/student_management.py - Student Management page
import streamlit as st
import cv2
import os
from datetime import datetime
from utils.database import (
    get_all_students, add_student, update_student, delete_student,
    get_student_by_id
)
from utils.ui_components import show_info_message, render_data_table, confirm_dialog
from utils.face_capture import capture_student_photos

def render_page(supabase):
    """Render the student management page"""
    st.markdown("## Student Management System")
    
    if not supabase:
        show_info_message("Please configure Supabase connection first!", "error")
        if st.button("Go to Setup"):
            st.session_state.page = 'Setup'
            st.rerun()
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View/Update Students", "📸 Capture Photos"])
    
    # Add Student Tab
    with tab1:
        render_add_student_tab(supabase)
    
    # View/Update Students Tab
    with tab2:
        render_view_update_tab(supabase)
    
    # Capture Photos Tab
    with tab3:
        render_capture_photos_tab(supabase)

def render_add_student_tab(supabase):
    """Render the add student form"""
    st.markdown("### Add New Student")
    
    # Create form
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            department = st.selectbox(
                "Department",
                ["Select Department", "FCI", "FIST", "FOB", "FOM", "FOE", "FET", "FCM", "FCL"]
            )
            course = st.selectbox(
                "Course",
                ["Select Course", "TSE", "TML", "CS", "IT", "BM", "ACC", "ENG", "COMM"]
            )
            year = st.selectbox(
                "Year",
                ["Select Year", "2023-24", "2024-25", "2025-26"]
            )
            semester = st.selectbox(
                "Semester",
                ["Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4"]
            )
            student_id = st.text_input("Student ID", placeholder="e.g., 1201234567")
        
        with col2:
            student_name = st.text_input("Student Name", placeholder="Full name")
            teacher_name = st.text_input("Teacher Name", placeholder="Supervisor/Teacher name")
            gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other"])
            email = st.text_input("Email", placeholder="student@example.com")
            st.markdown("")  # Add spacing
            submit_button = st.form_submit_button("Save Student", type="primary", use_container_width=True)
        
        if submit_button:
            # Validate inputs
            if all([
                department != "Select Department",
                course != "Select Course",
                year != "Select Year",
                semester != "Select Semester",
                student_id,
                student_name,
                teacher_name,
                gender != "Select Gender",
                email
            ]):
                # Check if email is valid
                if "@" not in email:
                    show_info_message("Please enter a valid email address.", "error")
                else:
                    # Prepare student data
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
                    
                    # Add to database
                    success, message = add_student(supabase, student_data)
                    if success:
                        st.balloons()
                        show_info_message(
                            f"{message} Please capture photos in the 'Capture Photos' tab.",
                            "success"
                        )
                        # Clear form by rerunning
                        st.rerun()
                    else:
                        show_info_message(f"Error: {message}", "error")
            else:
                show_info_message("All fields are required!", "error")

def render_view_update_tab(supabase):
    """Render the view and update students section"""
    st.markdown("### View and Update Students")
    
    # Fetch all students
    students_df = get_all_students(supabase)
    
    if not students_df.empty:
        # Add search/filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("🔍 Search by name", placeholder="Enter name...")
        with col2:
            dept_filter = st.selectbox(
                "Filter by Department",
                ["All"] + sorted(students_df['department'].unique().tolist())
            )
        with col3:
            photo_filter = st.selectbox(
                "Filter by Photo Status",
                ["All", "Photos Taken", "No Photos"]
            )
        
        # Apply filters
        filtered_df = students_df.copy()
        
        if search_name:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_name, case=False, na=False)
            ]
        
        if dept_filter != "All":
            filtered_df = filtered_df[filtered_df['department'] == dept_filter]
        
        if photo_filter == "Photos Taken":
            filtered_df = filtered_df[filtered_df['photo_status'] == 'Yes']
        elif photo_filter == "No Photos":
            filtered_df = filtered_df[filtered_df['photo_status'] == 'No']
        
        # Display count
        st.info(f"Showing {len(filtered_df)} of {len(students_df)} students")
        
        # Display students table
        render_data_table(filtered_df[['student_id', 'name', 'department', 'course', 'email', 'photo_status']])
        
        # Update/Delete section
        st.markdown("---")
        st.markdown("### Modify Student Record")
        
        if not filtered_df.empty:
            # Select student
            student_ids = filtered_df['student_id'].tolist()
            selected_id = st.selectbox(
                "Select Student to Modify",
                student_ids,
                format_func=lambda x: f"{x} - {filtered_df[filtered_df['student_id'] == x]['name'].iloc[0]}"
            )
            
            if selected_id:
                student_data = filtered_df[filtered_df['student_id'] == selected_id].iloc[0]
                
                # Update form
                with st.form("update_student_form"):
                    st.markdown("#### Update Student Information")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Name", value=student_data['name'])
                        new_email = st.text_input("Email", value=student_data['email'])
                        new_department = st.selectbox(
                            "Department",
                            ["FCI", "FIST", "FOB", "FOM", "FOE", "FET", "FCM", "FCL"],
                            index=["FCI", "FIST", "FOB", "FOM", "FOE", "FET", "FCM", "FCL"].index(student_data['department'])
                        )
                        new_course = st.selectbox(
                            "Course",
                            ["TSE", "TML", "CS", "IT", "BM", "ACC", "ENG", "COMM"],
                            index=["TSE", "TML", "CS", "IT", "BM", "ACC", "ENG", "COMM"].index(student_data['course']) if student_data['course'] in ["TSE", "TML", "CS", "IT", "BM", "ACC", "ENG", "COMM"] else 0
                        )
                    
                    with col2:
                        new_teacher = st.text_input("Teacher", value=student_data['teacher'])
                        new_gender = st.selectbox(
                            "Gender",
                            ["Male", "Female", "Other"],
                            index=["Male", "Female", "Other"].index(student_data['gender']) if student_data['gender'] in ["Male", "Female", "Other"] else 0
                        )
                        new_year = st.selectbox(
                            "Year",
                            ["2023-24", "2024-25", "2025-26"],
                            index=["2023-24", "2024-25", "2025-26"].index(student_data['year']) if student_data['year'] in ["2023-24", "2024-25", "2025-26"] else 0
                        )
                        new_semester = st.selectbox(
                            "Semester",
                            ["Semester-1", "Semester-2", "Semester-3", "Semester-4"],
                            index=["Semester-1", "Semester-2", "Semester-3", "Semester-4"].index(student_data['semester']) if student_data['semester'] in ["Semester-1", "Semester-2", "Semester-3", "Semester-4"] else 0
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Update Student", type="primary", use_container_width=True)
                    with col2:
                        delete_button = st.form_submit_button("Delete Student", type="secondary", use_container_width=True)
                
                # Handle update
                if update_button:
                    update_data = {
                        'name': new_name,
                        'email': new_email,
                        'teacher': new_teacher,
                        'gender': new_gender,
                        'department': new_department,
                        'course': new_course,
                        'year': new_year,
                        'semester': new_semester,
                        'updated_at': datetime.now().isoformat()
                    }
                    
                    success, message = update_student(supabase, selected_id, update_data)
                    if success:
                        show_info_message(message, "success")
                        st.rerun()
                    else:
                        show_info_message(f"Error: {message}", "error")
                
                # Handle delete
                if delete_button:
                    if confirm_dialog("I understand this will permanently delete the student and all associated data"):
                        success, message = delete_student(supabase, selected_id)
                        if success:
                            # Delete photos
                            photo_count = 0
                            for i in range(1, 101):
                                photo_path = f"data/user.{selected_id}.{i}.jpg"
                                if os.path.exists(photo_path):
                                    os.remove(photo_path)
                                    photo_count += 1
                            
                            show_info_message(
                                f"{message} {photo_count} photos deleted.",
                                "success"
                            )
                            st.rerun()
                        else:
                            show_info_message(f"Error: {message}", "error")
    else:
        show_info_message("No students found in the database. Add students using the 'Add Student' tab.", "info")

def render_capture_photos_tab(supabase):
    """Render the capture photos section"""
    st.markdown("### Capture Student Photos")
    
    # Get students
    students_df = get_all_students(supabase)
    
    if not students_df.empty:
        # Filter to show only students without photos
        no_photo_students = students_df[students_df['photo_status'] == 'No']
        
        if not no_photo_students.empty:
            st.info(f"📸 {len(no_photo_students)} students need photos to be captured")
        
        # Student selection
        student_options = [
            f"{row['student_id']} - {row['name']} ({'✅ Photos taken' if row['photo_status'] == 'Yes' else '❌ No photos'})"
            for _, row in students_df.iterrows()
        ]
        
        selected_student = st.selectbox("Select Student", student_options)
        
        if selected_student:
            student_id = selected_student.split(" - ")[0]
            student_name = selected_student.split(" - ")[1].split(" (")[0]
            
            # Get student details
            student = get_student_by_id(supabase, student_id)
            
            if student:
                # Display student info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Student ID", student_id)
                with col2:
                    st.metric("Name", student_name)
                with col3:
                    st.metric("Photos Status", "✅ Captured" if student['photo_status'] == 'Yes' else "❌ Not Captured")
                
                st.markdown("---")
                
                # Instructions
                st.markdown("#### 📷 Photo Capture Instructions")
                st.markdown("""
                1. Ensure good lighting and clear background
                2. Face should be clearly visible
                3. System will automatically capture 100 photos
                4. Keep face in frame and move slightly for variety
                5. Process takes about 30-60 seconds
                """)
                
                # Capture button
                if st.button("🎯 Start Photo Capture", type="primary", use_container_width=True):
                    success = capture_student_photos(student_id, student_name)
                    
                    if success:
                        # Update photo status in database
                        update_data = {
                            'photo_status': 'Yes',
                            'updated_at': datetime.now().isoformat()
                        }
                        success, message = update_student(supabase, student_id, update_data)
                        
                        if success:
                            st.balloons()
                            show_info_message(
                                "✅ Photo capture completed! 100 photos saved. You can now train the model.",
                                "success"
                            )
                            st.rerun()
                        else:
                            show_info_message(
                                f"Photos saved but failed to update database: {message}",
                                "warning"
                            )
                
                # Show existing photos if any
                if student['photo_status'] == 'Yes':
                    st.markdown("---")
                    st.markdown("#### Existing Photos")
                    
                    # Count existing photos
                    photo_count = 0
                    sample_photos = []
                    
                    for i in range(1, 101):
                        photo_path = f"data/user.{student_id}.{i}.jpg"
                        if os.path.exists(photo_path):
                            photo_count += 1
                            if len(sample_photos) < 5:  # Show first 5 photos
                                sample_photos.append(photo_path)
                    
                    st.info(f"Found {photo_count} photos for this student")
                    
                    if sample_photos:
                        st.markdown("Sample photos:")
                        cols = st.columns(5)
                        for idx, photo_path in enumerate(sample_photos):
                            with cols[idx]:
                                img = cv2.imread(photo_path)
                                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                st.image(img_rgb, caption=f"Photo {idx + 1}", use_column_width=True)
                    
                    # Option to recapture
                    if st.button("🔄 Recapture Photos", type="secondary"):
                        if confirm_dialog("This will delete existing photos and capture new ones"):
                            # Delete existing photos
                            for i in range(1, 101):
                                photo_path = f"data/user.{student_id}.{i}.jpg"
                                if os.path.exists(photo_path):
                                    os.remove(photo_path)
                            
                            # Update status
                            update_data = {
                                'photo_status': 'No',
                                'updated_at': datetime.now().isoformat()
                            }
                            update_student(supabase, student_id, update_data)
                            
                            show_info_message("Existing photos deleted. You can now capture new photos.", "info")
                            st.rerun()
    else:
        show_info_message("No students found. Please add students first.", "info")