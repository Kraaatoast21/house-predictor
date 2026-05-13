import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import get_all_users, delete_user, update_user_role, register_user

class AdminUsersView(ctk.CTkFrame):
    def __init__(self, master, current_user_id, colors):
        super().__init__(master, fg_color="transparent")
        self.current_user_id = current_user_id
        self.colors = colors
        self._setup_ui()

    def _setup_ui(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="User Directory", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(side="left")
        
        btn_f = ctk.CTkFrame(header, fg_color="transparent")
        btn_f.pack(side="right")
        
        ctk.CTkButton(btn_f, text="CHANGE ROLES", height=45, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], text_color=self.colors["background"], font=("Segoe UI", 12, "bold"), command=self._handle_toggle_role).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="DELETE SELECTED", height=45, fg_color="#ef4444", font=("Segoe UI", 12, "bold"), command=self._handle_delete).pack(side="left")
        
        # Add User Form - Glass Card Style
        add_f = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        add_f.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(add_f, text="USER REGISTRATION", font=("Segoe UI", 10, "bold"), text_color=self.colors["primary"]).pack(anchor="w", padx=30, pady=(20, 10))
        
        form_inner = ctk.CTkFrame(add_f, fg_color="transparent")
        form_inner.pack(fill="x", padx=30, pady=(0, 25))
        
        # Consistent height across all elements
        h = 45
        self.u_entry = ctk.CTkEntry(form_inner, placeholder_text="Username", width=220, height=h, fg_color=self.colors["background"], border_color=self.colors["secondary"], corner_radius=10)
        self.u_entry.pack(side="left", padx=(0, 15))
        
        self.p_entry = ctk.CTkEntry(form_inner, placeholder_text="Password", width=220, height=h, show="*", fg_color=self.colors["background"], border_color=self.colors["secondary"], corner_radius=10)
        self.p_entry.pack(side="left", padx=(0, 15))
        
        self.p_btn = ctk.CTkButton(self.p_entry, text="SHOW", width=45, height=28, font=("Segoe UI", 9, "bold"), fg_color="transparent", hover_color=self.colors["secondary"], text_color="#888888", corner_radius=4, command=self._toggle_pass)
        self.p_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)
        
        self.role_var = ctk.StringVar(value="user")
        ctk.CTkOptionMenu(form_inner, values=["user", "admin"], variable=self.role_var, width=120, height=h, fg_color=self.colors["background"], button_color=self.colors["secondary"], corner_radius=10).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(form_inner, text="ADD USER", width=120, height=h, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], text_color=self.colors["background"], font=("Segoe UI", 12, "bold"), corner_radius=10, command=self._handle_add).pack(side="left", padx=(0, 10))
        ctk.CTkButton(form_inner, text="UPDATE SELECTED", width=160, height=h, fg_color=self.colors["secondary"], hover_color=self.colors["primary"], text_color=self.colors["text_bright"], font=("Segoe UI", 12, "bold"), corner_radius=10, command=self._handle_update).pack(side="left")

        # Table Section
        from src.ui.components.data_table import DataTable
        self.table = DataTable(self, ["ID", "Username", "Password", "Role"], self.colors)
        self.table.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.table.clear()
        from src.database import get_all_users
        for u in get_all_users():
            self.table.insert((u["id"], u["username"], u["password"], u["role"].upper()))

    def _toggle_pass(self):
        if self.p_entry.cget("show") == "*":
            self.p_entry.configure(show="")
            self.p_btn.configure(text="HIDE")
        else:
            self.p_entry.configure(show="*")
            self.p_btn.configure(text="SHOW")

    def _handle_add(self):
        u, p, r = self.u_entry.get(), self.p_entry.get(), self.role_var.get()
        if not u or not p: return messagebox.showwarning("System", "Credentials incomplete.")
        res = register_user(u, p, r)
        if res == True:
            messagebox.showinfo("Success", f"Account [{u}] initialized as {r.upper()}.")
            self.u_entry.delete(0, 'end')
            self.p_entry.delete(0, 'end')
            self.refresh()
        elif res == "EXISTS":
            messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Failed to create user.")

    def _handle_toggle_role(self):
        vals = self.table.get_selection()
        if not vals: return messagebox.showwarning("System", "Select a user to update.")
        uid, uname, role = vals[0], vals[1], vals[3]
        
        new_role = "user" if role.upper() == "ADMIN" else "admin"
        
        if uid == 1: return messagebox.showerror("Denied", "Primary Admin role cannot be modified.")
        if uid == self.current_user_id: return messagebox.showerror("Denied", "Cannot demote your own active account.")

        if messagebox.askyesno("Clearance Update", f"Change [{uname}] role to {new_role.upper()}?"):
            from src.database import update_user_role
            if update_user_role(uid, new_role):
                messagebox.showinfo("Success", f"[{uname}] updated to {new_role.upper()} status.")
                self.refresh()

    def _handle_update(self):
        vals = self.table.get_selection()
        if not vals: return messagebox.showwarning("System", "Select a user to update.")
        uid = vals[0]
        u, p = self.u_entry.get(), self.p_entry.get()
        if not u or not p: return messagebox.showwarning("System", "Input new credentials in the form above.")
        
        if messagebox.askyesno("Confirm Update", f"Override credentials for account ID [{uid}]?"):
            from src.database import update_user_credentials
            if update_user_credentials(uid, u, p):
                messagebox.showinfo("Success", "User credentials updated and re-encrypted.")
                self.u_entry.delete(0, 'end')
                self.p_entry.delete(0, 'end')
                self.refresh()

    def _handle_delete(self):
        vals = self.table.get_selection()
        if not vals: return messagebox.showwarning("System", "Select a user.")
        uid = vals[0]
        if uid == self.current_user_id: return messagebox.showerror("Denied", "Cannot terminate own session.")
        if uid == 1: return messagebox.showerror("Denied", "Primary Admin node is protected.")
        
        if messagebox.askyesno("Confirm Termination", "Delete user and all associated neural data?"):
            if delete_user(uid): self.refresh()
