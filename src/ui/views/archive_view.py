import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import get_user_predictions, delete_prediction, delete_prediction_by_id
from src.ui.components.data_table import DataTable
from src.utils.exporter import export_data

class ArchiveView(ctk.CTkFrame):
    def __init__(self, master, user_id, colors):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.colors = colors
        
        self._setup_ui()

    def _setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        ctk.CTkLabel(header, text="Personal Archive", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(side="left")
        
        btn_f = ctk.CTkFrame(header, fg_color="transparent")
        btn_f.pack(side="right")
        
        ctk.CTkButton(btn_f, text="EXPORT CSV", width=120, height=40, corner_radius=10, fg_color=self.colors["secondary"], command=self._export_csv).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="DELETE SELECTED", width=140, height=40, corner_radius=10, fg_color=self.colors["secondary"], command=self._delete_selected).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="PURGE ALL", width=120, height=40, corner_radius=10, fg_color="#ef4444", command=self._purge_history).pack(side="left")
        
        self.table = DataTable(self, ["ID", "Subdivision", "Floor", "Land", "Beds", "Baths", "Year", "Estimate"], self.colors)
        self.table.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.table.clear()
        for r in get_user_predictions(self.user_id):
            self.table.insert((
                r["id"], 
                r["subdivision"], 
                f"{r['floor_area']} sq", 
                f"{r['land_size']} sq",
                r["bedrooms"], 
                r["bathrooms"], 
                r["build_year"], 
                f"₱{r['predicted_price']:,.0f}"
            ))

    def _export_csv(self):
        export_data(get_user_predictions(self.user_id), "csv")

    def _delete_selected(self):
        sel = self.table.get_selection()
        if not sel:
            return messagebox.showwarning("System", "Please select a record to delete.")


        
        if messagebox.askyesno("Delete", f"Confirm deletion of record ID: {sel[0]}?"):
            if delete_prediction_by_id(sel[0]):
                self.table.delete_selected_row() # Instant UI removal
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.refresh() # Solidify and sync with DB
            else:
                messagebox.showerror("Error", "Failed to delete record.")


    def _purge_history(self):
        if messagebox.askyesno("Purge", "Delete all personal history? This action cannot be undone."):
            if delete_prediction(self.user_id):
                messagebox.showinfo("Success", "History purged successfully.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to purge history.")

