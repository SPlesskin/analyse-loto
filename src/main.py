from pathlib import Path

import pandas as pd
import numpy as np

#------------------------------------------------------------------------------
# Constantes
#------------------------------------------------------------------------------
BALL_COLUMN_PATTERN = r"^boule_\d+$"

def load_data(csv_path):
    """Charge le fichier CSV contenant les résultats du Loto."""
    try:
        df = pd.read_csv(csv_path, sep=";")
        print(f"Fichier chargé avec succès : {len(df)} tirages trouvés.")
        return df
    except FileNotFoundError:
        print("Erreur : le fichier CSV est introuvable.")
        return None

def compute_frequencies(df: pd.DataFrame) -> np.ndarray:
    """
    Retourne un tableau 1D contenant la fréquence d'apparition pour chaque
    numéro (de 1 à 49).
    
    L'indice 0 correspond au numéro 1, l'indice 48 au numéro 49.
    """
    # Calcule le nombre de tirages
    num_draws = len(df)

    # Sélectionne uniquement les colonnes des boules principales
    ball_columns_df = df.filter(regex=BALL_COLUMN_PATTERN)

    # Regroupe tous les tirages dans une seule colonne
    all_draws = ball_columns_df.to_numpy().flatten()

    # Compte les occurrences de chaque nombre
    counts = pd.Series(all_draws).value_counts()

    # Force un tableau de taille 49 ordonné (de 1 à 49)
    sorted_counts = counts.reindex(range(1, 50), fill_value=0)

    # Transforme les occurrences en fréquences
    frequencies = sorted_counts.to_numpy() / num_draws

    return frequencies

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

            _ = compute_frequencies(df)
    else:
        print("Le répertoire data/ est introuvable.")

if __name__ == "__main__":
    main()