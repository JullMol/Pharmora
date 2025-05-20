import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox, ttk
from PIL import Image
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import login_user, register_user, is_username_exist
from admin.admin_features import add_medicine, view_medicine_data, delete_medicine
from features.pharmora_bot import save_to_csv, load_from_csv, response_bot
from loader import load_medicines

class LoadingScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora Loading...")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/loading.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.loading_label = ctk.CTkLabel(
            self, 
            text="Loading Pharmora...", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            fg_color="transparent", 
            bg_color="transparent"
        )
        self.loading_label.place(relx=0.5, rely=0.85, anchor="center")

        progress_width = int(screen_width * 0.5)  
        self.progress = ctk.CTkProgressBar(
            self, 
            width=progress_width, 
            progress_color="#FF6B9D", 
            fg_color="#1976D2"
        )

        self.progress.place(relx=0.5, rely=0.9, anchor="center")
        self.progress.set(0)

        self.after(100, self.load_animation) 

    def load_animation(self):
        for i in range(101):
            self.progress.set(i / 100)
            self.loading_label.configure(text=f"Loading Pharmora... {i}%")
            self.update_idletasks()
            time.sleep(0.03)  
        self.destroy()  
        self.open_get_started()

    def open_get_started(self):
        get_started_screen = GetStartedScreen()
        get_started_screen.mainloop()

class GetStartedScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Get Started")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/1st page.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        baloo_font = (r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf")
        baloo_font = CTkFont(family="BalooBhai2", size=24, weight="bold")
        self.get_started_button = ctk.CTkButton(
            self, 
            text="Get Started", 
            font=baloo_font, 
            width=170, 
            height=40, 
            corner_radius=0,
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",  
            hover_color="#FF6B9D", 
            bg_color="#FF6B9D", 
            command=self.open_which_one
        )
        self.get_started_button.place(relx=0.5, rely=0.68, anchor="center")

    def open_which_one(self):
            self.destroy()
            which_one_screen = WhichOneScreen()
            which_one_screen.mainloop()

class WhichOneScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Choose Role")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/which one.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.admin_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.admin_frame.place(relx=0.32, rely=0.8, anchor="center")
        
        # baloo_font = (r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf")
        baloo_font = CTkFont(family="BalooBhai2", size=24, weight="bold")
        self.admin_button = ctk.CTkButton(
            self.admin_frame, 
            text="Admin", 
            font=baloo_font, 
            width=185, 
            height=55, 
            corner_radius=0,
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",  
            hover_color="#FF6B9D",  
            border_width=0, 
            command=self.open_admin_login
        )
        self.admin_button.pack()

        self.user_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.user_frame.place(relx=0.68, rely=0.8, anchor="center")
        
        self.user_button = ctk.CTkButton(
            self.user_frame, 
            text="User", 
            font=baloo_font, 
            width=185, 
            height=55, 
            corner_radius=0,
            fg_color="#FF6B9D",  
            text_color="#FFFFFF",  
            hover_color="#FF6B9D",  
            border_width=0, 
            command=self.open_user_login
        )
        self.user_button.pack()

    def open_admin_login(self):
        self.destroy()
        login_screen = AdminLoginScreen()
        login_screen.mainloop()  

    def open_user_login(self):
        self.destroy()
        login_screen = UserLoginScreen()
        login_screen.mainloop()

class AdminLoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Login")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        self.show_login_screen()

    def show_login_screen(self):
        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/hi there.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.username_frame.place(relx=0.1, rely=0.51, anchor="w")
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Username",
            text_color="#000000",
            width=350,
            fg_color="#FFFFFF",
            border_width=0,
            corner_radius=0
        )
        self.username_entry.pack()

        self.password_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.password_frame.place(relx=0.1, rely=0.685, anchor="w")
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            text_color="#000000",
            width=350,
            fg_color="#FFFFFF",
            border_width=0,
            corner_radius=0,
            show="*"
        )
        self.password_entry.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signin_button.place(relx=0.21, rely=0.805, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0,border_width=0, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.71, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, command=self.show_signup_screen)
        self.signup_button.pack()

    def show_signup_screen(self):
        self.clear_screen()

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/welcome back.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.username_frame.place(relx=0.6, rely=0.45, anchor="w")
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Username",
            text_color="#000000",
            width=350,
            fg_color="#FFFFFF",
            border_width=0,
            corner_radius=0
        )
        self.username_entry.pack()

        self.password_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.password_frame.place(relx=0.6, rely=0.625, anchor="w")
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            text_color="#000000",
            width=350,
            fg_color="#FFFFFF",
            border_width=0,
            corner_radius=0,
            show="*"
        )
        self.password_entry.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signup_button.place(relx=0.71, rely=0.755, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0,border_width=0, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.21, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id, role = login_user(username, password)

        if user_id and role == "admin":
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
            self.destroy()
            dashboard = DisplayMedicinePage()      
            dashboard.mainloop()
        else:
            CTkMessagebox(title="Login Failed", message="Invalid username or password", icon="cancel")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if is_username_exist(username):
            CTkMessagebox(title="Registration Failed", message="Username already exists!", icon="cancel")
            return

        register_user(username, password, "admin")
        CTkMessagebox(title="Account Created", message="Account successfully created!", icon="check")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

class DisplayMedicinePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Display Medicine")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(self, text="Display Medicine", font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFFFFF", fg_color="#FF6B9D")
        self.title_label.place(relx=0.45, rely=0.1)

        self.table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", width=1500, height=1000, corner_radius=15)
        self.table_frame.place(relx=0.2, rely=0.25)

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", 
                        background="yellow", 
                        foreground="#FF6B9D", 
                        font=("Arial", 12, "bold"))
        style.configure("Custom.Treeview", 
                        rowheight=30,  
                        bordercolor="#FF6B9D", 
                        borderwidth=2,
                        relief="ridge",
                        font=("Arial", 11))
        style.map("Custom.Treeview.Heading",
                  background=[("active", "#E05A8A")],
                  relief=[("active", "groove")])

        self.table = ttk.Treeview(
            self.table_frame, 
            columns=("Name", "Composition", "Uses", "Side Effects"), 
            show="headings", 
            height=18, 
            style="Custom.Treeview"
        )
        self.table.heading("Name", text="Name")
        self.table.heading("Composition", text="Composition")
        self.table.heading("Uses", text="Uses")
        self.table.heading("Side Effects", text="Side Effects")

        self.table.column("Name", width=320)
        self.table.column("Composition", width=320)
        self.table.column("Uses", width=320)
        self.table.column("Side Effects", width=320)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Data", command=self.load_data, width=180, fg_color="#970032", text_color="#FFFFFF", font=ctk.CTkFont(size=16, weight="bold"))
        self.refresh_button.place(relx=0.45, rely=0.85)

        self.load_data()

        frame_add = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_add.place(relx=0.043, rely=0.28, anchor="nw")

        add_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/add.png")
        self.add_image = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(100, 100))  
        self.add_button = ctk.CTkButton(
            frame_add, 
            image=self.add_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.open_add_medicine_page
        )
        self.add_button.place(x=0, y=0) 

        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_display.place(relx=0.043, rely=0.15, anchor="nw")

        display_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/display all.png")
        self.display_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(100, 100))  
        self.display_button = ctk.CTkButton(
            frame_display, 
            image=self.display_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.display_medicine
        )
        self.display_button.place(x=0, y=0) 

        frame_delete = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_delete.place(relx=0.043, rely=0.4, anchor="nw")
        
        delete_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/delete.png")
        self.delete_image = ctk.CTkImage(light_image=delete_image, dark_image=delete_image, size=(80, 80))  
        self.delete_button = ctk.CTkButton(
            frame_delete, 
            image=self.delete_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.open_delete_medicine_page
        )
        self.delete_button.place(x=0, y=0) 

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_main_menu.place(relx=0.4, rely=0.08, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF",corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.08, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=100, 
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def open_add_medicine_page(self):
        self.destroy()
        add_medicine_screen = AddMedicinePage()
        add_medicine_screen.mainloop()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        data = view_medicine_data()
        for item in data:
            self.table.insert("", "end", values=item)

    def display_medicine(self):
        self.destroy()
        display_screen = DisplayMedicinePage()
        display_screen.mainloop()

    def open_delete_medicine_page(self):
        self.destroy()
        delete_medicine_screen = DeleteMedicinePage()
        delete_medicine_screen.mainloop()
    
    def close_app(self):
        self.destroy()
        sys.exit()

    def open_admin_login(self):
        self.destroy()
        login_screen = AdminLoginScreen()
        login_screen.mainloop()

    def open_main_menu(self):
        self.destroy()
        which_one_screen = WhichOneScreen()
        which_one_screen.mainloop()

class AddMedicinePage(ctk.CTk):
    def create_entry(self, placeholder):
        entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            fg_color="#FFFFFF",         
            text_color="#000000",       
            width=400,
            height=40,
            border_width=0,
            corner_radius=15,
            font=ctk.CTkFont(size=14),
            bg_color="#FF6B9D",
        )
        entry.pack(pady=10)
        return entry

    def __init__(self):
        super().__init__()
        self.title("Pharmora - Add Medicine")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self, text="Add Medicine", 
            font=ctk.CTkFont(size=28, weight="bold"), 
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.pack(pady=80)

        self.name_entry = self.create_entry("Name Medicine")
        self.comp_entry = self.create_entry("Composition")
        self.uses_entry = self.create_entry("Uses")
        self.side_effect_entry = self.create_entry("Side Effect")

        self.submit_button = ctk.CTkButton(
            self, text="Add Medicine",
            command=self.add_medicine_action,
            width=160,
            height=40,
            fg_color="#970032",
            text_color="#FFFFFF",
            hover_color="#E05A8A",
            corner_radius=12,
            bg_color="#FF6B9D",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.submit_button.pack(pady=35)

        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_display.place(relx=0.043, rely=0.15, anchor="nw")

        display_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/display all.png")
        self.display_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(100, 100))  
        self.display_button = ctk.CTkButton(
            frame_display, 
            image=self.display_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.display_medicine
        )
        self.display_button.place(x=0, y=0) 

        frame_delete = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_delete.place(relx=0.043, rely=0.4, anchor="nw")

        delete_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/delete.png")
        self.delete_image = ctk.CTkImage(light_image=delete_image, dark_image=delete_image, size=(80, 80))  
        self.delete_button = ctk.CTkButton(
            frame_delete, 
            image=self.delete_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.open_delete_medicine_page
        )
        self.delete_button.place(x=0, y=0) 

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_main_menu.place(relx=0.4, rely=0.08, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF",corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.08, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=100, 
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def open_delete_medicine_page(self):
        self.destroy()
        delete_medicine_screen = DeleteMedicinePage()
        delete_medicine_screen.mainloop()
    
    def close_app(self):
        self.destroy()
        sys.exit()

    def open_admin_login(self):
        self.destroy()
        login_screen = AdminLoginScreen()
        login_screen.mainloop()

    def open_main_menu(self):
        self.destroy()
        which_one_screen = WhichOneScreen()
        which_one_screen.mainloop()

    def add_medicine_action(self):
        name = self.name_entry.get()
        comp = self.comp_entry.get()
        uses = self.uses_entry.get()
        side_effect = self.side_effect_entry.get()

        success, msg = add_medicine(name, comp, uses, side_effect)
        messagebox.showinfo("Add Medicine", msg)

        if success:
            self.name_entry.delete(0, ctk.END)
            self.comp_entry.delete(0, ctk.END)
            self.uses_entry.delete(0, ctk.END)
            self.side_effect_entry.delete(0, ctk.END)

    def display_medicine(self):
        self.destroy()
        display_screen = DisplayMedicinePage()
        display_screen.mainloop()

class DeleteMedicinePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Delete Medicine")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(self, text="Delete Medicine", font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFFFFF", fg_color="#FF6B9D")
        self.title_label.pack(pady=80)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter Medicine Name", fg_color="#FFFFFF", text_color="#000000", width=400, height=40, corner_radius=15,  bg_color="#FF6B9D")
        self.name_entry.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Delete Medicine", command=self.delete_medicine_action, width=180, height=40, fg_color="#970032",   bg_color="#FF6B9D",text_color="#FFFFFF", font=ctk.CTkFont(size=16, weight="bold"))
        self.delete_button.pack(pady=20)

        frame_add = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_add.place(relx=0.043, rely=0.28, anchor="nw")
        add_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/add.png")
        self.add_image = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(100, 100))  
        self.add_button = ctk.CTkButton(
            frame_add, 
            image=self.add_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.open_add_medicine_page
        )
        self.add_button.place(x=0, y=0) 

        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_display.place(relx=0.043, rely=0.15, anchor="nw")
        display_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/display all.png")
        self.display_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(100, 100))  
        self.display_button = ctk.CTkButton(
            frame_display, 
            image=self.display_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=100, 
            height=100,
            command=self.display_medicine
        )
        self.display_button.place(x=0, y=0) 

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_main_menu.place(relx=0.4, rely=0.08, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF",corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.08, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=100, 
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def delete_medicine_action(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a medicine name.")
            return

        success, msg = delete_medicine(name)
        messagebox.showinfo("Delete Medicine", msg)

        if success:
            self.name_entry.delete(0, ctk.END)

    def close_app(self):
        self.destroy()
        sys.exit()

    def open_admin_login(self):
        self.destroy()
        login_screen = AdminLoginScreen()
        login_screen.mainloop()

    def open_main_menu(self):
        self.destroy()
        which_one_screen = WhichOneScreen()
        which_one_screen.mainloop()

    def display_medicine(self):
        self.destroy()
        display_screen = DisplayMedicinePage()
        display_screen.mainloop()

    def open_add_medicine_page(self):
        self.destroy()
        add_medicine_screen = AddMedicinePage()
        add_medicine_screen.mainloop()

class UserLoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora - Login")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.current_username = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)

        self.show_login_screen()

    def show_login_screen(self):
        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/hi there.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username",text_color="#000000", width=350, fg_color="#FFFFFF",border_width=0, corner_radius=0)
        self.username_entry.place(relx=0.1, rely=0.51, anchor="w")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password",text_color="#000000", width=350, show="*", fg_color="#FFFFFF",border_width=0, corner_radius=0)
        self.password_entry.place(relx=0.1, rely=0.685, anchor="w")

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signin_button.place(relx=0.21, rely=0.805, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0,border_width=0, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.71, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, command=self.show_signup_screen)
        self.signup_button.pack()

        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())

    def show_signup_screen(self):
        self.clear_screen()

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/welcome back.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username",text_color="#000000", width=350,fg_color="#FFFFFF",border_width=0, corner_radius=0)
        self.username_entry.place(relx=0.6, rely=0.45, anchor="w")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=350, show="*",text_color="#000000", fg_color="#FFFFFF",border_width=0, corner_radius=0)
        self.password_entry.place(relx=0.6, rely=0.625, anchor="w")

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signup_button.place(relx=0.71, rely=0.755, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0,border_width=0, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.21, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id, role = login_user(username, password)
        if user_id and role == "user":
            self.current_username = username
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
            self.show_user_dashboard()
        elif role == "wrong_role":
            CTkMessagebox(title="Login Failed", message="This account is not a user!", icon="cancel")
        else:
            CTkMessagebox(title="Login Failed", message="Invalid username or password", icon="cancel")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if is_username_exist(username):
            CTkMessagebox(title="Registration Failed", message="Username already exists!", icon="cancel")
            return

        register_user(username, password, "user")
        CTkMessagebox(title="Account Created", message="Account successfully created!", icon="check")

    def show_user_dashboard(self):
        dashboard = UserDashboard(self)
        dashboard.place(x=0, y=0, relwidth=1, relheight=1)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.username = getattr(master, 'current_username', 'User')
        self.drug_notes = []

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        bot_img = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/bot.png")
        bot_icon = ctk.CTkImage(light_image=bot_img, dark_image=bot_img, size=(120, 120))
        self.bot_button = ctk.CTkButton(self, image=bot_icon, text="", corner_radius=60, fg_color="#FF6B9D", command=self.show_bot_chat)
        self.bot_button.place(x=85, y=820)

        self.bot_frame = ctk.CTkFrame(self, fg_color="#FF6B9D", width=1100, height=600, corner_radius=60)
        self.bot_frame.place(x=200, y=100)

        self.chat_area = ctk.CTkTextbox(self.bot_frame, width=1050, height=500, state="disabled")
        self.chat_area.place(x=25, y=25)

        self.entry = ctk.CTkEntry(self.bot_frame, width=900)
        self.entry.place(x=25, y=540)
        self.send_btn = ctk.CTkButton(self.bot_frame, text="Send", command=self.send_message)
        self.send_btn.place(x=950, y=540)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.bot_frame.place_forget()
        self.bot_greeted = False

    def show_bot_chat(self):
        self.bot_frame.place(x=200, y=100)
        self.search_history = load_from_csv()
        self.nodes = load_medicines('data/Medicine_Details.csv').to_list()
        if not self.bot_greeted:
            welcome_msg = (
                f"Pharmora: Hi {self.username}! I can help you find information about medicines.\n"
                "Type 'history' to see your search history or search for any medicine!\n"
            )
            self.display_message(welcome_msg)
            for chat in load_from_csv():
                self.display_message(chat)
            self.bot_greeted = True

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        query = f"You: {user_input}"
        self.display_message(query)
        save_to_csv(query)
        
        bot_response = response_bot(user_input, self.nodes)
        self.display_message(bot_response)
        save_to_csv(bot_response)
        self.entry.delete(0, "end")
        
        if user_input.lower() in ["exit", "quit", "keluar"]:
            self.display_message("Pharmora: Thank you for using Pharmora. Stay healthy!")
            self.bot_frame.place_forget()
            return
        
        if user_input.lower() in ["history", "riwayat"]:
            self.show_chat_history()
            return        

    def display_message(self, msg):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", msg + "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

if __name__ == "__main__":
    app = LoadingScreen()
    app.mainloop()