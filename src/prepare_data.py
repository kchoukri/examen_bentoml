
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Définir les chemins
racine = Path(__file__).resolve().parent.parent
fichier = racine / "data/raw/admission.csv"
dossier_sortie = racine / "data/processed"

# Charger et nettoyer les données
df = pd.read_csv(fichier)
df.columns = df.columns.str.strip()
df = df.drop(columns=["Serial No."], errors="ignore")
df = df.dropna()

# Sépare les variables et la cible
X = df.drop(columns=["Chance of Admit"])
y = df["Chance of Admit"]

# Diviser les données : 80 % train, 20 % test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Sauvegarder les fichiers
dossier_sortie.mkdir(parents=True, exist_ok=True)

X_train.to_csv(dossier_sortie / "X_train.csv", index=False)
X_test.to_csv(dossier_sortie / "X_test.csv", index=False)
y_train.to_csv(dossier_sortie / "y_train.csv", index=False)
y_test.to_csv(dossier_sortie / "y_test.csv", index=False)

print("Préparation des données terminée !")
print("Entraînement :", len(X_train), "lignes")
print("Test :", len(X_test), "lignes")
