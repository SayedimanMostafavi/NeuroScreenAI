from pathlib import Path
import shutil

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from common.inference import EEGPredictor

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = (
    PROJECT_DIR
    / "models"
    / "depression"
    / "random_forest.pkl"
)

# ============================================================
# FastAPI
# ============================================================

app = FastAPI(title="NeuroScreenAI")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ============================================================
# Load Model
# ============================================================

predictor = EEGPredictor(MODEL_PATH)

# ============================================================
# Home Page
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# ============================================================
# Prediction
# ============================================================

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    file: UploadFile = File(...)
):

    filename = file.filename

    if not filename.lower().endswith(".edf"):

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "filename": filename,
                "diagnosis": "Invalid File",
                "probability": "0.00",
                "windows": 0,
                "error": "Please upload an EDF file."
            }
        )

    save_path = UPLOAD_DIR / filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        result = predictor.predict_edf(save_path)
        print("\n===== Prediction Result =====")
        print(result)
        print("=============================\n")
        print(result["prediction"])
        print(result["probability"])

        probability = round(result["probability"] * 100, 2)

        diagnosis = (
            "Depression"
            if result["prediction"] == 1
            else "Healthy"
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "filename": filename,
                "diagnosis": diagnosis,
                "probability": probability,
                "windows": result["windows"],
                "sampling_rate": f"{result['sampling_rate']:.1f}",
                "channels": len(result["channels"])
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "filename": filename,
                "diagnosis": "Error",
                "probability": "0.00",
                "windows": 0,
                "error": str(e)
            }
        )

# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "model": MODEL_PATH.name,
        "loaded": True
    }
