# Examen BentoML — Prédiction d'admission

## 1. Présentation

Ce projet permet de prédire les chances d'admission d'un étudiant à l'aide d'un modèle de régression linéaire déployé avec BentoML et Docker.

L'API dispose de deux endpoints :
- `/login` : authentification JWT.
- `/predict` : prédiction sécurisée.

## 2. outils

- Docker installé et démarré
- Python 3 et pip
- Port 3000 disponible

## 3. Charger l'image Docker

```bash
docker load -i admission_prediction_service.tar
```

## 4. Lancer le service Docker

```bash
docker run -d --rm --name admission-api -p 3000:3000 \
-e API_USERNAME=admin \
-e API_PASSWORD=exam_bentoml \
-e JWT_SECRET=secret_test_bentoml_2026 \
admission_prediction_service:latest serve
```

Vérifier que le conteneur fonctionne :

```bash
docker ps
```

L'API est accessible sur `http://localhost:3000`.

## 5. Installer les dépendances des tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 6. Exécuter les tests

Une fois le service démarré :

```bash
pytest -v
```

Les tests vérifient :
- L'authentification valide et invalide
- Les tokens JWT manquants, invalides ou expirés
- La prédiction avec un token valide
- Le rejet des données invalides

## 7. Arrêter le service

```bash
docker stop admission-api
```
