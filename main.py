# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 16:12:57 2022

@author: Msi_Pc
"""

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import strftime
from datetime import datetime
import tkinter
from student import student
from train import Train
from face_recognition import face_recognition
from list import list_atten
import os

class Face_Recognition_System:
    def __init__(main, root):
        main.root = root
        main.root.geometry("1530x790+0+0")
        main.root.title("Face Recognition System")
        
        # Frist Image
        img = Image.open(r"img\Contactless-Attendance-System_banner.png")
        img = img.resize((500,230), Image.ANTIALIAS)
        main.photoimg = ImageTk.PhotoImage(img)
        f_lbl=Label(main.root,image=main.photoimg)
        f_lbl.place(x = 0, y = 0, width = 500, height = 130)
        
        # Second Image
        img1 = Image.open(r"img\MMU-New-logo-png.png")
        img1 = img1.resize((500,130), Image.ANTIALIAS)
        main.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl=Label(main.root,image=main.photoimg1)
        f_lbl.place(x = 500, y = 0, width = 550, height = 130)
        
        # third Image
        img2 = Image.open(r"img\mmu-01.jpg")
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
        title_lbl = Label(bg_img, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Trebuchet MS", 35, 'bold'),bg="#e6e6e6", fg="red")
        title_lbl.place(x = 0, y = 0, width = 1530, height = 45)
        
        # ======= time ========
        def time():
            string=strftime("%H:%M:%S %p")
            lbl.config(text=string)
            lbl.after(1000,time)
            
        lbl=Label(title_lbl,font=("times new roman", 14, 'bold'),background='#c7c8ff',foreground='blue')
        lbl.place(x=0,y=0,width=110,height=50)
        time()
        
        # Student Button (Student Detail)
        img4 = Image.open(r"img\rr.png")
        img4 = img4.resize((220,220), Image.ANTIALIAS)
        main.photoimg4 = ImageTk.PhotoImage(img4)
        
        b1 = Button(bg_img, image=main.photoimg4, cursor="hand2", command=main.student_details)
        b1.place(x=320, y=100, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Student Details", command=main.student_details, cursor="hand2", font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=320, y=300, width=220, height=40)
        
        # Student Button (Face detect)
        img5 = Image.open(r"img\face_reco_pic.png")
        img5 = img5.resize((220,220), Image.ANTIALIAS)
        main.photoimg5 = ImageTk.PhotoImage(img5)
        
        b1 = Button(bg_img, image=main.photoimg5, cursor="hand2", command=main.face_rog)
        b1.place(x=620, y=100, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Face Detect", cursor="hand2", command=main.face_rog, font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=620, y=300, width=220, height=40)
        
        # Student Button (Attandace Face)
        img6 = Image.open(r"img\list_check.png")
        img6 = img6.resize((220,220), Image.ANTIALIAS)
        main.photoimg6 = ImageTk.PhotoImage(img6)
        
        b1 = Button(bg_img, image=main.photoimg6, cursor="hand2", command=main.attandance)
        b1.place(x=920, y=100, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Attendance", cursor="hand2", command=main.attandance, font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=920, y=300, width=220, height=40)
        
        # Student Button (photo)
        img8 = Image.open(r"img\gallery_pic.png")
        img8 = img8.resize((220,220), Image.ANTIALIAS)
        main.photoimg8 = ImageTk.PhotoImage(img8)
        
        b1 = Button(bg_img, image=main.photoimg8, cursor="hand2", command=main.open_img)
        b1.place(x=320, y=380, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Photo", command=main.open_img, cursor="hand2", font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=320, y=580, width=220, height=40)
        
        # Student Button (Train Data)
        img9 = Image.open(r"img\gear.png")
        img9 = img9.resize((220,220), Image.ANTIALIAS)
        main.photoimg9 = ImageTk.PhotoImage(img9)
        
        b1 = Button(bg_img, image=main.photoimg9, cursor="hand2", command=main.train_data)
        b1.place(x=620, y=380, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Train Data", cursor="hand2", command=main.train_data, font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=620, y=580, width=220, height=40)
        
        # Student Button (Exit)
        img10 = Image.open(r"img\exit_run.png")
        img10 = img10.resize((220,220), Image.ANTIALIAS)
        main.photoimg10 = ImageTk.PhotoImage(img10)
        
        b1 = Button(bg_img, image=main.photoimg10, cursor="hand2", command=main.iExit)
        b1.place(x=920, y=380, width=220, height=220)
        
        b1_1 = Button(bg_img, text="Exit", cursor="hand2", command=main.iExit, font=("times new roman", 15, 'bold'),bg="darkblue", fg="white")
        b1_1.place(x=920, y=580, width=220, height=40)
        
    # ====================== photo =================
    
    def open_img(main):
        os.startfile("data")
        
    # =======Function Button ==========

    def student_details(main):
        main.new_window=Toplevel(main.root)
        main.app=student(main.new_window)
        
    def train_data(main):
        main.new_window=Toplevel(main.root)
        main.app=Train(main.new_window)
        
    def face_rog(main):
        main.new_window=Toplevel(main.root)
        main.app=face_recognition(main.new_window)
    
    def attandance(main):
        main.new_window=Toplevel(main.root)
        main.app=list_atten(main.new_window)
    
    def iExit(main):
        main.iExit=tkinter.messagebox.askyesno("Face Recognition","Are you sure exit this project",parent=main.root)
        if main.iExit >0:
            main.root.destroy()
        else:
            return

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()