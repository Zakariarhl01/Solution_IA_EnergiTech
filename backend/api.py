from fastapi import FastAPI, Header
from auth import authenticate, get_current_user
from prometheus_client import generate_latest
from prometheus_client import Counter
from fastapi import HTTPException

PRED_COUNTER = Counter("predictions_total", "Total predictions")
LOGIN_COUNTER = Counter("login_total", "Total logins")

app = FastAPI()


@app.post("/login")
def login(data: dict):
    token = authenticate(data["username"], data["password"])
    if not token:
        raise HTTPException(401, "Bad credentials")
    LOGIN_COUNTER.inc()
    return {"access_token": token}


@app.post("/predict")
def predict(payload: dict, authorization: str = Header(...)):
    user = get_current_user(authorization)
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden")

    PRED_COUNTER.inc()
    return {"risk": "CRITIQUE", "RUL": 7}


@app.get("/metrics")
def metrics():
    return generate_latest()
