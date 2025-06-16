from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import os
import math
import random

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Login")
        # Set minimum size and start maximized
        self.root.minsize(1350, 700)
        self.root.state('zoomed')
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.root.config(bg="#f0f0f0")
        
        # Variables
        self.username_var = StringVar()
        self.password_var = StringVar()
        
        # Main container using Grid
        self.main_container = Frame(self.root, bg="#f0f0f0")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create canvas for background designs
        self.bg_canvas = Canvas(self.main_container, bg="#f0f0f0", highlightthickness=0)
        self.bg_canvas.grid(row=0, column=0, rowspan=3, sticky="nsew")
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        
        # Draw initial background
        self.draw_background()
        
        # Title at the top
        title_frame = Frame(self.main_container, bg="#f0f0f0")
        title_frame.grid(row=0, column=0, pady=20, sticky="ew")
        
        title = Label(title_frame, text="Student Management System",
                     font=("Arial", 36, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack()
        
        subtitle = Label(title_frame, text="Welcome Back!",
                        font=("Arial", 16), bg="#f0f0f0", fg="#34495e")
        subtitle.pack(pady=10)
        
        # Center frame for login
        center_frame = Frame(self.main_container, bg="#f0f0f0")
        center_frame.grid(row=1, column=0, sticky="nsew")
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        
        # Login Frame
        self.login_frame = Frame(center_frame, bg="white", bd=2, relief=RIDGE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=400)
        
        # Title
        title = Label(self.login_frame, text="Student Login",
                     font=("Arial", 20, "bold"), bg="white", fg="#2c3e50")
        title.place(relx=0.5, y=30, anchor=CENTER)
        
        # Username
        username_lbl = Label(self.login_frame, text="Username",
                           font=("Arial", 12), bg="white", fg="#2c3e50")
        username_lbl.place(relx=0.125, rely=0.25)
        
        self.username_entry = Entry(self.login_frame, textvariable=self.username_var,
                                  font=("Arial", 12), bg="#f8f9fa", bd=1)
        self.username_entry.place(relx=0.125, rely=0.35, relwidth=0.75, height=35)
        
        # Password
        password_lbl = Label(self.login_frame, text="Password",
                           font=("Arial", 12), bg="white", fg="#2c3e50")
        password_lbl.place(relx=0.125, rely=0.5)
        
        self.password_entry = Entry(self.login_frame, textvariable=self.password_var,
                                  font=("Arial", 12), bg="#f8f9fa", bd=1, show="•")
        self.password_entry.place(relx=0.125, rely=0.6, relwidth=0.75, height=35)
        
        # Login Button
        self.login_btn = Button(self.login_frame, text="LOGIN", command=self.login,
                              font=("Arial", 12, "bold"), bg="#2c3e50", fg="white",
                              bd=0, cursor="hand2", activebackground="#34495e")
        self.login_btn.place(relx=0.125, rely=0.75, relwidth=0.75, height=35)
        
        # Separator
        separator = ttk.Separator(self.login_frame, orient='horizontal')
        separator.place(relx=0.125, rely=0.9, relwidth=0.75)
        
        # Additional Buttons Frame
        btn_frame = Frame(self.login_frame, bg="white")
        btn_frame.place(relx=0.125, rely=0.92, relwidth=0.75, height=30)
        
        # Forgot Password Button
        forgot_btn = Button(btn_frame, text="Forgot Password?",
                          font=("Arial", 10), bg="white", fg="#2c3e50",
                          bd=0, cursor="hand2", command=self.forgot_password)
        forgot_btn.pack(side=LEFT)
        
        # Register Button
        register_btn = Button(btn_frame, text="New Registration",
                            font=("Arial", 10), bg="white", fg="#2c3e50",
                            bd=0, cursor="hand2", command=self.register_window)
        register_btn.pack(side=RIGHT)
        
        # Footer
        footer = Label(self.main_container, text="© 2024 Student Management System. All rights reserved.",
                      font=("Arial", 10), bg="#f0f0f0", fg="#7f8c8d")
        footer.grid(row=2, column=0, pady=10)
        
        # Bind events for hover effects
        self.login_btn.bind("<Enter>", self.on_enter)
        self.login_btn.bind("<Leave>", self.on_leave)
        forgot_btn.bind("<Enter>", lambda e: forgot_btn.config(fg="#3498db"))
        forgot_btn.bind("<Leave>", lambda e: forgot_btn.config(fg="#2c3e50"))
        register_btn.bind("<Enter>", lambda e: register_btn.config(fg="#3498db"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(fg="#2c3e50"))
        
    def on_enter(self, e):
        self.login_btn.config(bg="#34495e")
        
    def on_leave(self, e):
        self.login_btn.config(bg="#2c3e50")
        
    def connect_db(self):
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="181103",
                database="register"
            )
            return con
        except Exception as es:
            messagebox.showerror("Error", f"Database Connection Error: {str(es)}", parent=self.root)
            return None
        
    def login(self):
        if self.username_var.get() == "" or self.password_var.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = self.connect_db()
                if con:
                    cur = con.cursor(buffered=True)
                    # First verify the table exists
                    cur.execute("SHOW TABLES LIKE 'users'")
                    if not cur.fetchone():
                        messagebox.showerror("Error", "Database table not found. Please run setup script first.", parent=self.root)
                        return
                        
                    # Now try to login
                    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                              (self.username_var.get(), self.password_var.get()))
                    row = cur.fetchone()
                    
                    if row is None:
                        messagebox.showerror("Error", "Invalid Username & Password", parent=self.root)
                    else:
                        messagebox.showinfo("Success", f"Welcome {row[1]}!", parent=self.root)
                        self.root.destroy()
                        # Open dashboard
                        import dashboard
                        root = Tk()
                        obj = dashboard.DashboardClass(root)
                        root.mainloop()
                    con.close()
                
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root)
                
    def forgot_password(self):
        messagebox.showinfo("Info", "Please contact administrator", parent=self.root)
        
    def register_window(self):
        messagebox.showinfo("Info", "Registration coming soon!", parent=self.root)

    def draw_background(self):
        # Clear previous drawings
        self.bg_canvas.delete("all")
        
        # Get current window dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Calculate scaling factors based on screen size
        scale_factor = min(width/1920, height/1080)  # Base resolution 1920x1080
        
        # Draw classroom wall with gradient effect
        gradient_steps = 50
        for i in range(gradient_steps):
            y = i * (height / gradient_steps)
            color = self._interpolate_color("#e8f4f8", "#d4e6f1", i/gradient_steps)
            self.bg_canvas.create_rectangle(0, y, width, y + (height/gradient_steps),
                                         fill=color, outline=color)
        
        # Draw floor with better wooden texture
        floor_y = height * 0.8  # Moved floor down
        self.bg_canvas.create_rectangle(0, floor_y, width, height,
                                      fill="#8b4513", outline="#8b4513")
        
        # Floor boards
        board_width = 100 * scale_factor
        num_boards = int(width / board_width) + 1
        for i in range(num_boards):
            x = i * board_width
            # Main board
            self.bg_canvas.create_rectangle(x, floor_y, x+board_width-2, height,
                                         fill="#deb887", outline="#8b4513")
            # Wood grain lines
            for j in range(4):
                y = floor_y + (j * 30)
                self.bg_canvas.create_line(x, y, x+board_width-2, y,
                                        fill="#8b4513", width=1)
        
        # Draw improved blackboard
        board_width = width * 0.5  # Reduced width
        board_height = height * 0.35  # Reduced height
        board_x = (width - board_width) / 2
        board_y = height * 0.2  # Moved down
        
        # Blackboard outer frame (darker wood)
        frame_width = 25 * scale_factor
        self.bg_canvas.create_rectangle(board_x-frame_width, board_y-frame_width,
                                      board_x+board_width+frame_width, 
                                      board_y+board_height+frame_width,
                                      fill="#654321", outline="#3d2914")
        
        # Inner frame (lighter wood)
        self.bg_canvas.create_rectangle(board_x-frame_width+5, board_y-frame_width+5,
                                      board_x+board_width+frame_width-5, 
                                      board_y+board_height+frame_width-5,
                                      fill="#8b4513", outline="#654321")
        
        # Blackboard surface
        self.bg_canvas.create_rectangle(board_x, board_y,
                                      board_x+board_width, board_y+board_height,
                                      fill="#2c3e50", outline="#234567")
        
        # Add chalk residue effect
        for _ in range(50):
            x = board_x + (board_width * random.random())
            y = board_y + (board_height * random.random())
            size = random.randint(2, 5) * scale_factor
            opacity = random.randint(5, 8) * 0.1
            color = self._interpolate_color("#2c3e50", "#ffffff", opacity)
            self.bg_canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
        
        # Improved chalk tray
        tray_height = 20 * scale_factor
        self.bg_canvas.create_rectangle(board_x-frame_width, 
                                      board_y+board_height+frame_width,
                                      board_x+board_width+frame_width, 
                                      board_y+board_height+frame_width+tray_height,
                                      fill="#8b4513", outline="#654321")
        
        # Add chalk pieces in tray
        for i in range(5):
            chalk_x = board_x + (i * 50 * scale_factor) + 20
            chalk_y = board_y + board_height + frame_width + 5
            self.draw_chalk(chalk_x, chalk_y, scale_factor)
        
        # Draw welcome text with chalk effect
        text = "Welcome to\nStudent Management System"
        font_size = int(36 * scale_factor)
        self.draw_chalk_text(board_x + board_width/2, board_y + board_height/2,
                           text, ("Segoe Print", font_size, "bold"))
        
        # Draw improved teacher's desk
        desk_width = width * 0.3  # Reduced width
        desk_height = height * 0.1  # Reduced height
        desk_x = (width - desk_width) / 2
        desk_y = height * 0.75  # Moved down
        
        # Desk shadow
        shadow_offset = 15 * scale_factor
        self.bg_canvas.create_polygon(desk_x+shadow_offset, desk_y+shadow_offset,
                                    desk_x+desk_width+shadow_offset, desk_y+shadow_offset,
                                    desk_x+desk_width+shadow_offset, height*0.8+shadow_offset,
                                    desk_x+shadow_offset, height*0.8+shadow_offset,
                                    fill="#000000", outline="", stipple="gray50")
        
        # Desk top with 3D effect
        self.bg_canvas.create_polygon(desk_x, desk_y,
                                    desk_x+desk_width, desk_y,
                                    desk_x+desk_width, height*0.8,
                                    desk_x, height*0.8,
                                    fill="#8b4513", outline="#654321")
        
        # Desk front panel with gradient
        gradient_steps = 20
        panel_height = (height * 0.8 - desk_y) / gradient_steps
        for i in range(gradient_steps):
            y = desk_y + (i * panel_height)
            color = self._interpolate_color("#8b4513", "#654321", i/gradient_steps)
            self.bg_canvas.create_rectangle(desk_x+10, y,
                                         desk_x+desk_width-10, y+panel_height+1,
                                         fill=color, outline="")
        
        # Draw items on desk
        self.draw_desk_items(desk_x, desk_y, desk_width, desk_height, scale_factor)
        
        # Draw wall decorations
        self.draw_wall_decorations(width, height, board_x, board_y, board_width, scale_factor)
        
    def draw_chalk(self, x, y, scale_factor):
        # Draw chalk piece with shadow
        size = 15 * scale_factor
        self.bg_canvas.create_rectangle(x-1, y-1, x+size, y+size/2,
                                      fill="#ffffff", outline="#ebebeb")
        self.bg_canvas.create_rectangle(x, y, x+size-1, y+size/2-1,
                                      fill="#f5f5f5", outline="#ebebeb")
        
    def draw_chalk_text(self, x, y, text, font):
        # Create chalk text effect
        offset = 1
        # Shadow layer
        self.bg_canvas.create_text(x+offset, y+offset, text=text,
                                 font=font, fill="#1a2733", justify=CENTER)
        # Main text
        self.bg_canvas.create_text(x, y, text=text,
                                 font=font, fill="#ffffff", justify=CENTER)
        
    def draw_desk_items(self, desk_x, desk_y, desk_width, desk_height, scale_factor):
        # Draw books with 3D effect
        book_colors = ["#e74c3c", "#3498db", "#2ecc71"]
        for i, color in enumerate(book_colors):
            x = desk_x + 50 + (i * 40 * scale_factor)
            y = desk_y + 10
            self.draw_3d_book(x, y, color, scale_factor)
        
        # Draw improved globe
        globe_x = desk_x + desk_width - 100 * scale_factor
        globe_y = desk_y + 20
        self.draw_improved_globe(globe_x, globe_y, scale_factor)
        
        # Draw pencil holder with pencils
        holder_x = desk_x + desk_width - 180 * scale_factor
        holder_y = desk_y + 15
        self.draw_pencil_holder(holder_x, holder_y, scale_factor)
        
    def draw_3d_book(self, x, y, color, scale_factor):
        # Book spine
        size = 30 * scale_factor
        self.bg_canvas.create_polygon(x, y, x+size, y, x+size, y+size*1.3, x, y+size*1.3,
                                    fill=color, outline="#2c3e50")
        # Book cover
        darker_color = self._interpolate_color(color, "#000000", 0.2)
        self.bg_canvas.create_polygon(x+size, y, x+size*1.2, y+size*0.2, x+size*1.2, y+size*1.5, x+size, y+size*1.3,
                                    fill=darker_color, outline="#2c3e50")
        # Book top
        lighter_color = self._interpolate_color(color, "#ffffff", 0.2)
        self.bg_canvas.create_polygon(x, y, x+size, y, x+size*1.2, y+size*0.2, x+size*0.2, y+size*0.2,
                                    fill=lighter_color, outline="#2c3e50")
        
    def draw_improved_globe(self, x, y, scale_factor):
        # Stand base
        size = 20 * scale_factor
        self.bg_canvas.create_oval(x-size*0.75, y+size*2.25, x+size*0.75, y+size*2.75,
                                 fill="#34495e", outline="#2c3e50")
        # Stand pole
        self.bg_canvas.create_rectangle(x-size*0.1, y+size*0.5, x+size*0.1, y+size*2.5,
                                      fill="#34495e", outline="#2c3e50")
        
        # Globe with gradient
        for i in range(30):
            self.bg_canvas.create_oval(x-size+i/2, y-size+i/2, x+size-i/2, y+size-i/2,
                                     fill=self._interpolate_color("#3498db", "#2980b9", i/30),
                                     outline="")
        
        # Longitude/latitude lines
        for i in range(6):
            angle = i * 30
            self.bg_canvas.create_arc(x-size, y-size, x+size, y+size,
                                    start=angle, extent=2,
                                    fill="#fff")
            self.bg_canvas.create_arc(x-size, y-size, x+size, y+size,
                                    start=angle+90, extent=2,
                                    fill="#fff")
        
    def draw_pencil_holder(self, x, y, scale_factor):
        # Holder
        size = 15 * scale_factor
        self.bg_canvas.create_rectangle(x-size, y, x+size, y+size*2,
                                      fill="#34495e", outline="#2c3e50")
        # Pencils
        colors = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db"]
        for i, color in enumerate(colors):
            offset = (i - len(colors)/2) * 6 * scale_factor
            self.draw_pencil(x+offset, y-size, color, scale_factor)
            
    def draw_pencil(self, x, y, color, scale_factor):
        # Pencil body
        size = 2 * scale_factor
        length = 25 * scale_factor
        self.bg_canvas.create_rectangle(x-size, y, x+size, y+length,
                                      fill=color, outline="#2c3e50")
        # Pencil tip
        self.bg_canvas.create_polygon(x-size, y+length, x+size, y+length, x, y+length+size*2.5,
                                    fill="#34495e", outline="#2c3e50")
        
    def _interpolate_color(self, color1, color2, factor):
        # Convert hex colors to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_wall_decorations(self, width, height, board_x, board_y, board_width, scale_factor):
        # Draw clock
        clock_x = width * 0.1
        clock_y = height * 0.15
        size = 30 * scale_factor
        self.bg_canvas.create_oval(clock_x-size, clock_y-size,
                                 clock_x+size, clock_y+size,
                                 fill="white", outline="#34495e", width=2)
        # Clock hands
        self.bg_canvas.create_line(clock_x, clock_y,
                                 clock_x+size*0.5, clock_y-size*0.3,
                                 fill="#34495e", width=2)
        self.bg_canvas.create_line(clock_x, clock_y,
                                 clock_x-size*0.2, clock_y+size*0.7,
                                 fill="#34495e", width=2)
        
        # Draw educational posters
        poster_y = height * 0.25
        for i in range(3):
            poster_x = width * (0.85 - i * 0.15)
            self.draw_poster(poster_x, poster_y, scale_factor)
            
    def draw_poster(self, x, y, scale_factor):
        # Poster background
        size = 40 * scale_factor
        self.bg_canvas.create_rectangle(x-size, y-size, x+size, y+size,
                                      fill="#ecf0f1", outline="#bdc3c7")
        # Poster content (simple shapes)
        shapes = ["A", "1", "?"]
        font_size = int(24 * scale_factor)
        self.bg_canvas.create_text(x, y,
                                 text=shapes[int(x) % 3],
                                 font=("Arial", font_size, "bold"),
                                 fill="#2c3e50")
        
    def on_resize(self, event):
        # Redraw background when window is resized
        if event.widget == self.root:
            # Update canvas size
            self.bg_canvas.configure(width=event.width, height=event.height)
            # Redraw background elements
            self.draw_background()
            

if __name__ == "__main__":
    root = Tk()
    obj = LoginPage(root)
    root.mainloop()
