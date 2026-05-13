import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.ui.theme import COLORS, FONTS
from src.database import authenticate_user, register_user

class AuthUI:
    def __init__(self, master):
        self.master = master
        self.colors = COLORS
        self.fonts = FONTS

    def show_splash(self, on_complete):
        self.master.clear_window()
        self.master.configure(fg_color=self.colors["background"])
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        splash_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        splash_frame.grid(row=0, column=0)
        
        ctk.CTkLabel(splash_frame, text="📊", font=("Segoe UI", 80)).pack(pady=20)
        ctk.CTkLabel(splash_frame, text="ESTATEWISE", font=self.fonts["h1"], text_color=self.colors["text_bright"]).pack()
        
        status_label = ctk.CTkLabel(splash_frame, text="Initializing Neural Systems...", font=self.fonts["small"], text_color=self.colors["primary"])
        status_label.pack(pady=(10, 20))
        
        progress = ctk.CTkProgressBar(splash_frame, width=300, height=4, fg_color=self.colors["secondary"], progress_color=self.colors["primary"])
        progress.set(0)
        progress.pack()
        
        self._animate_splash(0, progress, status_label, on_complete)

    def _animate_splash(self, step, progress, status_label, on_complete):
        if step <= 100:
            progress.set(step / 100)
            if step == 20: status_label.configure(text="Loading Predictive Models...")
            if step == 50: status_label.configure(text="Connecting Secure Database...")
            if step == 80: status_label.configure(text="Finalizing Security Protocols...")
            self.master.after(30, lambda: self._animate_splash(step + 2, progress, status_label, on_complete))
        else:
            self.master.after(500, on_complete)

    def show_login(self, on_login_success, on_register_click):
        self.master.clear_window()
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        login_card = ctk.CTkFrame(self.master, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        login_card.grid(row=0, column=0, padx=20, pady=20)
        
        logo_frame = ctk.CTkFrame(login_card, fg_color=self.colors["primary"], width=60, height=60, corner_radius=10)
        logo_frame.grid(row=0, column=0, pady=(40, 20))
        ctk.CTkLabel(logo_frame, text="E", font=("Segoe UI", 30, "bold"), text_color=self.colors["background"]).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(login_card, text="ESTATEWISE", font=self.fonts["h2"], text_color=self.colors["text_bright"]).grid(row=1, column=0, pady=(0, 5))
        ctk.CTkLabel(login_card, text="Authentication Required", font=self.fonts["small"], text_color=self.colors["primary"]).grid(row=2, column=0, pady=(0, 30))

        user_entry = ctk.CTkEntry(login_card, placeholder_text="Username", width=320, height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"])
        user_entry.grid(row=3, column=0, padx=40, pady=10)

        pass_entry = ctk.CTkEntry(login_card, placeholder_text="Password", show="*", width=320, height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"])
        pass_entry.grid(row=4, column=0, padx=40, pady=10)
        
        show_btn = ctk.CTkButton(pass_entry, text="SHOW", width=45, height=28, font=("Segoe UI", 9, "bold"), fg_color="transparent", hover_color=self.colors["secondary"], text_color="#888888", corner_radius=4)
        show_btn.configure(command=lambda: self.toggle_password(pass_entry, show_btn))
        show_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)

        ctk.CTkButton(login_card, text="LOGIN", width=320, height=50, font=self.fonts["h3"], fg_color=self.colors["primary"], hover_color="#059669", text_color=self.colors["background"],
                      command=lambda: self._handle_login(user_entry.get(), pass_entry.get(), on_login_success)).grid(row=5, column=0, pady=(30, 10))
        
        ctk.CTkButton(login_card, text="Create Account", fg_color="transparent", text_color=self.colors["primary"], font=self.fonts["small"],
                      command=on_register_click).grid(row=6, column=0, pady=(0, 40))

    def show_register(self, on_back_click):
        self.master.clear_window()
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        reg_card = ctk.CTkFrame(self.master, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        reg_card.grid(row=0, column=0, padx=20, pady=20)

        # Profile Icon
        profile_logo_frame = ctk.CTkFrame(reg_card, fg_color=self.colors["primary"], width=60, height=60, corner_radius=30) # Circle
        profile_logo_frame.grid(row=0, column=0, pady=(40, 10))
        ctk.CTkLabel(profile_logo_frame, text="👤", font=("Segoe UI", 30), text_color=self.colors["background"]).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(reg_card, text="Create Account", font=self.fonts["h2"], text_color=self.colors["text_bright"]).grid(row=1, column=0, padx=40, pady=(0, 30))
        
        u_entry = ctk.CTkEntry(reg_card, placeholder_text="Username", width=320, height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"])
        u_entry.grid(row=2, column=0, padx=40, pady=10)
        
        p_entry = ctk.CTkEntry(reg_card, placeholder_text="Password", show="*", width=320, height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"])
        p_entry.grid(row=3, column=0, padx=40, pady=10)
        p_btn = ctk.CTkButton(p_entry, text="SHOW", width=45, height=28, font=("Segoe UI", 9, "bold"), fg_color="transparent", hover_color=self.colors["secondary"], text_color="#888888", corner_radius=4, command=lambda: self.toggle_password(p_entry, p_btn))
        p_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)
        
        c_entry = ctk.CTkEntry(reg_card, placeholder_text="Confirm Password", show="*", width=320, height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"])
        c_entry.grid(row=4, column=0, padx=40, pady=10)
        c_btn = ctk.CTkButton(c_entry, text="SHOW", width=45, height=28, font=("Segoe UI", 9, "bold"), fg_color="transparent", hover_color=self.colors["secondary"], text_color="#888888", corner_radius=4, command=lambda: self.toggle_password(c_entry, c_btn))
        c_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)
 
        ctk.CTkButton(reg_card, text="REGISTER", width=320, height=50, font=self.fonts["h3"], fg_color=self.colors["primary"], hover_color="#059669", text_color=self.colors["background"],
                      command=lambda: self._handle_register(u_entry.get(), p_entry.get(), c_entry.get(), on_back_click)).grid(row=5, column=0, pady=(30, 10))
        ctk.CTkButton(reg_card, text="Back to Login", fg_color="transparent", text_color=self.colors["primary"], font=self.fonts["small"],
                      command=on_back_click).grid(row=6, column=0, pady=(0, 40))

    def toggle_password(self, entry, button):
        if entry.cget("show") == "*":
            entry.configure(show="")
            button.configure(text="HIDE")
        else:
            entry.configure(show="*")
            button.configure(text="SHOW")

    def _handle_login(self, u, p, callback):
        if not u or not p: return messagebox.showwarning("System", "Credentials incomplete.")
        user = authenticate_user(u, p)
        if user: callback(user)
        else: messagebox.showerror("Denied", "Access credentials invalid.")

    def _handle_register(self, u, p, c, callback):
        if not u or not p or p != c: return messagebox.showerror("Error", "Validation failed.")
        if register_user(u, p): 
            messagebox.showinfo("Success", "Account initialized.")
            callback()
        else: 
            messagebox.showerror("Error", "Initialization failed.")
