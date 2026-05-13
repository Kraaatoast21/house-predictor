import customtkinter as ctk
from src.database import get_all_predictions
from src.ui.components.data_table import DataTable
from src.utils.exporter import export_data

class AdminLogsView(ctk.CTkFrame):
    def __init__(self, master, colors):
        super().__init__(master, fg_color="transparent")
        self.colors = colors
        self._setup_ui()

    def _setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="Global Audit", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(side="left")
        
        tool_f = ctk.CTkFrame(header, fg_color="transparent")
        tool_f.pack(side="right")
        
        for fmt in ["CSV", "EXCEL"]:
            ctk.CTkButton(tool_f, text=f"EXPORT {fmt}", width=120, height=40, corner_radius=10, fg_color=self.colors["secondary"], 
                          command=lambda f=fmt: self._export(f)).pack(side="left", padx=5)
        
        self.table = DataTable(self, ["ID", "User", "Subdivision", "Floor", "Land", "Beds", "Baths", "Year", "Estimate"], self.colors)
        self.table.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.table.clear()
        for rec in get_all_predictions():
            self.table.insert((
                rec["id"], 
                rec["username"], 
                rec["subdivision"], 
                f"{rec['floor_area']} sq", 
                f"{rec['land_size']} sq",
                rec["bedrooms"], 
                rec["bathrooms"], 
                rec["build_year"], 
                f"₱{rec['predicted_price']:,.0f}"
            ))

    def _export(self, fmt):
        export_data(get_all_predictions(), fmt.lower())
