import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartVisualizer:
    def __init__(self, map_frame, graph_frame, data_manager, api_manager):
        self.map_frame = map_frame
        self.graph_frame = graph_frame
        self.data_manager = data_manager
        self.api_manager = api_manager
        self.zoom_level = 1.0
        self.ax = None
        self.fig = None
        self.canvas = None
        self.map_canvas = None
        self.graph_canvas = None

    def create_zoom_controls(self):
        zoom_frame = ttk.Frame(self.map_frame)
        zoom_frame.place(relx=0.95, rely=0.05, anchor='ne')
        
        style = ttk.Style()
        style.configure("Zoom.TButton", padding=5)
        
        zoom_in_btn = ttk.Button(zoom_frame, text="🔍+", 
                                command=self.zoom_in, 
                                style="Zoom.TButton",
                                width=3)
        zoom_in_btn.pack(pady=(0, 2))
        
        zoom_out_btn = ttk.Button(zoom_frame, text="🔍-", 
                                 command=self.zoom_out, 
                                 style="Zoom.TButton",
                                 width=3)
        zoom_out_btn.pack()
        
        reset_zoom_btn = ttk.Button(zoom_frame, text="↺", 
                                  command=self.reset_zoom, 
                                  style="Zoom.TButton",
                                  width=3)
        reset_zoom_btn.pack(pady=(2, 0))

    def zoom_in(self):
        self.zoom_level *= 0.8
        self.apply_zoom()
        
    def zoom_out(self):
        self.zoom_level *= 1.2
        self.apply_zoom()
        
    def reset_zoom(self):
        self.zoom_level = 1.0
        self.apply_zoom()
        
    def apply_zoom(self):
        if self.ax is not None:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            
            xcenter = (xlim[1] + xlim[0]) / 2
            ycenter = (ylim[1] + ylim[0]) / 2
            
            xwidth = (xlim[1] - xlim[0]) * self.zoom_level
            ywidth = (ylim[1] - ylim[0]) * self.zoom_level
            
            self.ax.set_xlim(xcenter - xwidth/2, xcenter + xwidth/2)
            self.ax.set_ylim(ycenter - ywidth/2, ycenter + ywidth/2)
            
            if self.map_canvas:
                self.map_canvas.draw()

    def update_map(self, transport_type, region_name):
        for widget in self.map_frame.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.destroy()
                
        for widget in self.graph_frame.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.destroy()

        self.create_map(region_name)
        
        if transport_type == "Tous les types":
            if region_name == "Toutes les régions":
                self.create_default_graph()
            else:
                self.create_region_graphs(region_name)
        elif transport_type.startswith("🚌"):
            self.create_transport_specific_graph("Lignes de bus", region_name)
        elif transport_type.startswith("🚋"):
            self.create_transport_specific_graph("Nombre de tramways", region_name)
        elif transport_type.startswith("🚖"):
            self.create_transport_specific_graph("Grands taxis", region_name)
        elif transport_type.startswith("🚕"):
            self.create_transport_specific_graph("Petits taxis", region_name)
        else:
            self.create_default_graph()

    def create_map(self, region_name):
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        plot_data = self.data_manager.regions_gdf
        if region_name != "Toutes les régions":
            plot_data = self.data_manager.regions_gdf[
                self.data_manager.regions_gdf[self.data_manager.name_column] == region_name
            ]

        plot_data.plot(ax=self.ax, color="#D8BFD8", edgecolor="black")

        if region_name != "Toutes les régions":
            region_geom = plot_data.geometry
            if not region_geom.empty:
                bbox = region_geom.total_bounds
                stops_and_trams = self.api_manager.fetch_arrets_bus_and_trams(bbox)

                if stops_and_trams:
                    bus_stops = [(el["lat"], el["lon"]) for el in stops_and_trams 
                               if el.get("tags", {}).get("highway") == "bus_stop"]
                    tram_stops = [(el["lat"], el["lon"]) for el in stops_and_trams 
                                if el.get("tags", {}).get("railway") == "tram_stop"]
                    train_stations = [(el["lat"], el["lon"]) for el in stops_and_trams 
                                    if el.get("tags", {}).get("railway") == "station"]

                    if bus_stops:
                        bus_lats, bus_lons = zip(*bus_stops)
                        self.ax.scatter(bus_lons, bus_lats, color="#A4AFE9", marker="o", 
                                      label="Arrêts de bus", s=20)

                    if tram_stops:
                        tram_lats, tram_lons = zip(*tram_stops)
                        self.ax.scatter(tram_lons, tram_lats, color="#FFA500", marker="^", 
                                      label="Arrêts de tram", s=40)
                    if train_stations:
                        station_lats, station_lons = zip(*train_stations)
                        self.ax.scatter(station_lons, station_lats, color="#2741CC", marker="s", 
                                      label="Gares", s=50)

                    self.ax.legend()

        self.ax.set_title(f"Carte : {region_name}")
        self.ax.axis("off")
        self.apply_zoom()

        self.map_canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.create_zoom_controls()

    def create_default_graph(self):
        df = self.data_manager.data_df
        grouped_columns = ['Lignes de bus', 'Petits taxis', 'Grands taxis', 'Nombre de tramways']
        
        missing_columns = [col for col in grouped_columns if col not in df.columns]
        if missing_columns:
            messagebox.showerror("Erreur", f"Colonnes manquantes : {', '.join(missing_columns)}")
            return

        df_grouped = df.groupby('Régions')[grouped_columns].min()
        df_grouped_normalized = df_grouped / 1.7

        fig, ax = plt.subplots(figsize=(8, 4))
        df_grouped_normalized.plot(kind='bar', stacked=True, ax=ax, 
                                 color=["#CCCCCC", "#A4AFE9", "#E5D4B6", "#FFA500"])

        ax.set_title("Répartition des moyens de transport par région", fontsize=10)
        ax.set_xlabel("Régions")
        ax.set_ylabel("Nombre de véhicules / lignes")
        ax.legend(title="Type de transport")
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        fig.tight_layout()

        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_region_graphs(self, region_name):
        df = self.data_manager.data_df

        if region_name != "Toutes les régions":
            df = df[df['Régions'] == region_name]
        
        pie_columns = ['Lignes de bus', 'Petits taxis', 'Grands taxis', 'Nombre de tramways']
        bar_columns = ['Passagers/jour (bus)', 'Passagers/jour (trains)', 
                      'Passagers/jour (tramways)']

        missing_columns = [col for col in pie_columns + bar_columns if col not in df.columns]
        if missing_columns:
            messagebox.showerror("Erreur", f"Colonnes manquantes : {', '.join(missing_columns)}")
            return

        fig = Figure(figsize=(8, 4))
        
        ax1 = fig.add_subplot(121)
        pie_data = df[pie_columns].sum()
        ax1.pie(pie_data, labels=pie_columns, autopct='%1.1f%%', 
                colors=["#CCCCCC", "#A4AFE9", "#E5D4B6", "#FFA500"])
        ax1.set_title(f"Répartition des transports : {region_name}", fontsize=8)

        ax2 = fig.add_subplot(122)
        bar_data = df[bar_columns].iloc[0]
        ax2.bar(range(len(bar_columns)), bar_data, 
                color=["#CCCCCC", "#A4AFE9", "#FFA500"])
        ax2.set_title(f"Passagers par jour : {region_name}", fontsize=8)
        ax2.set_xticks(range(len(bar_columns)))
        ax2.set_xticklabels(bar_columns, rotation=45, ha='right', fontsize=8)

        fig.tight_layout()

        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_transport_specific_graph(self, transport_type, region_name):
        df = self.data_manager.data_df
        if region_name != "Toutes les régions":
            df = df[df['Régions'] == region_name]

        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        
        transport_data = df[transport_type]
        ax.bar(df['Régions'], transport_data, color="#A4AFE9")
        
        ax.set_title(f"{transport_type} par région")
        ax.set_xlabel("Régions")
        ax.set_ylabel("Nombre")
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
