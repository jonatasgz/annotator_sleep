FROM python:3.12-slim

# Install system build tools and libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libpq-dev \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download pt_core_news_lg

# Download HuggingFace model (and move to permanent path)
RUN python -c "from transformers import pipeline; pipeline('ner', model='portugueseNLP/medialbertina_pt-pt_900m_NER')"

# Copy app source code
COPY backend .