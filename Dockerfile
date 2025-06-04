FROM python:3.10-slim

# Set working directory
WORKDIR /app

# For opencv and other libraries
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

COPY ./libs/vid-extractor/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]