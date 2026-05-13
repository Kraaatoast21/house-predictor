import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import initialize_database
from src.ui.theme import COLORS, FONTS
from src.ui.auth import AuthUI
from src.ui.dashboard import DashboardUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EstateWise | Intelligence")
        self.geometry("1200x750")
        self.minsize(1200, 750)
        self.colors = COLORS
        self.fonts = FONTS
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        if not initialize_database():
            messagebox.showerror("System Error", "Critical: Database initialization failed.")
            
        self.current_user = None
        self.auth_ui = AuthUI(self)
        self.show_splash()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        # Reset grid weights to prevent layout bleed-through
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

    def show_splash(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.auth_ui.show_splash(on_complete=self.show_login)

    def show_login(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.auth_ui.show_login(on_login_success=self.on_login_success, on_register_click=self.show_register)

    def show_register(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.auth_ui.show_register(on_back_click=self.show_login)

    def on_login_success(self, user):
        self.current_user = user
        self.show_dashboard()

    def show_dashboard(self):
        self.dashboard_ui = DashboardUI(self, self.current_user, on_logout=self.logout)
        self.dashboard_ui.show()

    def logout(self):
        if messagebox.askyesno("Terminate", "Are you sure you want to terminate the secure session?"):
            self.current_user = None
            self.show_login()

    def on_closing(self):
        """Ensures a clean exit to prevent background thread/Tkinter errors."""
        try:
            self.withdraw() # Hide immediately to prevent interaction
            self.quit()     # Stop the mainloop
            self.destroy()  # Clean up widgets
        except:
            import os
            os._exit(0)     # Failsafe for background threads

if __name__ == "__main__":
    app = App()
    app.mainloop()
