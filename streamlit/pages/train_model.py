# pages/train_model.py - Train Model page
import streamlit as st
import cv2
import numpy as np
import os
import json
import pandas as pd
from PIL import Image
from utils.database import get_all_students
from utils.ui_components import show_info_message, create_metric_card

def render_page(supabase):
    """Render the train model page"""
    st.markdown("## Train Face Recognition Model")
    
    # Check prerequisites
    col1, col2, col3 = st.columns(3)
    
    # Check for photos
    photo_count = 0
    student_photo_count = {}
    
    if os.path.exists('data'):
        for file in os.listdir('data'):
            if file.endswith('.jpg'):
                photo_count += 1
                student_id = file.split('.')[1]
                if student_id not in student_photo_count:
                    student_photo_count[student_id] = 0
                student_photo_count[student_id] += 1
    
    with col1:
        st.metric("Total Photos", photo_count, help="Total face images in dataset")
    
    with col2:
        st.metric("Students with Photos", len(student_photo_count), help="Number of students with captured photos")
    
    with col3:
        model_exists = os.path.exists('classifier.xml')
        st.metric("Model Status", "✅ Trained" if model_exists else "❌ Not Trained", 
                 help="Current model training status")
    
    # Training prerequisites check
    st.markdown("### Training Prerequisites")
    
    prerequisites_met = True
    
    # Check 1: Photos exist
    if photo_count == 0:
        show_info_message("❌ No photos found. Please capture student photos first.", "error")
        prerequisites_met = False
    else:
        show_info_message(f"✅ Found {photo_count} photos from {len(student_photo_count)} students", "success")
    
    # Check 2: Haar Cascade file exists
    if not os.path.exists('haarcascade_frontalface_default.xml'):
        show_info_message("❌ Haar Cascade file not found. Please download it first.", "error")
        prerequisites_met = False
        st.code("wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml")
    else:
        show_info_message("✅ Face detection classifier found", "success")
    
    # Check 3: Database connection
    if supabase:
        students_df = get_all_students(supabase)
        if students_df.empty:
            show_info_message("⚠️ No students in database. Training will proceed but mapping might fail.", "warning")
        else:
            show_info_message(f"✅ Database connected with {len(students_df)} students", "success")
    else:
        show_info_message("❌ Database not connected", "error")
        prerequisites_met = False
    
    if prerequisites_met:
        st.markdown("---")
        st.markdown("### Training Options")
        
        # Training parameters
        col1, col2 = st.columns(2)
        with col1:
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=40,
                max_value=80,
                value=50,
                help="Lower values = stricter matching"
            )
        
        with col2:
            training_algorithm = st.selectbox(
                "Training Algorithm",
                ["LBPH (Recommended)", "Eigenfaces", "Fisherfaces"],
                help="LBPH works well with variations in lighting"
            )
        
        # Display training data statistics
        if student_photo_count:
            st.markdown("### Training Data Overview")
            
            # Create a dataframe for visualization
            import pandas as pd
            
            photo_stats = []
            for student_id, count in student_photo_count.items():
                # Get student name if connected to database
                student_name = "Unknown"
                if supabase and not students_df.empty:
                    student_record = students_df[students_df['student_id'] == student_id]
                    if not student_record.empty:
                        student_name = student_record.iloc[0]['name']
                
                photo_stats.append({
                    'Student ID': student_id,
                    'Name': student_name,
                    'Photo Count': count,
                    'Status': '✅ Ready' if count >= 50 else '⚠️ Low Photos'
                })
            
            photo_stats_df = pd.DataFrame(photo_stats)
            st.dataframe(photo_stats_df, use_container_width=True, hide_index=True)
            
            # Warning for students with low photos
            low_photo_students = photo_stats_df[photo_stats_df['Photo Count'] < 50]
            if not low_photo_students.empty:
                show_info_message(
                    f"⚠️ {len(low_photo_students)} students have less than 50 photos. This may affect recognition accuracy.",
                    "warning"
                )
        
        # Train button
        st.markdown("---")
        if st.button("🎯 Start Training", type="primary", use_container_width=True):
            train_model(supabase, students_df if 'students_df' in locals() else None, training_algorithm)
        
        # Model management
        if model_exists:
            st.markdown("### Model Management")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Get model size
                model_size = os.path.getsize('classifier.xml') / (1024 * 1024)  # MB
                st.metric("Model Size", f"{model_size:.2f} MB")
            
            with col2:
                # Get model info from mapping file
                if os.path.exists('student_mapping.json'):
                    with open('student_mapping.json', 'r') as f:
                        mapping = json.load(f)
                    st.metric("Trained Students", len(mapping))
            
            with col3:
                if st.button("🗑️ Delete Model", type="secondary"):
                    if st.checkbox("Confirm deletion of trained model"):
                        try:
                            os.remove('classifier.xml')
                            if os.path.exists('student_mapping.json'):
                                os.remove('student_mapping.json')
                            show_info_message("Model deleted successfully", "success")
                            st.rerun()
                        except Exception as e:
                            show_info_message(f"Error deleting model: {str(e)}", "error")
    
    else:
        # Show steps to fix prerequisites
        st.markdown("### 📋 Steps to Enable Training")
        st.markdown("""
        1. **Add Students**: Go to Student Management and add at least one student
        2. **Capture Photos**: Capture photos for each student (100 photos per student)
        3. **Download Haar Cascade**: Run the command shown above to download the face detector
        4. **Configure Database**: Ensure Supabase is properly configured in Setup
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Student Management", use_container_width=True):
                st.session_state.page = 'Student Management'
                st.rerun()
        with col2:
            if st.button("Go to Setup", use_container_width=True):
                st.session_state.page = 'Setup'
                st.rerun()

def train_model(supabase, students_df, algorithm="LBPH"):
    """Train the face recognition model"""
    with st.spinner("🔄 Training in progress... This may take a few minutes."):
        try:
            faces = []
            ids = []
            student_mapping = {}
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Get all image files
            image_files = [f for f in os.listdir('data') if f.endswith('.jpg')]
            total_images = len(image_files)
            
            if total_images == 0:
                show_info_message("No images found for training!", "error")
                return
            
            # Process each image
            for idx, image_file in enumerate(image_files):
                img_path = os.path.join('data', image_file)
                
                try:
                    # Load and convert image
                    img = Image.open(img_path).convert('L')
                    img_np = np.array(img, 'uint8')
                    
                    # Extract student_id from filename
                    student_id = image_file.split('.')[1]
                    
                    # Find or create numeric ID for this student
                    if student_id not in student_mapping:
                        numeric_id = len(student_mapping)
                        student_mapping[str(numeric_id)] = student_id
                    else:
                        # Find existing numeric ID
                        numeric_id = None
                        for num_id, stu_id in student_mapping.items():
                            if stu_id == student_id:
                                numeric_id = int(num_id)
                                break
                    
                    if numeric_id is not None:
                        faces.append(img_np)
                        ids.append(numeric_id)
                    
                    # Update progress
                    progress = (idx + 1) / total_images
                    progress_bar.progress(progress)
                    status_text.text(f"Processing image {idx + 1}/{total_images}")
                    
                except Exception as e:
                    st.warning(f"Failed to process {image_file}: {str(e)}")
                    continue
            
            if len(faces) > 0:
                status_text.text("Training the model...")
                
                # Create recognizer based on selected algorithm
                if algorithm == "LBPH (Recommended)":
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                elif algorithm == "Eigenfaces":
                    recognizer = cv2.face.EigenFaceRecognizer_create()
                else:  # Fisherfaces
                    recognizer = cv2.face.FisherFaceRecognizer_create()
                
                # Train the recognizer
                recognizer.train(faces, np.array(ids))
                
                # Save the model
                recognizer.write('classifier.xml')
                
                # Save student mapping
                with open('student_mapping.json', 'w') as f:
                    json.dump(student_mapping, f, indent=2)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Show success message
                st.balloons()
                show_info_message(
                    f"✅ Training completed successfully! Trained with {len(faces)} images from {len(student_mapping)} students.",
                    "success"
                )
                
                # Display training summary
                st.markdown("### Training Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Images", len(faces))
                with col2:
                    st.metric("Unique Students", len(student_mapping))
                with col3:
                    st.metric("Avg Images/Student", f"{len(faces) / len(student_mapping):.0f}")
                
                # Show trained students
                st.markdown("### Trained Students")
                trained_students = []
                
                for numeric_id, student_id in student_mapping.items():
                    student_name = "Unknown"
                    department = "Unknown"
                    
                    if students_df is not None and not students_df.empty:
                        student_record = students_df[students_df['student_id'] == student_id]
                        if not student_record.empty:
                            student_name = student_record.iloc[0]['name']
                            department = student_record.iloc[0]['department']
                    
                    trained_students.append({
                        'ID': numeric_id,
                        'Student ID': student_id,
                        'Name': student_name,
                        'Department': department
                    })
                
                trained_df = pd.DataFrame(trained_students)
                st.dataframe(trained_df, use_container_width=True, hide_index=True)
                
                st.success("Model is ready for face recognition!")
                
            else:
                show_info_message("No valid face data found for training!", "error")
                
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            show_info_message(
                "Please check that all images are valid and try again.",
                "error"
            )