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
    import uuid

    # 1. Generate a unique ID (we'll use this as the job_id and filenames)
    job_id = str(uuid.uuid4())

    # 2. Define file paths
    pdf_path = UPLOAD_DIR / f"{job_id}.pdf"
    txt_path = RESULT_DIR / f"{job_id}.txt"

    # 3. Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # 4. Launch OCR task
    task = ocr_pdf.delay(str(pdf_path), str(txt_path))

    # 5. Return the UUID that ties everything together
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    return {"job_id": job_id, "status": AsyncResult(job_id).status}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result_file = RESULT_DIR / f"{job_id}.txt"
    if result_file.exists():
        return {"text": result_file.read_text()}
    return {"error": "Result not available"}
