import base64

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.scorer import analyze_image
from app.models import AnalysisResult

app = FastAPI(title="Layout Critic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend origin before shipping
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


@app.get("/")
def root():
    return {"status": "ok", "service": "layout-critic-api"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a PNG, JPG, or WEBP image.")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    image_b64 = base64.b64encode(contents).decode("utf-8")

    try:
        result = analyze_image(image_b64)
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return result
