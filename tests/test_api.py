
import time
import requests
import jwt

URL = "http://localhost:3000"
SECRET = "secret_test_bentoml_2026"

# Données d'un étudiant
donnees = {
    "gre_score": 320,
    "toefl_score": 110,
    "university_rating": 4,
    "sop": 4.5,
    "lor": 4.0,
    "cgpa": 9.0,
    "research": 1
}


# Récupérer un token
def obtenir_token():
    r = requests.post(
        URL + "/login",
        json={"username": "admin", "password": "exam_bentoml"}
    )
    return r.json()["access_token"]


# Envoyer une prédiction
def predire(token=None, data=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.post(
        URL + "/predict",
        json=donnees if data is None else data,
        headers=headers
    )


# Test 1 : connexion correcte
def test_login_valide():
    token = obtenir_token()
    assert jwt.decode(token, SECRET, algorithms=["HS256"])


# Test 2 : connexion incorrecte
def test_login_invalide():
    r = requests.post(
        URL + "/login",
        json={"username": "admin", "password": "faux"}
    )
    assert r.status_code == 401


# Test 3 : sans token
def test_sans_token():
    assert predire().status_code == 401


# Test 4 : token invalide
def test_token_invalide():
    assert predire("faux_token").status_code == 401


# Test 5 : token expiré
def test_token_expire():
    token = jwt.encode(
        {"exp": int(time.time()) - 60},
        SECRET,
        algorithm="HS256"
    )
    assert predire(token).status_code == 401


# Test 6 : prédiction valide
def test_prediction_valide():
    r = predire(obtenir_token())
    assert r.status_code == 200
    assert isinstance(r.json()["chance_admission"], (int, float))


# Test 7 : données invalides
def test_donnees_invalides():
    data = donnees.copy()
    data["gre_score"] = -10

    r = predire(obtenir_token(), data)
    assert r.status_code in (400, 422)
