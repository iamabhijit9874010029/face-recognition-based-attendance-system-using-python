import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        try:
            Subject = tx.get().strip()
            if Subject == "":
                t = 'Please enter the subject name.'
                text_to_speech(t)
                return
            
            attendance_dir = os.path.join("Attendance", Subject)
            if not os.path.exists(attendance_dir):
                t = f"No attendance records found for {Subject}"
                text_to_speech(t)
                print(t)
                return

            filenames = glob(os.path.join(attendance_dir, f"{Subject}*.csv"))
            
            if not filenames:
                t = f"No CSV files found for {Subject}"
                text_to_speech(t)
                print(t)
                return

            df = [pd.read_csv(f) for f in filenames]
            if not df:
                t = f"No valid data found in CSV files for {Subject}"
                text_to_speech(t)
                print(t)
                return

            newdf = df[0]
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            newdf.fillna(0, inplace=True)
            newdf["Attendance"] = 0
            for i in range(len(newdf)):
                newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
            
            newdf.to_csv(os.path.join(attendance_dir, "attendance.csv"), index=False)

            root = tk.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background="pink")
            cs = os.path.join(attendance_dir, "attendance.csv")
            with open(cs) as file:
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
            print(newdf)
        
        except Exception as e:
            t = f"Error processing attendance data: {str(e)}"
            text_to_speech(t)
            print(f"Error: {str(e)}")

    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="pink")

    titl = tk.Label(subject, bg="pink", relief=tk.RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=tk.X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="pink",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        try:
            sub = tx.get().strip()
            if sub == "":
                t = "Please enter the subject name!!!"
                text_to_speech(t)
            else:
                attendance_dir = os.path.join("Attendance", sub)
                if not os.path.exists(attendance_dir):
                    raise FileNotFoundError(f"No directory found for {sub}")
                os.startfile(attendance_dir)
        except FileNotFoundError as e:
            t = str(e)
            text_to_speech(t)
            print(f"Error: {t}")
        except Exception as e:
            t = f"Error opening directory: {str(e)}"
            text_to_speech(t)
            print(f"Error: {str(e)}")

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="pink",
        fg="blue",
        height=2,
        width=10,
        relief=tk.RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="pink",
        fg="blue",
        bd=5,
        relief=tk.RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="pink",
        fg="blue",
        relief=tk.RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="pink",
        fg="blue",
        height=2,
        width=12,
        relief=tk.RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()

# Example usage:
subjectchoose(lambda x: print(x))
