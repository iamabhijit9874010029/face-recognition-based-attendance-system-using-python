import csv
import tkinter as tk
import os
import cv2
import pandas as pd
import datetime
import time

# Paths to files and directories (adjust these paths as per your actual directory structure)
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get().strip()  # Get subject name from entry field
        now = time.time()
        future = now + 20
        
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return
        
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(trainimagelabel_path)
        except cv2.error as e:
            e_msg = f"Error loading model: {str(e)}"
            print(e_msg)
            Notifica.configure(
                text=e_msg,
                bg="pink",
                fg="blue",
                width=33,
                font=("times", 15, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech(e_msg)
            return
        
        faceCascade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        
        try:
            while time.time() < future:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    
                    if conf < 70:
                        Subject = sub
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H_%M_%S")  # Use underscore instead of colon
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        tt = f"{Id}-{aa}"
                        
                        attendance.loc[len(attendance)] = [Id, aa]
                        
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                    else:
                        Id = "Unknown"
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                cv2.imshow("Filling Attendance...", im)
                key = cv2.waitKey(30) & 0xFF
                if key == 27:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            
            if not attendance.empty:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H_%M_%S")  # Use underscore instead of colon
                path = os.path.join(attendance_path, Subject)
                os.makedirs(path, exist_ok=True)  # Ensure path exists or create it
                fileName = f"{Subject}_{date}_{timeStamp}.csv"  # Removed path prefix
                filePath = os.path.join(path, fileName)
                attendance.to_csv(filePath, index=False)
                
                m = f"Attendance Filled Successfully for {Subject}"
                Notifica.configure(
                    text=m,
                    bg="pink",
                    fg="blue",
                    width=33,
                    relief=tk.RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                
                Notifica.place(x=20, y=250)
                
                # Display attendance in GUI
                root = tk.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="pink")
                with open(filePath, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tk.Label(
                                root,
                                width=10,
                                height=1,
                                fg="blue",
                                font=("times", 15, " bold "),
                                bg="pink",
                                text=row,
                                relief=tk.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                f = "No faces found for attendance"
                text_to_speech(f)
        
        except Exception as ex:
            f = f"Error: {str(ex)}"
            print(f)
            text_to_speech(f)
        
        cam.release()
        cv2.destroyAllWindows()
    
    # GUI setup for subject selection
    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="pink")
    
    titl = tk.Label(subject, text="Enter the Subject Name", bg="pink", fg="green", font=("arial", 25))
    titl.place(x=160, y=12)
    
    Notifica = tk.Label(subject, text="Attendance filled Successfully", bg="blue", fg="pink", width=33, height=2, font=("times", 15, "bold"))
    
    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            attendance_dir = os.path.join(attendance_path, sub)
            if os.path.exists(attendance_dir):
                os.startfile(attendance_dir)
            else:
                t = f"No attendance sheets found for {sub}"
                text_to_speech(t)
    
    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15), bg="pink", fg="blue", height=2, width=10, relief=tk.RIDGE)
    attf.place(x=360, y=170)

    
    
    sub = tk.Label(subject, text="Enter Subject", width=10, height=2, bg="pink", fg="blue", bd=5, relief=tk.RIDGE, font=("times new roman", 15))
    sub.place(x=50, y=100)
    
    tx = tk.Entry(subject, width=15, bd=5, bg="pink", fg="blue", relief=tk.RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)
    
    fill_a = tk.Button(subject, text="Fill Attendance", command=FillAttendance, bd=7, font=("times new roman", 15), bg="pink", fg="blue", height=2, width=12, relief=tk.RIDGE)
    fill_a.place(x=195, y=170)
    
    subject.mainloop()

# Example usage of subjectChoose function with dummy text-to-speech function
def text_to_speech(text):
    print(f"Text to speech: {text}")

if __name__ == "__main__":
    subjectChoose(text_to_speech)
