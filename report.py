from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry

class reportClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Management system")
        self.root.geometry("1100x400+200+190")  # Fixed size
        self.root.config(bg="white")
        self.root.resizable(False, False)

        headerresult=Label(self.root,text="View Student Result",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=0,y=10,width=100,relwidth=1)

        # ========== variables ===========
        self.var_search=StringVar()  # Changed from var_roll to var_search

        # ====== Labels ===========
        # Roll Number Selection
        lbl_SelectRoll = Label(self.root, text="Search By Roll No:", font=("goudy old style", 20, "bold"), bg="white").place(x=200, y=100)

        # ========== entry fields ============  
        self.txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 12), bg="lightyellow")
        self.txt_search.place(x=430, y=105, width=200)

        # ======== button =========== 
        search_button=Button(self.root,text="Search",font=("goudy old style", 15), bg="lightgreen",cursor="hand2",command=self.search)
        search_button.place(x=650,y=95,width=130)
        
        clear_button=Button(self.root,text="Clear",font=("goudy old style", 15), bg="lightgray", command=self.clear)
        clear_button.place(x=800,y=95,width=130)

        # ============ label =========
        lbl_roll=Label(self.root,text="Roll No", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=100,y=210,width=150,height=50)
        lbl_name=Label(self.root,text="Name", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=250,y=210,width=150,height=50)
        lbl_course=Label(self.root,text="Course", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=400,y=210,width=150,height=50)
        lbl_marksobt=Label(self.root,text="Marks Obtained", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=550,y=210,width=150,height=50)
        lbl_totalmarks=Label(self.root,text="Total Marks", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=700,y=210,width=150,height=50)
        lbl_per=Label(self.root,text="Percentage", font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE).place(x=850,y=210,width=150,height=50)
 
        # Result display labels
        self.lbl_roll_result = Label(self.root, font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_roll_result.place(x=100,y=260,width=150,height=50)
        
        self.lbl_name_result = Label(self.root,font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_name_result.place(x=250,y=260,width=150,height=50)
        
        self.lbl_course_result = Label(self.root,font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_course_result.place(x=400,y=260,width=150,height=50)
        
        self.lbl_marksobt_result = Label(self.root,font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_marksobt_result.place(x=550,y=260,width=150,height=50)
        
        self.lbl_totalmarks_result = Label(self.root,font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_totalmarks_result.place(x=700,y=260,width=150,height=50)
        
        self.lbl_per_result = Label(self.root,font=("goudy old style", 15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.lbl_per_result.place(x=850,y=260,width=150,height=50)

        # ========== delete button =======
        # delete_button=Button(self.root,text="Delete",font=("goudy old style", 15), bg="red", command=self.delete)
        # delete_button.place(x=450,y=325,width=130)

    def clear(self):
        self.var_search.set("")
        self.lbl_roll_result.config(text="")
        self.lbl_name_result.config(text="")
        self.lbl_course_result.config(text="")
        self.lbl_marksobt_result.config(text="")
        self.lbl_totalmarks_result.config(text="")
        self.lbl_per_result.config(text="")

    def delete(self):
        if self.var_search.get() == "":
            messagebox.showerror("Error", "Please search a result first", parent=self.root)
        else:
            try:
                confirm = messagebox.askyesno("Confirm", "Do you really want to delete this result?", parent=self.root)
                if confirm:
                    con = sqlite3.connect(database="rms.db")
                    cur = con.cursor()
                    cur.execute("DELETE FROM result WHERE roll=?", (self.var_search.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Result deleted successfully", parent=self.root)
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        if self.var_search.get() == "":
            messagebox.showerror("Error", "Roll number is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                
                if row:
                    # Calculate percentage
                    marks_obt = float(row[3])  # marks_obtained
                    total_marks = float(row[4])  # full_marks
                    percentage = (marks_obt / total_marks) * 100
                    
                    # Update labels
                    self.lbl_roll_result.config(text=row[0])  # roll
                    self.lbl_name_result.config(text=row[1])  # name
                    self.lbl_course_result.config(text=row[2])  # course
                    self.lbl_marksobt_result.config(text=row[3])  # marks_obtained
                    self.lbl_totalmarks_result.config(text=row[4])  # full_marks
                    self.lbl_per_result.config(text=f"{percentage:.2f}%")
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
                    
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                if 'con' in locals():
                    con.close()

if __name__=="__main__":
    root=Tk()
    obj=reportClass(root)
    root.mainloop()