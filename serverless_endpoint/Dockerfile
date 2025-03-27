FROM python:3.10-slim

WORKDIR /

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    cmake \
    libgomp1 \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install common Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Data science stack
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    matplotlib \
    seaborn \
    plotly \
    statsmodels

# Install PyTorch separately
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Try to install TensorFlow with compatibility flag
RUN pip install --no-cache-dir tensorflow-cpu==2.13.0

# Machine learning libraries (without TensorFlow and PyTorch)
RUN pip install --no-cache-dir \
    transformers \
    scikit-image \
    xgboost \
    lightgbm

# NLP tools
RUN pip install --no-cache-dir \
    nltk \
    spacy \
    gensim

# Download spaCy models
RUN python -m spacy download en_core_web_sm

# Web libraries
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    fastapi \
    uvicorn

# Database connectors
RUN pip install --no-cache-dir \
    sqlalchemy \
    psycopg2-binary \
    pymongo \
    redis

# Other useful libraries
RUN pip install --no-cache-dir \
    tqdm \
    pillow \
    networkx \
    pyyaml \
    pytest \
    joblib \
    sympy

# RunPod and handler dependencies
RUN pip install --no-cache-dir runpod fastapi pydantic

# Copy handler code
COPY code_handler.py /

# Start the container
CMD ["python3", "-u", "code_handler.py"]