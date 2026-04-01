import tkinter as tk
from tkinter import ttk, messagebox
from api_manager import ApiManager
from data_manager import DataManager
from chart_visualizer import ChartVisualizer

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisateur de Transport et Graphiques")
        self.root.geometry("1200x800")

        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.upper_frame = ttk.Frame(self.main_frame)
        self.upper_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.data_manager = DataManager()
        self.api_manager = ApiManager()

        self.create_header_style()
        self.create_controls()
        self.paned_window = tk.PanedWindow(self.upper_frame, orient=tk.HORIZONTAL,
                                           sashwidth=4, showhandle=True, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.map_frame = ttk.Frame(self.paned_window)
        self.graph_frame = ttk.Frame(self.paned_window, width=200, height=300)

        self.paned_window.add(self.map_frame)
        self.paned_window.add(self.graph_frame)

        self.footer_frame = ttk.Frame(self.main_frame, height=250)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        self.footer_frame.pack_propagate(False)

        self.chart_visualizer = ChartVisualizer(self.map_frame, self.graph_frame, 
                                              self.data_manager, self.api_manager)

        self.create_footer_table()
        self.chart_visualizer.update_map("Carte", "Toutes les régions")

    def create_header_style(self):
        style = ttk.Style()
        style.configure("Header.TLabel", background="white", 
                       font=("Arial", 12, "bold"), foreground="black")
        style.configure("HeaderFrame.TFrame", background="#A4AFE9")
        style.configure("TCombobox", font=("Arial", 12), foreground="black")

    def create_controls(self):
        header_frame = ttk.Frame(self.upper_frame, style="HeaderFrame.TFrame", 
                               relief="solid", borderwidth=2, padding="5")
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        control_frame = ttk.Frame(header_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Sélectionner une région:", 
                 style="Header.TLabel").pack(side=tk.LEFT)

        regions = [
            "Tangier-Tetouan-Al Hoceima",
            "Fez-Meknes",
            "Rabat-Salé-Kenitra",
            "Casablanca-Settat",
            "Marrakech-Safi"
        ]
        
        self.region_combobox = ttk.Combobox(control_frame, state="readonly",
                                          values=["Toutes les régions"] + regions)
        self.region_combobox.pack(side=tk.LEFT, padx=5)
        self.region_combobox.bind("<<ComboboxSelected>>", self.on_region_selected)
        self.region_combobox.set("Toutes les régions")

        transport_icons = {
            "Lignes de bus": "🚌",
            "Tramways": "🚋",
            "Grands taxis": "🚖",
            "Petits taxis": "🚕"
        }

        ttk.Label(control_frame, text="Sélectionner un type de transport:",
                 style="Header.TLabel").pack(side=tk.LEFT, padx=10)
        self.transport_combobox = ttk.Combobox(control_frame, state="readonly")
        self.transport_combobox.pack(side=tk.LEFT, padx=5)
        self.transport_combobox.bind("<<ComboboxSelected>>", self.on_transport_selected)
        self.transport_combobox['values'] = ["Carte", "Tous les types"] + [
            f"{icon} {name}" for name, icon in transport_icons.items()
        ]
        self.transport_combobox.set("Carte")

    def on_region_selected(self, event):
        region_name = self.region_combobox.get()
        transport_type = self.transport_combobox.get()
        self.chart_visualizer.update_map(transport_type, region_name)

    def on_transport_selected(self, event):
        transport_type = self.transport_combobox.get()
        region_name = self.region_combobox.get()
        self.chart_visualizer.update_map(transport_type, region_name)

    def create_footer_table(self):
        style = ttk.Style()
        style.configure("Footer.TFrame", background='#CCCCCCC')
        self.footer_frame.configure(style="Footer.TFrame")

        try:
            df = self.data_manager.data_df

            self.footer_table = ttk.Treeview(
                self.footer_frame,
                columns=df.columns.tolist(),
                show="headings",
                height=6
            )

            for col in df.columns:
                self.footer_table.heading(col, text=col)
                self.footer_table.column(col, width=100, anchor="center")

            for _, row in df.iterrows():
                self.footer_table.insert("", "end", values=row.tolist())

            self.footer_table.pack(fill=tk.BOTH, expand=True)

            vsb = ttk.Scrollbar(self.footer_frame, orient="vertical", 
                               command=self.footer_table.yview)
            vsb.pack(side=tk.RIGHT, fill="y")
            self.footer_table.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(self.footer_frame, orient="horizontal", 
                               command=self.footer_table.xview)
            hsb.pack(side=tk.BOTTOM, fill="x")
            self.footer_table.configure(xscrollcommand=hsb.set)

        except Exception as e:
            messagebox.showerror("Erreur",
                               f"Erreur lors de l'affichage des données dans le footer : {str(e)}")
