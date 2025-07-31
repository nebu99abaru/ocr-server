from fastapi import FastAPI, File, UploadFile
from uuid import uuid4
from pathlib import Path
from celery.result import AsyncResult
from app.tasks import ocr_pdf

app = FastAPI()
UPLOAD_DIR = Path("/data/uploads")
RESULT_DIR = Path("/data/results")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    job_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{job_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    task = ocr_pdf.delay(str(file_path), str(RESULT_DIR / f"{job_id}.txt"))
    return {"job_id": task.id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    res = AsyncResult(job_id)
    return {"job_id": job_id, "status": res.status}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result_file = RESULT_DIR / f"{job_id}.txt"
    if result_file.exists():
        return {"text": result_file.read_text()}
    return {"error": "Result not available"}
