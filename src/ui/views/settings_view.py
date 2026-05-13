import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import update_user

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, current_user, colors):
        super().__init__(master, fg_color="transparent")
        self.user = current_user
        self.colors = colors
        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self, text="System Config", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(anchor="w", pady=(0, 30))
        
        # Account Section
        acc_card = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        acc_card.pack(fill="x", pady=10)
        ctk.CTkLabel(acc_card, text="ACCOUNT SETTINGS", font=("Segoe UI", 13, "bold"), text_color=self.colors["primary"]).pack(anchor="w", padx=25, pady=(20, 15))
        
        self.new_u = self._create_row(acc_card, "Username", self.user["username"])
        self.new_p = self._create_row(acc_card, "New Password", "", is_pass=True)
        
        ctk.CTkButton(acc_card, text="APPLY ACCOUNT CHANGES", font=("Segoe UI", 15, "bold"), height=65, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], text_color=self.colors["background"],
                      command=self._handle_update).pack(fill="x", padx=25, pady=30)

        # System Info
        self._create_info_card("ENGINE CORE", [("Model", "Neural-X1"), ("Status", "ONLINE"), ("Region", "GLOBAL")])
        
        # Maintenance Section
        m_card = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        m_card.pack(fill="x", pady=10)
        ctk.CTkLabel(m_card, text="SYSTEM MAINTENANCE", font=("Segoe UI", 13, "bold"), text_color=self.colors["primary"]).pack(anchor="w", padx=25, pady=(20, 15))
        
        ctk.CTkLabel(m_card, text="Export a secure SQL dump of all intelligence nodes and user records.", font=("Segoe UI", 12), text_color=self.colors["text"]).pack(anchor="w", padx=25)
        
        ctk.CTkButton(m_card, text="INITIALIZE DATABASE BACKUP", font=("Segoe UI", 15, "bold"), height=65, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], text_color=self.colors["background"],
                      command=self._handle_backup).pack(fill="x", padx=25, pady=25)

    def _create_row(self, parent, label, val, is_pass=False):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=25, pady=5)
        ctk.CTkLabel(row, text=label, font=("Segoe UI", 11), text_color=self.colors["text"]).pack(side="left")
        entry = ctk.CTkEntry(row, width=200, height=35, show="*" if is_pass else "", fg_color=self.colors["background"], border_color=self.colors["secondary"])
        entry.insert(0, val)
        entry.pack(side="right")
        return entry

    def _create_info_card(self, title, fields):
        card = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 13, "bold"), text_color=self.colors["primary"]).pack(anchor="w", padx=25, pady=(20, 15))
        for l, v in fields:
            r = ctk.CTkFrame(card, fg_color="transparent")
            r.pack(fill="x", padx=25, pady=5)
            ctk.CTkLabel(r, text=l, font=("Segoe UI", 11), text_color=self.colors["text"]).pack(side="left")
            ctk.CTkLabel(r, text=v, font=("Segoe UI", 11, "bold"), text_color=self.colors["text_bright"]).pack(side="right")
        ctk.CTkLabel(card, text="", height=10).pack()

    def _handle_update(self):
        u, p = self.new_u.get(), self.new_p.get()
        if not u or not p: return messagebox.showwarning("System", "Fields required.")
        res = update_user(self.user["id"], u, p)
        if res == True:
            messagebox.showinfo("Success", "Updated.")
            self.user["username"] = u
        elif res == "EXISTS":
            messagebox.showerror("Error", "Username taken.")
        else:
            messagebox.showerror("Error", "Failure.")

    def _handle_backup(self):
        from tkinter import filedialog
        from src.database import backup_database
        from datetime import datetime
        
        default_name = f"estatewise_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        file_path = filedialog.asksaveasfilename(defaultextension=".sql", initialfile=default_name, title="Select Backup Destination",
                                                filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
        
        if not file_path: return
        
        if backup_database(file_path):
            messagebox.showinfo("Success", f"Neural node backup completed successfully.\nDestination: {file_path}")
        else:
            messagebox.showerror("Error", "Database backup sequence failed. Check system logs.")
