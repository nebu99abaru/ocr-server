from celery import Celery
import subprocess

app = Celery("worker", broker="redis://redis:6379/0")

@app.task
def ocr_pdf(pdf_path, output_path):
    subprocess.run(["ocrmypdf", "--force-ocr", "--sidecar", output_path, pdf_path], check=True)
