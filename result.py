from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry

class resultClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Management system")
        self.root.geometry("1100x400+200+190")  # Fixed size
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # Title
        title = Label(self.root, text="Add Student Result", font=("goudy old style",20,"bold"), bg="orange", fg="#262626")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.var_percentage = StringVar()
        self.var_grade = StringVar()

        # Left Frame for Input
        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(x=10, y=60, width=450, height=330)

        # Right Frame for Preview
        right_frame = Frame(self.root, bd=0, bg="white")
        right_frame.place(x=470, y=60, width=620, height=330)

        # Preview Title with gradient effect
        preview_title = Label(right_frame, 
                            text="Result Preview", 
                            font=("Helvetica",18,"bold"), 
                            bg="#4D77FF", 
                            fg="white",
                            pady=10)
        preview_title.place(x=0, y=0, relwidth=1, height=50)

        # Preview Content - Card Style
        preview_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        preview_frame.place(x=20, y=60, width=580, height=260)

        # Decorative line
        Canvas(preview_frame, width=540, height=2, bg="#4D77FF").place(x=20, y=40)
        Canvas(preview_frame, width=540, height=2, bg="#4D77FF").place(x=20, y=140)

        # Student Details Section
        Label(preview_frame, 
              text="✧ Student Details", 
              font=("Helvetica", 14, "bold"), 
              bg="white",
              fg="#4D77FF").place(x=20, y=10)

        # Details with improved styling
        Label(preview_frame, text="Roll No", font=("Helvetica", 12), bg="white", fg="#555555").place(x=30, y=60)
        Label(preview_frame, text=":", font=("Helvetica", 12), bg="white").place(x=120, y=60)
        Label(preview_frame, text="Name", font=("Helvetica", 12), bg="white", fg="#555555").place(x=30, y=90)
        Label(preview_frame, text=":", font=("Helvetica", 12), bg="white").place(x=120, y=90)
        Label(preview_frame, text="Course", font=("Helvetica", 12), bg="white", fg="#555555").place(x=30, y=120)
        Label(preview_frame, text=":", font=("Helvetica", 12), bg="white").place(x=120, y=120)

        # Result Section
        Label(preview_frame, 
              text="✧ Result Details", 
              font=("Helvetica", 14, "bold"), 
              bg="white",
              fg="#4D77FF").place(x=20, y=160)

        # Result details with improved styling
        Label(preview_frame, text="Marks Obtained", font=("Helvetica", 12), bg="white", fg="#555555").place(x=30, y=190)
        Label(preview_frame, text=":", font=("Helvetica", 12), bg="white").place(x=160, y=190)
        Label(preview_frame, text="Full Marks", font=("Helvetica", 12), bg="white", fg="#555555").place(x=30, y=220)
        Label(preview_frame, text=":", font=("Helvetica", 12), bg="white").place(x=160, y=220)

        # Percentage and Grade Section with highlight
        percentage_frame = Frame(preview_frame, bg="#E8F0FE", bd=0)
        percentage_frame.place(x=300, y=180, width=250, height=70)
        
        Label(percentage_frame, text="Percentage:", font=("Helvetica", 12, "bold"), bg="#E8F0FE", fg="#4D77FF").place(x=20, y=10)
        Label(percentage_frame, text="Grade:", font=("Helvetica", 12, "bold"), bg="#E8F0FE", fg="#4D77FF").place(x=20, y=40)

        # Value Labels with modern styling
        self.lbl_roll = Label(preview_frame, textvariable=self.var_roll, font=("Helvetica", 12), bg="white", fg="#333333")
        self.lbl_roll.place(x=140, y=60)
        
        self.lbl_name = Label(preview_frame, textvariable=self.var_name, font=("Helvetica", 12), bg="white", fg="#333333")
        self.lbl_name.place(x=140, y=90)
        
        self.lbl_course = Label(preview_frame, textvariable=self.var_course, font=("Helvetica", 12), bg="white", fg="#333333")
        self.lbl_course.place(x=140, y=120)
        
        self.lbl_marks = Label(preview_frame, textvariable=self.var_marks, font=("Helvetica", 12), bg="white", fg="#333333")
        self.lbl_marks.place(x=180, y=190)
        
        self.lbl_full_marks = Label(preview_frame, textvariable=self.var_full_marks, font=("Helvetica", 12), bg="white", fg="#333333")
        self.lbl_full_marks.place(x=180, y=220)
        
        self.lbl_percentage = Label(percentage_frame, textvariable=self.var_percentage, font=("Helvetica", 14, "bold"), bg="#E8F0FE", fg="#4D77FF")
        self.lbl_percentage.place(x=120, y=10)
        
        self.lbl_grade = Label(percentage_frame, textvariable=self.var_grade, font=("Helvetica", 14, "bold"), bg="#E8F0FE", fg="#4D77FF")
        self.lbl_grade.place(x=120, y=40)

        # Labels and Entry Fields in Left Frame
        lbl_roll = Label(left_frame, text="Select Roll No:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_roll.place(x=10, y=20)

        # Roll Number Combobox
        self.roll_combo = ttk.Combobox(left_frame, textvariable=self.var_roll, font=("goudy old style", 13), state='readonly')
        self.roll_combo.place(x=170, y=20, width=200)
        self.roll_combo.bind('<<ComboboxSelected>>', self.get_student)
        self.load_roll_numbers()

        # Name
        lbl_name = Label(left_frame, text="Name:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_name.place(x=10, y=70)
        txt_name = Entry(left_frame, textvariable=self.var_name, font=("goudy old style", 13), bg="lightyellow", state='readonly')
        txt_name.place(x=170, y=70, width=200)

        # Course
        lbl_course = Label(left_frame, text="Course:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_course.place(x=10, y=120)
        txt_course = Entry(left_frame, textvariable=self.var_course, font=("goudy old style", 13), bg="lightyellow", state='readonly')
        txt_course.place(x=170, y=120, width=200)

        # Marks Obtained
        lbl_marks = Label(left_frame, text="Marks Obtained:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_marks.place(x=10, y=170)
        txt_marks = Entry(left_frame, textvariable=self.var_marks, font=("goudy old style", 13), bg="lightyellow")
        txt_marks.place(x=170, y=170, width=200)
        txt_marks.bind('<KeyRelease>', self.calculate_result)

        # Full Marks
        lbl_full_marks = Label(left_frame, text="Full Marks:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_full_marks.place(x=10, y=220)
        txt_full_marks = Entry(left_frame, textvariable=self.var_full_marks, font=("goudy old style", 13), bg="lightyellow")
        txt_full_marks.place(x=170, y=220, width=200)
        txt_full_marks.bind('<KeyRelease>', self.calculate_result)

        # Buttons
        btn_submit = Button(left_frame, text="Submit", font=("goudy old style", 15), bg="lightgreen", cursor="hand2", command=self.submit)
        btn_submit.place(x=100, y=270, width=120)

        btn_clear = Button(left_frame, text="Clear", font=("goudy old style", 15), bg="lightgray", cursor="hand2", command=self.clear)
        btn_clear.place(x=230, y=270, width=120)

    def load_roll_numbers(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            
            # Fetch all roll numbers
            cur.execute("SELECT roll FROM student ORDER BY roll")
            rolls = cur.fetchall()
            
            # Update combobox values
            roll_list = ["Select"]
            roll_list.extend([roll[0] for roll in rolls])
            self.roll_combo['values'] = tuple(roll_list)
            self.roll_combo.current(0)
            
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def get_student(self, event=None):
        try:
            if self.var_roll.get() == "Select":
                self.clear()
                return
                
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            
            # Fetch student details
            cur.execute("SELECT name, selectcourse FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.var_percentage.set("")
        self.var_grade.set("")

    def calculate_result(self, event=None):
        try:
            marks = float(self.var_marks.get()) if self.var_marks.get() else 0
            full_marks = float(self.var_full_marks.get()) if self.var_full_marks.get() else 0
            if full_marks > 0:
                percentage = (marks / full_marks) * 100
                self.var_percentage.set(f"{percentage:.1f}%")
                
                # Calculate grade
                if percentage >= 90:
                    grade = "A+"
                elif percentage >= 80:
                    grade = "A"
                elif percentage >= 70:
                    grade = "B+"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C"
                elif percentage >= 40:
                    grade = "D"
                else:
                    grade = "F"
                
                self.var_grade.set(grade)
            else:
                self.var_percentage.set("")
                self.var_grade.set("")
        except ValueError:
            self.var_percentage.set("")
            self.var_grade.set("")

    def submit(self):
        if self.var_roll.get() == "Select":
            messagebox.showerror("Error", "Please select Roll Number", parent=self.root)
        elif self.var_marks.get() == "":
            messagebox.showerror("Error", "Please enter marks obtained", parent=self.root)
        elif self.var_full_marks.get() == "":
            messagebox.showerror("Error", "Please enter full marks", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                
                # Check if result already exists
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Result already exists for this student", parent=self.root)
                else:
                    # Insert result
                    cur.execute("""
                        INSERT INTO result (roll, name, course, marks_obtained, full_marks)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Result added successfully", parent=self.root)
                    self.clear()
                    
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

if __name__=="__main__":
    root=Tk()
    obj=resultClass(root)
    root.mainloop()