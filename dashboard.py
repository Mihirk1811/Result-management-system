from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
import time
import mysql.connector

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.state('zoomed')  # Start maximized
        self.root.config(bg="#f0f0f0")

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(2, weight=1)  # Content area row
        self.root.grid_columnconfigure(0, weight=1)

        # ==== Load icons ====
        try:
            # Load and resize the logo
            logo_img = Image.open("Images/icon.png")
            logo_img = logo_img.resize((40,40), Image.Resampling.LANCZOS)
            self.logo_dash = ImageTk.PhotoImage(logo_img)
        except:
            self.logo_dash = None

        # ==== Title Frame ====
        title_frame = Frame(self.root, bg="#033054", bd=2, relief=RIDGE)
        title_frame.grid(row=0, column=0, sticky="ew")
        
        # Title with logo
        if self.logo_dash:
            title = Label(title_frame, text=" STUDENT RESULT MANAGEMENT SYSTEM", image=self.logo_dash,
                         compound=LEFT, padx=20, bg="#033054", fg="white",
                         font=("Helvetica", 30, "bold"))
        else:
            title = Label(title_frame, text="STUDENT RESULT MANAGEMENT SYSTEM",
                         padx=20, bg="#033054", fg="white",
                         font=("Helvetica", 30, "bold"))
        title.pack(side=LEFT, pady=10)

        # Clock
        self.clock_label = Label(title_frame, text="", font=("Helvetica", 15),
                                bg="#033054", fg="white")
        self.clock_label.pack(side=RIGHT, padx=20)
        self.update_clock()

        # ==== Menu Frame ====
        menu_frame = LabelFrame(self.root, text=" Menu ", font=("times new roman", 20, "bold"),
                              bg="white", bd=2, relief=RIDGE)
        menu_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Center container for buttons
        center_container = Frame(menu_frame, bg="white")
        center_container.pack(expand=True, fill="both")
        
        # Configure grid for center container
        center_container.grid_columnconfigure(0, weight=1)  # Left padding
        center_container.grid_columnconfigure(7, weight=1)  # Right padding
        
        # Button style
        btn_style = {
            "font": ("times new roman", 15, "bold"),
            "bg": "#002B5B",  # Darker blue color
            "fg": "white",
            "cursor": "hand2",
            "relief": RAISED,
            "width": 18,
            "height": 2
        }

        # Create buttons with exact spacing
        buttons = [
            ("Course", self.add_course),
            ("Student", self.add_student),
            ("Result", self.add_result),
            ("View Student Result", self.add_report),
            ("Logout", self.logout),
            ("Exit", self.exit_app)
        ]

        # Place buttons in grid with padding
        for i, (text, command) in enumerate(buttons):
            Button(center_container, text=text, command=command, **btn_style).grid(
                row=0, column=i+1, padx=2, pady=10
            )

        # ==== Content Area ====
        content_frame = Frame(self.root, bd=2, relief=RIDGE)
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Configure content frame grid
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        try:
            # Load and display background image
            self.bg_img = Image.open("Images/bg.png")
            # Calculate the size to maintain aspect ratio
            display_width = min(1300, self.root.winfo_screenwidth() - 100)
            display_height = int(display_width * 0.4)  # Maintain aspect ratio
            
            self.bg_img = self.bg_img.resize((display_width, display_height), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            
            self.bg_label = Label(content_frame, image=self.bg_img, bg="#f0f0f0")
            self.bg_label.grid(row=0, column=0, sticky="nsew")
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_label = Label(content_frame, bg="#e0e0e0")
            self.bg_label.grid(row=0, column=0, sticky="nsew")

        # ==== Statistics Frame ====
        stats_frame = Frame(self.root, bg="#f0f0f0")
        stats_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Configure stats frame for equal column weights
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)

        # Base style for stats cards
        stats_base_style = {
            "font": ("times new roman", 20, "bold"),
            "bd": 2,
            "relief": RIDGE,
            "fg": "white",
            "height": 3
        }

        # Create statistics labels with different colors
        self.lbl_course = Label(stats_frame, text="Total Courses\n[ 0 ]", 
                              bg="#002B5B",  # Navy blue
                              **stats_base_style)
        self.lbl_course.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.lbl_student = Label(stats_frame, text="Total Students\n[ 0 ]",
                               bg="#003B73",  # Royal blue
                               **stats_base_style)
        self.lbl_student.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.lbl_result = Label(stats_frame, text="Total Results\n[ 0 ]",
                              bg="#0A4D68",  # Steel blue
                              **stats_base_style)
        self.lbl_result.grid(row=0, column=2, padx=10, sticky="ew")

        # ==== Footer ====
        footer_frame = Frame(self.root, bg="#033054", bd=1, relief=RIDGE)
        footer_frame.grid(row=4, column=0, sticky="ew")

        footer_text = "SRMS - Student Result Management System  |  Contact us for technical support: 63521xxx20"
        Label(footer_frame, text=footer_text, font=("arial", 12),
              bg="#033054", fg="white").pack(pady=2)

        # Initialize counters and start updates
        self.update_details()
        # Update counts every 5 seconds
        self.root.after(5000, self.update_details)

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        # Only handle if the root window is resized
        if event.widget == self.root:
            try:
                # Recalculate image size
                display_width = min(1300, event.width - 100)
                display_height = int(display_width * 0.4)
                
                # Resize and update background image
                if hasattr(self, 'bg_img') and isinstance(self.bg_img, ImageTk.PhotoImage):
                    new_img = Image.open("Images/bg.png")
                    new_img = new_img.resize((display_width, display_height), Image.Resampling.LANCZOS)
                    self.bg_img = ImageTk.PhotoImage(new_img)
                    self.bg_label.configure(image=self.bg_img)
            except Exception as e:
                print(f"Error resizing image: {e}")

    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%d-%m-%Y")
        self.clock_label.config(text=f"{current_date}\n{current_time}")
        self.root.after(1000, self.update_clock)

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return None

    def get_count(self, table_name):
        connection = self.get_db_connection()
        
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                return count
            except Exception as e:
                print(f"Error fetching {table_name} count: {str(e)}")
                return 0
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return 0

    def update_details(self):
        try:
            # Get counts from database
            course_count = self.get_count("course")
            student_count = self.get_count("student")
            result_count = self.get_count("result")

            # Update labels with new counts
            self.lbl_course.config(text=f"Total Courses\n[ {course_count} ]")
            self.lbl_student.config(text=f"Total Students\n[ {student_count} ]")
            self.lbl_result.config(text=f"Total Results\n[ {result_count} ]")

        except Exception as e:
            print(f"Error updating details: {str(e)}")
        finally:
            # Schedule next update
            self.root.after(5000, self.update_details)

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
    
    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)
    
    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)
    
    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

    def logout(self):
        self.root.destroy()
        # Add code to return to login page

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()