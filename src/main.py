from pathlib import Path

import pandas as pd

def load_data(csv_path):
    """Charge le fichier CSV contenant les résultats du Loto."""
    try:
        df = pd.read_csv(csv_path, sep=";")
        print(f"Fichier chargé avec succès : {len(df)} tirages trouvés.")
        return df
    except FileNotFoundError:
        print("Erreur : le fichier CSV est introuvable.")
        return None

def main():
    # Récupère le chemin absolu du fichier actuel (main.py)
    BASE_DIR = Path(__file__).parent.parent

    # Construit le chemin vers le répertoire data/
    DATA_DIR = BASE_DIR / "data"

    # Vérifie que le répertoire en question existe bien
    if DATA_DIR.is_dir():
        print("Le répertoire data/ a été trouvé.")

        # Chemin vers le fichier CSV contenant les résultats du Loto
        csv_path = DATA_DIR / "loto.csv"

        df = load_data(csv_path)

        if df is not None:
            # Affiche les premières lignes pour vérifier les noms de colonnes
            print("\nAperçu des données :")
            print(df.head())
    else:
        print("Le répertoire data/ est introuvable.")

if __name__ == "__main__":
    main()