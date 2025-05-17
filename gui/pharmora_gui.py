import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import login_user, register_user, is_username_exist

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
        self.progress = ctk.CTkProgressBar(self, width=progress_width)
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

        self.get_started_button = ctk.CTkButton(
            self, 
            text="Get Started", 
            font=ctk.CTkFont(size=26, weight="bold"), 
            width=220, 
            height=60, 
            corner_radius=0,
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",  
            hover_color="#E05A8A",  
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
        
        self.admin_button = ctk.CTkButton(
            self.admin_frame, 
            text="Admin", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            width=195, 
            height=65, 
            corner_radius=0,
            fg_color="#FF6B9D", 
            text_color="#FFFFFF",  
            hover_color="#E05A8A",  
            border_width=0, 
            command=self.open_admin_login
        )
        self.admin_button.pack()

        self.user_frame = ctk.CTkFrame(self, fg_color="#FF6B9D")
        self.user_frame.place(relx=0.68, rely=0.8, anchor="center")
        
        self.user_button = ctk.CTkButton(
            self.user_frame, 
            text="User", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            width=195, 
            height=65, 
            corner_radius=0,
            fg_color="#FF6B9D",  
            text_color="#FFFFFF",  
            hover_color="#E05A8A",  
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
        user_id, role = login_user(username, password, "admin")
        if user_id:
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
        elif role == "wrong_role":
            CTkMessagebox(title="Login Failed", message="This account is not an admin!", icon="cancel")
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

class UserLoginScreen(ctk.CTk):
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
        user_id, role = login_user(username, password, "user")
        if user_id:
            CTkMessagebox(title="Login Successful", message=f"Welcome, {username}!", icon="check")
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

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
    
if __name__ == "__main__":
    app = LoadingScreen()
    app.mainloop()