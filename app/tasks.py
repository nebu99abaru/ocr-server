from celery import Celery
import subprocess

app = Celery("worker", broker="redis://redis:6379/0")

@app.task
def ocr_pdf(pdf_path, output_path):
    output_pdf = "/tmp/output.pdf"  # dummy output path
    subprocess.run(["ocrmypdf", "--force-ocr", "--sidecar", output_path, pdf_path, output_pdf], check=True)
