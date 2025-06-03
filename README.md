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
As a result, even small code changes re-trigger `pip install`.

-*Building Time*: (48.9s -> 52.5s) | *Image Size* : 990mb

### 4. Using a smaller base image (`python:3.11-alpine`)

Switching to the `python:3.11-alpine` base image significantly improved both build time and image size.
Alpine is a minimal Linux distribution that provides a much smaller base footprint compared to Debian-based images.

Smaller base image: `python:3.11-alpine` is ~50MB compared to ~900MB for `python:3.11-buster`.


*Building Time*: (48,9s  -> 17.9s) |
*Image Size* : 990mb -> 98.5 mb

### 5. After add `numpy` methods for multiplying matrices

The increase in build time and image size is specifically caused by the addition of the `numpy` library.
`numpy` introduces heavy compiled dependencies that are not present in the minimal base image. Since `numpy` relies on 
compiled C and Fortran extensions, which require several heavy system dependencies to be installed in Alpine.
In summary, the size increase is not from `numpy` alone, but from the system-level build tools and libraries required to 
compile it in an Alpine environment.


*Building Time*: (17.9s  -> 27.0s) |
*Image Size* : 98.5mb -> 293 mb

### 6. Measure with debian-based image `python:3.11-bullseye`

Switching from the Alpine-based image to the Debian-based image resulted in a significant increase in both build time
and image size. Debian-based images come with a much larger base footprint compared to Alpine.
While Alpine is built for minimalism and uses lightweight `musl` C library, Debian uses the more feature-rich
(but heavier) glibc, and includes many additional tools and libraries coming out-of-the-box.
Additionally, installing numpy on Debian may process slower and heavier due to `apt` package manager which install more
metadata and documentation


*Building Time* : (27.0s -> 54.9s) |
*Image Size* : 293 mb -> 1.16 gb


## Go

1. Base Dockerfile

When we check our directory, we can see that there are some files that are not included in the Dockerfile, such as:
`templates`, `README.rst`, `cmd`, `fizzbuzz`, `go.sum`, `go.mod` `main.go`

*Building Time* 47.3s : 
*Image Size* 899 mb : 

