# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 17:48:05 2022

@author: Msi_Pc
"""

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
import cv2
import os


class student:
    def __init__(main, root):
        main.root = root
        main.root.geometry("1530x790+0+0")
        main.root.title("Face Recognition System")
        
        #======vatiable=======
        main.var_dep=StringVar()
        main.var_course=StringVar()
        main.var_year=StringVar()
        main.var_semester=StringVar()
        main.va_id=StringVar()
        main.var_name=StringVar()
        main.var_teacher=StringVar()
        main.var_gender=StringVar()
        main.var_email=StringVar()
        main.var_photo=StringVar()
        main.var_Stu_id=StringVar()
       
        
        # Frist Image
        img = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img = img.resize((500,130), Image.ANTIALIAS)
        main.photoimg = ImageTk.PhotoImage(img)
        f_lbl=Label(main.root,image=main.photoimg)
        f_lbl.place(x = 0, y = 0, width = 500, height = 130)
        
        # Second Image
        img1 = Image.open(r"img\PicsArt_04-07-10.53.25.jpg")
        img1 = img1.resize((500,130), Image.ANTIALIAS)
        main.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl=Label(main.root,image=main.photoimg1)
        f_lbl.place(x = 500, y = 0, width = 550, height = 130)
        
        # third Image
        img2 = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img2 = img2.resize((500,130), Image.ANTIALIAS)
        main.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl=Label(main.root,image=main.photoimg2)
        f_lbl.place(x = 1000, y = 0, width = 550, height = 130)
        
        # BG Image
        img3 = Image.open(r"img\banner-image_196890.jpg")
        img3 = img3.resize((1530,710), Image.ANTIALIAS)
        main.photoimg3 = ImageTk.PhotoImage(img3)
        bg_img=Label(main.root,image=main.photoimg3)
        bg_img.place(x = 0, y = 130, width = 1530, height = 710)
        
        title_lbl = Label(bg_img, text="STUDENT MANAGEMENT SYSTEM", font=("Trebuchet MS", 35, 'bold'),bg="white", fg="red")
        title_lbl.place(x = 0, y = 0, width = 1530, height = 45)
        
        main_frame=Frame(bg_img, bd=2)
        main_frame.place(x=20, y=50, width=1480, height=600)
        
        # Left label frame
        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,text="Student Details", font=("times new roman", 12, 'bold'))
        Left_frame.place(x=10, y=10, width=730, height=580)
        
        img_left = Image.open(r"img\MMU-New-logo-png.png")
        img_left = img_left.resize((720,130), Image.ANTIALIAS)
        main.photoimg_left = ImageTk.PhotoImage(img_left)
        f_lbl=Label(Left_frame,image=main.photoimg_left)
        f_lbl.place(x = 5, y = 0, width = 720, height = 130)
        
        # Current course information
        current_course_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE,text="Current course information", font=("times new roman", 12, 'bold'))
        current_course_frame.place(x=5, y=135, width=720, height=150)
        
        # Department
        dep_label=Label(current_course_frame, text="Department", font=("times new roman", 12, 'bold'))
        dep_label.grid(row=0, column=0, padx=10, sticky=W)
        
        dep_combo=ttk.Combobox(current_course_frame, textvariable=main.var_dep, font=("times new roman", 12, 'bold'), state="readonly")
        dep_combo["values"]=("Select Department", "FCI", 'FIST','FOB','FOM','FOE','FET','FCM','FCL')
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        # Course
        course_label=Label(current_course_frame, text="Course", font=("times new roman", 12, 'bold'))
        course_label.grid(row=0, column=2, padx=10, sticky=W)
        
        course_combo=ttk.Combobox(current_course_frame, textvariable=main.var_course, font=("times new roman", 12, 'bold'), state="readonly")
        course_combo["values"]=("Select Course", "TSE", 'TML')
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)
        
        # Year
        year_label=Label(current_course_frame, text="Year", font=("times new roman", 12, 'bold'))
        year_label.grid(row=1, column=0, padx=10, sticky=W)
        
        year_combo=ttk.Combobox(current_course_frame, textvariable=main.var_year, font=("times new roman", 12, 'bold'), state="readonly")
        year_combo["values"]=("Select Year", "2020-21", '2021-22')
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        
        # Semester
        semester_label=Label(current_course_frame, text="Semester", font=("times new roman", 12, 'bold'))
        semester_label.grid(row=1, column=2, padx=10, sticky=W)
        
        semester_combo=ttk.Combobox(current_course_frame, textvariable=main.var_semester, font=("times new roman", 12, 'bold'), state="readonly")
        semester_combo["values"]=("Select Semester", "Semester-1", "Semester-2", 'Semester-3')
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        
        # Class student information
        class_student_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE,text="Class Student Information", font=("times new roman", 12, 'bold'))
        class_student_frame.place(x=5, y=290, width=720, height=260)
        
        # Student Name
        Studentname_label=Label(class_student_frame, text="Student Name:", font=("times new roman", 12, 'bold'))
        Studentname_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        
        Studentname_entry=ttk.Entry(class_student_frame, textvariable=main.var_name, width=20, font=("times new roman", 12, 'bold'))
        Studentname_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        
        # Techer name
        techername_label=Label(class_student_frame, text="Techer Name:", font=("times new roman", 12, 'bold'))
        techername_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        
        techername_entry=ttk.Entry(class_student_frame, textvariable=main.var_teacher, width=20, font=("times new roman", 12, 'bold'))
        techername_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        # Gender
        Gender_label=Label(class_student_frame, text="Gender:", font=("times new roman", 12, 'bold'))
        Gender_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        
        Gender_combo=ttk.Combobox(class_student_frame, textvariable=main.var_gender, width=20, font=("times new roman", 12, 'bold'), state="readonly")
        Gender_combo["values"]=("Select gender", "Male", 'Female', "Other")
        Gender_combo.current(0)
        Gender_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)
        
        # Email
        emali_label=Label(class_student_frame, text="Email:", font=("times new roman", 12, 'bold'))
        emali_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        
        emali_entry=ttk.Entry(class_student_frame, textvariable=main.var_email, width=20, font=("times new roman", 12, 'bold'))
        emali_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        
        # Roll ID
        #Rollid_label=Label(class_student_frame, text="Roll ID:", font=("times new roman", 12, 'bold'))
        #Rollid_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        #Rollid_entry=ttk.Entry(class_student_frame, textvariable=main.va_id, width=20, font=("times new roman", 12, 'bold'))
        #Rollid_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student_ID
        Student_ID_label=Label(class_student_frame, text="Student ID:", font=("times new roman", 12, 'bold'))
        Student_ID_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        Student_ID_entry=ttk.Entry(class_student_frame, textvariable=main.var_Stu_id, width=20, font=("times new roman", 12, 'bold'))
        Student_ID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        main.va_id = main.var_Stu_id
        
        # Radio Button
        radionbtn=ttk.Radiobutton(class_student_frame, variable=main.var_photo, text="Photos Sample Have Been Taken", value="Yes")
        radionbtn.grid(row=6, column=0)
        
        radionbtn2=ttk.Radiobutton(class_student_frame, variable=main.var_photo, text="Photo Sample Not Yet Taken", value="No")
        radionbtn2.grid(row=6, column=1)
    
        # button frame
        btn_frame = Frame(class_student_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=30, y=160, width=650, height=35)
        
        save_btn=Button(btn_frame, text="Save", command=main.add_data, width=17, font=("times new roman", 12, 'bold'), bg="blue", fg="white")
        save_btn.grid(row=0, column=0)
        
        update_btn=Button(btn_frame, text="Update", command=main.update_data, width=17, font=("times new roman", 12, 'bold'), bg="blue", fg="white")
        update_btn.grid(row=0, column=1)
        
        delete_btn=Button(btn_frame, text="Delete", command=main.delete_data, width=17, font=("times new roman", 12, 'bold'), bg="red", fg="white")
        delete_btn.grid(row=0, column=2)
        
        reset_btn=Button(btn_frame, text="Reset", command=main.reset_data, width=17, font=("times new roman", 12, 'bold'), bg="#e08f31", fg="white")
        reset_btn.grid(row=0, column=3)
        
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE)
        btn_frame1.place(x=180, y=200, height=35)
        
        take_Photo_btn=Button(btn_frame1, command=main.generate_dataset, text="Take Photo Sample", width=35, font=("impact", 12), bg="green",fg="white")
        take_Photo_btn.grid(row=1, column=0)
        
        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,text="Student Details", font=("times new roman", 12, 'bold'))
        Right_frame.place(x=750, y=10, width=720, height=580)
        
        img_rigth = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img_rigth = img_rigth.resize((720,130), Image.ANTIALIAS)
        main.photoimg_rigth = ImageTk.PhotoImage(img_rigth)
        f_lbl=Label(Right_frame,image=main.photoimg_rigth)
        f_lbl.place(x = 5, y = 0, width = 720, height = 130)
        
        
        
        # ======= Table =========
        Table_frame = Frame(Right_frame, bd=2, relief=RIDGE)
        Table_frame.place(x=5, y=210, width=710, height=345)
        
        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_Y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        
        main.student_table = ttk.Treeview(Table_frame, column=("dep", "course", "year", "semester", "id", "name", "teacher", "gender", "email", "photo", "Stu_id"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_Y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_Y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=main.student_table.xview)
        scroll_Y.config(command=main.student_table.yview)
       
        
        main.student_table.heading("dep", text="Department")
        main.student_table.heading("course", text="Course")
        main.student_table.heading("year", text="Year")
        main.student_table.heading("semester", text="Semester")
        main.student_table.heading("id", text="Roll ID")
        main.student_table.heading("name", text="Name")
        main.student_table.heading("teacher", text="Teacher")
        main.student_table.heading("gender", text="Gender")
        main.student_table.heading("email", text="Email")
        main.student_table.heading("photo", text="PhaotoSampleStatus")
        main.student_table.heading("Stu_id", text="Student ID")
        main.student_table['show']="headings"
        
        main.student_table.column("dep", width=150)
        main.student_table.column("course",width=150)
        main.student_table.column("year",width=150)
        main.student_table.column("semester",width=150)
        main.student_table.column("id",width=150)
        main.student_table.column("name",width=150)
        main.student_table.column("teacher",width=150)
        main.student_table.column("gender",width=150)
        main.student_table.column("email",width=150)
        main.student_table.column("photo",width=150)
        main.student_table.column("Stu_id",width=150)
        
        
        
        main.student_table.pack(fill=BOTH, expand=1)
        main.student_table.bind("<ButtonRelease>", main.get_cursor)
        main.fetch_data()
    # ====quit or back button=====
        back_img = Image.open(r"img\pngegg.png")
        back_img = back_img.resize((50,50), Image.ANTIALIAS)
        main.back_logo = ImageTk.PhotoImage(back_img)
            
        quit_btn=Button(main.root, command=main.quit_button, image=main.back_logo, cursor="hand2")
        quit_btn.place(x=5,y=5)
    
    def quit_button(main):
        main.root.destroy()    
    # ====== function decration =========
    def add_data(main):
        if main.var_dep.get()=="Select Department" or main.var_course.get()=="Select Course" or main.var_year.get()=="Select Year" or main.var_semester.get()=="Select Semester" or main.va_id.get()=="" or main.var_name.get()=="" or main.var_teacher.get()=="" or main.var_gender.get()=="Select gender" or main.var_email.get()=="" or main.var_photo.get()=="" or main.var_Stu_id.get()=="":
            messagebox.showerror("Error", "All Fields are required", parent=main.root)
            return None
        elif main.var_photo.get()=="Yes":
            messagebox.showerror("Reselect the Answer", "For new student, please select the selection “Photo Sample Not Yet Taken”.", parent=main.root)
            return None
        else:
            try:
                conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(main.var_dep.get(),
                                                                         main.var_course.get(),
                                                                         main.var_year.get(),
                                                                         main.var_semester.get(),
                                                                         main.va_id.get(),
                                                                         main.var_name.get(),
                                                                         main.var_teacher.get(),
                                                                         main.var_gender.get(),
                                                                         main.var_email.get(),
                                                                         main.var_photo.get(),
                                                                         main.var_Stu_id.get()))
                conn.commit()
                main.fetch_data()
                conn.close()
                messagebox.showinfo('Success', "Student detail has been added Successfully",  parent=main.root)
                messagebox.showinfo('Take Photo', "Please Press 'Take Photo Sample' to register the face.",  parent=main.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)   
                         
    #==========fetch data===========
    def fetch_data(main):
        conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student")
        data=my_cursor.fetchall()
        
        if len(data)!=0:
            main.student_table.delete(*main.student_table.get_children())
            for i in data:
                main.student_table.insert("", END, values=i)
        else:
            main.student_table.delete(*main.student_table.get_children())
        conn.commit()
        conn.close()
        
    # =============== get cursor ==================
    def get_cursor(main, event=""):
        cursor_focus=main.student_table.focus()
        content=main.student_table.item(cursor_focus)
        data=content["values"]
        
        main.var_dep.set(data[0]),
        main.var_course.set(data[1]),
        main.var_year.set(data[2]),
        main.var_semester.set(data[3]),
        main.va_id.set(data[4]),
        main.var_name.set(data[5]),
        main.var_teacher.set(data[6]),
        main.var_gender.set(data[7]),
        main.var_email.set(data[8]),
        main.var_photo.set(data[9]),
        main.var_Stu_id.set(data[10])
        
    # ============== updata fuction ==============
    def update_data(main):
        myfile="data/user."+main.va_id.get()+".1.jpg"

        conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student where id=%s",main.va_id.get())
        data=my_cursor.fetchall()
        
        
        if main.var_dep.get()=="Select Department" or main.var_course.get()=="Select Course" or main.var_year.get()=="Select Year" or main.var_semester.get()=="Select Semester" or main.va_id.get()=="" or main.var_name.get()=="" or main.var_teacher.get()=="" or main.var_gender.get()=="Select gender" or main.var_email.get()=="" or main.var_photo.get()=="" or main.var_Stu_id.get()=="":
            messagebox.showerror("Error", "All Fields are required", parent=main.root)
            return None
        if len(data)==0:
            messagebox.showerror("New User", "For newly register student, please press 'Save' button before execute other action.", parent=main.root)
            return None
        elif os.path.isfile(myfile) and main.var_photo.get()=="No": ## If file exists, show error
            messagebox.showerror("Sample Photo is Taken", "Please select the selection 'Photos Sample Have Been Taken' \nSample Photo for this student found.", parent=main.root)
            return None
        elif os.path.isfile(myfile)==False and main.var_photo.get()=="Yes": ## If photo no take and user want update to photo taken, show error
            messagebox.showerror("Sample Photo Not Taken", "Please select the selection 'Photos Sample Not Yet Taken' \nSample Photo for this student haven't taken.", parent=main.root)
            return None
        else:
            try:
                Upadate=messagebox.askyesno("Upadte", "Do you want to update this student details", parent=main.root)
                if Upadate>0:
                    my_cursor=conn.cursor()
                    my_cursor.execute("update student set dep=%s, course=%s, year=%s, semester=%s, name=%s, teacher=%s, gender=%s, email=%s, photo=%s, Stu_id=%s where id=%s",(main.var_dep.get(),
                                                                                                                                                      main.var_course.get(),
                                                                                                                                                      main.var_year.get(),
                                                                                                                                                      main.var_semester.get(),
                                                                                                                                                      main.var_name.get(),
                                                                                                                                                      main.var_teacher.get(),
                                                                                                                                                      main.var_gender.get(),
                                                                                                                                                      main.var_email.get(),
                                                                                                                                                      main.var_photo.get(),
                                                                                                                                                      main.var_Stu_id.get(),
                                                                                                                                                      main.va_id.get()))
                else:
                    if not Upadate:
                        return
                messagebox.showinfo("Success", "Student details successfully update completed", parent=main.root)
                conn.commit()
                main.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
    
    # =============== delete function ============
    def delete_data(main):
        conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student where id=%s",main.va_id.get())
        data=my_cursor.fetchall()
        
        if len(data)==0: #validate if user is registered or not
            messagebox.showerror("New User", "For newly register student, please press 'Save' button before execute other action.", parent=main.root)
            return None
        elif main.va_id.get()=="":
            messagebox.showerror("Error", "Student id must be required", parent=main.root)
            return None
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page", "Do you want to delete this student", parent=main.root)
                if delete>0:
                    my_cursor=conn.cursor()
                    sql="delete from student where id=%s"
                    val=(main.va_id.get())
                    main.delete_user_photo(val)
                    my_cursor.execute(sql,val)
                else:
                    return None
                    
                conn.commit()
                conn.close()
                messagebox.showinfo("Delete", "Successfully removed the details of the selected student.", parent=main.root)
                main.fetch_data()
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
    
    def delete_user_photo(main,id):
        for i in range(1,101):
            myfile="data/user."+str(id)+"."+str(i)+".jpg"

            ## If file exists, delete it ##
            if os.path.isfile(myfile):
                os.remove(myfile)
            else:    ## Show an error ##
                messagebox.showinfo("Info","No sample photo taken.\nNo file has been deleted.", parent=main.root)
                break
   
    # ============= reset ==============
    def reset_data(main):
        main.var_dep.set("Select Department")
        main.var_course.set("Select Course")
        main.var_year.set("Select Year")
        main.var_semester.set("Select Semester")
        main.va_id.set("")
        main.var_name.set("")
        main.var_teacher.set("")
        main.var_gender.set("Select Gender")
        main.var_email.set("")
        main.var_photo.set("")
        main.var_Stu_id.set("")
        
    #========= Generate data set or take photo smaples ==============
    def generate_dataset(main):
        conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student where id=%s",main.va_id.get())
        data=my_cursor.fetchall()
        
        
        if main.var_dep.get()=="Select Department" or main.var_course.get()=="Select Course" or main.var_year.get()=="Select Year" or main.var_semester.get()=="Select Semester" or main.va_id.get()=="" or main.var_name.get()=="" or main.var_teacher.get()=="" or main.var_gender.get()=="Select gender" or main.var_email.get()=="" or main.var_photo.get()=="" or main.var_Stu_id.get()=="":
            messagebox.showerror("Error", "All Fields are required", parent=main.root)
            return None
        elif len(data)==0: #validate if user is registered or not
            messagebox.showerror("New User", "For newly register student, please press 'Save' button before execute other action.", parent=main.root)
            return None
        elif main.var_photo.get()=="Yes":
            messagebox.showerror("Repeated", "Photo Sample for this student have been taken", parent=main.root)
            return None
        else:
            try:
                my_cursor=conn.cursor()
                primary_key=main.va_id.get()
                my_cursor.execute("update student set photo='Yes' where id=%s",(main.va_id.get()))
                conn.commit()
                main.fetch_data()
                main.reset_data()
                conn.close()
                
                # ============== Load predifiend data on face frontals from opencv ================
                
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                def face_cropped(img):
                    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray, 1.3, 5)
                    #Scaling factor=1.3
                    #Minimum Neighbor=5
                    
                    for (x,y,w,h) in faces:
                        face_cropped=img[y:y+h, x:x+w]
                        return face_cropped
                    
                cap=cv2.VideoCapture(0)

                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame), (450, 450))
                        face=cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path="data/user."+primary_key+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                        cv2.imshow("Crooped Face", face)
                    
                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                
                messagebox.showinfo("Result", "Generating data set compled!!!",parent=main.root)
            except Exception as es:
                 messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
                
if __name__ == "__main__":
    root = Tk()
    obj = student(root)
    root.mainloop()