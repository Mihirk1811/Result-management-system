from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry

class studentClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Management system")
        self.root.geometry("1100x500+95+80")  # Fixed size
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # Create database and table if they don't exist
        self.create_database()

#  ======== title ==============
        title1=Label(self.root,text="Manage Student Details",bg="#033054",fg="white",relief=RIDGE,font=("arial",25,"bold")).place(x=0,y=0,width=1100,height=50)

#  ========== variables =======
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_gender=StringVar()
        self.var_state=StringVar()
        self.var_dob=StringVar()
        self.var_city=StringVar()
        self.var_pin=StringVar()
        self.var_contact=StringVar()
        self.var_admissiondate=StringVar()
        self.var_selectcourse=StringVar()

#  ============ widgets ==========

        # Left Frame with Header
        self.leftframe = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.leftframe.place(x=10, y=60, width=530, height=430)

        # Header Label
        header_label = Label(self.leftframe, 
                           text="Manage Student Details",
                           font=("times new roman", 15, "bold"),
                           bg="#0B5466",  # Dark teal color
                           fg="white",
                           bd=0,
                           relief=RIDGE)
        header_label.place(x=0, y=0, width=530, height=40)

        # Form Frame (white background)
        form_frame = Frame(self.leftframe, bg="white")
        form_frame.place(x=5, y=45, width=520, height=380)

        # Form Labels and Entry Fields
        lbl_rollno = Label(form_frame, text="Roll No.", font=("times new roman", 12), bg="white").place(x=10, y=20)
        lbl_name = Label(form_frame, text="Name", font=("times new roman", 12), bg="white").place(x=10, y=60)
        lbl_email = Label(form_frame, text="Email", font=("times new roman", 12), bg="white").place(x=10, y=100)
        lbl_gender = Label(form_frame, text="Gender", font=("times new roman", 12), bg="white").place(x=10, y=140)
        lbl_state = Label(form_frame, text="State", font=("times new roman", 12), bg="white").place(x=10, y=180)
        lbl_dob = Label(form_frame, text="D.O.B(dd/mm/yy)", font=("times new roman", 12), bg="white").place(x=250, y=20)
        lbl_contactno = Label(form_frame, text="Contact No.", font=("times new roman", 12), bg="white").place(x=250, y=60)
        lbl_selectcourse = Label(form_frame, text="Select Course", font=("times new roman", 12), bg="white").place(x=250, y=100)
        lbl_admissiondate = Label(form_frame, text="Admission Date", font=("times new roman", 12), bg="white").place(x=250, y=140)
        lbl_address = Label(form_frame, text="Address", font=("times new roman", 12), bg="white").place(x=10, y=220)

        # Entry Fields
        self.txt_roll = Entry(form_frame, textvariable=self.var_roll, font=("times new roman", 12), bg="lightyellow")
        self.txt_roll.place(x=70, y=20, width=150)

        self.txt_name = Entry(form_frame, textvariable=self.var_name, font=("times new roman", 12), bg="lightyellow")
        self.txt_name.place(x=70, y=60, width=150)

        txt_email = Entry(form_frame, textvariable=self.var_email, font=("times new roman", 12), bg="lightyellow")
        txt_email.place(x=70, y=100, width=150)

        # Gender Combobox
        gender_combo = ttk.Combobox(form_frame, textvariable=self.var_gender, font=("times new roman", 12), state='readonly')
        gender_combo['values'] = ("Select", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.place(x=70, y=140, width=150)

        # state Combobox
        state_combo = ttk.Combobox(form_frame, textvariable=self.var_state, font=("times new roman", 12), state='readonly')
        state_combo['values'] = ("Select","Gujarat","Rajsthan","Maharashtra","UP","MP")  # Add your course values here
        state_combo.current(0)
        state_combo.place(x=70, y=180, width=150)
       
        # DOB Calendar
        cal_dob = DateEntry(form_frame, textvariable=self.var_dob, font=("times new roman", 12), bg="lightyellow", date_pattern='dd/mm/yyyy')
        cal_dob.place(x=360, y=20, width=150)

        txt_contact = Entry(form_frame, textvariable=self.var_contact, font=("times new roman", 12), bg="lightyellow")
        txt_contact.place(x=360, y=60, width=150)

        # Course Combobox
        course_combo = ttk.Combobox(form_frame, textvariable=self.var_selectcourse, font=("times new roman", 12), state='readonly')
        course_combo['values'] = ("Select","Java","Python","C++","MongoDB")  # Add your course values here
        course_combo.current(0)
        course_combo.place(x=360, y=100, width=150)

        txt_admissiondate = DateEntry(form_frame, textvariable=self.var_admissiondate, font=("times new roman", 12), bg="lightyellow", date_pattern='dd/mm/yyyy')
        txt_admissiondate.place(x=360, y=140, width=150)

        # City field
        lbl_city = Label(form_frame, text="City", font=("times new roman", 12), bg="white").place(x=200, y=180)
        txt_city = Entry(form_frame, textvariable=self.var_city, font=("times new roman", 12), bg="lightyellow")
        txt_city.place(x=240, y=180, width=120)
        
        # Pin Code field
        lbl_pin = Label(form_frame, text="Pin Code", font=("times new roman", 12), bg="white").place(x=370, y=180)
        txt_pin = Entry(form_frame, textvariable=self.var_pin, font=("times new roman", 12), bg="lightyellow")
        txt_pin.place(x=440, y=180, width=70)

        # Address Text Field
        self.txt_address = Text(form_frame, font=("times new roman", 12), bg="lightyellow")
        self.txt_address.place(x=70, y=220, width=440, height=100)

        # Buttons Frame
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.place(x=10, y=330, width=500, height=35)

        # Save Button
        btn_save = Button(btn_frame, text="Save", font=("times new roman", 12), bg="#2196f3", fg="white", cursor="hand2", command=self.save)
        btn_save.place(x=10, y=0, width=110, height=35)

        # Update Button
        btn_update = Button(btn_frame, text="Update", font=("times new roman", 12), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        btn_update.place(x=130, y=0, width=110, height=35)

        # Delete Button
        btn_delete = Button(btn_frame, text="Delete", font=("times new roman", 12), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        btn_delete.place(x=250, y=0, width=110, height=35)

        # Clear Button
        btn_clear = Button(btn_frame, text="Clear", font=("times new roman", 12), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        btn_clear.place(x=370, y=0, width=110, height=35)

        # Right Frame
        right_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        right_frame.place(x=550, y=60, width=530, height=430)

        # Search Frame
        search_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        search_frame.place(x=5, y=5, width=520, height=70)

        # Search Label
        lbl_search = Label(search_frame, 
                          text="Search Student", 
                          font=("times new roman", 15, "bold"), 
                          bg="white")
        lbl_search.place(x=10, y=15)
        
        # Search Combobox
        self.var_search = StringVar()
        search_combo = ttk.Combobox(search_frame, 
                                  textvariable=self.var_search,
                                  font=("times new roman", 13),
                                  state="readonly")
        search_combo['values'] = ("Roll No", "Name", "Email", "Contact")
        search_combo.current(0)
        search_combo.place(x=150, y=15, width=150)
        
        # Roll Number Combobox
        self.var_roll_search = StringVar()
        self.roll_combo = ttk.Combobox(search_frame, 
                                     textvariable=self.var_roll_search,
                                     font=("times new roman", 13),
                                     state="readonly")
        self.roll_combo.place(x=310, y=15, width=100)
        
        # Search Entry (for non-roll searches)
        self.txt_search = Entry(search_frame, 
                          font=("times new roman", 13), 
                          bg="lightyellow")
        self.txt_search.place(x=310, y=15, width=100)
        
        # Search Button
        btn_search = Button(search_frame,
                         text="Search",
                         font=("times new roman", 13, "bold"),
                         bg="#033054",
                         fg="white",
                         cursor="hand2",
                         command=self.search)
        btn_search.place(x=420, y=15, width=90, height=30)

        # Show All Button
        btn_show_all = Button(search_frame,
                         text="Show All",
                         font=("times new roman", 13, "bold"),
                         bg="#033054",
                         fg="white",
                         cursor="hand2",
                         command=self.fetch_data)
        btn_show_all.place(x=10, y=45, width=90, height=25)

        # Bind search type change
        search_combo.bind('<<ComboboxSelected>>', self.on_search_type_change)
        
        # Initially hide search entry and show roll combo
        self.txt_search.place_forget()
        self.update_roll_numbers()

        # Image Frame
        img_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        img_frame.place(x=5, y=80, width=520, height=340)
        
        # Load and display image
        try:
            print("Starting image loading process...")
            img_path = "Images/result1.png"
            print(f"Image path: {img_path}")
            
            # Load image
            img = Image.open(img_path)
            print("Image opened successfully")
            
            # Resize image
            img = img.resize((520, 340))
            print("Image resized successfully")
            
            # Convert to PhotoImage
            self.photo_img = ImageTk.PhotoImage(img)
            print("PhotoImage created successfully")
            
            # Create and place label
            img_label = Label(img_frame, image=self.photo_img)
            img_label.pack(fill=BOTH, expand=True)
            print("Image label packed successfully")
            
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            # Fallback to colored background
            img_label = Label(img_frame, 
                            bg="#f0f0f0", 
                            text="Student Image\n(Image loading failed)",
                            font=("times new roman", 15))
            img_label.pack(fill=BOTH, expand=True)

        # Table Frame - Commented out to make room for image
        # table_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        # table_frame.place(x=10, y=80, width=650, height=340)

        # content
        self.c_frame=Frame(self.root,bd=2,relief=RIDGE)
        self.c_frame.place(x=570,y=150,width=510,height=320)

        scrollx=Scrollbar(self.c_frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.c_frame,orient=VERTICAL)
        self.course_table=ttk.Treeview(self.c_frame,columns=("roll","name","email","gender","dob","state","address","city","pincode","contact","selectcourse","admissiondate"))
        
        # Configure scrollbars
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)
        self.course_table.configure(xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Pack scrollbars
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        # Configure columns
        self.course_table.heading("roll",text="Roll No")
        self.course_table.heading("name",text="Name")
        self.course_table.heading("email",text="Email")
        self.course_table.heading("gender",text="Gender")
        self.course_table.heading("dob",text="D.O.B")
        self.course_table.heading("state",text="State")
        self.course_table.heading("address",text="Address")
        self.course_table.heading("city",text="City")
        self.course_table.heading("pincode",text="Pin Code")
        self.course_table.heading("contact",text="Contact")
        self.course_table.heading("selectcourse",text="Course")
        self.course_table.heading("admissiondate",text="Admission Date")

        self.course_table.column("roll",width=70)
        self.course_table.column("name",width=100)
        self.course_table.column("email",width=100)
        self.course_table.column("gender",width=70)
        self.course_table.column("dob",width=100)
        self.course_table.column("state",width=100)
        self.course_table.column("address",width=100)
        self.course_table.column("city",width=100)
        self.course_table.column("pincode",width=100)
        self.course_table.column("contact",width=100)
        self.course_table.column("selectcourse",width=100)
        self.course_table.column("admissiondate",width=100)

        self.course_table["show"]='headings'
        self.course_table.pack(fill=BOTH,expand=1)
        
        # Bind table selection
        self.course_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Fetch data from database
        self.fetch_data()

    def create_database(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            
            # Create student table if it doesn't exist
            cur.execute('''CREATE TABLE IF NOT EXISTS student(
                roll TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                state TEXT,
                dob TEXT,
                selectcourse TEXT,
                contact TEXT,
                admissiondate TEXT,
                city TEXT,
                pincode TEXT,
                address TEXT
            )''')
            
            # Check if table is empty and insert test data
            cur.execute("SELECT COUNT(*) FROM student")
            count = cur.fetchone()[0]
            if count == 0:
                # Insert some test data
                test_data = [
                    ("101", "John Doe", "john@email.com", "Male", "Gujarat", "01/01/2000", "Python", "1234567890", "01/01/2024", "Ahmedabad", "380001", "Test Address 1"),
                    ("102", "Jane Smith", "jane@email.com", "Female", "Maharashtra", "02/02/2000", "Java", "9876543210", "02/01/2024", "Mumbai", "400001", "Test Address 2"),
                    ("103", "Bob Wilson", "bob@email.com", "Male", "UP", "03/03/2000", "C++", "5555555555", "03/01/2024", "Lucknow", "226001", "Test Address 3")
                ]
                cur.executemany("""INSERT INTO student 
                    (roll, name, email, gender, state, dob, selectcourse, contact, admissiondate, city, pincode, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", test_data)
                print("Test data inserted successfully")
            
            conn.commit()
            print("Database and table created successfully")
            
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def fetch_data(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
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

    def get_cursor(self, ev):
        try:
            cursor_row = self.course_table.focus()
            content = self.course_table.item(cursor_row)
            row = content["values"]
            
            if row:
                self.var_roll.set(row[0])
                self.var_name.set(row[1])
                self.var_email.set(row[2])
                self.var_gender.set(row[3])
                self.var_state.set(row[4])
                self.var_dob.set(row[5])
                self.var_selectcourse.set(row[6])
                self.var_contact.set(row[7])
                self.var_admissiondate.set(row[8])
                self.var_city.set(row[9])
                self.var_pin.set(row[10])
                self.txt_address.delete("1.0", END)
                self.txt_address.insert(END, row[11] if len(row) > 11 else "")
        except Exception as e:
            pass

    def save(self):
        if self.var_roll.get() == "" or self.var_name.get() == "" or self.var_email.get() == "" or \
           self.var_gender.get() == "Select" or self.var_state.get() == "Select" or \
           self.var_selectcourse.get() == "Select":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        elif not self.var_contact.get().isdigit():
            messagebox.showerror("Error", "Contact Number should contain only digits", parent=self.root)
        elif len(self.var_contact.get()) != 10:
            messagebox.showerror("Error", "Contact Number should be exactly 10 digits", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                
                # Check if roll number exists
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                
                if row:
                    messagebox.showerror("Error", "Roll Number already exists", parent=self.root)
                else:
                    # Insert new student
                    cur.execute("""
                        INSERT INTO student (
                            roll, name, email, gender, state,
                            dob, selectcourse, contact, admissiondate,
                            city, pincode, address
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_state.get(),
                        self.var_dob.get(),
                        self.var_selectcourse.get(),
                        self.var_contact.get(),
                        self.var_admissiondate.get(),
                        self.var_city.get(),
                        self.var_pin.get(),
                        self.txt_address.get("1.0", END).strip()
                    ))
                    
                    conn.commit()
                    self.fetch_data()
                    self.clear()
                messagebox.showinfo("Success", "Student has been added", parent=self.root)
                    
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

    def update(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll Number is required", parent=self.root)
        elif not self.var_contact.get().isdigit():
            messagebox.showerror("Error", "Contact Number should contain only digits", parent=self.root)
        elif len(self.var_contact.get()) != 10:
            messagebox.showerror("Error", "Contact Number should be exactly 10 digits", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                
                cur.execute("""
                    UPDATE student SET 
                        name=?, email=?, gender=?, state=?,
                        dob=?, selectcourse=?, contact=?, admissiondate=?,
                        city=?, pincode=?, address=?
                    WHERE roll=?
                """, (
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_gender.get(),
                    self.var_state.get(),
                    self.var_dob.get(),
                    self.var_selectcourse.get(),
                    self.var_contact.get(),
                    self.var_admissiondate.get(),
                    self.var_city.get(),
                    self.var_pin.get(),
                    self.txt_address.get("1.0", END).strip(),
                    self.var_roll.get()
                ))
                
                conn.commit()
                self.fetch_data()
                self.clear()
                messagebox.showinfo("Success", "Student has been updated", parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

    def delete(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll Number is Required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('rms.db')
                cur = conn.cursor()
                
                delete = messagebox.askyesno("Confirm", "Do you really want to delete this student?", parent=self.root)
                if delete:
                    cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                    conn.commit()
                    messagebox.showinfo("Success", "Student Deleted Successfully", parent=self.root)
                    self.clear()
                    self.fetch_data()
                    
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
            finally:
                if 'conn' in locals():
                    conn.close()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_state.set("Select")
        self.var_dob.set("")
        self.var_selectcourse.set("Select")
        self.var_contact.set("")
        self.var_admissiondate.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)

    def on_search_type_change(self, event=None):
        if self.var_search.get() == "Roll No":
            self.txt_search.place_forget()
            self.roll_combo.place(x=310, y=15, width=100)
        else:
            self.roll_combo.place_forget()
            self.txt_search.place(x=310, y=15, width=100)

    def update_roll_numbers(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            cur.execute("SELECT roll FROM student ORDER BY roll")
            rolls = [row[0] for row in cur.fetchall()]
            print(f"Found roll numbers: {rolls}")  # Debug print
            self.roll_combo['values'] = rolls
            if rolls:
                self.roll_combo.current(0)
        except Exception as es:
            print(f"Error updating roll numbers: {str(es)}")  # Debug print
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()

    def search(self):
        try:
            conn = sqlite3.connect('rms.db')
            cur = conn.cursor()
            
            search_by = self.var_search.get()
            
            if search_by == "Roll No":
                search_text = self.var_roll_search.get()
            else:
                search_text = self.txt_search.get()
            
            if not search_text:
                messagebox.showerror("Error", "Please enter search criteria", parent=self.root)
                return
            
            # Map search field to database column
            field_map = {
                "Roll No": "roll",
                "Name": "name",
                "Email": "email",
                "Contact": "contact"
            }
            
            search_field = field_map.get(search_by)
            if not search_field:
                messagebox.showerror("Error", "Invalid search field", parent=self.root)
                return
            
            # Search query
            cur.execute(f"""SELECT * FROM student 
                          WHERE {search_field} LIKE ?""",
                       ('%' + search_text + '%',))
            
            rows = cur.fetchall()
            
            if len(rows) != 0:
                self.course_table.delete(*self.course_table.get_children())
                for row in rows:
                    self.course_table.insert('', END, values=row)
            else:
                messagebox.showinfo("Not Found", "No matching records found", parent=self.root)
                
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
        finally:
            if 'conn' in locals():
                conn.close()


if __name__=="__main__":
    root=Tk()
    obj=studentClass(root)
    root.mainloop()