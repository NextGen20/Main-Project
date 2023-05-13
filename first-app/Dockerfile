FROM python:3.8-slim-buster

# Create app directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code to the container
COPY . .


EXPOSE 5000
CMD ["python3.8", "app.py"]
