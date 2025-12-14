from pathlib import Path

def main():
    # Récupère le chemin absolu du fichier actuel (main.py)
    BASE_DIR = Path(__file__).parent.parent

    # Construit le chemin vers le répertoire data/
    DATA_DIR = BASE_DIR / "data"

    # Vérifie que le répertoire en question existe bien
    if DATA_DIR.is_dir():
        print("Le répertoire data/ a été trouvé.")
    else:
        print("Le répertoire data/ est introuvable.")

if __name__ == "__main__":
    main()