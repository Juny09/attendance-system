# utils/face_capture.py - Face capture utilities
import cv2
import streamlit as st
import os
import time

def capture_student_photos(student_id: str, student_name: str) -> bool:
    """Capture photos for a student"""
    try:
        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        if face_classifier.empty():
            st.error("Face classifier not found. Please ensure haarcascade_frontalface_default.xml is in the project directory.")
            return False
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("Cannot access camera. Please check camera permissions.")
            return False
        
        img_counter = 0
        
        # Create placeholders
        progress_bar = st.progress(0)
        status_text = st.empty()
        photo_placeholder = st.empty()
        instruction_text = st.empty()
        
        instruction_text.info("🎯 Position your face in the camera view. Photos will be captured automatically.")
        
        # Capture loop
        start_time = time.time()
        no_face_counter = 0
        
        while img_counter < 100:
            ret, frame = cap.read()
            
            if not ret:
                st.error("Failed to grab frame from camera.")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                no_face_counter = 0
                for (x, y, w, h) in faces:
                    img_counter += 1
                    
                    # Extract face
                    face_img = frame[y:y+h, x:x+w]
                    face_img = cv2.resize(face_img, (450, 450))
                    
                    # Save image
                    file_path = f"data/user.{student_id}.{img_counter}.jpg"
                    cv2.imwrite(file_path, face_img)
                    
                    # Update progress
                    progress = img_counter / 100
                    progress_bar.progress(progress)
                    status_text.text(f"📸 Captured {img_counter}/100 photos for {student_name}")
                    
                    # Show the captured face with rectangle
                    display_frame = frame.copy()
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(display_frame, f"Photo {img_counter}", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    # Convert to RGB for display
                    display_frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                    photo_placeholder.image(display_frame_rgb, channels="RGB", use_column_width=True)
                    
                    if img_counter >= 100:
                        break
                    
                    # Small delay to get variety in photos
                    time.sleep(0.1)
            else:
                no_face_counter += 1
                # Show frame without rectangle when no face detected
                display_frame = frame.copy()
                cv2.putText(display_frame, "No face detected", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                display_frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                photo_placeholder.image(display_frame_rgb, channels="RGB", use_column_width=True)
                
                # Timeout if no face detected for too long
                if no_face_counter > 100:  # About 10 seconds
                    st.warning("No face detected for extended period. Please adjust your position.")
                    no_face_counter = 0
            
            # Overall timeout
            if time.time() - start_time > 120:  # 2 minutes timeout
                st.error("Photo capture timeout. Please try again.")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Clear placeholders
        progress_bar.empty()
        status_text.empty()
        photo_placeholder.empty()
        instruction_text.empty()
        
        if img_counter >= 100:
            return True
        else:
            st.error(f"Only captured {img_counter} photos. Please try again.")
            # Clean up partial photos
            for i in range(1, img_counter + 1):
                photo_path = f"data/user.{student_id}.{i}.jpg"
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            return False
            
    except Exception as e:
        st.error(f"Error during photo capture: {str(e)}")
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        return False

def verify_photos_exist(student_id: str) -> tuple:
    """Verify if photos exist for a student"""
    photo_count = 0
    missing_photos = []
    
    for i in range(1, 101):
        photo_path = f"data/user.{student_id}.{i}.jpg"
        if os.path.exists(photo_path):
            photo_count += 1
        else:
            missing_photos.append(i)
    
    return photo_count, missing_photos

def delete_student_photos(student_id: str) -> int:
    """Delete all photos for a student"""
    deleted_count = 0
    
    for i in range(1, 101):
        photo_path = f"data/user.{student_id}.{i}.jpg"
        if os.path.exists(photo_path):
            try:
                os.remove(photo_path)
                deleted_count += 1
            except Exception as e:
                st.error(f"Error deleting photo {i}: {str(e)}")
    
    return deleted_count