from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# Constantes
#------------------------------------------------------------------------------
BALL_COLUMN_PATTERN = r"^boule_\d+$"
DATE_COLUMN_NAME = "date_de_tirage"
DATE_COLUMN_FORMAT = "%d/%m/%Y"
NORMALIZATION_SCALE = 100 # Nombre de tirages de référence pour la fréquence

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

def find_period(df: pd.DataFrame):
    """Récupère la date de début et celle de fin de tous les tirages."""
    # Vérifie l'existence de la colonne contenant les dates de tirage
    if DATE_COLUMN_NAME not in df.columns:
        print(f"La colonne '{DATE_COLUMN_NAME}' est absente du DataFrame.")
        return None
    
    try:
        all_dates = pd.to_datetime(df[DATE_COLUMN_NAME], format=DATE_COLUMN_FORMAT)
    except ValueError as e:
        print(f"Erreur lors de la conversion des dates. Détails : {e}")
        return None

    return all_dates.min(), all_dates.max()

def plot_frequency_heatmap(frequencies: np.ndarray, period: tuple[pd.Timestamp, pd.Timestamp]):
    """Affiche une carte de chaleur 7x7 des fréquences normalisées sur 100 tirages."""
    # Normalise les fréquences sur 100 tirages
    freq_per_100 = np.round(frequencies * NORMALIZATION_SCALE).astype(int)

    # Transforme le tableau 1D en grille 7x7
    # Les numéros seront disposés de gauche à droite et de haut en bas.
    matrix = freq_per_100.reshape(7, 7)

    # Prépare les étiquettes pour l'affichage (les numéros 1 à 49)
    labels = np.arange(1, 50).reshape(7, 7)

    # Création de la carte
    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap="magma", vmin=0, vmax=100)

    # Enlève les axes x et y qui n'ont aucune utilité
    plt.axis("off")

    # Affiche un numéro dans chaque case
    for i in range(7):
        for j in range(7):
            ax.text(j, i, labels[i, j], ha="center", va="center", color="w")
    
    # Ajoute une barre de couleurs
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(f"Fréquence pour {NORMALIZATION_SCALE} tirages", rotation=-90, va="bottom")

    # Titre du graphique
    title = "Carte thermique des numéros du LOTO"
    if period is not None:
        title += f"\ndu {period[0].strftime("%d/%m/%Y")} au {period[1].strftime("%d/%m/%Y")}"
    ax.set_title(title)

    fig.tight_layout()
    plt.show()

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

            frequencies = compute_frequencies(df)
            
            period = find_period(df)

            plot_frequency_heatmap(frequencies, period)
    else:
        print("Le répertoire data/ est introuvable.")

if __name__ == "__main__":
    main()