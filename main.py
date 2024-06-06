import tkinter as tk
import cv2

from PIL import Image,ImageTk
import os
import face_recognition
import datetime
import util

class App:
    def __init__(self):
        self.main_window=tk.Tk() #creating an empty windoww
        self.main_window.geometry("1200x520+130+100")

        self.Scan_button=util.get_button(self.main_window,"Login","blue",self.Scan)
        self.Scan_button.place(x=800,y=150)

        self.Register_button=util.get_button(self.main_window,"Capture new face","gray",self.Register,fg="black")
        self.Register_button.place(x=800,y=275)

        self.Register_button=util.get_button(self.main_window,"Close","red",self.Close,fg="black")
        self.Register_button.place(x=800,y=400)
       

        self.Webcam=util.get_img_label(self.main_window)
        self.Webcam.place(x=10,y=0,width=700,height=500)

        self.Add_webcam(self.Webcam)

        self.text_label=util.get_text_label(self.main_window,"Face Recognizer and Authenticator")
        self.text_label.place(x=720,y=70)

        self.db_dir='./db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
    
    def Add_webcam(self,label):
        if 'cap' not in self.__dict__:
            self.cap=cv2.VideoCapture(0)
        
        self._label=label
        self.process_webcam()

    def process_webcam(self):
        ret,frame=self.cap.read()
        self.most_recent_capture_arr=frame
        img=cv2.cvtColor(self.most_recent_capture_arr,cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil=Image.fromarray(img)
        imgtk=ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk=imgtk
        self._label.configure(image=imgtk)
        self._label.after(20,self.process_webcam)

    def Scan(self):

        unknown_img_path='./.tmp.jpg'

        cv2.imwrite(unknown_img_path,self.most_recent_capture_arr)

        Known_face_encodings=[]
        Known_face_names=[]

        for filename in os.listdir(self.db_dir):
            if filename.endswith(('jpg','jpeg','png')):
                image_path=os.path.join(self.db_dir,filename)
                image=face_recognition.load_image_file(image_path)
                face_encodings=face_recognition.face_encodings(image)
                if face_encodings:
                    Known_face_encodings.append(face_encodings[0])
                    Known_face_names.append(os.path.splitext(filename)[0])
        
        unknown_image=face_recognition.load_image_file(unknown_img_path)
        unknown_face_encodings=face_recognition.face_encodings(unknown_image)

        if not unknown_face_encodings:
            util.msg_box("Result","NO Faces Detected!")
        else:
            found_match=False
            for unknown_face_encoding in unknown_face_encodings:
                result=face_recognition.compare_faces(Known_face_encodings,unknown_face_encoding)
                face_distance=face_recognition.face_distance(Known_face_encodings,unknown_face_encoding)
        
                if True in result:
                    best_match_index=result.index(True)
                    name=Known_face_names[best_match_index]
                    util.msg_box("Login Successfull",f"Login successfull: \n  {name} you are Authorized!")
                    found_match=True
                    break
            if not found_match:
                util.msg_box("UnAuthorized","Match Not Found: \n  Unknow Person you are UnAuthorized!")
        
        os.remove(unknown_img_path)


    def Register(self):
        self.register_new_face_window=tk.Toplevel(self.main_window)
        self.register_new_face_window.geometry("1200x520+150+120")

        self.Accept_button=util.get_button(self.register_new_face_window,"Accept","blue",self.Accept)
        self.Accept_button.place(x=800,y=300)

        self.Try_again_button=util.get_button(self.register_new_face_window,"Try Again","red",self.Try_again)
        self.Try_again_button.place(x=800,y=400)

        self.Capture=util.get_img_label(self.register_new_face_window)
        self.Capture.place(x=10,y=0,width=700,height=500)

        self.Add_img_to_Capture(self.Capture)

        self.entry_text_register_new_face=util.get_entry_text(self.register_new_face_window)  #create a text box
        self.entry_text_register_new_face.place(x=800,y=150)

        self.text_register_new_face=util.get_text_label(self.register_new_face_window,"Please, \nEnter your name :")
        self.text_register_new_face.place(x=800,y=70)

    def Close(self):
        self.main_window.destroy()
    
    def Try_again(self):
        self.register_new_face_window.destroy()

    def Add_img_to_Capture(self,label):
        imgtk=ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk=imgtk
        label.configure(image=imgtk)

        self.register_new_face_Capture=self.most_recent_capture_arr.copy()

    
    def start(self):
        self.main_window.mainloop()

    def Accept(self):
        name=self.entry_text_register_new_face.get(1.0,"end-1c")

        cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)),self.register_new_face_Capture)

        util.msg_box("Success","New Face Registered Successfully!")

        self.register_new_face_window.destroy()


if __name__ == "__main__":
    app= App()
    app.start()
