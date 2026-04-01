# urbanmove - Visualisation Interactive des Transports au Maroc

## 🎯 Objectif du projet

urbanmove est une application interactive développée en Python qui permet de visualiser et d'analyser les infrastructures de transport en commun dans cinq régions stratégiques du Maroc : Tanger-Tétouan-Al Hoceima, Rabat-Salé-Kénitra, Casablanca-Settat, Marrakech-Safi et Fès-Meknès.

## ✨ Fonctionnalités principales

- **Carte interactive** des régions avec zoom avant/arrière
- **Visualisations graphiques** : diagrammes à barres empilées, diagrammes circulaires, histogrammes des passagers
- **Filtres dynamiques** : sélection par région et par type de transport (bus, tramway, grands taxis, petits taxis)
- **Tableau de données** interactif avec toutes les informations tabulaires
- **Génération de données synthétiques** avec CTGAN pour pallier l'insuffisance des données réelles

## 🛠️ Technologies utilisées

- **Python 3.8+** : Langage principal
- **Tkinter/ttk** : Interface graphique
- **Matplotlib** : Visualisation de données
- **GeoPandas** : Données géospatiales
- **Pandas/NumPy** : Manipulation et calculs numériques
- **CTGAN** : Génération de données synthétiques

## 📊 Principaux résultats

### Constats généraux
- **Dominance des taxis** : représentent environ 97% des moyens de transport
- **Sous-représentation des bus** : seulement 2% du parc total
- **Tramways limités** : présents uniquement à Casablanca et Rabat
- **Flux passagers** : les bus transportent le plus de monde malgré leur faible nombre

### Par région
- **Casablanca-Settat** : Plus grand parc (~8,200 véhicules), infrastructure développée
- **Rabat-Salé-Kénitra** : Transport multimodal équilibré avec tramways
- **Fès-Meknès** : Forte dépendance aux petits taxis (65%), potentiel tramway
- **Marrakech-Safi** : Défi de gestion des flux touristiques
- **Tanger-Tétouan** : Potentiel de développement des transports en commun

## 🔬 Génération des données synthétiques

Face à l'insuffisance des données réelles (5 lignes initiales), CTGAN a été utilisé pour générer des données synthétiques fiables tout en préservant les relations entre variables et garantissant la confidentialité des informations.

## 📝 Conclusion

urbanmove offre une solution intuitive et complète pour visualiser et analyser les infrastructures de transport au Maroc. L'application permet aux décideurs, planificateurs urbains et citoyens de mieux comprendre les dynamiques de mobilité et d'identifier les zones nécessitant des améliorations.

