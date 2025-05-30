import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox, ttk
from PIL import Image
from tkinter.ttk import Combobox
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import login_user, register_user, is_username_exist
from admin.admin_features import add_medicine, view_medicine_data, delete_medicine
from models.linked_list import DoubleLinkedList
from models.medicine import Medicine
from models.search import binary_search_suggestions
from features.pharmora_bot import save_to_csv, load_from_csv, response_bot
from loader import load_medicines

class AppManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pharmora")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.resizable(False, False)
        self.active_frame = None

        self.show_frame(LoadingScreen)

    def show_frame(self, frame_class):
        if self.active_frame is not None:
            self.active_frame.pack_forget()  
            self.active_frame.destroy()      
        self.active_frame = frame_class(self)
        self.active_frame.pack(fill="both", expand=True)

class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/loading.png")
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

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/1st page.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        baloo_font = (r"C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/fonts/BalooBhai2-VariableFont_wght.ttf", 30, "bold")

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

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/which one.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.admin_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.admin_frame.place(relx=0.32, rely=0.8, anchor="center")

        baloo_font = ("Baloo Bhai 2", 30, "bold")
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
        self.parent.show_frame(AdminLoginScreen)

    def open_user_login(self):
        self.parent.show_frame(UserLoginScreen)

class AdminLoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()

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
        frame_signin_button.place(relx=0.19, rely=0.8, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.69, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_signup_screen)
        self.signup_button.pack()

    def show_signup_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

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
        frame_signup_button.place(relx=0.69, rely=0.75, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.19, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id, role = login_user(username, password)

        if user_id and role == "admin":
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
            self.parent.show_frame(DisplayMedicinePage)
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

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin.png")
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
        self.title_label.place(relx=0.45, rely=0.1)

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

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin.png")
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

        bg_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/admin.png")
        self.bg_photo = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(screen_width, screen_height))

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(self, text="Delete Medicine", font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFFFFF", fg_color="#FF6B9D")
        self.title_label.pack(pady=80)

        raw_data = view_medicine_data()
        self.medicine_names = sorted([row[0] for row in raw_data if row])

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
        frame_add.place(relx=0.043, rely=0.28, anchor="nw")
        add_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/add.png")
        self.add_image = ctk.CTkImage(light_image=add_image, dark_image=add_image, size=(100, 100))  
        self.add_button = ctk.CTkButton(frame_add, image=self.add_image, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=100, height=100, command=self.open_add_medicine_page)
        self.add_button.place(x=0, y=0)

        frame_display = ctk.CTkFrame(self, fg_color="#FF6B9D", width=100, height=100)
        frame_display.place(relx=0.043, rely=0.15, anchor="nw")
        display_image = Image.open("C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/assets/images/display all.png")
        self.display_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(100, 100))  
        self.display_button = ctk.CTkButton(frame_display, image=self.display_image, text="", fg_color="#FF6B9D", hover_color="#FFFFFF", width=100, height=100, command=self.display_medicine)
        self.display_button.place(x=0, y=0)

        frame_main_menu = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_main_menu.place(relx=0.4, rely=0.08, anchor="sw")
        self.main_menu_button = ctk.CTkButton(frame_main_menu, text="Main Menu", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_main_menu)
        self.main_menu_button.pack()

        frame_back_button = ctk.CTkFrame(self, fg_color="#FF6B9D", corner_radius=5)
        frame_back_button.place(relx=0.25, rely=0.08, anchor="sw")
        self.back_button = ctk.CTkButton(frame_back_button, text="Back", width=100, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=5, font=ctk.CTkFont(size=18, weight="bold"), command=self.open_admin_login)
        self.back_button.pack()

        self.exit_button = ctk.CTkButton(self, text="Exit", width=100, fg_color="transparent", text_color="#FFFFFF", font=ctk.CTkFont(size=18, weight="bold"), command=self.close_app)
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

class UserLoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="transparent")
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()

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
        frame_signin_button.place(relx=0.19, rely=0.8, anchor="w")
        self.signin_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.login)
        self.signin_button.pack()

        frame_signup_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signup_button.place(relx=0.69, rely=0.605, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Create Account", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_signup_screen)
        self.signup_button.pack()

    def show_signup_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

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
        frame_signup_button.place(relx=0.69, rely=0.75, anchor="w")
        self.signup_button = ctk.CTkButton(frame_signup_button, text="Sign Up", width=150, fg_color="#FFFFFF", text_color="#FF6B9D", corner_radius=0, border_width=0, hover=False, command=self.register)
        self.signup_button.pack()

        frame_signin_button = ctk.CTkFrame(self, fg_color="#FF6B9D")
        frame_signin_button.place(relx=0.19, rely=0.625, anchor="w")
        self.back_button = ctk.CTkButton(frame_signin_button, text="Sign In", width=150, fg_color="#FF6B9D", text_color="#FFFFFF", corner_radius=0, border_width=0, hover=False, command=self.show_login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id, role = login_user(username, password)

        if user_id and role == "admin":
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
            self.parent.show_frame(UserDashboard)
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
    app = AppManager()
    app.mainloop()


# ======== Content from gui3.py below ========

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pandas as pd

class UserDashboard:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.bg_color = controller.bg_color
        self.baloo_font = controller.baloo_font
        self.roboto_flex_font = controller.roboto_flex_font
        self.button_color = controller.button_color
        self.white = controller.white
        self.dark_text = controller.dark_text
        self.gray_text = controller.gray_text
        self.pink_display = controller.pink_display
        
        self.setup_ui()

    def setup_ui(self):
        """Setup the main user dashboard"""
        self.clear_frame()

        self.user_display_frame = tk.Frame(self.root, bg=self.bg_color)
        self.user_display_frame.pack(fill=tk.BOTH, expand=True)

        # Load background image
        bg_path = os.path.join(self.controller.assets_path, "images/user's.png")
        if not os.path.exists(bg_path):
            print(f"Error: Background image not found at {bg_path}")
            return

        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.user_display_frame, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Left menu buttons (Vertical alignment)
        left_button_frame = tk.Frame(self.root)
        left_button_frame.place(x=20, y=500, anchor=tk.W)

        left_buttons = [
            ("Display All Medicine", self.controller.show_all_medicines),
            ("Search", self.controller.show_search),
            ("Favorite", self.controller.show_favorites),
            ("Feedback", self.controller.show_feedback),
            ("History", self.controller.show_history),
            ("Chatbot", self.controller.show_chatbot),
        ]

        for text, command in left_buttons:
            btn = tk.Button(
                left_button_frame,
                text=text,
                font=(self.baloo_font, 12, "bold"),
                bg='#FF6B9D',
                fg='white',
                relief=tk.FLAT,
                command=command,
                padx=30,
                pady=10
            )
            btn.pack(pady=10, fill=tk.X)

        # Navigation buttons
        self.setup_navigation_buttons()

    def setup_navigation_buttons(self):
        """Setup common navigation buttons"""
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=(self.baloo_font, 16),
            fg="#fffff0",
            bg='#FF6B9D',
            relief=tk.FLAT,
            command=self.controller.show_welcome_screen,
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
            font=(self.baloo_font, 16),
            fg="#fffff0",
            bg='#FF6B9D',
            relief=tk.FLAT,
            command=self.controller.show_admin_dashboard,  
            padx=10,
            pady=10,
            activebackground="#FF6B9D",
            activeforeground="#FF6B9D",
            borderwidth=0,
            highlightthickness=0
        )
        main_menu_btn.place(x=760, y=40, width=250, height=50) 

        # Exit button (Bottom right)
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=(self.baloo_font, 22),
            fg="#fffff0",
            bg='#552626',
            relief=tk.FLAT,
            command=self.root.quit,
            padx=10,
            pady=10,
            activebackground="#552626", 
            activeforeground="#552626",
            borderwidth=0,  
            highlightthickness=0 
        )
        exit_btn.place(x=1500, y=self.root.winfo_screenheight()//2+400, width=300, height=40)

    def clear_frame(self):
        """Clear the current frame"""
        for widget in self.root.winfo_children():
            if widget not in [self.user_display_frame]:
                widget.destroy()


class AllMedicinesView:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Display all medicines"""
        title_label = tk.Label(
            self.controller.user_display_frame,
            text="All Medicines",
            font=(self.controller.baloo_font, 16, "bold"),
            bg=self.controller.pink_display,
            fg=self.controller.dark_text
        )
        title_label.pack(pady=(20, 10))
        
        meds_frame = tk.Frame(self.controller.user_display_frame, bg=self.controller.pink_display)
        meds_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(meds_frame, bg=self.controller.pink_display, highlightthickness=0)
        scrollbar = ttk.Scrollbar(meds_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.controller.pink_display)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for idx, med in enumerate(self.controller.medicines):
            med_frame = tk.Frame(scrollable_frame, bg=self.controller.white, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['name']} - {med['desc']}\nDose: {med['dose']}",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.white,
                fg=self.controller.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            is_fav = any(m['name'] == med['name'] for m in self.controller.favorites)
            
            fav_btn = tk.Button(
                med_frame,
                text="♥ Add to Fav" if not is_fav else "♥ Remove Fav",
                font=(self.controller.roboto_flex_font, 10),
                bg=self.controller.white,
                fg="#ff6b9d" if is_fav else "#cccccc",
                relief=tk.FLAT,
                command=lambda m=med, is_f=is_fav: self.controller.toggle_favorite(m, is_f)
            )
            fav_btn.pack(side=tk.RIGHT, padx=10)
            
        if not self.controller.medicines:
            empty_label = tk.Label(
                scrollable_frame,
                text="No medicines available.",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.pink_display,
                fg=self.controller.gray_text
            )
            empty_label.pack(pady=50)


class SearchView:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Setup the search interface"""
        self.clear_frame()

        bg_path = os.path.join(self.controller.assets_path, "images/user's.png")
        self.bg_photo = tk.PhotoImage(file=bg_path)
        bg_label = tk.Label(self.controller.user_display_frame, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        search_frame = tk.Frame(self.controller.user_display_frame, bg=self.bg_photo)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        self.search_entry = tk.Entry(
            search_frame,
            font=(self.controller.baloo_font, 14),
            relief=tk.FLAT,
            bg=self.controller.white,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor=self.controller.button_color,
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=(self.controller.baloo_font, 12, "bold"),
            bg=self.controller.button_color,
            fg=self.controller.white,
            relief=tk.FLAT,
            command=self.perform_search,
            padx=20,
            pady=5
        )
        search_btn.pack(side=tk.RIGHT)

        self.search_results_frame = tk.Frame(self.controller.user_display_frame, bg=self.bg_photo)
        self.search_results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        initial_msg = tk.Label(
            self.search_results_frame,
            text="Enter a search term to find medicines",
            font=(self.controller.roboto_flex_font, 12),
            bg=self.controller.pink_display,
            fg=self.controller.gray_text
        )
        initial_msg.pack(pady=50)

    def perform_search(self):
        """Perform the search operation"""
        search_term = self.search_entry.get().lower()

        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
            
        if not search_term:
            error_label = tk.Label(
                self.search_results_frame,
                text="Please enter a search term",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.pink_display,
                fg="#ff0000"
            )
            error_label.pack(pady=50)
            return
        
        self.controller.history.append(search_term)
            
        dataset_path = os.path.join(self.controller.data_path, "Medicine_1000_cleaned.csv")
        medicines = pd.read_csv(dataset_path)
        
        results = medicines[medicines.apply(lambda row: search_term in row.to_string().lower(), axis=1)]

        if results.empty:
            no_results = tk.Label(
                self.search_results_frame,
                text=f"No results found for '{search_term}'",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.pink_display,
                fg=self.controller.gray_text
            )
            no_results.pack(pady=50)
            return
            
        canvas = tk.Canvas(self.search_results_frame, bg=self.bg_photo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.search_results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_photo)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for _, med in results.iterrows():
            med_frame = tk.Frame(scrollable_frame, bg=self.controller.white, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['Medicine Name']} - {med['Uses']}\n"
                     f"Composition: {med['Composition']}\n"
                     f"Side Effects: {med['Side_effects']}\n"
                     f"Manufacturer: {med['Manufacturer']}\n"
                     f"Reviews: Excellent {med['Excellent Review %']}%, "
                     f"Average {med['Average Review %']}%, Poor {med['Poor Review %']}%",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.white,
                fg=self.controller.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            is_fav = any(m['name'] == med['name'] for m in self.controller.favorites)
            
            fav_btn = tk.Button(
                med_frame,
                text="♥ Add to Fav" if not is_fav else "♥ Remove Fav",
                font=(self.controller.roboto_flex_font, 10),
                bg=self.controller.white,
                fg="#ff6b9d" if is_fav else "#cccccc",
                relief=tk.FLAT,
                command=lambda m=med, is_f=is_fav: self.controller.toggle_favorite(m, is_f)
            )
            fav_btn.pack(side=tk.RIGHT, padx=10)

    def clear_frame(self):
        """Clear the search frame"""
        for widget in self.controller.user_display_frame.winfo_children():
            widget.destroy()


class FavoritesView:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Setup the favorites interface"""
        for widget in self.controller.user_display_frame.winfo_children():
            widget.destroy()
            
        bg_path = os.path.join(self.controller.assets_path, "images/user's.png")
        bg_image = Image.open(bg_path).convert("RGBA")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        
        favs_frame = tk.Frame(self.controller.user_display_frame)
        favs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        if not self.controller.favorites:
            empty_label = tk.Label(
                favs_frame,
                text="You haven't added any favorites yet.",
                font=(self.controller.roboto_flex_font, 12),
                bg=self.bg_photo,
                fg="#fffff0"
            )
            empty_label.pack(pady=50)
            return
            
        canvas = tk.Canvas(favs_frame, bg=self.bg_photo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(favs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for med in self.controller.favorites:
            med_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, bd=1)
            med_frame.pack(fill=tk.X, pady=5, padx=5)
            
            med_info = tk.Label(
                med_frame,
                text=f"{med['name']} - {med['desc']}\nDose: {med['dose']}",
                font=(self.controller.roboto_flex_font, 12),
                fg=self.controller.dark_text,
                anchor="w",
                justify=tk.LEFT
            )
            med_info.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            remove_btn = tk.Button(
                med_frame,
                text="✕ Remove",
                font=(self.controller.roboto_flex_font, 10),
                bg=self.controller.white,
                fg="#ff0000",
                relief=tk.FLAT,
                command=lambda m=med: self.controller.toggle_favorite(m, True)
            )
            remove_btn.pack(side=tk.RIGHT, padx=10)


class HistoryView:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Setup the history interface"""
        self.clear_frame()

        bg_path = os.path.join(self.controller.assets_path, "images/user's.png")
        self.bg_photo = tk.PhotoImage(file=bg_path)  
        bg_label = tk.Label(self.controller.user_display_frame, image=self.bg_photo)  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        history_frame = tk.Frame(self.bg_photo)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        if not self.controller.history:
            empty_label = tk.Label(
                history_frame,
                text="Your search history is empty.",
                font=(self.controller.roboto_flex_font, 12),
                fg="#fffff0"
            )
            empty_label.pack(pady=50)
            return
            
        canvas = tk.Canvas(history_frame, bg=self.bg_photo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_photo)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for search_term in reversed(self.controller.history):
            hist_frame = tk.Frame(scrollable_frame, bg=self.controller.white, relief=tk.RAISED, bd=1)
            hist_frame.pack(fill=tk.X, pady=5, padx=5)
            
            hist_label = tk.Label(
                hist_frame,
                text=search_term,
                font=(self.controller.roboto_flex_font, 12),
                bg=self.controller.white,
                fg=self.controller.dark_text,
                anchor="w"
            )
            hist_label.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            repeat_btn = tk.Button(
                hist_frame,
                text="Search Again",
                font=(self.controller.roboto_flex_font, 10),
                bg=self.controller.white,
                fg=self.controller.button_color,
                relief=tk.FLAT,
                command=lambda st=search_term: self.repeat_search(st)
            )
            repeat_btn.pack(side=tk.RIGHT, padx=10)

    def repeat_search(self, search_term):
        """Repeat a search from history"""
        self.controller.show_search()
        self.controller.search_view.search_entry.insert(0, search_term)
        self.controller.search_view.perform_search()

    def clear_frame(self):
        """Clear the history frame"""
        for widget in self.controller.user_display_frame.winfo_children():
            widget.destroy()


class FeedbackView:
    def _init_(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Setup the feedback interface"""
        self.clear_frame()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Feedback section frame
        feedback_frame = tk.Frame(self.root, bg="#FF6B9D")
        feedback_frame.place(x=screen_width * 0.15, y=screen_height//2-350, 
                           width=screen_width * 0.7, height=screen_height * 0.3)

        # Left-aligned title
        title_label = tk.Label(
            feedback_frame,
            text="Send Feedback",
            font=(self.controller.baloo_font, 16, "bold"),
            bg="#FF6B9D",
            fg="#fffff0",
            anchor="w"
        )
        title_label.pack(fill=tk.X, padx=10, pady=(20, 5))

        # Form frame
        form_frame = tk.Frame(feedback_frame, bg="#FF6B9D")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        feedback_label = tk.Label(
            form_frame,
            text="Your Feedback",
            font=("Arial", 11),
            bg="#FF6B9D",
            fg="#fffff0",
            anchor="w"
        )
        feedback_label.pack(fill=tk.X, pady=(5, 0))

        # Feedback input
        self.feedback_text = tk.Text(
            form_frame, 
            font=("Arial", 12), 
            height=5, 
            width=50, 
            wrap=tk.WORD, 
            bg="#FF6B9D"
        )
        self.feedback_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # History display (read-only Text widget)
        history_frame = tk.Frame(feedback_frame, bg="#FF6B9D")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.history_display = tk.Text(
            history_frame, 
            font=("Arial", 12), 
            height=8, 
            state=tk.DISABLED, 
            bg="#fff0f5"
        )
        self.history_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Submit button (left-aligned)
        submit_btn = tk.Button(
            form_frame,
            text="Submit Feedback",
            font=(self.controller.baloo_font, 16, "bold"),
            bg="#FF6B9D",
            fg="#fffff0",
            relief=tk.FLAT,
            command=self.submit_feedback
        )
        submit_btn.pack(anchor="w", padx=10)

    def submit_feedback(self):
        """Handle feedback submission"""
        feedback = self.feedback_text.get("1.0", tk.END).strip()
        if feedback:
            self.history_display.config(state=tk.NORMAL)
            self.history_display.insert(tk.END, f"- {feedback}\n")
            self.history_display.config(state=tk.DISABLED)
            self.feedback_text.delete("1.0", tk.END)

    def clear_frame(self):
        """Clear the feedback frame"""
        for widget in self.root.winfo_children():
            widget.destroy()


class MainController:
    def _init_(self, root):
        self.root = root
        self.assets_path = "C:/Users/LOQ/Python latihan/college studies/2nd semester/Pharmora-main/assets"
        self.data_path = "C:/Users/LOQ/Python latihan/college studies/2nd semester/Pharmora-main/data"
        
        # Initialize properties
        self.bg_color = "#fff0f5"
        self.button_color = "#FF6B9D"
        self.white = "#ffffff"
        self.dark_text = "#333333"
        self.gray_text = "#777777"
        self.pink_display = "#fff0f5"
        
        # Font paths
        self.baloo_font = os.path.join(self.assets_path, "fonts/BalooBhai2-VariableFont_wght.ttf")
        self.roboto_flex_font = "Arial"  # Fallback font
        
        # Data storage
        self.medicines = []
        self.favorites = []
        self.history = []
        
        # Initialize views
        self.user_dashboard = None
        self.all_medicines_view = None
        self.search_view = None
        self.favorites_view = None
        self.history_view = None
        self.feedback_view = None
        
        # Load data
        self.load_medicines()
        
    def load_medicines(self):
        """Load medicines from CSV"""
        dataset_path = os.path.join(self.data_path, "Medicine_1000_cleaned.csv")
        try:
            df = pd.read_csv(dataset_path)
            self.medicines = df.to_dict('records')
        except Exception as e:
            print(f"Error loading medicines: {e}")
            self.medicines = []

    def show_user_dashboard(self):
        """Show the user dashboard"""
        self.user_dashboard = UserDashboard(self.root, self)
        
    def show_all_medicines(self):
        """Show all medicines view"""
        self.user_dashboard = UserDashboard(self.root, self)
        self.all_medicines_view = AllMedicinesView(self.root, self)
        
    def show_search(self):
        """Show search view"""
        self.user_dashboard = UserDashboard(self.root, self)
        self.search_view = SearchView(self.root, self)
        
    def show_favorites(self):
        """Show favorites view"""
        self.user_dashboard = UserDashboard(self.root, self)
        self.favorites_view = FavoritesView(self.root, self)
        
    def show_history(self):
        """Show history view"""
        self.user_dashboard = UserDashboard(self.root, self)
        self.history_view = HistoryView(self.root, self)
        
    def show_feedback(self):
        """Show feedback view"""
        self.user_dashboard = UserDashboard(self.root, self)
        self.feedback_view = FeedbackView(self.root, self)
        
    def show_chatbot(self):
        """Show chatbot view (to be implemented)"""
        pass
        
    def show_welcome_screen(self):
        """Show welcome screen (to be implemented)"""
        pass
        
    def show_admin_dashboard(self):
        """Show admin dashboard (to be implemented)"""
        pass
        
    def toggle_favorite(self, medicine, is_favorite):
        """Toggle a medicine's favorite status"""
        if is_favorite:
            self.favorites = [m for m in self.favorites if m['name'] != medicine['name']]
        else:
            self.favorites.append(medicine)
        
        # Refresh the current view if needed
        if self.favorites_view:
            self.show_favorites()
        elif self.all_medicines_view:
            self.show_all_medicines()
        elif self.search_view:
            self.search_view.perform_search()


if __name__ == "_main_":
    root = tk.Tk()
    root.title("Pharmora - User Dashboard")
    root.state('zoomed')  # Maximize window
    
    controller = MainController(root)
    controller.show_user_dashboard()
    
    root.mainloop()