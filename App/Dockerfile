# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Setting the working directory in the container
WORKDIR /app

# Installing necessary system libraries
RUN apt-get update && apt-get install -y \
    curl \
    unixodbc \
    unixodbc-dev \
    g++ \
    gcc \
    gnupg \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Clean up the apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the project files to the working directory
COPY . .

# Install the required Python packages
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
