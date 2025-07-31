
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from uuid import uuid4
from pathlib import Path
from celery.result import AsyncResult
from app.tasks import ocr_pdf

app = FastAPI()
UPLOAD_DIR = Path("/data/uploads")
RESULT_DIR = Path("/data/results")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Create temporary file with random name
    temp_id = str(uuid4())
    pdf_path = UPLOAD_DIR / f"{temp_id}.pdf"

    # Save file before launching the task
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Create OCR job AFTER file is saved
    # Use Celery task.id as the actual filename we track
    task = ocr_pdf.delay(
        str(pdf_path),
        str(RESULT_DIR / f"{task.id}.txt")
    )

    return {"job_id": task.id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    return {"job_id": job_id, "status": AsyncResult(job_id).status}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result_file = RESULT_DIR / f"{job_id}.txt"
    if result_file.exists():
        return {"text": result_file.read_text()}
    return {"error": "Result not available"}
