FROM python:3.11-slim

# System deps for PDF + OCR
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Download NLTK data at build time
RUN python - <<EOF
import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
EOF

# Copy app
COPY app ./app

ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
