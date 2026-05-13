import customtkinter as ctk
from tkinter import ttk

class DataTable(ctk.CTkFrame):
    def __init__(self, master, columns, colors, **kwargs):
        super().__init__(master, fg_color=colors["surface"], corner_radius=20, border_width=1, border_color=colors["secondary"], **kwargs)
        self.colors = colors
        
        # 1. High-Fidelity Style Engine
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass # Theme might already be in use
        
        self.style.configure("Treeview", 
                    background=colors["surface"], 
                    foreground=colors["text"], 
                    fieldbackground=colors["surface"], 
                    borderwidth=0, 
                    rowheight=50, 
                    font=("Segoe UI", 11))
        
        self.style.configure("Treeview.Heading", 
                    background=colors["secondary"], 
                    foreground=colors["primary"], 
                    relief="flat", 
                    font=("Segoe UI", 10, "bold"),
                    padding=(10, 12))
        
        self.style.map("Treeview.Heading",
              background=[('active', colors["primary"])],
              foreground=[('active', colors["background"])])
        
        self.style.map("Treeview", 
              background=[('selected', colors["primary"])], 
              foreground=[('selected', colors["background"])])
        
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode="browse")
        
        # 2. Stable Grid Geometry
        for col in columns:
            self.tree.heading(col, text=f"  {col.upper()}")
            
            # Calibrated baseline widths
            if col == "ID": w = 65
            elif col in ["Subdivision", "Username"]: w = 220
            elif col in ["Estimate", "Password"]: w = 160
            elif col in ["User", "Role"]: w = 130
            elif col in ["Floor", "Land", "Created At"]: w = 130
            elif col in ["Beds", "Baths", "Year"]: w = 90
            else: w = 110
            
            # Stretch only the primary descriptive columns to fill the frame
            is_stretchy = col in ["Subdivision", "Username", "Estimate", "Password"]
            self.tree.column(col, width=w, minwidth=w, anchor="center", stretch=is_stretchy)
            self.tree.heading(col, text=col.upper(), anchor="center")
        
        # Horizontal + Vertical Scroll
        ys = ctk.CTkScrollbar(self, orientation="vertical", command=self.tree.yview, fg_color="transparent", button_color=colors["secondary"], button_hover_color=colors["primary"])
        xs = ctk.CTkScrollbar(self, orientation="horizontal", command=self.tree.xview, fg_color="transparent", button_color=colors["secondary"], button_hover_color=colors["primary"])
        self.tree.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        
        # 3. Robust Grid Geometry (Fixes Resize Errors)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=2, pady=(2, 0))
        ys.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=2)
        xs.grid(row=1, column=0, sticky="ew", padx=2, pady=(0, 2))

    def clear(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def insert(self, values):
        self.tree.insert("", "end", values=values)
        
    def get_selection(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])["values"]
