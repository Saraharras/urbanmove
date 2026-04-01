import requests
from tkinter import messagebox

class ApiManager:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"

    def fetch_arrets_bus_and_trams(self, bbox):
        query = f"""
        [out:json];
        (
          node["highway"="bus_stop"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          node["railway"="tram_stop"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          node["railway"="station"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
        );
        out body;
        """
        try:
            response = requests.get(self.overpass_url, params={"data": query})
            response.raise_for_status()
            data = response.json()
            return data.get("elements", [])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erreur API", f"Erreur lors de la requête API : {str(e)}")
            return []
