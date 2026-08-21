from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "income-lab-khoa")
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """Tải file model.joblib từ S3 về máy khi server khởi động."""
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}, skipping download")
        return
    s3 = boto3.client("s3")
    s3.download_file(ARTIFACT_BUCKET, MODEL_KEY, MODEL_PATH)
    print(f"Model downloaded from s3://{ARTIFACT_BUCKET}/{MODEL_KEY} to {MODEL_PATH}")


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features")
    prediction = int(model.predict([req.features])[0])
    label = "thu_nhap_cao" if prediction == 1 else "thu_nhap_thap"
    return {"prediction": prediction, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
