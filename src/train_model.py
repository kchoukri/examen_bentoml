
import pandas as pd
import bentoml
import bentoml.sklearn

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Charger les données préparées
dossier = Path(__file__).resolve().parent.parent / "data/processed"

X_train = pd.read_csv(dossier / "X_train.csv")
X_test = pd.read_csv(dossier / "X_test.csv")
y_train = pd.read_csv(dossier / "y_train.csv").iloc[:, 0]
y_test = pd.read_csv(dossier / "y_test.csv").iloc[:, 0]

# Créer et entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Les prédictions
y_pred = model.predict(X_test)

# Evaluer les performances
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE :", round(mae, 4))
print("R2 :", round(r2, 4))

# Sauvegarder le modèle dans BentoML
bento_model = bentoml.sklearn.save_model(
    "admission_lr",
    model
)

print("Modèle enregistré :", bento_model.tag)
