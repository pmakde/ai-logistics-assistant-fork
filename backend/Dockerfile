# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for Git LFS, AI support, OCR, and PDFs)
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    libgl1 \
    poppler-utils \
    tesseract-ocr \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first for caching
COPY req.txt .

# Install dependencies
# Note: We use the CPU version of torch for the container to keep it smaller
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code
COPY . .

# 🚀 FORCE LFS PULL: Turn pointers into real binaries
RUN git init && \
    git remote add origin https://huggingface.co/spaces/kushagramkhare/institute_RAG_assistant && \
    git lfs install && \
    git lfs pull && \
    rm -rf .git

# Verify that files are now REAL (should be > 1KB, pointers are < 200 bytes)
RUN echo "=== VERIFYING FILE SIZES (LFS Check Post-Pull) ===" && \
    ls -lh faiss_store/index.faiss && \
    head -c 100 faiss_store/index.faiss | grep "version https" && \
    echo "❌ Still an LFS pointer!" && exit 1 || \
    echo "✅ Success: Real binary downloaded."

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Command to run the application on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]