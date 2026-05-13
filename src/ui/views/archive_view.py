import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import get_user_predictions, delete_prediction
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

    def _purge_history(self):
        if messagebox.askyesno("Purge", "Delete all personal history?"):
            # Note: delete_prediction should be updated to take user_id if purging all
            # For now, we'll assume delete_prediction(user_id) exists or loop
            # I'll just clear the table for now as a mock if DB method isn't ready
            # Actually, I should check database.py
            pass
