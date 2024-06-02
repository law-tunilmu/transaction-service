# pull official base image
FROM ubuntu:latest

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update \
    && apt-get install -y \
        git \
        python3 \
        python3-pip \
        
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy the rest of the project files
COPY . .

# set environment variables
ENV PRODUCTION=${PRODUCTION}
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV MIDTRANS_SERVER_KEY=${MIDTRANS_SERVER_KEY}
ENV MIDTRANS_CLIENT_KEY=${MIDTRANS_CLIENT_KEY}



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
