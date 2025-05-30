# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:26:08 2022

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
import numpy as np


class Train:
    def __init__(main, root):
        main.root = root
        main.root.geometry("1530x790+0+0")
        main.root.title("Face Recognition System")
        
        title_lbl = Label(main.root, text="TRAIN PHOTO TO DATASET", font=("Trebuchet MS", 35, 'bold'),bg="white", fg="red")
        title_lbl.place(x = 0, y = 0, width = 1530, height = 45)
        
        img_top = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img_top = img_top.resize((1530,325), Image.ANTIALIAS)
        main.photoimg_top = ImageTk.PhotoImage(img_top)
        
        f_lbl=Label(main.root,image=main.photoimg_top)
        f_lbl.place(x = 0, y = 55, width = 1530, height = 325)
        
        # ==== train data btn ======= 
        b1_1 = Button(main.root, text="Start Train", cursor="hand2", command=main.train_classifier, font=("times new roman", 30, 'bold'),bg="red", fg="white")
        b1_1.place(x=0, y=380, width=1530, height=60)
        
        img_bottom = Image.open(r"img\PicsArt_05-01-10.15.30.jpg")
        img_bottom = img_bottom.resize((1530,325), Image.ANTIALIAS)
        main.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        
        f_lbl=Label(main.root,image=main.photoimg_bottom)
        f_lbl.place(x = 0, y = 440, width = 1530, height = 325)

        # ====quit or back button=====
        back_img = Image.open(r"img\pngegg.png")
        back_img = back_img.resize((50,50), Image.ANTIALIAS)
        main.back_logo = ImageTk.PhotoImage(back_img)
            
        quit_btn=Button(main.root, command=main.quit_button, image=main.back_logo, cursor="hand2")
        quit_btn.place(x=5,y=5)
    
    def quit_button(main):
        main.root.destroy()
        
    # ===== Train Function =============
    def train_classifier(main):
        if len(os.listdir('data/')) == 0: #check if any photo exist
            messagebox.showerror("No photo detected","There are no photos available for training.\nPlease take sample photo at 'Student Details'", parent=main.root)
            return False
        try:
            data_dir=("data")
            path=[os.path.join(data_dir, file) for file in os.listdir(data_dir)]
            
            faces=[]
            ids=[]
            
            for image in path:
                img=Image.open(image).convert('L') #Gray scale image
                imageNp=np.array(img, 'uint8')
                id=int(os.path.split(image)[1].split('.')[1])
                
                faces.append(imageNp)
                ids.append(id)
                cv2.imshow("Training", imageNp)
                cv2.waitKey(1)==13
            ids=np.array(ids)
            
            # ================ Train the Classifier And save =============
            clf=cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces,ids)
            clf.write("classifier.xml")
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training datasets completed!!",parent=main.root)
            main.root.destroy() #close window
        except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}", parent=main.root)
        
        
            

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()