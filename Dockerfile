# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8888

# set environment variables
ENV PRODUCTION=${PRODUCTION}
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV MIDTRANS_SERVER_KEY=${MIDTRANS_SERVER_KEY}
ENV MIDTRANS_CLIENT_KEY=${MIDTRANS_CLIENT_KEY}



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
