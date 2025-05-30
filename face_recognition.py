# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 00:08:46 2022

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
import cv2
import os
import numpy as np


class face_recognition:
    def __init__(main, root):
        main.root = root
        main.root.geometry("1530x790+0+0")
        main.root.title("Face Recognition System")
        
        title_lbl = Label(main.root, text="FACE RECOGNITION", font=("Trebuchet MS", 35, 'bold'),bg="#e6e6e6", fg="red")
        title_lbl.place(x = 0, y = 0, width = 1530, height = 45)
        
        # === 1ST image =======
        img_top = Image.open(r"img\face_recognition.png")
        img_top = img_top.resize((650,700), Image.ANTIALIAS)
        main.photoimg_top = ImageTk.PhotoImage(img_top)
        
        f_lbl=Label(main.root,image=main.photoimg_top)
        f_lbl.place(x = 0, y = 55, width = 650, height = 700)
        
        # ===== 2ND image =====
        img_bottom = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img_bottom = img_bottom.resize((950,700), Image.ANTIALIAS)
        main.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        
        f_lbl=Label(main.root,image=main.photoimg_bottom)
        f_lbl.place(x = 650, y = 55, width = 950, height = 700)
        
        # ==== btn =====
        b1_1 = Button(f_lbl, text="Face Recognition", cursor="hand2", command=main.face_recog, font=("times new roman", 18, 'bold'),bg="red", fg="white")
        b1_1.place(x=0, y=520, width=200, height=40)

        notice_label=Label(main.root,text="Press Enter to close the window after face detected.",font=("impact", 18),bg="green", fg="white")
        notice_label.place(x = 500, y = 650)

    # ====quit or back button=====
        back_img = Image.open(r"img\pngegg.png")
        back_img = back_img.resize((50,50), Image.ANTIALIAS)
        main.back_logo = ImageTk.PhotoImage(back_img)
            
        quit_btn=Button(main.root, command=main.quit_button, image=main.back_logo, cursor="hand2")
        quit_btn.place(x=5,y=5)
    
    def quit_button(main):
        main.root.destroy()    
    # =================== attendance ==================
    def mark_attendance(main,i,n,d):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (n not in name_list) and (d not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{n},{d},{dtString},{d1},Attended")

        
        
    # ================ face recognition ===============
    def face_recog(main):
        myfile="classifier.xml"
        conn=pymysql.connect(host="localhost", user="root", passwd="", database="face_attendance")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from student ")

        try:
            if os.path.isfile(myfile)==False: #check if data trained or not
                messagebox.showerror("No classifier.xml found", "Data has not been trained.\nPlease close the window and train the data.", parent=main.root)
                return False
            elif my_cursor.rowcount==0: # check if there are any registered student
                messagebox.showerror("No student registered", "No data found in the database.\nPlease register first.", parent=main.root)
                os.remove(myfile)
                return False

            def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
                gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
                
                coord=[]
                
                for (x,y,w,h) in features:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                    id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                    confidence=int((100*(1-predict/300)))
                    
                    my_cursor.execute("select name from student where id="+str(id))
                    n=my_cursor.fetchone()
                    n="+".join(n)
                    
                    my_cursor.execute("select dep from student where id="+str(id))
                    d=my_cursor.fetchone()
                    d="+".join(d)
                    
                    my_cursor.execute("select Stu_id from student where id="+str(id))
                    i=my_cursor.fetchone()
                    i="+".join(i)
                    
                    
                    
                    if confidence>77:
                        cv2.putText(img, f"Student ID: {i}", (x,y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (26, 232, 39),3)
                        cv2.putText(img, f"Department: {d}", (x,y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (26, 232, 39),3)
                        cv2.putText(img, f"Name: {n}", (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (26, 232, 39),3)
                        main.mark_attendance(i, n, d)
                    else:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                        cv2.putText(img, "Unkown Face", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255),3)
                        
                    coord=[x,y,w,y]
                    
                return coord
        except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
        
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img
        
        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        
        video_cap=cv2.VideoCapture(0)
        
        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face recognition",img)
            
            if cv2.waitKey(1)==13:
                break
            
        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = face_recognition(root)
    root.mainloop()