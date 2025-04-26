FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file (from project root)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend source code (everything under backend/)
COPY backend/ .

# Set PYTHONPATH inside container
ENV PYTHONPATH=backend

# Command to start FastAPI app
CMD ["uvicorn", "app.root:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
