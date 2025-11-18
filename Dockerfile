# -------------------------------
# 1. Base Image (Slim + Python)
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# 2. Install system dependencies
# (required for Pillow and image ops)
# -------------------------------
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libopenjp2-7 \
    libwebp-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 3. Create app directory
# -------------------------------
WORKDIR /app

# -------------------------------
# 4. Install Python dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 5. Copy API code
# -------------------------------
COPY main.py .

# -------------------------------
# 6. Expose port
# -------------------------------
EXPOSE 8000

# -------------------------------
# 7. Run the server
# -------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
