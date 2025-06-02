from PIL import Image
import time
import sys
import os
import csv
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import login_user, register_user
from admin.admin_features import add_medicine, view_medicine_data, delete_medicine
from models.linked_list import DoubleLinkedList
from models.medicine import Medicine
from models.search import binary_search_suggestions
from admin.admin_features import view_medicine_data
from features.history_manager import HistoryManager
from features.favorites import add_to_favorites, get_favorites, remove_from_favorites
from features.user_feedback import add_user_feedback, get_feedbacks_by_user, get_all_feedbacks, get_feedbacks_by_medicine
from features.pharmora_bot import response_bot, save_to_csv, load_from_csv
from tkinter.ttk import Combobox
from customtkinter import CTkFont
from models.linked_list import DoubleLinkedList
from loader import load_medicines

class AppManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.resizable(False, False)
        self.active_frame = None
        self.user_id = None
        self.history_manager = HistoryManager()

        # self.show_frame(UserDashboard)
        self.show_frame(LoadingScreen)


    def show_frame(self, frame_class, **kwargs): 
        if self.active_frame is not None:
            self.active_frame.pack_forget()  
            self.active_frame.destroy()      
        self.active_frame = frame_class(self, **kwargs)
        self.active_frame.pack(fill="both", expand=True)
 
class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/loading.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.loading_label = ctk.CTkLabel(self, text="Loading Pharmora...", font=ctk.CTkFont(size=24, weight="bold"))
        self.loading_label.place(relx=0.5, rely=0.85, anchor="center")

        progress_width = int(screen_width * 0.5)
        self.progress = ctk.CTkProgressBar(self, width=progress_width)
        self.progress.place(relx=0.5, rely=0.9, anchor="center")
        self.progress.set(0)

        self.after(100, self.load_animation)

    def load_animation(self):
        for i in range(101):
            self.progress.set(i / 100)
            self.loading_label.configure(text=f"Loading Pharmora... {i}%")
            self.update_idletasks()
            time.sleep(0.02)
        self.parent.show_frame(GetStartedScreen) 

class GetStartedScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/1st page.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        baloo_font = (r"assets/fonts/BalooBhai2-VariableFont_wght.ttf", 30, "bold")

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
        self.parent.show_frame(WhichOneScreen)

class WhichOneScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/which one.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.admin_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.admin_frame.place(relx=0.32, rely=0.79, anchor="center")

        baloo_font = ("Baloo Bhai 2", 30, "bold")
        self.admin_button = ctk.CTkButton(
            self.admin_frame,
            text="Admin",
            font=baloo_font,
            width=200,
            height=75,
            corner_radius=0,
            fg_color="#FF6B9D",
            text_color="#FFFFFF",
            hover_color="#FF6B9D",
            border_width=0,
            command=self.open_admin_login
        )
        self.admin_button.pack()

        self.user_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.user_frame.place(relx=0.68, rely=0.79, anchor="center")

        self.user_button = ctk.CTkButton(
            self.user_frame,
            text="User",
            font=baloo_font,
            width=200,
            height=75,
            corner_radius=0,
            fg_color="#FF6B9D",
            text_color="#FFFFFF",
            hover_color="#FF6B9D",
            border_width=0,
            command=self.open_user_login
        )
        self.user_button.pack()

    def open_admin_login(self):
        self.parent.show_frame(AdminLoginScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)                            

class AdminLoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")

        self.show_login_screen()

    def show_login_screen(self):
        bg_image = Image.open("assets/images/hi there.png")
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
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())

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
        self.password_entry.bind("<Return>", lambda event: self.login())

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signin_button.place(relx=0.19, rely=0.805, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=200, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.69, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=200, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_signup_screen)
        self.signup_button.pack()

    def show_signup_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        bg_image = Image.open("assets/images/welcome back.png")
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
        frame_signup_button.place(relx=0.7, rely=0.755, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=200, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.2, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=200, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty!")
            return

        try:
            user_id, role = login_user(username, password)
            if user_id and role == "admin":
                self.parent.show_frame(DisplayMedicinePage)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password or not an admin.")
        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred: {str(e)}")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty!")
            return

        if len(username) < 4:
            messagebox.showerror("Registration Failed", "Username must be at least 4 characters!")
            return

        if len(password) < 6:
            messagebox.showerror("Registration Failed", "Password must be at least 6 characters!")
            return

        if ' ' in username:
            messagebox.showerror("Registration Failed", "Username cannot contain spaces!")
            return

        try:
            if register_user(username, password, "admin"):
                messagebox.showinfo("Account Created", "Account successfully created as Admin!")
                self.show_login_screen()
            else:
                messagebox.showerror("Registration Failed", "Username already exists or invalid input.")
        except Exception as e:
            messagebox.showerror("Registration Error", f"An error occurred: {str(e)}")

class UserLoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.show_login_screen()

    def show_login_screen(self):
        bg_image = Image.open("assets/images/hi there.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, 
                                   size=(self.winfo_screenwidth(), self.winfo_screenheight()))

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
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())

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
        self.password_entry.bind("<Return>", lambda event: self.login())

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FFFFFF")
        frame_signin_button.place(relx=0.19, rely=0.805, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=200, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.69, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=200, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_signup_screen)
        self.signup_button.pack()

    def show_signup_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        bg_image = Image.open("assets/images/welcome back.png")
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
        frame_signup_button.place(relx=0.7, rely=0.755, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=200, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.2, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=200, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty!")
            return

        try:
            user_id, role = login_user(username, password)
            if user_id and role == "user":
                self.parent.user_id = user_id
                self.parent.show_frame(UserDashboard)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password or not a user account.")
        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred: {str(e)}")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty!")
            return

        if len(username) < 4:
            messagebox.showerror("Registration Failed", "Username must be at least 4 characters!")
            return

        if len(password) < 6:
            messagebox.showerror("Registration Failed", "Password must be at least 6 characters!")
            return

        if ' ' in username:
            messagebox.showerror("Registration Failed", "Username cannot contain spaces!")
            return

        try:
            if register_user(username, password, "user"):
                messagebox.showinfo("Account Created", "Account successfully created as User!")
                self.show_login_screen()
            else:
                messagebox.showerror("Registration Failed", "Username already exists or invalid input.")
        except Exception as e:
            messagebox.showerror("Registration Error", f"An error occurred: {str(e)}")

class SimpleMedicine:
    def __init__(self, name, composition, uses, side_effect):
        self.name = name
        self.composition = composition
        self.uses = uses
        self.side_effect = side_effect

class DisplayMedicinePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/admin's.jpg")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Display Medicine",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.45, rely=0.15)

        self.sort_option = ctk.CTkComboBox(
            self,
            values=[
                "Name (A-Z)", "Name (Z-A)",
                "Composition (A-Z)", "Composition (Z-A)",
                "Uses (A-Z)", "Uses (Z-A)",
                "Side Effect (A-Z)", "Side Effect (Z-A)"
            ],
            width=200,
            height=35,
            corner_radius=8,
            fg_color="#FF6B9D",
            text_color="#FFFFFF",
            bg_color= "#FF6B9D",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#000000",
            command=self.sort_and_reload
        )
        self.sort_option.place(relx=0.73, rely=0.2)
        self.sort_option.set("Name (A-Z)")

        self.table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", width=1500, height=1000, corner_radius=15,bg_color="#FF6B9D")
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

        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(self, text="Refresh Data", command=self.load_data, width=180, fg_color="#970032", text_color="#FFFFFF",bg_color="#FF6B9D", font=ctk.CTkFont(size=16, weight="bold"))
        self.refresh_button.place(relx=0.45, rely=0.85)

        self.load_data()

        frame_add = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_add.place(relx=0.05, rely=0.3, anchor="nw")

        add_image = Image.open("assets/images/add.png")
        self.add_image = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(120, 120))  
        self.add_button = ctk.CTkButton(
            frame_add, 
            image=self.add_image, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=120, 
            height=120,
            command=self.open_add_medicine_page
        )
        self.add_button.place(x=0, y=0)  

        frame_delete = ctk.CTkFrame(self, fg_color="#FF6B9D",width=100, height=100)
        frame_delete.place(relx=0.05, rely=0.44, anchor="nw")
        
        delete_image = Image.open("assets/images/delete.png")
        self.delete_image = ctk.CTkImage(light_image=delete_image, dark_image=delete_image, size=(100, 100))  
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
        frame_main_menu.place(relx=0.425, rely=0.07, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF",corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.07, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        data_raw = view_medicine_data()

        dll = DoubleLinkedList()
        for row in data_raw:
            medicine = SimpleMedicine(*row[:4])
            dll.append(medicine)

        key_mapping = {
            "Name": lambda med: med.name.lower(),
            "Composition": lambda med: med.composition.lower(),
            "Uses": lambda med: med.uses.lower(),
            "Side Effects": lambda med: med.side_effect.lower()
        }
        sort_key = key_mapping.get(self.sort_option.get(), lambda med: med.name.lower())

        dll.merge_sort(key=sort_key)

        for med in dll.to_list():
            self.table.insert("", "end", values=(med.name, med.composition, med.uses, med.side_effect))

    def sort_and_reload(self, choice=None):
        key_map = {
            "Name": lambda m: m.name.lower(),
            "Composition": lambda m: m.composition.lower(),
            "Uses": lambda m: m.uses.lower(),
            "Side Effect": lambda m: m.side_effect.lower()
        }

        selected = self.sort_option.get()
        field, order = selected.split(" (")

        dll = DoubleLinkedList()
        for row in view_medicine_data():
            if len(row) >= 4:
                medicine = SimpleMedicine(*row[:4])
                dll.append(medicine)

        dll.merge_sort(key=key_map[field])
        sorted_list = dll.to_list()

        if "Z-A" in selected:
            sorted_list.reverse()

        self.table.delete(*self.table.get_children())
        for med in sorted_list:
            self.table.insert("", "end", values=(med.name, med.composition, med.uses, med.side_effect))

    def open_add_medicine_page(self):
        self.parent.show_frame(AddMedicinePage)

    def open_delete_medicine_page(self):
        self.parent.show_frame(DeleteMedicinePage)
    
    def close_app(self):
        self.parent.destroy()
        sys.exit()

    def open_admin_login(self):
        self.parent.show_frame(AdminLoginScreen)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

class AddMedicinePage(ctk.CTkFrame):
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

    def __init__(self, parent):
        super().__init__(parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.parent = parent

        bg_image = Image.open("assets/images/admin's.jpg")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self, text="Add Medicine", 
            font=ctk.CTkFont(size=28, weight="bold"), 
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.pack(pady=120)

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
        frame_display.place(relx=0.05, rely=0.15, anchor="nw")

        display_image = Image.open("assets/images/display all.png")
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
        frame_delete.place(relx=0.05, rely=0.44, anchor="nw")

        delete_image = Image.open("assets/images/delete.png")
        self.delete_image = ctk.CTkImage(light_image=delete_image, dark_image=delete_image, size=(100, 100))  
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
        frame_main_menu.place(relx=0.425, rely=0.07, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF",corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), hover=False,command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D",corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.07, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), hover=False,command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

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
        self.parent.show_frame(DisplayMedicinePage)

    def open_delete_medicine_page(self):
        self.parent.show_frame(DeleteMedicinePage)
    
    def close_app(self):
        self.parent.destroy()
        sys.exit()

    def open_admin_login(self):
        self.parent.show_frame(AdminLoginScreen)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

from tkinter.ttk import Combobox
from models.search import binary_search_suggestions

class DeleteMedicinePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/admin's.jpg")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(self, text="Delete Medicine", font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFFFFF", fg_color="#FF6B9D")
        self.title_label.pack(pady=120)

        raw_data = view_medicine_data()
        dll = DoubleLinkedList()
        for row in raw_data:
            if row:
                dll.append(row[0])
        dll.merge_sort(key=lambda name: name.lower())
        self.medicine_names = dll.to_list()

        entry_wrapper = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=15,bg_color="#FF6B9D")
        entry_wrapper.pack(pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TCombobox",
                        fieldbackground="#FFFFFF",
                        background="#FFFFFF",
                        foreground="#FF6B9D",
                        borderwidth=0,
                        font=("Arial", 18))  

        self.name_entry = Combobox(entry_wrapper, width=55, font=("Arial", 18), style="Custom.TCombobox")
        self.name_entry.pack(padx=10, pady=10) 
        self.name_entry.bind("<KeyRelease>", self.update_suggestions)

        self.delete_button = ctk.CTkButton(self, text="Delete Medicine", command=self.delete_medicine_action, width=180, height=40, fg_color="#970032", bg_color="#FF6B9D", text_color="#FFFFFF", font=ctk.CTkFont(size=16, weight="bold"))
        self.delete_button.pack(pady=20)

        self.create_nav_buttons()

    def update_suggestions(self, event=None):
        input_text = self.name_entry.get()

        if not input_text:
            self.name_entry['values'] = []
            return

        matches = binary_search_suggestions(self.medicine_names, input_text)
        self.name_entry['values'] = matches

        if matches:
            self.name_entry.event_generate('<Down>')  

    def delete_medicine_action(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a medicine name.")
            return

        success, msg = delete_medicine(name)
        messagebox.showinfo("Delete Medicine", msg)

        if success:
            self.name_entry.delete(0, tk.END)

    def create_nav_buttons(self):
        frame_add = ctk.CTkFrame(self, fg_color="#FF6B9D", width=100, height=100)
        frame_add.place(relx=0.05, rely=0.3, anchor="nw")
        add_image = Image.open("assets/images/add.png")
        self.add_image = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(100, 100))  
        self.add_button = ctk.CTkButton(frame_add, image=self.add_image, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=100, height=100, command=self.open_add_medicine_page)
        self.add_button.place(x=0, y=0)

        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D", width=100, height=100)
        frame_display.place(relx=0.05, rely=0.15, anchor="nw")
        display_image = Image.open("assets/images/display all.png")
        self.display_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(100, 100))  
        self.display_button = ctk.CTkButton(frame_display, image=self.display_image, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=100, height=100, command=self.display_medicine)
        self.display_button.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.07, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.07, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(self, text="Exit", width=200,height=40, fg_color="transparent", text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold"), command=self.close_app)
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def open_add_medicine_page(self):
        self.parent.show_frame(AddMedicinePage)

    def display_medicine(self):
        self.parent.show_frame(DisplayMedicinePage)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

    def open_admin_login(self):
        self.parent.show_frame(AdminLoginScreen)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

class UserDashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.medicines = load_medicines("data/Medicine_1000_noimage.csv").to_list()
        
        self.show_display_medicine()

    def show_display_medicine(self):
        self.clear_frame()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Medicine Catalog",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.45, rely=0.175)

        self.sort_option = ctk.CTkComboBox(
            self,
            values=[
                "Name (A-Z)", "Name (Z-A)",
                "Composition (A-Z)", "Composition (Z-A)",
                "Uses (A-Z)", "Uses (Z-A)",
                "Side Effect (A-Z)", "Side Effect (Z-A)"
            ],
            width=200,
            height=35,
            corner_radius=8,
            fg_color="#FF6B9D",
            text_color="#FFFFFF",
            bg_color="#FF6B9D",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#000000",
            command=self.sort_and_reload
        )
        self.sort_option.place(relx=0.73, rely=0.2)
        self.sort_option.set("Name (A-Z)")

        self.table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", width=1500, height=1000, corner_radius=15, bg_color="#FF6B9D")
        self.table_frame.place(relx=0.2, rely=0.25)

        style = ttk.Style()
        style.configure("User.Treeview.Heading", 
                      background="#FF6B9D", 
                      foreground="#000000",  
                      font=("Arial", 12, "bold"))
        style.configure("User.Treeview", 
                      rowheight=30,  
                      bordercolor="#FF6B9D", 
                      borderwidth=2,
                      relief="ridge",
                      font=("Arial", 11))
        style.map("User.Treeview.Heading",
                background=[("active", "#E05A8A")],
                relief=[("active", "groove")])

        self.table = ttk.Treeview(
            self.table_frame, 
            columns=("Name", "Composition", "Uses", "Side Effects"), 
            show="headings", 
            height=18, 
            style="User.Treeview"
        )
        self.table.heading("Name", text="Name")
        self.table.heading("Composition", text="Composition")
        self.table.heading("Uses", text="Uses")
        self.table.heading("Side Effects", text="Side Effects")

        self.table.column("Name", width=320)
        self.table.column("Composition", width=320)
        self.table.column("Uses", width=320)
        self.table.column("Side Effects", width=320)

        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_nav_buttons()
        self.load_data()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        dll = DoubleLinkedList()
        for med in self.medicines:
            dll.append(med)

        key_mapping = {
            "Name": lambda med: med.name.lower(),
            "Composition": lambda med: med.composition.lower(),
            "Uses": lambda med: med.uses.lower(),
            "Side Effects": lambda med: med.side_effect.lower()
        }
        
        sort_key = key_mapping.get(self.sort_option.get().split(" (")[0], lambda med: med.name.lower())
        dll.merge_sort(key=sort_key)

        if "(Z-A)" in self.sort_option.get():
            med_list = reversed(dll.to_list())
        else:
            med_list = dll.to_list()

        for med in med_list:
            self.table.insert("", "end", values=(med.name, med.composition, med.uses, med.side_effect))

    def sort_and_reload(self, choice=None):
        self.load_data()

    def create_nav_buttons(self):
        frame_search = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_search.place(relx=0.045, rely=0.23, anchor="nw")
        
        search_img = Image.open("assets/images/search.png")
        self.search_icon = ctk.CTkImage(light_image=search_img, dark_image=search_img, size=(150, 150))  
        self.search_btn = ctk.CTkButton(
            frame_search, 
            image=self.search_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_search
        )
        self.search_btn.place(x=0, y=0)

        frame_fav = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_fav.place(relx=0.045, rely=0.35, anchor="nw")
        
        fav_img = Image.open("assets/images/star.png")
        self.fav_icon = ctk.CTkImage(light_image=fav_img, dark_image=fav_img, size=(150, 150))  
        self.fav_btn = ctk.CTkButton(
            frame_fav, 
            image=self.fav_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_favorites
        )
        self.fav_btn.place(x=0, y=0)

        frame_feedback = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_feedback.place(relx=0.045, rely=0.47, anchor="nw")
        
        feedback_img = Image.open("assets/images/feedback.png")
        self.feedback_icon = ctk.CTkImage(light_image=feedback_img, dark_image=feedback_img, size=(150, 150))  
        self.feedback_btn = ctk.CTkButton(
            frame_feedback, 
            image=self.feedback_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_feedback
        )
        self.feedback_btn.place(x=0, y=0)

        frame_history = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_history.place(relx=0.043, rely=0.6, anchor="nw")
        
        history_img = Image.open("assets/images/history.png")
        self.history_icon = ctk.CTkImage(light_image=history_img, dark_image=history_img, size=(150, 150))  
        self.history_btn = ctk.CTkButton(
            frame_history, 
            image=self.history_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_history
        )
        self.history_btn.place(x=0, y=0)

        frame_chatbot = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_chatbot.place(relx=0.043, rely=0.74, anchor="nw")
        
        chatbot_img = Image.open("assets/images/bot.png")
        self.chatbot_icon = ctk.CTkImage(light_image=chatbot_img, dark_image=chatbot_img, size=(150, 150))  
        self.chatbot_btn = ctk.CTkButton(
            frame_chatbot, 
            image=self.chatbot_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_chatbot
        )
        self.chatbot_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(
            frame_main_menu, 
            text="Main Menu", 
            width=150, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_main_menu
        )
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(
            frame_back, 
            text="Back", 
            width=100, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF", 
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_user_login
        )
        self.back_btn.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_search(self):
        self.parent.show_frame(SearchPage, medicines=self.medicines) 

    def open_favorites(self):
        self.parent.show_frame(FavoritePage)

    def open_feedback(self):
        self.parent.show_frame(FeedbackPage)

    def open_history(self):
        self.parent.show_frame(HistoryPage)
        
    def open_chatbot(self):
        self.parent.show_frame(ChatbotPage, medicines=self.medicines)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, medicines=None):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.medicines = load_medicines("data/Medicine_1000_noimage.csv").to_list() if medicines is None else medicines
        self.show_search_screen()

        dll = DoubleLinkedList()
        for med in self.medicines:
            dll.append(med.name)
        dll.merge_sort(key=lambda name: name.lower())
        self.medicine_names = dll.to_list()

    def show_search_screen(self):
        self.clear_frame()      
        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, 
                                    size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_container = ctk.CTkFrame(
            self, 
            fg_color="#FFFFFF", 
            width=self.winfo_screenwidth() * 0.75,  
            height=self.winfo_screenheight() * 0.9, 
            border_width=0,
            bg_color="#FF6B9D"
        )
        self.main_container.place(relx=0.538, rely=0.5, anchor="center")

        header = ctk.CTkFrame(
            self.main_container, 
            fg_color="#FF6B9D", 
            height=180, 
            corner_radius=20 
        )
        header.pack(fill="x", padx=25, pady=25)

        search_bar = ctk.CTkFrame(
            header, 
            fg_color="#FFFFFF", 
            height=100, 
            corner_radius=50
        )
        search_bar.pack(pady=40, padx=50, fill="x")
        
        search_icon = ctk.CTkLabel(
            search_bar, 
            text="🔍", 
            font=ctk.CTkFont(size=40), 
            text_color="#FF6B9D"
        )  
        search_icon.pack(side="left", padx=40)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'TCombobox', 
            fieldbackground='#FFFFFF',
            foreground='#000000',
            background='#FFFFFF',
            bordercolor='#FF6B9D',
            font=('Arial', 24),
            padding=16
        )
        style.map(
            'TCombobox', 
            fieldbackground=[('readonly', '#FFFFFF')],
            foreground=[('readonly', '#000000')]
        )
        
        self.search_entry = ttk.Combobox(
            search_bar,
            width=55,
            font=('Arial', 24),
            style='TCombobox'
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(15, 40), pady=20)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)

        self.split_container = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent",
        )
        self.split_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.after(100, lambda: self.setup_panels())

    def setup_panels(self):
        self.detail_panel = ctk.CTkScrollableFrame(
            self.split_container,
            width=self.split_container.winfo_width() * 0.7,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#FFE5ED",
            scrollbar_button_color="#FF6B9D",
            scrollbar_button_hover_color="#E05A8A"
        )
        self.detail_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))  

        self.results_panel = ctk.CTkScrollableFrame(
            self.split_container,
            fg_color="#FFF5F9",
            corner_radius=15,
            scrollbar_button_color="#FF6B9D",
            scrollbar_button_hover_color="#E05A8A"
        )
        self.results_panel.pack(side="right", fill="both", expand=True) 

        self.show_detail_placeholder()       
        self.create_nav_buttons()

    def update_suggestions(self, event=None):
        input_text = self.search_entry.get()
        
        if not input_text:
            self.search_entry['values'] = []
            self.show_popular_medicines()
            return
        
        matches = binary_search_suggestions(self.medicine_names, input_text)
        self.search_entry['values'] = matches
        
        if matches and (event is None or event.keysym not in ['Return', 'Tab']):
            self.search_entry.event_generate('<Down>')
        elif event and event.keysym in ['Return', 'Tab']:
            self.perform_search()

    def show_popular_medicines(self):
        for widget in self.results_panel.winfo_children():
            widget.destroy()
        
        dll = DoubleLinkedList()
        for med in self.medicines:
            dll.append(med)
        dll.merge_sort(key=lambda x: len(x.name))
        popular_meds = dll.to_list()[:10]
        
        ctk.CTkLabel(
            self.results_panel,
            text="Popular Medicines:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B9D"
        ).pack(pady=(10,5), anchor="w")
        
        for med in popular_meds:
            self.create_medicine_card(med)

    def perform_search(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_popular_medicines()
            return
        
        user_id = getattr(self.parent, "user_id", None)
        if user_id is not None and hasattr(self.parent, "history_manager"):
            self.parent.history_manager.add_history(user_id, query)

        for widget in self.results_panel.winfo_children():
            widget.destroy()
        results = [med for med in self.medicines if query.lower() in med.name.lower()]
        
        if results:
            ctk.CTkLabel(
                self.results_panel,
                text=f"Search Results ({len(results)}):",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#FF6B9D"
            ).pack(pady=(10,5), anchor="w")
            
            for med in results:
                self.create_medicine_card(med)
        else:
            ctk.CTkLabel(
                self.results_panel,
                text="No matching medicines found",
                text_color="#888888"
            ).pack(pady=20)

    def create_medicine_card(self, medicine):
        card = ctk.CTkFrame(
            self.results_panel, 
            fg_color="#FFFFFF", 
            corner_radius=10,
            border_width=1,
            border_color="#FFE5ED"
        )
        card.pack(fill="x", pady=5, padx=5)
        
        btn = ctk.CTkButton(
            card,
            text=medicine.name,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color="#FFF0F5",
            text_color="#FF6B9D",
            anchor="w",
            command=lambda m=medicine: self.show_medicine_detail(m)
        )
        btn.pack(fill="x", padx=10, pady=8)

    def show_detail_placeholder(self):
        for widget in self.detail_panel.winfo_children():
            widget.destroy()
        
        placeholder = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            placeholder,
            text="💊",
            font=ctk.CTkFont(size=40),
            text_color="#FFB6C1"
        ).pack()
        
        ctk.CTkLabel(
            placeholder,
            text="Select a medicine to view details",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        ).pack(pady=10)

    def show_medicine_detail(self, medicine):
        for widget in self.detail_panel.winfo_children():
            widget.destroy()
        
        scroll_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0,15))
        
        ctk.CTkLabel(
            header,
            text=medicine.name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF6B9D"
        ).pack(side="left")
        
        fav_btn = ctk.CTkButton(
            header,
            text="★ Add to Favorites",
            width=120,
            fg_color="#FF6B9D",
            hover_color="#E05A8A",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.add_to_favorites(medicine)
        )
        fav_btn.pack(side="right")
        
        details = [
            ("🧪 Composition", medicine.composition),
            ("🩺 Uses", medicine.uses),
            ("⚠️ Side Effects", medicine.side_effect)
        ]
        
        for icon, text in details:
            frame = ctk.CTkFrame(scroll_frame, fg_color="#FFF5F9", corner_radius=10)
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                frame,
                text=icon,
                font=ctk.CTkFont(size=16),
                text_color="#FF6B9D"
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                frame,
                text=text,
                font=ctk.CTkFont(size=13),
                text_color="#555555",
                wraplength=450,
                justify="left"
            ).pack(side="left", padx=5, pady=10, fill="x", expand=True)

    def add_to_favorites(self, medicine):
        try:
            user_id = getattr(self.parent, "user_id", 0)
            success = add_to_favorites(user_id, medicine.name)
            if success:
                messagebox.showinfo("Success", f"{medicine.name} added to favorites!")
            else:
                messagebox.showwarning("Info", f"{medicine.name} is already in your favorites!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to favorites: {str(e)}")

    def create_nav_buttons(self):
        frame_display = ctk.CTkFrame(self,fg_color="#FF6B9D", width=150, height=150)
        frame_display.place(relx=0.045, rely=0.11,anchor="nw")

        display_image = Image.open("assets/images/display all.png")
        self.display_icon = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(150, 150))  
        self.display_btn = ctk.CTkButton(
            frame_display, 
            image=self.display_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_user_dashboard
        )
        self.display_btn.place(x=0, y=0)

        frame_fav = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_fav.place(relx=0.045, rely=0.35, anchor="nw")
        
        fav_img = Image.open("assets/images/star.png")
        self.fav_icon = ctk.CTkImage(light_image=fav_img, dark_image=fav_img, size=(150, 150))  
        self.fav_btn = ctk.CTkButton(
            frame_fav, 
            image=self.fav_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_favorites
        )
        self.fav_btn.place(x=0, y=0)

        frame_feedback = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_feedback.place(relx=0.045, rely=0.47, anchor="nw")
        
        feedback_img = Image.open("assets/images/feedback.png")
        self.feedback_icon = ctk.CTkImage(light_image=feedback_img, dark_image=feedback_img, size=(150, 150))  
        self.feedback_btn = ctk.CTkButton(
            frame_feedback, 
            image=self.feedback_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_feedback
        )
        self.feedback_btn.place(x=0, y=0)

        frame_history = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_history.place(relx=0.043, rely=0.6, anchor="nw")
        
        history_img = Image.open("assets/images/history.png")
        self.history_icon = ctk.CTkImage(light_image=history_img, dark_image=history_img, size=(150, 150))  
        self.history_btn = ctk.CTkButton(
            frame_history, 
            image=self.history_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_history
        )
        self.history_btn.place(x=0, y=0)

        frame_chatbot = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_chatbot.place(relx=0.043, rely=0.74, anchor="nw")
        
        chatbot_img = Image.open("assets/images/bot.png")
        self.chatbot_icon = ctk.CTkImage(light_image=chatbot_img, dark_image=chatbot_img, size=(150, 150))  
        self.chatbot_btn = ctk.CTkButton(
            frame_chatbot, 
            image=self.chatbot_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_chatbot
        )
        self.chatbot_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(
            frame_main_menu, 
            text="Main Menu", 
            width=150, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_main_menu
        )
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(
            frame_back, 
            text="Back", 
            width=100, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF", 
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_user_login
        )
        self.back_btn.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_user_dashboard(self):
        self.parent.show_frame(UserDashboard)

    def open_favorites(self):
        self.parent.show_frame(FavoritePage)

    def open_feedback(self):
        self.parent.show_frame(FeedbackPage)

    def open_history(self):
        self.parent.show_frame(HistoryPage)

    def open_chatbot(self):
        self.parent.show_frame(ChatbotPage, medicines=self.medicines)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

class FavoritePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.show_favorite_screen()
        
    def show_favorite_screen(self):
        self.clear_frame()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.title_label = ctk.CTkLabel(
            self,
            text="Favorite Medicines",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.75, rely=0.1, anchor="center")

        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#FF6B9D",  
            corner_radius=15,
            border_width=2,
            bg_color="#FF6B9D",
            border_color="#FF6B9D"
        )
        self.main_frame.place(relx=0.55, rely=0.53, anchor="center", relwidth=0.75, relheight=0.7)  

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame, 
            fg_color="#FF6B9D",  
            scrollbar_button_color="#FFFFFF",
            scrollbar_button_hover_color="#E05A8A"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.initial_msg = ctk.CTkLabel(
            self.scroll_frame,
            text="Your favorite medicines will appear here",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",  # White text
            wraplength=400
        )
        self.initial_msg.pack(pady=40, padx=20)

        self.load_favorites()
        self.create_nav_buttons()
        
    def load_favorites(self):
        user_id = getattr(self.parent, "user_id", 0)
        favorites = get_favorites(user_id)
        
        if not favorites:
            no_favs = ctk.CTkLabel(
                self.scroll_frame,
                text="No favorite medicines found",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FFFFFF"
            )
            no_favs.pack(pady=40)
            return
            
        for med in favorites:
            self.create_medicine_card(med)

    def create_medicine_card(self, medicine):
        card_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color="#E05A8A",  
            corner_radius=10,
            border_width=1,
            border_color="#FFFFFF"
        )
        card_frame.pack(fill="x", pady=8, padx=5)

        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{medicine['Medicine Name']} - {medicine['Uses']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF",  
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(0,5))

        comp_label = ctk.CTkLabel(
            info_frame,
            text=f"Composition: {medicine['Composition']}",
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",  
            anchor="w"
        )
        comp_label.pack(anchor="w", pady=(0,5))

        side_label = ctk.CTkLabel(
            info_frame,
            text=f"Side Effects: {medicine['Side_effects']}",
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",  # White text
            anchor="w"
        )
        side_label.pack(anchor="w")

        remove_btn = ctk.CTkButton(
            card_frame,
            text="Remove",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#970032",
            hover_color="#E05A8A",
            bg_color="#E05A8A",
            text_color="#FFFFFF",
            width=100,
            height=30,
            command=lambda m=medicine: self.remove_favorite(m)
        )
        remove_btn.pack(side="right", padx=10, pady=10)

    def remove_favorite(self, medicine):
        user_id = self.parent.current_user.id if hasattr(self.parent, 'current_user') else 0
        success, message = remove_from_favorites(user_id, medicine['Medicine Name'])
        if success:
            messagebox.showinfo("Success", message)
            self.clear_frame()
            self.show_favorite_screen()
        else:
            messagebox.showerror("Error", message)

    def create_nav_buttons(self):
        frame_display = ctk.CTkFrame(self,fg_color="#FF6B9D", width=150, height=150)
        frame_display.place(relx=0.045, rely=0.11,anchor="nw")

        display_image = Image.open("assets/images/display all.png")
        self.display_icon = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(150, 150))  
        self.display_btn = ctk.CTkButton(
            frame_display, 
            image=self.display_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_user_dashboard
        )
        self.display_btn.place(x=0, y=0)

        frame_search = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_search.place(relx=0.045, rely=0.23, anchor="nw")
        
        search_img = Image.open("assets/images/search.png")
        self.search_icon = ctk.CTkImage(light_image=search_img, dark_image=search_img, size=(150, 150))  
        self.search_btn = ctk.CTkButton(
            frame_search, 
            image=self.search_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_search
        )
        self.search_btn.place(x=0, y=0)

        frame_feedback = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_feedback.place(relx=0.045, rely=0.47, anchor="nw")
        
        feedback_img = Image.open("assets/images/feedback.png")
        self.feedback_icon = ctk.CTkImage(light_image=feedback_img, dark_image=feedback_img, size=(150, 150))  
        self.feedback_btn = ctk.CTkButton(
            frame_feedback, 
            image=self.feedback_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_feedback
        )
        self.feedback_btn.place(x=0, y=0)

        frame_history = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_history.place(relx=0.043, rely=0.6, anchor="nw")
        
        history_img = Image.open("assets/images/history.png")
        self.history_icon = ctk.CTkImage(light_image=history_img, dark_image=history_img, size=(150, 150))  
        self.history_btn = ctk.CTkButton(
            frame_history, 
            image=self.history_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_history
        )
        self.history_btn.place(x=0, y=0)

        frame_chatbot = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_chatbot.place(relx=0.043, rely=0.74, anchor="nw")
        
        chatbot_img = Image.open("assets/images/bot.png")
        self.chatbot_icon = ctk.CTkImage(light_image=chatbot_img, dark_image=chatbot_img, size=(150, 150))  
        self.chatbot_btn = ctk.CTkButton(
            frame_chatbot, 
            image=self.chatbot_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_chatbot
        )
        self.chatbot_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(
            frame_main_menu, 
            text="Main Menu", 
            width=150, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_main_menu
        )
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(
            frame_back, 
            text="Back", 
            width=100, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF", 
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_user_login
        )
        self.back_btn.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_user_dashboard(self):
        self.parent.show_frame(UserDashboard)

    def open_search(self):
        self.parent.show_frame(SearchPage)

    def open_feedback(self):
        self.parent.show_frame(FeedbackPage)

    def open_history(self):
        self.parent.show_frame(HistoryPage)

    def open_chatbot(self):
        self.parent.show_frame(ChatbotPage)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.show_history_screen()
        
    def show_history_screen(self):
        self.clear_frame()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Search History",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.75, rely=0.1, anchor="center")
        
        self.history_frame = ctk.CTkScrollableFrame(self, fg_color="#FF6B9D",corner_radius=15,
            border_width=2,
            bg_color="#FF6B9D",
            border_color="#FF6B9D")
        self.history_frame.place(relx=0.55, rely=0.2, anchor="n", relwidth=0.75, relheight=0.7)
        
        self.load_history()
        self.create_nav_buttons()

    def load_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        user_id = getattr(self.parent, "user_id", None)
        if user_id is not None and hasattr(self.parent, "history_manager"):
            history = self.parent.history_manager.get_history(user_id)
        else:
            history = []

        if not history:
            empty_label = ctk.CTkLabel(
                self.history_frame,
                text="Your search history is empty.",
                font=ctk.CTkFont(family="Roboto Flex", size=14),
                text_color="#FF6B9D"
            )
            empty_label.pack(pady=50)
            return
            
        for entry in history:
            self.create_history_card(entry)

    def create_history_card(self, entry):
        hist_frame = ctk.CTkFrame(self.history_frame, fg_color="#FFFFFF", corner_radius=5)
        hist_frame.pack(fill="x", pady=5, padx=5)
        
        hist_info = ctk.CTkLabel(
            hist_frame,
            text=f"Search Term: {entry['search_term']}\n"
                f"Timestamp: {entry['timestamp']}",
            font=ctk.CTkFont(family="Roboto Flex", size=12),
            text_color="#FF6B9D",
            anchor="w",
            justify="left"
        )
        hist_info.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        repeat_btn = ctk.CTkButton(
            hist_frame,
            text="Repeat Search",
            font=ctk.CTkFont(family="Roboto Flex", size=10),
            fg_color="#970032",
            text_color="#FFFFFF",
            hover_color="#E05A8A",
            bg_color="#FFFFFF",
            width=100,
            command=lambda term=entry['search_term']: self.repeat_search(term)
        )
        repeat_btn.pack(side="right", padx=10)

    def repeat_search(self, search_term):
        self.parent.show_frame(SearchPage)
        self.parent.after(100, lambda: self._do_repeat_search(search_term))

    def _do_repeat_search(self, search_term):
        search_page = self.parent.active_frame
        if hasattr(search_page, "search_entry"):
            search_page.search_entry.delete(0, tk.END)
            search_page.search_entry.insert(0, search_term)
            if hasattr(search_page, "perform_search"):
                search_page.perform_search()

    # def repeat_search(self, search_term):
    #     self.controller.show_page("Search")
    #     self.controller.pages["Search"].search_entry.insert(0, search_term)
    #     self.controller.pages["Search"].perform_search()

    def create_nav_buttons(self):
        frame_display = ctk.CTkFrame(self,fg_color="#FF6B9D", width=150, height=150)
        frame_display.place(relx=0.045, rely=0.11,anchor="nw")

        display_image = Image.open("assets/images/display all.png")
        self.display_icon = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(150, 150))  
        self.display_btn = ctk.CTkButton(
            frame_display, 
            image=self.display_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_user_dashboard
        )
        self.display_btn.place(x=0, y=0)

        frame_search = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_search.place(relx=0.045, rely=0.23, anchor="nw")
        search_img = Image.open("assets/images/search.png")
        self.search_icon = ctk.CTkImage(light_image=search_img, dark_image=search_img, size=(150, 150))
        self.search_btn = ctk.CTkButton(frame_search, image=self.search_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_search)
        self.search_btn.place(x=0, y=0)

        frame_fav = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_fav.place(relx=0.045, rely=0.35, anchor="nw")
        
        fav_img = Image.open("assets/images/star.png")
        self.fav_icon = ctk.CTkImage(light_image=fav_img, dark_image=fav_img, size=(150, 150))  
        self.fav_btn = ctk.CTkButton(
            frame_fav, 
            image=self.fav_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_favorites
        )
        self.fav_btn.place(x=0, y=0)

        frame_feedback = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_feedback.place(relx=0.045, rely=0.47, anchor="nw")
        
        feedback_img = Image.open("assets/images/feedback.png")
        self.feedback_icon = ctk.CTkImage(light_image=feedback_img, dark_image=feedback_img, size=(150, 150))  
        self.feedback_btn = ctk.CTkButton(
            frame_feedback, 
            image=self.feedback_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_feedback
        )
        self.feedback_btn.place(x=0, y=0)

        frame_chatbot = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_chatbot.place(relx=0.043, rely=0.74, anchor="nw")
        
        chatbot_img = Image.open("assets/images/bot.png")
        self.chatbot_icon = ctk.CTkImage(light_image=chatbot_img, dark_image=chatbot_img, size=(150, 150))  
        self.chatbot_btn = ctk.CTkButton(
            frame_chatbot, 
            image=self.chatbot_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_chatbot
        )
        self.chatbot_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(
            frame_main_menu, 
            text="Main Menu", 
            width=150, 
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",
            corner_radius=5, 
            hover=False,
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_main_menu
        )
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(
            frame_back, 
            text="Back", 
            width=100, 
            hover=False,
            fg_color="#FF6B9D", 
            text_color="#FFFFFF", 
            corner_radius=5, 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.open_user_dashboard
        )
        self.back_btn.pack()

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            width=200, 
            height=40,
            fg_color="transparent", 
            text_color="#FFFFFF", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            command=self.close_app
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_user_dashboard(self):
        self.parent.show_frame(UserDashboard)

    def open_favorites(self):
        self.parent.show_frame(FavoritePage)

    def open_feedback(self):
        self.parent.show_frame(FeedbackPage)

    def open_search(self):
        self.parent.show_frame(SearchPage)

    def open_chatbot(self):
        self.parent.show_frame(ChatbotPage)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

    def close_app(self): 
        self.parent.destroy()
        sys.exit()

class FeedbackPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.medicine_names = self.load_medicines_names()
        self.show_feedback_screen()

    def load_medicines_names(self):
        medicine_names = []
        dataset_path = os.path.join('data', 'Medicine_1000_noimage.csv')
        if os.path.exists(dataset_path):
            with open(dataset_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    medicine_names.append(row['Medicine Name'])
        dll = DoubleLinkedList()
        for name in medicine_names:
            dll.append(name)
        dll.merge_sort(key=lambda x: x.lower())
        return dll.to_list()
    
    def get_username(self):
        user_id = self.parent.user_id if hasattr(self.parent, 'user_id') else None
        if not user_id:
            return "Unknown User"

        users_csv_path = os.path.join('data', 'users.csv')
        if os.path.exists(users_csv_path):
            with open(users_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['user_id'] == str(user_id):
                        return row['username']
        return "Unknown User"
    
    def show_feedback_screen(self):
        self.clear_frame()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Feedback",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.75, rely=0.1, anchor="center")

        main_frame = ctk.CTkFrame(
            self,
            fg_color="#FF6B9D",
            border_color="#FF6B9D",
            bg_color="#FF6B9D",
            border_width=2,
            corner_radius=15
        )
        main_frame.place(relx=0.55, rely=0.53, anchor="center", relwidth=0.7, relheight=0.7)  

        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#FF6B9D",
            corner_radius=10
        )
        input_frame.pack(fill="x", padx=20, pady=20)

        medicine_rating_frame = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        medicine_rating_frame.pack(fill="x", padx=15, pady=(5,5))

        medicine_label = ctk.CTkLabel(
            medicine_rating_frame,
            text="Medicine Name:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF"
        )
        medicine_label.grid(row=0, column=0, sticky="w", pady=(0,5))
        
        self.medicine_combo = ctk.CTkComboBox(
            medicine_rating_frame,
            width=300,
            values=[],
            font=ctk.CTkFont(size=13),
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#FF6B9D",
            button_color="#FF6B9D"
        )
        self.medicine_combo.grid(row=1, column=0, sticky="w", pady=(0,15))
        self.medicine_combo.set("") 
        self.medicine_combo.bind("<KeyRelease>", self.update_suggestions)

        rating_label = ctk.CTkLabel(
            medicine_rating_frame,
            text="Rating:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF"
        )
        rating_label.grid(row=0, column=1, sticky="w", padx=(50,0), pady=(0,5))
        
        self.rating_combo = ctk.CTkComboBox(
            medicine_rating_frame,
            values=["Excellent", "Average", "Poor"],
            width=150,
            font=ctk.CTkFont(size=13),
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#333333",
            button_color="#FF6B9D"
        )
        self.rating_combo.set("Excellent")
        self.rating_combo.grid(row=1, column=1, sticky="w", padx=(50,0), pady=(0,15))

        feedback_label = ctk.CTkLabel(
            input_frame,
            text="Your Feedback:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF"
        )
        feedback_label.pack(anchor="w", padx=15, pady=(5,5))
        
        self.feedback_text = ctk.CTkTextbox(
            input_frame,
            width=580,
            height=50, 
            font=ctk.CTkFont(size=13),
            fg_color="#FFFFFF",
            border_color="#FF6B9D",
            border_width=1,
            text_color="#FF6B9D"
        )
        self.feedback_text.pack(fill="x", padx=15, pady=(0,15))

        submit_button = ctk.CTkButton(
            input_frame,
            text="Submit Feedback",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#970032",
            hover_color="#800029",
            text_color="#FFFFFF",
            width=200,
            height=40,
            command=self.submit_feedback
        )
        submit_button.pack(pady=(10,15))  

        history_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#FFFFFF",
            corner_radius=10
        )
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        history_title = ctk.CTkLabel(
            history_frame,
            text="Feedback History",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF6B9D"
        )
        history_title.pack(pady=(15,10))

        self.history_scroll = ctk.CTkScrollableFrame(
            history_frame,
            fg_color="#FFFFFF",
            scrollbar_button_color="#FF6B9D",
            height=180  
        )
        self.history_scroll.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
        self.create_nav_buttons()
        self.display_feedback_history()

    def update_suggestions(self, event):
        input_text = self.medicine_combo.get()
        
        if not input_text:
            self.medicine_combo.configure(values=[])
            return
        
        matches = binary_search_suggestions(self.medicine_names, input_text)
        self.medicine_combo.configure(values=matches)
        
        if matches and (event is None or event.keysym not in ['Return', 'Tab']):
            self.medicine_combo._open_dropdown_menu()

    def submit_feedback(self):
        medicine_name = self.medicine_combo.get().strip()
        rating = self.rating_combo.get()
        feedback = self.feedback_text.get("1.0", "end-1c").strip()

        if not medicine_name or not feedback:
            messagebox.showwarning("Warning", "Medicine name and feedback cannot be empty.")
            return
        
        if medicine_name not in self.medicine_names:
            messagebox.showerror("Error", "Selected medicine is not in the dataset.")
            return

        user_id = self.parent.current_user.id if hasattr(self.parent, 'current_user') else 0
        username = self.get_username()
        success, message = add_user_feedback(user_id, username, medicine_name, rating, feedback)
        messagebox.showinfo("Feedback", message)

        if success:
            self.medicine_combo.set("")
            self.feedback_text.delete("1.0", "end")
            self.rating_combo.set("Excellent")
            self.display_feedback_history()

    def display_feedback_history(self):
        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        feedbacks = get_all_feedbacks()

        if not feedbacks:
            empty_label = ctk.CTkLabel(
                self.history_scroll,
                text="No feedback history available",
                font=ctk.CTkFont(size=14),
                text_color="#777777"
            )
            empty_label.pack(pady=40)
            return

        for feedback in reversed(feedbacks):
            feedback_card = ctk.CTkFrame(
                self.history_scroll,
                fg_color="#FFF0F5",
                corner_radius=10,
                border_color="#FF6B9D",
                border_width=1
            )
            feedback_card.pack(fill="x", pady=5, padx=5)

            header_frame = ctk.CTkFrame(feedback_card, fg_color="transparent")
            header_frame.pack(fill="x", padx=10, pady=(10,5))

            username_label = ctk.CTkLabel(
                header_frame,
                text=feedback['username'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#333333"
            )
            username_label.pack(side="left")

            rating_color = {
                "Excellent": "#4CAF50", 
                "Average": "#FFC107", 
                "Poor": "#F44336"
            }.get(feedback['rating'], "#333333")
            
            rating_label = ctk.CTkLabel(
                header_frame,
                text=feedback['rating'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=rating_color
            )
            rating_label.pack(side="right")

            medicine_label = ctk.CTkLabel(
                feedback_card,
                text=f"Medicine: {feedback['medicine_name']}",
                font=ctk.CTkFont(size=12),
                text_color="#555555"
            )
            medicine_label.pack(anchor="w", padx=10, pady=(0,5))

            comment_label = ctk.CTkLabel(
                feedback_card,
                text=feedback['comment'],
                font=ctk.CTkFont(size=12),
                text_color="#333333",
                wraplength=600,
                justify="left"
            )
            comment_label.pack(anchor="w", padx=10, pady=(0,5))

            timestamp_label = ctk.CTkLabel(
                feedback_card,
                text=f"Submitted: {feedback['timestamp']}",
                font=ctk.CTkFont(size=10),
                text_color="#777777"
            )
            timestamp_label.pack(anchor="w", padx=10, pady=(0,10))

    def create_nav_buttons(self):
        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_display.place(relx=0.045, rely=0.11, anchor="nw")
        display_image = Image.open("assets/images/display all.png")
        self.display_icon = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(150, 150))
        self.display_btn = ctk.CTkButton(frame_display, image=self.display_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_user_dashboard)
        self.display_btn.place(x=0, y=0)

        frame_search = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_search.place(relx=0.045, rely=0.23, anchor="nw")
        search_img = Image.open("assets/images/search.png")
        self.search_icon = ctk.CTkImage(light_image=search_img, dark_image=search_img, size=(150, 150))
        self.search_btn = ctk.CTkButton(frame_search, image=self.search_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_search)
        self.search_btn.place(x=0, y=0)

        frame_fav = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_fav.place(relx=0.045, rely=0.35, anchor="nw")
        fav_img = Image.open("assets/images/star.png")
        self.fav_icon = ctk.CTkImage(light_image=fav_img, dark_image=fav_img, size=(150, 150))
        self.fav_btn = ctk.CTkButton(frame_fav, image=self.fav_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_favorites)
        self.fav_btn.place(x=0, y=0)

        frame_history = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_history.place(relx=0.043, rely=0.6, anchor="nw")
        history_img = Image.open("assets/images/history.png")
        self.history_icon = ctk.CTkImage(light_image=history_img, dark_image=history_img, size=(150, 150))
        self.history_btn = ctk.CTkButton(frame_history, image=self.history_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_history)
        self.history_btn.place(x=0, y=0)

        frame_chatbot = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_chatbot.place(relx=0.043, rely=0.74, anchor="nw")
        chatbot_img = Image.open("assets/images/bot.png")
        self.chatbot_icon = ctk.CTkImage(light_image=chatbot_img, dark_image=chatbot_img, size=(150, 150))
        self.chatbot_btn = ctk.CTkButton(frame_chatbot, image=self.chatbot_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_chatbot)
        self.chatbot_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_main_menu)
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(frame_back, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_user_dashboard)
        self.back_btn.pack()

        self.exit_btn = ctk.CTkButton(self, text="Exit", width=200,height=40, fg_color="transparent", text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold"), command=self.close_app)
        self.exit_btn.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_user_dashboard(self):
        self.parent.show_frame(UserDashboard)

    def open_favorites(self):
        self.parent.show_frame(FavoritePage)

    def open_search(self):
        self.parent.show_frame(SearchPage)

    def open_history(self):
        self.parent.show_frame(HistoryPage)

    def open_chatbot(self):
        self.parent.show_frame(ChatbotPage)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

class ChatbotPage(ctk.CTkFrame):
    def __init__(self, parent, medicines=None):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        self.username = self.get_username()
        self.medicines = medicines if medicines is not None else load_medicines('data/Medicine_1000_noimage.csv').to_list()
        self.create_nav_buttons()
        self.create_chatbot_ui()

    def get_username(self):
        user_id = getattr(self.parent, "user_id", None)
        if not user_id:
            return "Unknown User"
        users_csv_path = os.path.join('data', 'users.csv')
        if os.path.exists(users_csv_path):
            with open(users_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['user_id'] == str(user_id):
                        return row['username']
        return "Unknown User"

    def create_chatbot_ui(self):
        self.clear_frame()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("assets/images/user's.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Chatbot",
            font=ctk.CTkFont(family="Roboto Flex", size=32, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#FF6B9D"
        )
        self.title_label.place(relx=0.75, rely=0.1, anchor="center")

        self.bot_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            border_color="#FF6B9D",
            bg_color="#FF6B9D",
            border_width=2,
            corner_radius=15,
            width=1450,  
            height=750  
        )
        self.bot_frame.place(relx=0.55, rely=0.54, anchor="center")

        self.chat_area = ctk.CTkTextbox(
            self.bot_frame,
            width=1300,
            height=650,
            state="disabled",
            fg_color="#FF6B9D",
            text_color="#FFFFFF",  
            font=ctk.CTkFont(size=18),
            wrap="word"
        )
        self.chat_area.place(relx=0.5, rely=0.45, anchor="center")

        input_frame = ctk.CTkFrame(
            self.bot_frame,
            fg_color="#FFFFFF",
            height=60
        )
        input_frame.place(relx=0.5, rely=0.9, y=30, anchor="center")

        self.entry = ctk.CTkEntry(
            input_frame,
            width=600,
            height=40,
            placeholder_text="Type your message here...",
            fg_color="#FFFFFF",
            border_color="#FF6B9D",
            text_color="#FF6B9D"
        )
        self.entry.pack(anchor="center", side="left", padx=5)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100,
            height=40,
            fg_color="#970032",
            hover_color="#800029",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self.send_message
        )
        self.send_btn.pack(anchor="center", side="right", padx=5)

        self.bot_greeted = False
        self.show_bot_chat()
        self.create_nav_buttons()

    def show_bot_chat(self):
        user_id = getattr(self.parent, "user_id", None)
        
        if not self.bot_greeted:
            welcome_msg = (
                f"Pharmora: Hi {self.username}! I'm here to help you with medicine information.\n"
                "You can ask me about:\n"
                "- Medicine details\n"
                "- Side effects\n"
                "- Usage instructions\n"
                "Type 'history' to see your previous queries.\n"
            )
            self.display_message(welcome_msg)
            
            for chat in load_from_csv(user_id):
                self.display_message(chat)
            
            self.bot_greeted = True

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        
        user_id = getattr(self.parent, "user_id", None)
        
        self.display_message(f"You: {user_input}", is_user=True)
        save_to_csv(user_id, f"You: {user_input}")
        
        bot_response = response_bot(user_input, self.medicines)
        self.display_message(f"Pharmora: {bot_response}")
        save_to_csv(user_id, f"Pharmora: {bot_response}")
        
        self.entry.delete(0, "end")

        if user_input.lower() in ["exit", "quit", "keluar"]:
            self.display_message("Pharmora: Thank you for chatting with me! Stay healthy!")
            return

        if user_input.lower() in ["history", "riwayat"]:
            self.show_chat_history()
            return

    def show_chat_history(self):
        user_id = getattr(self.parent, "user_id", None)
        self.display_message("\nPharmora: Your chat history:")
        for chat in load_from_csv(user_id):
            self.display_message(chat)

    def display_message(self, msg, is_user=False):
        self.chat_area.configure(state="normal")
        
        if is_user:
            self.chat_area.tag_config("user", foreground="#970032")  
        
        if is_user:
            self.chat_area.insert("end", msg + "\n", "user")
        else:
            self.chat_area.insert("end", msg + "\n")
        
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def create_nav_buttons(self):
        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_display.place(relx=0.045, rely=0.11, anchor="nw")
        display_image = Image.open("assets/images/display all.png")
        self.display_icon = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(150, 150))
        self.display_btn = ctk.CTkButton(frame_display, image=self.display_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_user_dashboard)
        self.display_btn.place(x=0, y=0)

        frame_search = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_search.place(relx=0.045, rely=0.23, anchor="nw")
        search_img = Image.open("assets/images/search.png")
        self.search_icon = ctk.CTkImage(light_image=search_img, dark_image=search_img, size=(150, 150))
        self.search_btn = ctk.CTkButton(frame_search, image=self.search_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_search)
        self.search_btn.place(x=0, y=0)

        frame_fav = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_fav.place(relx=0.045, rely=0.35, anchor="nw")
        fav_img = Image.open("assets/images/star.png")
        self.fav_icon = ctk.CTkImage(light_image=fav_img, dark_image=fav_img, size=(150, 150))
        self.fav_btn = ctk.CTkButton(frame_fav, image=self.fav_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_favorites)
        self.fav_btn.place(x=0, y=0)

        frame_history = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_history.place(relx=0.043, rely=0.6, anchor="nw")
        history_img = Image.open("assets/images/history.png")
        self.history_icon = ctk.CTkImage(light_image=history_img, dark_image=history_img, size=(150, 150))
        self.history_btn = ctk.CTkButton(frame_history, image=self.history_icon, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=150, height=150, command=self.open_history)
        self.history_btn.place(x=0, y=0)

        frame_feedback = ctk.CTkFrame(self, fg_color="#FF6B9D", width=150, height=150)
        frame_feedback.place(relx=0.045, rely=0.47, anchor="nw")
        feedback_img = Image.open("assets/images/feedback.png")
        self.feedback_icon = ctk.CTkImage(light_image=feedback_img, dark_image=feedback_img, size=(150, 150))  
        self.feedback_btn = ctk.CTkButton(
            frame_feedback, 
            image=self.feedback_icon, 
            text="", 
            fg_color="#FF6B9D", 
            hover_color="#FFFFFF", 
            width=150, 
            height=150,
            command=self.open_feedback
        )
        self.feedback_btn.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.425, rely=0.115, anchor="sw")
        self.main_menu_btn = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_main_menu)
        self.main_menu_btn.pack()

        frame_back = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back.place(relx=0.25, rely=0.115, anchor="sw")
        self.back_btn = ctk.CTkButton(frame_back, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"),hover=False, command=self.open_user_dashboard)
        self.back_btn.pack()

        self.exit_btn = ctk.CTkButton(self, text="Exit", width=200,height=40, fg_color="transparent", text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold"), command=self.close_app)
        self.exit_btn.place(relx=0.95, rely=0.95, anchor="se")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_user_dashboard(self):
        self.parent.show_frame(UserDashboard)

    def open_search(self):
        self.parent.show_frame(SearchPage)

    def open_favorites(self):
        self.parent.show_frame(FavoritePage)

    def open_feedback(self):
        self.parent.show_frame(FeedbackPage)

    def open_history(self):
        self.parent.show_frame(HistoryPage)

    def open_main_menu(self):
        self.parent.show_frame(WhichOneScreen)

    def close_app(self):
        self.parent.destroy()
        sys.exit()

if __name__ == "__main__":
    app = AppManager()
    app.mainloop()