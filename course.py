from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class CourseClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Result Management system")
        self.root.geometry("1100x500+95+80")  # Fixed size
        self.root.config(bg="white")
        self.root.resizable(False, False)  # Prevent resizing

        # Create database and table
        self.create_table()

#  ======== title ==============
        title1=Label(self.root,text="Manage course details",bg="#033054",fg="white",relief=RIDGE,font=("arial",25,"bold")).place(x=0,y=0,width=1100,height=50)

#  ========== variables =======
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()
        self.var_search=StringVar()

#  ============ widgets ==========

        # Left Frame
        left_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        left_frame.place(x=10, y=60, width=450, height=430)

        lbl_coursename=Label(left_frame,text="Course Name",font=("times new roman",15,"bold"),bg="white").place(x=10,y=10)
        lbl_duration=Label(left_frame,text="Duration",font=("times new roman",15,"bold"),bg="white").place(x=10,y=60)
        lbl_charges=Label(left_frame,text="Charges",font=("times new roman",15,"bold"),bg="white").place(x=10,y=110)
        lbl_description=Label(left_frame,text="Description",font=("times new roman",15,"bold"),bg="white").place(x=10,y=160)

        self.txt_coursename=Entry(left_frame,textvariable=self.var_course,font=("times new roman",13),bg="white")
        self.txt_coursename.place(x=140,y=10,width=250)

        txt_duration=Entry(left_frame,textvariable=self.var_duration,font=("times new roman",13),bg="white").place(x=140,y=60,width=250)
        txt_charges=Entry(left_frame,textvariable=self.var_charges,font=("times new roman",13),bg="white").place(x=140,y=110,width=250)
        
        self.txt_description=Text(left_frame,font=("times new roman",13),bg="white")
        self.txt_description.place(x=140,y=160,width=250,height=150)

        # Buttons Frame
        btn_frame = Frame(left_frame, bg="white")
        btn_frame.place(x=120, y=320)

        # Save Button (Green)
        btn_save = Button(btn_frame, 
                        text="Save",
                        font=("times new roman", 13, "bold"),
                        bg="#28a745",
                        fg="white",
                        cursor="hand2",
                        command=self.save)
        btn_save.pack(side=LEFT, padx=5)

        # Update Button (Blue)
        btn_update = Button(btn_frame,
                          text="Update",
                          font=("times new roman", 13, "bold"),
                          bg="#007bff",
                          fg="white",
                          cursor="hand2",
                          command=self.update)
        btn_update.pack(side=LEFT, padx=5)

        # Delete Button (Red)
        btn_delete = Button(btn_frame,
                          text="Delete",
                          font=("times new roman", 13, "bold"),
                          bg="#dc3545",
                          fg="white",
                          cursor="hand2",
                          command=self.delete)
        btn_delete.pack(side=LEFT, padx=5)

        # Clear Button (Gray)
        btn_clear = Button(btn_frame,
                         text="Clear",
                         font=("times new roman", 13, "bold"),
                         bg="#6c757d",
                         fg="white",
                         cursor="hand2",
                         command=self.clear)
        btn_clear.pack(side=LEFT, padx=5)

        # Right Frame
        right_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        right_frame.place(x=470, y=60, width=631, height=430)

        # Search Frame
        search_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        search_frame.place(x=5, y=5, width=650, height=70)

        lbl_search=Label(search_frame,text="Search Course",font=("times new roman",15,"bold"),bg="white").place(x=10,y=15)
        txt_search=Entry(search_frame,textvariable=self.var_search,font=("times new roman",13),bg="white").place(x=200,y=15,width=300)
        btn_search = Button(search_frame,
                         text="Search",
                         font=("times new roman", 13, "bold"),
                         bg="#6c757d",
                         fg="white",
                         cursor="hand2",
                         command=self.search)
        btn_search.place(x=520,y=15)

        # Table Frame
        table_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=5, y=80, width=650, height=340)

        # content
        self.c_frame=Frame(self.root,bd=2,relief=RIDGE)
        self.c_frame.place(x=500,y=150,width=570,height=320)

        scrollx=Scrollbar(self.c_frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.c_frame,orient=VERTICAL)
        self.course_table=ttk.Treeview(self.c_frame,columns=("cid","name","duration","charges","description"))
        
        # Configure scrollbars
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)
        self.course_table.configure(xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Pack scrollbars
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        self.course_table.heading("cid",text="Course Id")
        self.course_table.heading("name",text="Name")
        self.course_table.heading("duration",text="Duration")
        self.course_table.heading("charges",text="Charges")
        self.course_table.heading("description",text="Description")
        self.course_table["show"]='headings'

        self.course_table.column("cid",width=70)
        self.course_table.column("name",width=180)
        self.course_table.column("duration",width=100)
        self.course_table.column("charges",width=100)
        self.course_table.column("description",width=200)

        self.course_table.pack(fill=BOTH,expand=1)
        
        # Bind table selection
        self.course_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Fetch data from database
        self.fetch_data()

    def create_table(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS course(
                cid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                duration TEXT NOT NULL,
                charges TEXT NOT NULL,
                description TEXT
            )''')
            conn.commit()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def fetch_data(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.course_table.delete(*self.course_table.get_children())
                for row in rows:
                    self.course_table.insert('', END, values=row)
            conn.commit()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def get_cursor(self, event=""):
        try:
            cursor_row = self.course_table.focus()
            content = self.course_table.item(cursor_row)
            row = content['values']
            if row:
                self.var_course.set(row[1])  # name
                self.var_duration.set(row[2])
                self.var_charges.set(row[3])
                self.txt_description.delete("1.0", END)
                self.txt_description.insert(END, row[4])
                # Store the course ID for deletion
                self.var_cid = row[0]  # Store course ID
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)

    def save(self):
        if self.var_course.get() == "" or self.var_duration.get() == "" or self.var_charges.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                
                # Check if course already exists
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course Already Exists", parent=self.root)
                    return
                
                # If course doesn't exist, insert new course
                cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?,?,?,?)",
                          (self.var_course.get(),
                           self.var_duration.get(),
                           self.var_charges.get(),
                           self.txt_description.get("1.0", END)))
                conn.commit()
                messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                self.fetch_data()
                self.clear()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

    def update(self):
        if self.var_course.get() == "" or self.var_duration.get() == "" or self.var_charges.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?",
                          (self.var_duration.get(),
                           self.var_charges.get(),
                           self.txt_description.get("1.0", END),
                           self.var_course.get()))
                conn.commit()
                messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                self.fetch_data()
                self.clear()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

    def delete(self):
        if not hasattr(self, 'var_cid'):
            messagebox.showerror("Error", "Please Select Course to Delete", parent=self.root)
            return
            
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM course WHERE cid=?", (self.var_cid,))
            conn.commit()
            messagebox.showinfo("Success", "Course Deleted Successfully", parent=self.root)
            self.fetch_data()
            self.clear()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_description.delete("1.0", END)
        if hasattr(self, 'var_cid'):
            delattr(self, 'var_cid')  # Clear the stored course ID

    def search(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            if len(rows) != 0:
                self.course_table.delete(*self.course_table.get_children())
                for row in rows:
                    self.course_table.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No Record Found", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

if __name__=="__main__":
    root=Tk()
    obj=CourseClass(root)
    root.mainloop()