FROM python:3.12-slim

# Install OS-level dependencies
RUN apt-get update && apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y numpy && pip install --no-cache-dir numpy && pip install --no-cache-dir runpod

# Run the serverless entrypoint script
CMD ["python", "runpod_serverless.py"]


# Dockerfile for Amazon AWS Docker-Lambda
# # Stage 1: Install dependencies on Amazon Linux
# FROM amazonlinux:2 as builder

# RUN yum install -y python3 ffmpeg && \
#     python3 -m ensurepip && \
#     pip3 install --upgrade pip

# WORKDIR /app

# COPY requirements.txt .

# # Install all dependencies
# RUN pip3 install -r requirements.txt -t . && \
#     # Force remove conflicting numpy and reinstall a safe version
#     pip3 uninstall -y numpy && \
#     pip3 install numpy -t .

# COPY . .

# # Stage 2: Lambda runtime + app
# FROM public.ecr.aws/lambda/python:3.12

# # Copy everything from the builder stage
# COPY --from=builder /app /var/task

# # Set the handler
# CMD ["jzuluaga_accent_classifier.handler"]

















# # Stage 1: Install dependencies on Amazon Linux
# FROM amazonlinux:2 as builder

# RUN yum install -y python3 ffmpeg && \
#     python3 -m ensurepip && \
#     pip3 install --upgrade pip

# WORKDIR /app
# COPY requirements.txt .
# RUN pip3 install -r requirements.txt -t .

# COPY . .

# # Stage 2: Lambda runtime + app
# FROM public.ecr.aws/lambda/python:3.12

# # Copy from builder
# COPY --from=builder /app /var/task

# # Set handler
# CMD ["jzuluaga_accent_classifier.handler"]