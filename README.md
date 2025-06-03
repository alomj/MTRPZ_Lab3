# Lab 3 : Containerization

## Python

### 1. Base optimal Docker File

-Base image used: `python:3.11-buster`

-*Building Time*: 48.9s | *Image Size* : 990mb

### 2. After Changing Code

Docker leverages layer caching. As a result significantly reducing the container build time (48.9s -> 10.8s)
*Image size*: 990mb (unchanged)

### 3. Ineffective method


-Dockerfile breaks layer caching by copying all files (COPY . .) before installing dependencies.
As a result, even small code changes re-trigger pip install.

-*Building Time*: (48.9s -> 52.5s) | *Image Size* : 990mb