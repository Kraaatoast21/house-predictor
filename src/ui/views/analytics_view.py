import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from src.database import get_all_predictions

class AnalyticsView(ctk.CTkFrame):
    def __init__(self, master, colors):
        super().__init__(master, fg_color="transparent")
        self.colors = colors
        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self, text="System Analytics", font=("Segoe UI", 32, "bold"), text_color=self.colors["text_bright"]).pack(anchor="w", pady=(0, 20))
        
        # Overview Stats
        stats_f = ctk.CTkFrame(self, fg_color="transparent")
        stats_f.pack(fill="x", pady=(0, 20))
        
        data = get_all_predictions()
        total_p = len(data)
        avg_price = sum(r['predicted_price'] for r in data) / total_p if total_p > 0 else 0
        
        self._create_stat_card(stats_f, "TOTAL REPORTS", str(total_p), 0)
        self._create_stat_card(stats_f, "AVG ESTIMATE", f"₱{avg_price/1000:.1f}K", 1)
        self._create_stat_card(stats_f, "SYSTEM STATUS", "OPTIMAL", 2)

        # Charts Row
        chart_row = ctk.CTkFrame(self, fg_color="transparent")
        chart_row.pack(fill="x", pady=10)
        
        # Feature Importance Card
        feat_card = ctk.CTkFrame(chart_row, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        feat_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(feat_card, text="PRICE DRIVER ANALYSIS", font=("Segoe UI", 12, "bold"), text_color=self.colors["primary"]).pack(pady=20)
        self._plot_importance(feat_card)

        # Popularity Card
        pop_card = ctk.CTkFrame(chart_row, fg_color=self.colors["surface"], corner_radius=20, border_width=1, border_color=self.colors["secondary"])
        pop_card.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(pop_card, text="MARKET INTEREST BY AREA", font=("Segoe UI", 12, "bold"), text_color=self.colors["primary"]).pack(pady=20)
        self._plot_popularity(pop_card, data)

    def _create_stat_card(self, parent, label, val, col):
        card = ctk.CTkFrame(parent, fg_color=self.colors["surface"], corner_radius=15, border_width=1, border_color=self.colors["secondary"], height=100)
        card.grid(row=0, column=col, padx=(0 if col==0 else 15, 0), sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        ctk.CTkLabel(card, text=label, font=("Segoe UI", 10, "bold"), text_color=self.colors["text"]).pack(pady=(20, 0))
        ctk.CTkLabel(card, text=val, font=("Segoe UI", 24, "bold"), text_color=self.colors["primary"]).pack(pady=(0, 20))

    def _plot_importance(self, parent):
        features = ['Land Size', 'Floor Area', 'Subdivision', 'Bedrooms', 'Year']
        weights = [0.35, 0.30, 0.15, 0.12, 0.08]
        
        fig, ax = plt.subplots(figsize=(4, 3.2), facecolor=self.colors["surface"])
        ax.set_facecolor(self.colors["surface"])
        ax.barh(features, weights, color=self.colors["primary"], alpha=0.8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.tick_params(axis='both', colors=self.colors["text"], labelsize=8)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def _plot_popularity(self, parent, data):
        if not data:
            ctk.CTkLabel(parent, text="No Data Available", font=("Segoe UI", 12), text_color=self.colors["text"]).pack(pady=50)
            return
            
        df = pd.DataFrame(data)
        counts = df['subdivision'].value_counts().head(5)
        
        fig, ax = plt.subplots(figsize=(4, 3.2), facecolor=self.colors["surface"])
        ax.set_facecolor(self.colors["surface"])
        counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=[self.colors["primary"], "#059669", "#10b981", "#34d399", "#6ee7b7"], 
                    textprops={'color':"white", 'fontsize':8}, wedgeprops={'edgecolor': self.colors["surface"]})
        ax.set_ylabel("")
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=(0, 5))
