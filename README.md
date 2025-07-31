# OCR Server with PDF Upload and Job Queue

This project sets up a Dockerized OCR (Optical Character Recognition) API server that accepts PDF files, processes them locally using OCR, and returns extracted text via job ID.

## 🔧 Features
- Upload PDF via HTTP API
- Scalable OCR processing using Celery and Redis
- Get job status and results by ID
- Local-only processing (no external OCR services)

---

## 🧑‍🏫 Step-by-Step Setup (For Beginners)

### 1. Prerequisites
Ensure your Ubuntu Server has:
- **Docker** installed: https://docs.docker.com/engine/install/ubuntu/
- **Docker Compose** installed: https://docs.docker.com/compose/install/

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/ocr-server.git
cd ocr-server
```

### 3. Build and Run the Docker Containers
```bash
docker-compose up --build
```
This will start:
- The API server on `http://localhost:8000`
- A background OCR worker
- Redis as the job queue backend

### 4. Upload a PDF for OCR
Use `curl` or Postman to send a PDF:
```bash
curl -F "file=@example.pdf" http://localhost:8000/upload
```
You will get a response with a `job_id`:
```json
{"job_id": "abc123..."}
```

### 5. Check Job Status
```bash
curl http://localhost:8000/status/abc123
```

### 6. Get OCR Result
```bash
curl http://localhost:8000/result/abc123
```

---

## 🧼 Stopping the Server
```bash
docker-compose down
```

## 🧪 Development Tips
- Modify OCR logic in `app/tasks.py`
- Add endpoints in `app/main.py`

---

## 📝 License
MIT License
