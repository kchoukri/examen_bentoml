
import os
import hmac
from datetime import datetime, timedelta, timezone

import bentoml
import bentoml.sklearn
import jwt
import pandas as pd
from pydantic import Field


@bentoml.service(name="admission_prediction_service")
class AdmissionService:

    # Charger le modèle
    modele_ref = bentoml.models.BentoModel("admission_lr:latest")

    def __init__(self):
        self.modele = bentoml.sklearn.load_model(self.modele_ref)

    # Authentification
    @bentoml.api
    def login(self, username: str, password: str,
              ctx: bentoml.Context) -> dict:

        utilisateur = os.environ["API_USERNAME"]
        mot_de_passe = os.environ["API_PASSWORD"]
        secret = os.environ["JWT_SECRET"]

        if not (hmac.compare_digest(username, utilisateur)
                and hmac.compare_digest(password, mot_de_passe)):
            ctx.response.status_code = 401
            return {"detail": "Identifiants incorrects"}

        token = jwt.encode(
            {
                "sub": username,
                "exp": datetime.now(timezone.utc)
                + timedelta(minutes=30)
            },
            secret,
            algorithm="HS256"
        )

        return {"access_token": token, "token_type": "bearer"}

    # Prédiction sécurisée
    @bentoml.api
    def predict(
        self,
        gre_score: int = Field(ge=0, le=340),
        toefl_score: int = Field(ge=0, le=120),
        university_rating: int = Field(ge=1, le=5),
        sop: float = Field(ge=0, le=5),
        lor: float = Field(ge=0, le=5),
        cgpa: float = Field(ge=0, le=10),
        research: int = Field(ge=0, le=1),
        ctx: bentoml.Context = None
    ) -> dict:

        # Vérifier le token JWT
        authorization = ctx.request.headers.get(
            "authorization", ""
        )

        if not authorization.startswith("Bearer "):
            ctx.response.status_code = 401
            return {"detail": "Token manquant"}

        token = authorization.split(" ", 1)[1]

        try:
            jwt.decode(
                token,
                os.environ["JWT_SECRET"],
                algorithms=["HS256"]
            )
        except jwt.PyJWTError:
            ctx.response.status_code = 401
            return {"detail": "Token invalide ou expiré"}

        # Préparer les données
        donnees = pd.DataFrame([{
            "GRE Score": gre_score,
            "TOEFL Score": toefl_score,
            "University Rating": university_rating,
            "SOP": sop,
            "LOR": lor,
            "CGPA": cgpa,
            "Research": research
        }])

        # Prédire la chance d'admission
        prediction = self.modele.predict(donnees)[0]

        return {
            "chance_admission": float(prediction)
        }