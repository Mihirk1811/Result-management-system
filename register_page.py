from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import mysql

class register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register Page")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="lightblue")

#  ==== Bg Image ==
        # # Load and resize image for right side
        # img = Image.open("Images/b12.png")
        # img = img.resize((700,700), Image.Resampling.LANCZOS)  # Adjust size for right half
        # self.bg = ImageTk.PhotoImage(img)
        
        # # Place image on right side only
        # bg = Label(self.root, image=self.bg)
        # bg.place(x=300, y=0, width=700, height=700)  # Position on right side

#  ======= left image =============

        self.left=ImageTk.PhotoImage(file="Images/b4.png")
        left=Label(self.root,image=self.left).place(x=80,y=100,width=400,height=500)


#  ========== variable ==============

        self.var_firstname=StringVar()
        self.var_lastname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityanswer=StringVar()
        self.cmb_quest=StringVar()
        self.var_password=StringVar()
        self.var_confirmpassword=StringVar()
        self.var_check=IntVar()

# =========== register Frame =========== 

        frame1=Frame(self.root,bg="white")
        frame1.place(x=480,y=100,width=700,height=500)

        title1=Label(frame1,text="REGISTER HERE",font=("times new roman",25,"bold"),bg="white",fg="green").place(x=50,y=30)

        # Left side fields
        firstname=Label(frame1,text="First Name",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=50,y=100)
        self.txt_firstname = Entry(frame1, textvariable=self.var_firstname, font=("times new roman",12), bg="lightgray")
        self.txt_firstname.place(x=50, y=140, width=250)

        contact=Label(frame1,text="Contact No.",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=50,y=180)
        self.txt_contact = Entry(frame1,textvariable=self.var_contact, font=("times new roman", 12), bg="lightgray")
        self.txt_contact.place(x=50, y=220, width=250)   

        selectqueryquestion=Label(frame1,text="Select Security Question",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=50,y=260)
        cmb_quest = ttk.Combobox(frame1, 
                                  textvariable=self.cmb_quest,
                                  font=("times new roman", 13),
                                  state="readonly")
        cmb_quest['values'] = ("Select", "What is your pet name?", "Your first school name", "Your birth place", "Your best friend name")
        cmb_quest.current(0)
        cmb_quest.place(x=50, y=300, width=250)

        password=Label(frame1,text="Password",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=50,y=340)
        self.txt_password = Entry(frame1, textvariable=self.var_password, font=("times new roman", 12), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=380, width=250)

        # Right side fields
        lastname=Label(frame1,text="Last Name",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=370,y=100)
        self.txt_lastname = Entry(frame1, textvariable=self.var_lastname, font=("times new roman", 12), bg="lightgray")
        self.txt_lastname.place(x=370, y=140, width=250)

        email=Label(frame1,text="Email",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=370,y=180)
        self.txt_email = Entry(frame1, textvariable=self.var_email, font=("times new roman", 12), bg="lightgray")
        self.txt_email.place(x=370, y=220, width=250)

        answer=Label(frame1,text="Security Answer",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=370,y=260)
        self.txt_answer = Entry(frame1, textvariable=self.var_securityanswer, font=("times new roman", 12), bg="lightgray")
        self.txt_answer.place(x=370, y=300, width=250)

        confirmpass=Label(frame1,text="Confirm Password",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=370,y=340)
        self.txt_confirmpass = Entry(frame1, textvariable=self.var_confirmpassword, font=("times new roman", 12), bg="lightgray", show="*")
        self.txt_confirmpass.place(x=370, y=380, width=250)


# =========== check button =============

        self.check_btn=Checkbutton(frame1,text="I agree the terms & conditions",variable=self.var_check,font=("times new roman",12),bg="white",cursor="hand2",onvalue=1,offvalue=0)
        self.check_btn.place(x=50,y=430)

# ====== register button ==========
        # Load and resize the register button image
        img = Image.open("Images/register.png")
        img = img.resize((150, 50), Image.Resampling.LANCZOS)  # Smaller size for button
        self.btn_img = ImageTk.PhotoImage(img)
        btn = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data)
        btn.place(x=400, y=420, width=150, height=50)  # Adjusted position below checkbox

#  ========= login button =========

        loginbtn=Button(self.root,text="Sign In",font=("times new roman",20),bd=0,bg="green",fg="white",cursor="hand2")
        loginbtn.place(x=180,y=500,width=200)

#  ==============================================================================================

    def clear(self):
        self.var_firstname.set("")
        self.var_lastname.set("")
        self.var_contact.set("")
        self.var_email.set("")
        self.cmb_quest.set("Select")
        self.var_securityanswer.set("")
        self.var_password.set("")
        self.var_confirmpassword.set("")
        self.var_check.set(0)

    def register_data(self):
        if self.var_firstname.get()=="" or self.var_contact.get()=="" or self.var_email.get()=="" or self.cmb_quest.get()=="Select" or self.var_securityanswer.get()=="" or self.var_password.get()=="" or self.var_confirmpassword.get()=="":
            messagebox.showerror("Error","All Fields Are Required",parent=self.root)
        elif self.var_password.get() != self.var_confirmpassword.get():
            messagebox.showerror("Error","Password & Confirm Password should be same",parent=self.root)
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please Agree our terms & conditions",parent=self.root)
        else:
            try:
                con=mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181103",
                    database="register"
                )
                cur=con.cursor()
                cur.execute("select * from employee where email=%s",(self.var_email.get(),))
                row=cur.fetchone()

                if row!=None:
                    messagebox.showerror("Error","User already Exist,Please try with another email",parent=self.root)
                else:
                    cur.execute("insert into employee (f_name,l_name,contact,email,question,answer,password) values(%s,%s,%s,%s,%s,%s,%s)",
                        (
                            self.var_firstname.get(),
                            self.var_lastname.get(),
                            self.var_contact.get(),
                            self.var_email.get(),
                            self.cmb_quest.get(),
                            self.var_securityanswer.get(),
                            self.var_password.get()
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Register Successful",parent=self.root)
                    self.clear()
                    
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=register(root)
    root.mainloop()