import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.ui.theme import COLORS, FONTS

# View Imports
from src.ui.views.predictor_view import PredictorView
from src.ui.views.archive_view import ArchiveView
from src.ui.views.admin_users_view import AdminUsersView
from src.ui.views.admin_logs_view import AdminLogsView
from src.ui.views.analytics_view import AnalyticsView
from src.ui.views.settings_view import SettingsView

class DashboardUI:
    def __init__(self, master, current_user, on_logout):
        self.master = master
        self.current_user = current_user
        self.on_logout = on_logout
        self.role = current_user.get("role", "user")
        self.colors = COLORS
        self.fonts = FONTS
        
        # State Management
        self.active_tab = None
        self.current_view = None
        
        # Shared Resources Cache
        self.cache = {"subdivisions": None}
        
        # self._setup_main_layout() # Removed from init, moved to show()

    def show(self):
        self.master.clear_window()
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        
        self._create_sidebar()
        self._navigate("predict")

    def _create_sidebar(self):
        # 1. Main Sidebar Container (Regular Frame for stable placement)
        self.sidebar = ctk.CTkFrame(self.master, width=280, corner_radius=0, fg_color=self.colors["surface"], border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(1, weight=1) # Middle area expands
        self.sidebar.grid_columnconfigure(0, weight=1)

        # 2. Top Logo Area
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.grid(row=0, column=0, padx=25, pady=(50, 20), sticky="ew")
        logo_f.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(logo_f, text="💎", font=("Segoe UI", 36)).grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="nsew")
        ctk.CTkLabel(logo_f, text="ESTATEWISE", font=("Segoe UI", 22, "bold"), text_color=self.colors["primary"]).grid(row=0, column=1, sticky="sw")
        ctk.CTkLabel(logo_f, text="NEURAL CORE v2.0", font=("Segoe UI", 9, "bold"), text_color=self.colors["text"]).grid(row=1, column=1, sticky="nw")

        # 3. Middle Scrollable Nav Area
        self.nav_container = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", 
                                                   scrollbar_button_color=self.colors["secondary"],
                                                   scrollbar_button_hover_color=self.colors["primary"])
        self.nav_container.grid(row=1, column=0, sticky="nsew", padx=5)
        self.nav_container.grid_columnconfigure(0, weight=1)

        # 4. Bottom Logout Area (Pinned)
        logout_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logout_f.grid(row=2, column=0, padx=25, pady=(20, 40), sticky="ew")
        ctk.CTkButton(logout_f, text="LOGOUT SESSION", font=("Segoe UI", 13, "bold"), 
                      fg_color="#ef4444", hover_color="#dc2626", height=55, corner_radius=12, 
                      command=self._confirm_logout).pack(fill="x")

        # Navigation Links
        self.nav_btns = {}
        ctk.CTkLabel(self.nav_container, text="SYSTEM CORE", font=("Segoe UI", 10, "bold"), text_color="#475569").grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        self.nav_btns["predict"] = self._create_nav_button("🔮  Price Predictor", lambda: self._navigate("predict"), 1)
        self.nav_btns["history"] = self._create_nav_button("📜  Personal Archive", lambda: self._navigate("history"), 2)

        if self.role == "admin":
            ctk.CTkLabel(self.nav_container, text="ADMIN CONTROL", font=("Segoe UI", 10, "bold"), text_color="#475569").grid(row=3, column=0, padx=20, pady=(30, 10), sticky="w")
            self.nav_btns["admin_users"] = self._create_nav_button("👥  User Directory", lambda: self._navigate("admin_users"), 4)
            self.nav_btns["admin_logs"] = self._create_nav_button("📊  Global Audit", lambda: self._navigate("admin_logs"), 5)
            self.nav_btns["analytics"] = self._create_nav_button("📈  System Analytics", lambda: self._navigate("analytics"), 6)
            self.nav_btns["settings"] = self._create_nav_button("⚙️  System Config", lambda: self._navigate("settings"), 7)

    def _create_nav_button(self, text, command, row):
        btn = ctk.CTkButton(self.nav_container, text=f"   {text}", anchor="w", height=65, font=("Segoe UI", 14), 
                            fg_color="transparent", hover_color=self.colors["secondary"], 
                            text_color=self.colors["text_bright"], corner_radius=15, command=command)
        btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
        return btn

    def _navigate(self, tab):
        if self.active_tab == tab: return
        self.active_tab = tab
        
        # Update Sidebar Styling
        for t, btn in self.nav_btns.items():
            is_active = (t == tab)
            btn.configure(fg_color=self.colors["primary"] if is_active else "transparent",
                          hover_color=self.colors["primary_hover"] if is_active else self.colors["secondary"],
                          text_color=self.colors["background"] if is_active else self.colors["text_bright"])
        
        # Create Main Content Area (Scrollable)
        if not hasattr(self, "content_area"):
            self.content_area = ctk.CTkScrollableFrame(self.master, fg_color="transparent", corner_radius=0)
            self.content_area.grid(row=0, column=1, sticky="nsew")
            self.content_area.grid_columnconfigure(0, weight=1)

        # Clear previous view safely
        if self.current_view:
            try:
                self.current_view.pack_forget()
                self.current_view.destroy()
            except:
                pass
        
        # Load new view into content_area
        if tab == "predict":
            self.current_view = PredictorView(self.content_area, self.current_user["id"], self.colors, self.cache["subdivisions"])
        elif tab == "history":
            self.current_view = ArchiveView(self.content_area, self.current_user["id"], self.colors)
        elif tab == "admin_users":
            self.current_view = AdminUsersView(self.content_area, self.current_user["id"], self.colors)
        elif tab == "admin_logs":
            self.current_view = AdminLogsView(self.content_area, self.colors)
        elif tab == "analytics":
            self.current_view = AnalyticsView(self.content_area, self.colors)
        elif tab == "settings":
            self.current_view = SettingsView(self.content_area, self.current_user, self.colors)
            
        # Use anchor 'n' and fill 'x' to ensure content stacks correctly and doesn't collapse
        self.current_view.pack(fill="both", expand=True, padx=25, pady=(40, 40), anchor="n")

    def _confirm_logout(self):
        if messagebox.askyesno("Terminate Session", "Confirm secure logout and session termination?"):
            self.on_logout()
