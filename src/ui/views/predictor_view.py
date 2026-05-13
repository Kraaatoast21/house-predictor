import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.database import save_prediction
from src.model import predict_price, get_subdivisions

class PredictorView(ctk.CTkFrame):
    def __init__(self, master, user_id, colors, subdivisions_cache):
        super().__init__(master, fg_color="transparent")
        self.user_id = user_id
        self.colors = colors
        self.subdivisions = subdivisions_cache if subdivisions_cache else get_subdivisions()
        
        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self, text="Predictive Analysis", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(anchor="w", pady=(0, 5))
        
        # Neural Status Card
        status_f = ctk.CTkFrame(self, fg_color=self.colors["surface"], height=50, corner_radius=12, border_width=1, border_color=self.colors["secondary"])
        status_f.pack(fill="x", pady=(0, 20))
        status_f.pack_propagate(False)
        ctk.CTkLabel(status_f, text="⚡ NEURAL ENGINE: ACTIVE", font=("Segoe UI", 10, "bold"), text_color=self.colors["primary"]).pack(side="left", padx=20)
        ctk.CTkLabel(status_f, text="ACCURACY: 89.4%  |  RMSE: ₱12.4K  |  NODE: CLUSTER-01", font=("Segoe UI", 10), text_color=self.colors["text"]).pack(side="right", padx=20)

        ctk.CTkLabel(self, text="Enter property attributes to generate a neural market estimate.", font=("Segoe UI", 14), text_color=self.colors["text"]).pack(anchor="w", pady=(0, 20))

        input_card = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=24, border_width=1, border_color=self.colors["secondary"])
        input_card.pack(fill="x", pady=10)
        
        fields = [
            ("Property Subdivision", "option", self.subdivisions),
            ("Bedrooms Total", "entry", None),
            ("Bathrooms Total", "entry", None),
            ("Floor Area (sqft)", "entry", None),
            ("Land Size (sqft)", "entry", None),
            ("Year Constructed", "entry", None)
        ]
        
        self.inputs = {}
        grid_container = ctk.CTkFrame(input_card, fg_color="transparent")
        grid_container.pack(fill="x", padx=40, pady=40)
        
        for i, (label, type, opts) in enumerate(fields):
            r, c = i // 2, i % 2
            f = ctk.CTkFrame(grid_container, fg_color="transparent")
            f.grid(row=r, column=c, padx=20, pady=15, sticky="ew")
            grid_container.grid_columnconfigure(c, weight=1)
            
            ctk.CTkLabel(f, text=label.upper(), font=("Segoe UI", 10, "bold"), text_color=self.colors["primary"]).pack(anchor="w", pady=(0, 5))
            if type == "option":
                var = ctk.CTkOptionMenu(f, values=opts, height=50, fg_color=self.colors["background"], button_color=self.colors["secondary"], corner_radius=12)
                var.pack(fill="x")
                self.inputs[label] = var
            else:
                entry = ctk.CTkEntry(f, placeholder_text=f"e.g. {label.split(' ')[0]}", height=50, fg_color=self.colors["background"], border_color=self.colors["secondary"], corner_radius=12)
                entry.pack(fill="x")
                self.inputs[label] = entry

        self.proc_btn = ctk.CTkButton(self, text="GENERATE INTELLIGENCE REPORT", font=("Segoe UI", 16, "bold"), height=70, corner_radius=20, 
                                    fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"], text_color=self.colors["background"], 
                                    command=self._handle_prediction)
        self.proc_btn.pack(fill="x", pady=40, padx=40)
        
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.pack(fill="x")
        
        self.result_label = ctk.CTkLabel(self.result_container, text="", font=("Segoe UI", 48, "bold"), text_color=self.colors["primary"])
        self.result_label.pack(pady=(0, 10))

    def _handle_prediction(self):
        if hasattr(self, "_processing") and self._processing: return
        self._processing = True
        self.proc_btn.configure(state="disabled", text="NEURAL PROCESSING...")
        
        try:
            d = {k: v.get() for k, v in self.inputs.items()}
            year = int(d["Year Constructed"])
            land = float(d["Land Size (sqft)"])
            floor = float(d["Floor Area (sqft)"])
            
            if year > 2024: 
                self._reset_btn()
                return messagebox.showwarning("Temporal Conflict", "Cannot predict for future construction.")
            if land < 50:
                self._reset_btn()
                return messagebox.showwarning("Spatial Error", "Land size below standard density.")
            
            v_ratio = floor / land
            est_levels = max(1, round(v_ratio + 0.4))
            
            sub = d["Property Subdivision"]
            bed = int(d["Bedrooms Total"])
            bath = int(d["Bathrooms Total"])
            
            feat = {"bedrooms": bed, "bathrooms": bath, "floor_area": floor, "land_size": land, "subdivision": sub, "build_year": year}
            
            res = predict_price(feat)
            p = float(res["price"]) # Normalize for MySQL
            self.result_label.configure(text=f"₱{p:,.0f}")
            
            if hasattr(self, 'analysis_f'): self.analysis_f.destroy()
            self.analysis_f = ctk.CTkFrame(self, fg_color=self.colors["surface"], corner_radius=25, border_width=1, border_color=self.colors["primary"])
            self.analysis_f.pack(fill="x", pady=20, padx=40)
            
            head_f = ctk.CTkFrame(self.analysis_f, fg_color=self.colors["secondary"], height=40, corner_radius=0)
            head_f.pack(fill="x")
            ctk.CTkLabel(head_f, text="NEURAL MARKET ANALYSIS REPORT", font=("Segoe UI", 10, "bold"), text_color=self.colors["primary"]).pack(pady=10)
            
            body_f = ctk.CTkFrame(self.analysis_f, fg_color="transparent")
            body_f.pack(fill="x", padx=40, pady=30)
            
            # Metric Grid
            m_grid = ctk.CTkFrame(body_f, fg_color="transparent")
            m_grid.pack(fill="x")
            
            metrics = [
                ("DRIVE ENGINE", res['driver']),
                ("CONFIDENCE", f"{res['accuracy']*100:.1f}%"),
                ("EST. LEVELS", f"~{est_levels} FLOORS"),
                ("DENSITY RATIO", f"{v_ratio:.2f}x")
            ]
            
            for i, (l, v) in enumerate(metrics):
                col = i % 4
                f = ctk.CTkFrame(m_grid, fg_color="transparent")
                f.grid(row=0, column=col, sticky="nsew")
                m_grid.grid_columnconfigure(col, weight=1)
                ctk.CTkLabel(f, text=l, font=("Segoe UI", 9, "bold"), text_color=self.colors["text"]).pack()
                ctk.CTkLabel(f, text=v, font=("Segoe UI", 16, "bold"), text_color=self.colors["text_bright"]).pack()

            save_prediction(self.user_id, bed, bath, floor, land, sub, year, p)
        except Exception as e: messagebox.showerror("Error", str(e))
        finally:
            self._processing = False
            self._reset_btn()

    def _reset_btn(self):
        self.proc_btn.configure(state="normal", text="GENERATE INTELLIGENCE REPORT")
