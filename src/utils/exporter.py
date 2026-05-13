import csv
import pandas as pd
import os
from datetime import datetime
from tkinter import filedialog, messagebox

def export_data(data, format="csv"):
    if not data:
        messagebox.showwarning("Export Error", "No data available to export.")
        return False

    file_types = {
        "csv": [("CSV Files", "*.csv")],
        "excel": [("Excel Files", "*.xlsx")],
        "pdf": [("PDF Files", "*.pdf")]
    }

    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{format}",
        filetypes=file_types.get(format, [("All Files", "*.*")]),
        initialfile=f"EstateWise_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    if not file_path:
        return False

    try:
        df = pd.DataFrame(data)
        
        if format == "csv":
            df.to_csv(file_path, index=False)
        elif format == "excel":
            # Using pandas built-in excel writer (might require openpyxl)
            df.to_excel(file_path, index=False)
        elif format == "pdf":
            # Basic PDF generation using a text-based approach if fpdf is missing
            # For now, we'll implement a simple text export or use fpdf if possible
            with open(file_path, "w") as f:
                f.write("ESTATEWISE INTELLIGENCE REPORT\n")
                f.write("="*30 + "\n")
                f.write(df.to_string(index=False))
        
        messagebox.showinfo("Export Success", f"Report successfully saved to:\n{file_path}")
        return True
    except Exception as e:
        messagebox.showerror("Export Failed", f"An error occurred during export: {str(e)}")
        return False
