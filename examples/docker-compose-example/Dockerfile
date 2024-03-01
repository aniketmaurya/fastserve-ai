FROM python:3.11

WORKDIR /api

# Copying requirements.txt to the container's working directory
COPY requirements.txt .

# Copying all other files and directories to the container's working directory
COPY . /api

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Running the api
CMD ["python", "api.py"]
