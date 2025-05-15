import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
from user.dashboard import user_dashboard, user
from admin.dashboard import admin_dashboard
import csv
import time

class PharmoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmora")
        self.root.state("zoomed") 

        # self.admin_display_frame = tk.Frame(self.root, bg=self.bg_color)
        
        try:
            self.baloo_font = font.Font(family="Baloo Bhai 2", size=12)
            self.roboto_flex_font = font.Font(family="Roboto Flex", size=12)
            
            if "Baloo Bhai 2" not in font.families():
                self.baloo_font = font.Font(family="Arial", size=12)
            if "Roboto Flex" not in font.families():
                self.roboto_flex_font = font.Font(family="Arial", size=12)
        except:
            self.baloo_font = font.Font(family="Arial", size=12)
            self.roboto_flex_font = font.Font(family="Arial", size=12)
        
        self.bg_color = "#552626"
        self.pink_display = "#ffd6e7"
        self.button_color = "#ff6b9d"
        self.white = "#fffff0"
        self.dark_text = "#333333"
        self.gray_text = "#666666"
        
        self.current_user = None
        self.current_role = None
        
        self.medicines = [
            {"name": "Paracetamol", "desc": "Pain reliever and fever reducer", "dose": "500mg"},
            {"name": "Ibuprofen", "desc": "Anti-inflammatory pain reliever", "dose": "200mg"},
            {"name": "Amoxicillin", "desc": "Antibiotic for bacterial infections", "dose": "250mg"},
            {"name": "Loratadine", "desc": "Antihistamine for allergies", "dose": "10mg"},
            {"name": "Omeprazole", "desc": "Reduces stomach acid", "dose": "20mg"}
        ]
        self.favorites = []
        self.history = []
        
        self.current_frame = None
        self.setup_welcome_screen()
        
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        

    def setup_welcome_screen(self):
        """Page 1: Welcome screen with background image"""
        self.clear_frame()

        self.root.state('zoomed')  # Windows-only fullscreen
        self.root.update_idletasks()  # Ensure size is updated
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Buat canvas
        self.current_frame = tk.Canvas(self.root, width=width, height=height)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Load image background
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/1st page.png"
        self.bg_image = Image.open(bg_path).resize((width, height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Tampilkan gambar di canvas
        self.current_frame.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)

        # Load custom font (Baloo Bhai 2)
        font_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf"
        baloo_font = ("Baloo Bhai 2", 20, "bold")


        # Buat tombol gambar
        get_started_btn = tk.Button(
            self.root,
            text="Get Started",
            font=baloo_font,
            bg="#FF6B9D",  # Pink color
            fg="#fffff0",
            relief=tk.FLAT,
            command=self.setup_role_selection,
            padx=20,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )


        # Tempatkan tombol di tengah bawah
        get_started_btn.place(x=width // 2 - 115, y=height - 350, width=230, height=60)

    def setup_role_selection(self):
        """Page 2: Role selection with image background and buttons"""
        self.clear_frame()

        # Load background image
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/which one.png"
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load custom font (Baloo Bhai 2)
        font_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf"
        baloo_font = (r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf", 40, "bold")


        # Button colors (pink)
        button_color = "#FF6B9D"

        # Admin button
        admin_btn = tk.Button(
            self.root,
            text="Admin",
            font=baloo_font,
            bg=button_color,
            fg="#fffff0",
            relief=tk.FLAT,
            command=lambda: self.setup_auth_screen("admin"),
            padx=40,
            pady=15,
            width=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        admin_btn.place(x=screen_width // 2 - 460, y=770, width=240, height=100)

        # User button
        user_btn = tk.Button(
            self.root,
            text="User",
            font=baloo_font,
            bg=button_color,
            fg="#fffff0",
            relief=tk.FLAT,
            command=lambda: self.setup_auth_screen("user"),
            padx=40,
            pady=15,
            width=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        user_btn.place(x=screen_width // 2 +230, y=770, width=235, height=100)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=(baloo_font, 12),
            fg="#fffff0",
            relief=tk.FLAT,
            command=self.setup_welcome_screen,
            padx=0,
            pady=20,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        back_btn.place(x=10, y=screen_height - 30)

    def setup_auth_screen(self, role):
        """Page 3: Sign Up screen with background image (no text, only input fields and buttons)"""
        self.clear_frame()

        # Load background image
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/welcome back.png"
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Hitung posisi tengah layar
        right_x = screen_width//2  
        input_y = screen_height //2

        font_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf"

        # Username entry
        self.username_entry = tk.Entry(
            self.root,
            font=(font_path, 14),
            relief=tk.FLAT,
            bg="#fffff0",
            fg="#FF6B9D",
            borderwidth=0,
            highlightthickness=0,
            highlightbackground="#fffff0",
            highlightcolor=self.button_color
        )
        self.username_entry.place(x=right_x+160, y=input_y-110, width=640, height=60)

        # Password entry
        self.password_entry = tk.Entry(
            self.root,
            font=(font_path, 14),
            relief=tk.FLAT,
            bg="#fffff0",
            fg="#FF6B9D",
            show="*",
            borderwidth=0,
            highlightthickness=0,
            highlightbackground="#fffff0",
            highlightcolor=self.button_color
        )
        self.password_entry.place(x=right_x+150 , y=input_y+70, width=650, height=60)

        # Sign-in button
        sign_in_btn = tk.Button(
            self.root,
            text="Sign In",
            font=(self.baloo_font, 14, "bold"),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            command=lambda: self.setup_register_screen(role),
            padx=30,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        sign_in_btn.place(x=350, y=input_y+60, width=250, height=60)

        sign_up_btn = tk.Button(
            self.root,
            text="Sign Up",
            font=(self.baloo_font, 14, "bold"),
            fg=self.button_color,
            bg=self.white,
            relief=tk.FLAT,
            command=lambda: self.setup_register_screen(role),
            padx=30,
            pady=10,
            activebackground="#fffff0", 
            activeforeground="#fffff0",
            borderwidth=0,  
            highlightthickness=0 
        )
        sign_up_btn.place(x=screen_width//2+350, y=screen_height//2+200, width=250, height=60)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=(font_path, 14),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,  
            command=self.setup_role_selection,
            padx=30,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        back_btn.place(x=320, y=input_y+400, width=300, height=40)


    def setup_register_screen(self, role):
        """Page 4: Sign in screen (7.png)"""
        self.clear_frame()
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/hi there.png"
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Hitung posisi tengah layar
        right_x = screen_width//2  
        input_y = screen_height //2

        font_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf"

        # Username entry
        self.username_entry = tk.Entry(
            self.root,
            font=(font_path, 14),
            relief=tk.FLAT,
            bg="#fffff0",
            fg="#FF6B9D",
            borderwidth=0,
            highlightthickness=0,
            highlightbackground="#fffff0",
            highlightcolor=self.button_color
        )
        self.username_entry.place(x=right_x-800, y=input_y-65, width=650, height=60)

        # Password entry
        self.password_entry = tk.Entry(
            self.root,
            font=(font_path, 14),
            relief=tk.FLAT,
            bg="#fffff0",
            fg="#FF6B9D",
            show="*",
            borderwidth=0,
            highlightthickness=0,
            highlightbackground="#fffff0",
            highlightcolor=self.button_color
        )
        self.password_entry.place(x=right_x-800 , y=input_y+125, width=650, height=60)

        # Sign-in button
        sign_in_btn = tk.Button(
            self.root,
            text="Sign In",
            font=(self.baloo_font, 14, "bold"),
            bg="#fffff0",
            fg="#FF6B9D",
            relief=tk.FLAT,
            command=lambda: self.authenticate(role),
            padx=30,
            pady=10,
            activebackground="#fffff0", 
            activeforeground="#fffff0",
            borderwidth=0,  
            highlightthickness=0 
        )
        sign_in_btn.place(x=350, y=input_y+250, width=250, height=60)

        sign_up_btn = tk.Button(
            self.root,
            text="Sign Up",
            font=(self.baloo_font, 14, "bold"),
            fg="#fffff0",
            bg="#FF6B9D",
            relief=tk.FLAT,
            command=lambda: self.authenticate(self, role),
            padx=30,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        sign_up_btn.place(x=screen_width//2+350, y=screen_height//2+40, width=250, height=60)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=(font_path, 14),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,  
            command=self.setup_role_selection,
            padx=30,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        back_btn.place(x=1250, y=input_y+400, width=300, height=40)

        
    def authenticate(self, role):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return
        
        self.current_user = username
        self.current_role = role
        
        if role == "admin":
            self.setup_admin_dashboard()
        else:
            self.setup_user_dashboard()
        
        # In real implementation, you would use:
        # authenticate_user(username, password, role)
        # self.current_user = username
        # self.current_role = role
        # if role == "admin":
        #     self.setup_admin_dashboard()
        # else:
        #     self.setup_user_dashboard()
    def register(self, role):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Registration Failed", "Please fill in all fields.")
            return
            
        messagebox.showinfo("Registration Success", "Account created successfully!")
        self.setup_auth_screen(role)


    def setup_admin_dashboard(self):
        """Page 5: Admin main menu with background image"""
        self.clear_frame()

        # Inisialisasi admin_display_frame
        self.admin_display_frame = tk.Frame(self.root, bg=self.bg_color)
        self.admin_display_frame.pack(fill=tk.BOTH, expand=True)

        # Load background image
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin's.png"
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.admin_display_frame, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        baloo_font = (r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf", 40, "bold")

        # Button container
        left_button_frame = tk.Frame(self.root)
        left_button_frame.place(x=20, rely=0.5, anchor=tk.W)

        left_buttons = [
            ("Display All Medicine", lambda: self.setup_admin_manage_medicines()),
            ("Add Medicine", lambda: self.setup_admin_add_medicine())
        ]

        for text, command in left_buttons:
            btn = tk.Button(
                left_button_frame,
                text=text,
                font=(baloo_font, 12, "bold"),
                bg='#FF6B9D',  # Green color
                fg='white',
                relief=tk.FLAT,
                command=command,
                padx=30,
                pady=10
            )
            btn.pack(pady=10, fill=tk.X)

        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=(baloo_font, 16),
            fg="#fffff0",
            bg='#FF6B9D',
            relief=tk.FLAT,
            command=self.setup_welcome_screen,
            padx=10,
            pady=10,
            activebackground="#FF6B9D", 
            activeforeground="#FF6B9D",
            borderwidth=0,  
            highlightthickness=0 
        )
        back_btn.place(x=400, y=40, width=250, height=50)

        main_menu_btn = tk.Button(
            self.root,
            text="Main Menu",
            font=(baloo_font, 16),
            fg="#fffff0",
            bg='#FF6B9D',
            relief=tk.FLAT,
            command=self.setup_admin_dashboard,  
            padx=10,
            pady=10,
            activebackground="#FF6B9D",
            activeforeground="#FF6B9D",
            borderwidth=0,
            highlightthickness=0
        )
        main_menu_btn.place(x=760, y=40, width=250, height=50) 

        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=(baloo_font, 22),
            fg="#fffff0",
            bg='#552626',
            relief=tk.FLAT,
            command=self.setup_welcome_screen,
            padx=10,
            pady=10,
            activebackground="#552626", 
            activeforeground="#552626",
            borderwidth=0,  
            highlightthickness=0 
        )
        exit_btn.place(x=1500, y=screen_height//2+400,  width=300, height=40)

    def setup_admin_manage_medicines(self):
        """Page 6: Admin manage medicines (display all)"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        # Load display medicine background
        display_bg_path = r"C:\Users\LOQ\Python latihan\college studies\2nd semester\Pharmora-main\assets\images\admin display medicine.png"
        if os.path.exists(display_bg_path):
            display_bg = Image.open(display_bg_path)
            display_bg = display_bg.resize((self.admin_display_frame.winfo_width(), self.admin_display_frame.winfo_height()), Image.LANCZOS)
            self.display_bg_photo = ImageTk.PhotoImage(display_bg)
            bg_label = tk.Label(self.admin_display_frame, image=self.display_bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container
        main_frame = tk.Frame(self.admin_display_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with sort options
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text="Manage Medicines",
            font=('Arial', 16, "bold"),
            bg='white',
            fg='black'
        )
        title_label.pack(side=tk.LEFT)
        
        # Sort buttons
        sort_frame = tk.Frame(header_frame, bg='white')
        sort_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            sort_frame,
            text="Newest First",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.sort_medicines('newest')
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            sort_frame,
            text="Oldest First",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.sort_medicines('oldest')
        ).pack(side=tk.LEFT, padx=5)
        
        # Medicine list
        meds_frame = tk.Frame(main_frame, bg='white')
        meds_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(meds_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(meds_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load medicines from CSV
        self.load_medicines_from_csv()
        
        for idx, med in enumerate(self.medicines):
            med_frame = tk.Frame(scrollable_frame, bg='#FFCDD2', relief=tk.RAISED, bd=1)  # Light red/pink
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"Name: {med['name']}\nComposition: {med['composition']}\nSide Effects: {med['side_effect']}",
                font=('Arial', 12),
                bg='#FFCDD2',
                fg='black',
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            remove_btn = tk.Button(
                med_frame,
                text="✕ Delete",
                font=('Arial', 10),
                bg='#FFCDD2',
                fg='#D32F2F',  # Dark red
                relief=tk.FLAT,
                command=lambda m=med: self.remove_medicine(m)
            )
            remove_btn.pack(side=tk.RIGHT, padx=10)
            
        if not self.medicines:
            empty_label = tk.Label(
                scrollable_frame,
                text="No medicines available.",
                font=('Arial', 12),
                bg='white',
                fg='gray'
            )
            empty_label.pack(pady=50)
            
        # Main Menu button
        main_menu_btn = tk.Button(
            main_frame,
            text="Main Menu",
            font=('Arial', 12),
            bg='#2196F3',  # Blue color
            fg='white',
            relief=tk.FLAT,
            command=self.setup_admin_dashboard,
            padx=20,
            pady=5
        )
        main_menu_btn.pack(pady=10)

    def setup_admin_add_medicine(self):
        """Page 7: Admin add medicine"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        # Load edit medicine background
        edit_bg_path = r"C:\Users\LOQ\Python latihan\college studies\2nd semester\Pharmora-main\assets\images\admin edit medicine.png"
        if os.path.exists(edit_bg_path):
            edit_bg = Image.open(edit_bg_path)
            edit_bg = edit_bg.resize((self.admin_display_frame.winfo_width(), self.admin_display_frame.winfo_height()), Image.LANCZOS)
            self.edit_bg_photo = ImageTk.PhotoImage(edit_bg)
            bg_label = tk.Label(self.admin_display_frame, image=self.edit_bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container
        main_frame = tk.Frame(self.admin_display_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="Please fill this form",
            font=('Arial', 16, "bold"),
            bg='white',
            fg='black'
        )
        title_label.pack(pady=(10, 20))
        
        # Form table
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Medicine Name row
        name_frame = tk.Frame(form_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            name_frame,
            text="Medicine Name",
            font=('Arial', 12),
            bg='white',
            fg='black'
        ).pack(side=tk.LEFT, padx=10)
        
        self.med_name_entry = tk.Entry(
            name_frame,
            font=('Arial', 12),
            relief=tk.FLAT,
            bg='white',
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.med_name_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)
        
        # Composition row
        comp_frame = tk.Frame(form_frame, bg='white')
        comp_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            comp_frame,
            text="Composition",
            font=('Arial', 12),
            bg='white',
            fg='black'
        ).pack(side=tk.LEFT, padx=10)
        
        self.med_comp_entry = tk.Entry(
            comp_frame,
            font=('Arial', 12),
            relief=tk.FLAT,
            bg='white',
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.med_comp_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)
        
        # Side Effect row
        side_frame = tk.Frame(form_frame, bg='white')
        side_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            side_frame,
            text="Side Effect",
            font=('Arial', 12),
            bg='white',
            fg='black'
        ).pack(side=tk.LEFT, padx=10)
        
        self.med_side_entry = tk.Entry(
            side_frame,
            font=('Arial', 12),
            relief=tk.FLAT,
            bg='white',
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.med_side_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)
        
        # Add button
        add_btn = tk.Button(
            form_frame,
            text="Add",
            font=('Arial', 12, "bold"),
            bg='#4CAF50',  # Green color
            fg='white',
            relief=tk.FLAT,
            command=self.add_new_medicine,
            padx=30,
            pady=10
        )
        add_btn.pack(pady=20)
        
        # Main Menu button
        main_menu_btn = tk.Button(
            main_frame,
            text="Main Menu",
            font=('Arial', 12),
            bg='#2196F3',  # Blue color
            fg='white',
            relief=tk.FLAT,
            command=self.setup_admin_dashboard,
            padx=20,
            pady=5
        )
        main_menu_btn.pack(pady=10)

    def load_medicines_from_csv(self):
        """Load medicines from CSV file"""
        csv_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/data/Medicine_Details.csv"
        self.medicines = []
        
        try:
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.medicines.append({
                        'name': row.get('Medicine Name', ''),
                        'composition': row.get('Composition', ''),
                        'side_effect': row.get('Side Effect', '')
                    })
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_path}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def sort_medicines(self, order):
        """Sort medicines by newest or oldest"""
        if order == 'newest':
            self.medicines = sorted(self.medicines, key=lambda x: x.get('timestamp', 0), reverse=True)
        else:
            self.medicines = sorted(self.medicines, key=lambda x: x.get('timestamp', 0))
        
        self.setup_admin_manage_medicines()

    def remove_medicine(self, medicine):
        """Remove a medicine from the list and update CSV"""
        self.medicines = [m for m in self.medicines if m != medicine]
        self.update_medicines_csv()
        self.setup_admin_manage_medicines()
        messagebox.showinfo("Success", f"{medicine['name']} has been removed.")

    def add_new_medicine(self):
        """Add a new medicine to the list and update CSV"""
        name = self.med_name_entry.get().strip()
        composition = self.med_comp_entry.get().strip()
        side_effect = self.med_side_entry.get().strip()
        
        if not name or not composition or not side_effect:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        new_med = {
            'name': name,
            'composition': composition,
            'side_effect': side_effect,
            'timestamp': time.time()
        }
        
        self.medicines.append(new_med)
        self.update_medicines_csv()
        messagebox.showinfo("Success", f"{name} has been added to the medicine list.")
        self.setup_admin_manage_medicines()

    def update_medicines_csv(self):
        """Update the CSV file with current medicines data"""
        csv_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/data/Medicine_Details.csv"
        
        try:
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['Medicine Name', 'Composition', 'Side Effect']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for med in self.medicines:
                    writer.writerow({
                        'Medicine Name': med['name'],
                        'Composition': med['composition'],
                        'Side Effect': med['side_effect']
                    })
        except Exception as e:
            print(f"Error writing to CSV file: {e}")        

    def setup_user_dashboard(self):
        """Page 8: User main menu with background image"""
        self.clear_frame()

        # Load background image
        bg_path = r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/user dashboard.png"
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Ensure background is behind other elements

        # Left menu buttons (Vertical alignment)
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.place(x=50, y=screen_height // 4)  # Positioned on the left

        buttons = [
            ("Display All Medicine", self.setup_user_all_medicines),
            ("Search", self.setup_user_search),
            ("Favorite", self.setup_user_favorites),
            ("Feedback", self.setup_user_feedback),
            ("History", self.setup_user_history),
            ("Chatbot", self.setup_user_chatbot),
            ("Main Menu", self.setup_role_selection)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                font=(self.baloo_font, 12),
                bg=self.button_color,
                fg=self.white,
                relief=tk.FLAT,
                command=command,
                width=20,
                pady=10
            )
            btn.pack(pady=5)  # Vertical spacing

        # Exit button (Bottom right)
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=(self.roboto_flex_font, 12),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            command=self.root.quit,
            padx=30,
            pady=5
        )
        exit_btn.place(x=screen_width - 150, y=screen_height - 80, width=100, height=40)

    def setup_user_all_medicines(self):
        """Page 9: User view all medicines (10.png)"""
        for widget in self.user_display_frame.winfo_children():
            widget.destroy()
            
        title_label = tk.Label(
            self.user_display_frame,
            text="All Medicines",
            font=(self.baloo_font, 16, "bold"),
            bg=self.pink_display,
            fg=self.dark_text
        )
        title_label.pack(pady=(20, 10))
        
        meds_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        meds_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(meds_frame, bg=self.pink_display, highlightthickness=0)
        scrollbar = ttk.Scrollbar(meds_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.pink_display)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for idx, med in enumerate(self.medicines):
            med_frame = tk.Frame(scrollable_frame, bg=self.white, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['name']} - {med['desc']}\nDose: {med['dose']}",
                font=(self.roboto_flex_font, 12),
                bg=self.white,
                fg=self.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            is_fav = any(m['name'] == med['name'] for m in self.favorites)
            
            fav_btn = tk.Button(
                med_frame,
                text="♥ Add to Fav" if not is_fav else "♥ Remove Fav",
                font=(self.roboto_flex_font, 10),
                bg=self.white,
                fg="#ff6b9d" if is_fav else "#cccccc",
                relief=tk.FLAT,
                command=lambda m=med, is_f=is_fav: self.toggle_favorite(m, is_f)
            )
            fav_btn.pack(side=tk.RIGHT, padx=10)
            
        if not self.medicines:
            empty_label = tk.Label(
                scrollable_frame,
                text="No medicines available.",
                font=(self.roboto_flex_font, 12),
                bg=self.pink_display,
                fg=self.gray_text
            )
            empty_label.pack(pady=50)
            
    def setup_user_search(self):
        """Page 10: User search (11.png)"""
        for widget in self.user_display_frame.winfo_children():
            widget.destroy()
            
            def setup_user_search(self):
                """Page 10: User search (11.png)"""
                for widget in self.user_display_frame.winfo_children():
                    widget.destroy()
            
        title_label = tk.Label(
            self.user_display_frame,
            text="What are you looking for?",
            font=(self.baloo_font, 16, "bold"),
            bg=self.pink_display,
            fg=self.dark_text
        )
        title_label.pack(pady=(20, 10))

        search_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        self.search_entry = tk.Entry(
            search_frame,
            font=(self.roboto_flex_font, 14),
            relief=tk.FLAT,
            bg=self.white,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor=self.button_color,
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=(self.baloo_font, 12, "bold"),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            command=self.perform_search,
            padx=20,
            pady=5
        )
        search_btn.pack(side=tk.RIGHT)

        self.search_results_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        self.search_results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        initial_msg = tk.Label(
            self.search_results_frame,
            text="Enter a search term to find medicines",
            font=(self.roboto_flex_font, 12),
            bg=self.pink_display,
            fg=self.gray_text
        )
        initial_msg.pack(pady=50)
        
    def perform_search(self):
        search_term = self.search_entry.get().lower()

        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
            
        if not search_term:
            error_label = tk.Label(
                self.search_results_frame,
                text="Please enter a search term",
                font=(self.roboto_flex_font, 12),
                bg=self.pink_display,
                fg="#ff0000"
            )
            error_label.pack(pady=50)
            return
            
        self.history.append(search_term)
        
        results = [
            med for med in self.medicines 
            if (search_term in med['name'].lower() or 
                search_term in med['desc'].lower() or
                search_term in med['dose'].lower())
        ]
        
        if not results:
            no_results = tk.Label(
                self.search_results_frame,
                text=f"No results found for '{search_term}'",
                font=(self.roboto_flex_font, 12),
                bg=self.pink_display,
                fg=self.gray_text
            )
            no_results.pack(pady=50)
            return
            
        canvas = tk.Canvas(self.search_results_frame, bg=self.pink_display, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.search_results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.pink_display)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for med in results:
            med_frame = tk.Frame(scrollable_frame, bg=self.white, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['name']} - {med['desc']}\nDose: {med['dose']}",
                font=(self.roboto_flex_font, 12),
                bg=self.white,
                fg=self.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            is_fav = any(m['name'] == med['name'] for m in self.favorites)
            
            fav_btn = tk.Button(
                med_frame,
                text="♥ Add to Fav" if not is_fav else "♥ Remove Fav",
                font=(self.roboto_flex_font, 10),
                bg=self.white,
                fg="#ff6b9d" if is_fav else "#cccccc",
                relief=tk.FLAT,
                command=lambda m=med, is_f=is_fav: self.toggle_favorite(m, is_f)
            )
            fav_btn.pack(side=tk.RIGHT, padx=10)
            
    def setup_user_favorites(self):
        """Page 11: User favorites (12.png)"""
        for widget in self.user_display_frame.winfo_children():
            widget.destroy()
            
        title_label = tk.Label(
            self.user_display_frame,
            text="Your Favorite Medicines",
            font=(self.baloo_font, 16, "bold"),
            bg=self.pink_display,
            fg=self.dark_text
        )
        title_label.pack(pady=(20, 10))
        
        favs_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        favs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        if not self.favorites:
            empty_label = tk.Label(
                favs_frame,
                text="You haven't added any favorites yet.",
                font=(self.roboto_flex_font, 12),
                bg=self.pink_display,
                fg=self.gray_text
            )
            empty_label.pack(pady=50)
            return
            
        canvas = tk.Canvas(favs_frame, bg=self.pink_display, highlightthickness=0)
        scrollbar = ttk.Scrollbar(favs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.pink_display)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for med in self.favorites:
            med_frame = tk.Frame(scrollable_frame, bg=self.white, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['name']} - {med['desc']}\nDose: {med['dose']}",
                font=(self.roboto_flex_font, 12),
                bg=self.white,
                fg=self.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            remove_btn = tk.Button(
                med_frame,
                text="✕ Remove",
                font=(self.roboto_flex_font, 10),
                bg=self.white,
                fg="#ff0000",
                relief=tk.FLAT,
                command=lambda m=med: self.toggle_favorite(m, True)
            )
            remove_btn.pack(side=tk.RIGHT, padx=10)
            
    def setup_user_history(self):
        """Page 12: User search history (13.png)"""
        for widget in self.user_display_frame.winfo_children():
            widget.destroy()
            
        title_label = tk.Label(
            self.user_display_frame,
            text="Your Search History",
            font=(self.baloo_font, 16, "bold"),
            bg=self.pink_display,
            fg=self.dark_text
        )
        title_label.pack(pady=(20, 10))
        
        history_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        if not self.history:
            empty_label = tk.Label(
                history_frame,
                text="Your search history is empty.",
                font=(self.roboto_flex_font, 12),
                bg=self.pink_display,
                fg=self.gray_text
            )
            empty_label.pack(pady=50)
            return
            
        canvas = tk.Canvas(history_frame, bg=self.pink_display, highlightthickness=0)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.pink_display)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for search_term in reversed(self.history):
            hist_frame = tk.Frame(scrollable_frame, bg=self.white, relief=tk.RAISED, bd=1)
            hist_frame.pack(fill=tk.X, pady=5, padx=5)
            
            hist_label = tk.Label(
                hist_frame,
                text=search_term,
                font=(self.roboto_flex_font, 12),
                bg=self.white,
                fg=self.dark_text,
                anchor="w"
            )
            hist_label.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            repeat_btn = tk.Button(
                hist_frame,
                text="Search Again",
                font=(self.roboto_flex_font, 10),
                bg=self.white,
                fg=self.button_color,
                relief=tk.FLAT,
                command=lambda st=search_term: self.repeat_search(st)
            )
            repeat_btn.pack(side=tk.RIGHT, padx=10)
            
    def setup_user_feedback(self):
        """Page 13: User feedback"""
        for widget in self.user_display_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.user_display_frame,
            text="Send Feedback",
            font=(self.baloo_font, 16, "bold"),
            bg=self.pink_display,
            fg=self.dark_text
        )
        title_label.pack(pady=(20, 10))

        form_frame = tk.Frame(self.user_display_frame, bg=self.pink_display)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        feedback_label = tk.Label(
            form_frame,
            text="Your Feedback",
            font=(self.roboto_flex_font, 11),
            bg=self.pink_display,
            fg=self.gray_text,
            anchor="w"
        )
        feedback_label.pack(fill=tk.X, pady=(10, 0))
        
        self.feedback_text = tk.Text(
            form_frame,
            font=(self.roboto_flex_font, 12),
            relief=tk.FLAT,
            bg=self.white,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor=self.button_color,
            height=10,
            width=50,
            wrap=tk.WORD
        )
        self.feedback_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        submit_btn = tk.Button(
            form_frame,
            text="Submit Feedback",
            font=(self.baloo_font, 12, "bold"),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            command=self.submit_feedback,
            padx=30,
            pady=10
        )
        submit_btn.pack()
        
    def toggle_favorite(self, medicine, is_favorite):
        if is_favorite:
            self.favorites = [m for m in self.favorites if m['name'] != medicine['name']]
            messagebox.showinfo("Removed", f"{medicine['name']} removed from favorites")
        else:
            self.favorites.append(medicine)
            messagebox.showinfo("Added", f"{medicine['name']} added to favorites")

        if hasattr(self, 'user_display_frame'):
            for widget in self.user_display_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Canvas):
                            if "All Medicines" in self.user_display_frame.winfo_children()[0].cget("text"):
                                self.setup_user_all_medicines()
                            elif "results" in str(widget):
                                self.perform_search()
                            elif "Favorite" in self.user_display_frame.winfo_children()[0].cget("text"):
                                self.setup_user_favorites()
                            break
        
    def repeat_search(self, search_term):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, search_term)
        self.perform_search()
        
    def submit_feedback(self):
        feedback = self.feedback_text.get("1.0", tk.END).strip()
        if not feedback:
            messagebox.showerror("Error", "Please enter your feedback before submitting")
            return
            
        messagebox.showinfo("Thank You", "Your feedback has been submitted!")
        self.feedback_text.dele
        self.setup_user_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = PharmoraApp(root)
    root.mainloop()