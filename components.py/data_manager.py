import pandas as pd
import geopandas as gpd
from tkinter import messagebox

class DataManager:
    def __init__(self):
        self.geojson_path = "morocco-with-regions_.geojson"
        self.csv_path = 'donnees_synthetiques_finales.csv'
        self.load_geo_data()
        self.data_df = pd.read_csv(self.csv_path)
        self.data_df.columns = self.data_df.columns.str.strip()

    def load_geo_data(self):
        try:
            self.regions_gdf = gpd.read_file(self.geojson_path)
            possible_name_columns = ['nom', 'name', 'NAME', 'NOM', 'region', 'REGION']
            self.name_column = next((col for col in possible_name_columns if col in self.regions_gdf.columns), None)
            
            if self.name_column is None:
                string_columns = self.regions_gdf.select_dtypes(include=['object']).columns
                if len(string_columns) > 0:
                    self.name_column = string_columns[0]
                else:
                    raise ValueError("Aucune colonne appropriée trouvée pour les noms des régions")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données géographiques : {str(e)}")
