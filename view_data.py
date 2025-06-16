from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class DataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Registered Users")
        self.root.geometry("1000x600+200+100")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        title = Label(self.root, text="Registered Users Data", font=("goudy old style", 20, "bold"), bg="lightblue", fg="white")
        title.pack(fill=X)

        # Create Treeview
        self.tree_frame = Frame(self.root)
        self.tree_frame.place(x=0, y=40, width=1000, height=560)

        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "First Name", "Last Name", "Contact", "Email", "Security Question", "Answer"), 
                                show="headings", yscrollcommand=self.tree_scroll.set)
        
        # Set column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Security Question", text="Security Question")
        self.tree.heading("Answer", text="Answer")

        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("First Name", width=150)
        self.tree.column("Last Name", width=150)
        self.tree.column("Contact", width=100)
        self.tree.column("Email", width=200)
        self.tree.column("Security Question", width=200)
        self.tree.column("Answer", width=150)

        self.tree.pack(fill=BOTH, expand=1)
        self.tree_scroll.config(command=self.tree.yview)

        # Load data
        self.load_data()

        # Refresh button
        refresh_btn = Button(self.root, text="Refresh Data", command=self.load_data, 
                           font=("times new roman", 12), bg="lightgreen", cursor="hand2")
        refresh_btn.place(x=850, y=5, width=120, height=30)

    def load_data(self):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Connect to database
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="181103",
                database="register"
            )
            cur = con.cursor()
            
            # Fetch all records
            cur.execute("SELECT id, f_name, l_name, contact, email, question, answer FROM employee")
            rows = cur.fetchall()
            
            if rows:
                for row in rows:
                    self.tree.insert("", END, values=row)
            else:
                messagebox.showinfo("No Data", "No registered users found!", parent=self.root)
                
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

if __name__ == "__main__":
    root = Tk()
    obj = DataViewer(root)
    root.mainloop() 