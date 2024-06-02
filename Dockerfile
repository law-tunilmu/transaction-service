# pull official base image
FROM ubuntu:latest

# set work directory
WORKDIR /src/app
COPY . /src/app

# install dependencies
RUN apt-get update \
    && apt-get install -y \
        git \
        python3 \
        python3-pip \
        rm -rf /var/lib/apt/lists/*
        
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# set environment variables
ENV PRODUCTION=${PRODUCTION}
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV MIDTRANS_SERVER_KEY=${MIDTRANS_SERVER_KEY}
ENV MIDTRANS_CLIENT_KEY=${MIDTRANS_CLIENT_KEY}



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
