# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 22:01:56 2022

@author: Msi_Pc
"""

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
from time import strftime
from datetime import datetime
from tkinter import filedialog
import cv2
import os
import csv
import numpy as np
from tkinter.messagebox import askyesno


mydata=[]

class list_atten:
    def __init__(main, root):
        main.root = root
        main.root.geometry("1530x790+0+0")
        main.root.title("Face Recognition System")
        
        # ============ varaibles =================
        main.var_atten_id=StringVar()
        main.var_name_atten=StringVar()
        main.var_date=StringVar()
        main.var_dep_atten=StringVar()
        main.var_time=StringVar()
        main.var_atten=StringVar()
        main.var_exportnopresent=StringVar()
        
        # Frist Image
        img = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img = img.resize((800,200), Image.ANTIALIAS)
        main.photoimg = ImageTk.PhotoImage(img)
        f_lbl=Label(main.root,image=main.photoimg)
        f_lbl.place(x = 0, y = 0, width = 800, height = 200)
        
        # Second Image
        img1 = Image.open(r"img\PicsArt_04-07-10.53.25.jpg")
        img1 = img1.resize((800,200), Image.ANTIALIAS)
        main.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl=Label(main.root,image=main.photoimg1)
        f_lbl.place(x = 800, y = 0, width = 800, height = 200)
        
        # BG Image
        img3 = Image.open(r"img\banner-image_196890.jpg")
        img3 = img3.resize((1530,710), Image.ANTIALIAS)
        main.photoimg3 = ImageTk.PhotoImage(img3)
        bg_img=Label(main.root,image=main.photoimg3)
        bg_img.place(x = 0, y = 200, width = 1530, height = 710)
        
        title_lbl = Label(bg_img, text="ATTENDANCE MANAGEMENT SYSTEM", font=("Trebuchet MS", 35, 'bold'),bg="white", fg="red")
        title_lbl.place(x = 0, y = 0, width = 1530, height = 45)
        
        main_frame=Frame(bg_img, bd=2)
        main_frame.place(x=20, y=50, width=1480, height=600)
        
        # Left label frame
        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,text="Student Attendence Details", font=("times new roman", 12, 'bold'))
        Left_frame.place(x=10, y=10, width=730, height=500)
        
        img_left = Image.open(r"img\MMU-New-logo-png.png")
        img_left = img_left.resize((720,130), Image.ANTIALIAS)
        main.photoimg_left = ImageTk.PhotoImage(img_left)
        
        left_inside_frame=Frame(Left_frame, bd=2, relief=RIDGE, bg="white")
        left_inside_frame.place(x=3, y=135, width=720, height=365)
        
        # ================ Labeland entery =============
        # attendance id
        attendanceid_label=Label(left_inside_frame, text="Attendance ID:", font="comicsansns 11 bold", bg="white")
        attendanceid_label.grid(row=0, column=0, pady=5, sticky=E)
        
        attendanceid_entry=ttk.Label(left_inside_frame, width=20, textvariable=main.var_atten_id, font="comicsansns 11 bold")
        attendanceid_entry.grid(row=0, column=1, pady=8)
        
        # name
        namelabel=Label(left_inside_frame, text="Name:", font="comicsansns 11 bold", bg="white")
        namelabel.grid(row=0, column=2, pady=8,sticky=E)
        
        namelabel_entry=ttk.Label(left_inside_frame, width=20, textvariable=main.var_name_atten, font="comicsansns 11 bold")
        namelabel_entry.grid(row=0, column=3, pady=8)
        
         # Department
        deplabel=Label(left_inside_frame, text="Department:", font="comicsansns 11 bold", bg="white")
        deplabel.grid(row=1, column=0,sticky=E)
        
        depentry=ttk.Label(left_inside_frame, width=20, textvariable=main.var_dep_atten, font="comicsansns 11 bold")
        depentry.grid(row=1, column=1, pady=8)

        # time
        time_label=Label(left_inside_frame, text="Time:", font="comicsansns 11 bold", bg="white")
        time_label.grid(row=1, column=2,sticky=E)
        
        time_entry=ttk.Label(left_inside_frame, width=20, textvariable=main.var_time, font="comicsansns 11 bold")
        time_entry.grid(row=1, column=3, pady=8)

        # date
        datelabel=Label(left_inside_frame, text="Date:", font="comicsansns 11 bold", bg="white")
        datelabel.grid(row=2, column=0,sticky=E)
        
        datelabel_entry=ttk.Label(left_inside_frame, width=20, textvariable=main.var_date, font="comicsansns 11 bold")
        datelabel_entry.grid(row=2, column=1, pady=8)

        # attendance
        atten_label=Label(left_inside_frame, text="Attendance Status:", font="comicsansns 11 bold", bg="white")
        atten_label.grid(row=3, column=0,sticky=E)
        
        main.atten_status=ttk.Label(left_inside_frame, width=20, textvariable=main.var_atten, font="comicsansns 11 bold", state="readonly")
        main.atten_status.grid(row=3, column=1, pady=8)
        
        # Radio Button
        radionbtn=ttk.Radiobutton(left_inside_frame, variable=main.var_exportnopresent, text="Export Attended & No Present Student", value="Yes")
        radionbtn.grid(row=4, column=1)
        
        radionbtn2=ttk.Radiobutton(left_inside_frame, variable=main.var_exportnopresent, text="Export Attended Student Only", value="No")
        radionbtn2.grid(row=4, column=0)
        main.var_exportnopresent.set('No')
        # nbutton frame
        btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=100, y=250,width=490, height=35)
        
        save_btn=Button(btn_frame, text="Import CSV",  command=main.imCsv, width=17, font=("times new roman", 12, 'bold'), bg="blue", fg="white")
        save_btn.grid(row=0, column=0)
        
        update_btn=Button(btn_frame, text="Export CSV", command=main.exportCsv, width=17, font=("times new roman", 12, 'bold'), bg="blue", fg="white")
        update_btn.grid(row=0, column=1)

        clear_btn=Button(btn_frame, text="Clear Main CSV File",  command=main.clCsv, width=17, font=("times new roman", 12, 'bold'), bg="blue", fg="white")
        clear_btn.grid(row=0, column=2)
        
        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE,text="Attendence Details", font=("times new roman", 12, 'bold'))
        Right_frame.place(x=750, y=10, width=720, height=580)
        f_lbl=Label(Left_frame,image=main.photoimg_left)
        f_lbl.place(x = 5, y = 0, width = 720, height = 130)
        
        Table_frame = Frame(Right_frame, bd=2, relief=RIDGE)
        Table_frame.place(x=2, y=5, width=708, height=455)
        
        # ============ scroll bar table ==============
        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_Y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        
        main.AttendanceReportTable = ttk.Treeview(Table_frame, column=("id", "name", "major", "time", "date", "status"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_Y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_Y.pack(side=RIGHT, fill=Y)
        
        scroll_x.config(command=main.AttendanceReportTable.xview)
        scroll_Y.config(command=main.AttendanceReportTable.yview)
        
        main.AttendanceReportTable.heading("id", text="Attendance_ID")
        main.AttendanceReportTable.heading("name", text="Name")
        main.AttendanceReportTable.heading("major", text="Major")
        main.AttendanceReportTable.heading("time", text="Time")
        main.AttendanceReportTable.heading("date", text="Date")
        main.AttendanceReportTable.heading("status", text="Attendance_Status")
        main.AttendanceReportTable['show']="headings"
        
        main.AttendanceReportTable.column("id", width=100)
        main.AttendanceReportTable.column("name",width=100)
        main.AttendanceReportTable.column("major",width=100)
        main.AttendanceReportTable.column("date",width=100)
        main.AttendanceReportTable.column("time",width=100)
        main.AttendanceReportTable.column("status",width=100)
        
        main.AttendanceReportTable.pack(fill=BOTH, expand=1)
        
        main.AttendanceReportTable.bind("<ButtonRelease>",main.get_cursor)
        
        main.auto_load_attendance()
    # ====quit or back button=====
        back_img = Image.open(r"img\pngegg.png")
        back_img = back_img.resize((50,50), Image.ANTIALIAS)
        main.back_logo = ImageTk.PhotoImage(back_img)
            
        quit_btn=Button(main.root, command=main.quit_button, image=main.back_logo, cursor="hand2")
        quit_btn.place(x=5,y=5)
    
    def quit_button(main):
        main.root.destroy()


    # auto import attendance.csv & fetch data to table
    def auto_load_attendance(main):
        global mydata
        mydata.clear()
        try:
            with open("attendance.csv", "r") as myfile:
                csvread=csv.reader(myfile,delimiter=",")
                next(csvread)
                for i in csvread:
                    mydata.append(i)
                main.fetchData(mydata)
        except Exception as es:
            messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)


    # auto load no attend student from database
    def auto_load_no_attented(main):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])

            conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
            my_cursor=conn.cursor()
            my_cursor.execute("select dep,name,Stu_id from student")
            for row in my_cursor: 
                i=row[2]
                n=row[1]
                d=row[0]

                if i not in name_list:
                    mydata.append([i,n,d,'N/A','N/A','Not present'])
            f.close()


    # ========== fetch data ============
        
    def fetchData(main,rows):
        main.AttendanceReportTable.delete(*main.AttendanceReportTable.get_children())
        main.auto_load_no_attented()
        for i in rows:
            main.AttendanceReportTable.insert("",END,values=i)
    
    # fetch data but only shows user imported data
    def fetchData_imported(main,rows):
        main.AttendanceReportTable.delete(*main.AttendanceReportTable.get_children())
        for i in rows:
            main.AttendanceReportTable.insert("",END,values=i)
    
    # ========== import csv ============   
    def imCsv(main):
        try:
            fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV", filetypes=(("CSV File", "*csv"),("ALL File", "*.*")),parent=main.root)
            with open(fln) as myfile:
                mydata.clear()
                csvread=csv.reader(myfile,delimiter=",")
                next(csvread)
                for i in csvread:
                    mydata.append(i)

                if os.path.basename(fln)!='attendance.csv':
                    main.fetchData_imported(mydata)
                elif os.path.basename(fln)=='attendance.csv':
                    main.fetchData(mydata)
        except Exception as es:
            messagebox.showerror("Error","No file selected.\nNo data imported.", parent=main.root)
            return None

            
    # ============== export csv =============
    def exportCsv(main):
        try:
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV", filetypes=(("CSV File", "*.csv"),("ALL File", "*.*")),defaultextension=".csv",parent=main.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile, delimiter=",")
                exp_write.writerow(['Student ID', 'Name', 'Faculty', 'Time', 'Date', 'Status'])
                for i in mydata:
                    if main.var_exportnopresent.get()=='No': # No = only export attended
                        if "N/A" in i:
                            continue # if data contain N/A, skip to next loop
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export", "Your data exported to "+os.path.basename(fln)+" successfully",parent=main.root)
                myfile.close()
        except Exception as es:
            messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)

    # ================ Clear CSV file ============
    def clCsv(main):
        try:
            if len(mydata)<1:
                    messagebox.showerror("No data", "No Data found to be clear", parent=main.root)
                    return False
            else:
                if messagebox.askyesno(title='Confirnmation of clearing attendance.csv', message='Are you sure that you want to clear the data? \n(This action cannot be revert)',parent=main.root):
                    with open("attendance.csv", "w") as f:
                        f.writelines(f"Student ID, Name, Faculty, Time, Date, Status")
                        f.close()
                    messagebox.showinfo(title="Clear Done", message="The data is successfully cleared!",parent=main.root)
                    if messagebox.askyesno(title='Back to Main Panel', message='Do you want to back to the Main Panel? \n(This will close the current window)',parent=main.root):
                        main.root.destroy()
                        return None
                    main.auto_load_attendance()
        except Exception as es:
            messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
    #================      
    def get_cursor(main,event=""):
        cursor_row=main.AttendanceReportTable.focus()
        content=main.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        main.var_atten_id.set(rows[0])
        main.var_name_atten.set(rows[1])
        main.var_dep_atten.set(rows[2])
        main.var_time.set(rows[3])
        main.var_date.set(rows[4])
        main.var_atten.set(rows[5])
        

if __name__ == "__main__":
    root = Tk()
    obj = list_atten(root)
    root.mainloop()