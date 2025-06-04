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

### 1. Base Dockerfile

When we check our directory, we can see that there are some files that are not included in the Dockerfile, such as:
`templates`, `README.rst`, `cmd`, `fizzbuzz`, `go.sum`, `go.mod` `main.go`

*Building Time*: 47.3s |
*Image Size*: 899 mb 


### 2. Add multi-stage build 

We introduced a multi-stage build using the `golang:1.22` image to compile the application and the scratch image as the
final minimal runtime environment. This approach copies only the final compiled binary into the final image, excluding 
unnecessary files and dependencies. However, because `scratch` image is completely empty ( no package manager, no shell)
It is not convenient for running commands or debugging inside the container.

*Building Time*: 45.5s  |
*Image Size*: 10.2 mb 

### 3. Using distroless 

Distroless images are still minimal and secure but include essential runtime components such as certificate authorities
and minimal system libraries. This allows the application to run HTTPS or TLS connections out of the box
    
*Building Time*: 47.2s  |
*Image Size*: 12 mb 

## Node.js

### 1. Initial docker-compose 

include 2 services:
-node.js (app)
-mongo.db (mongodb)

To ensure data consistency and persistence, we mounted a volume in the docker-compose.yml file:

```
    volumes:
      - mongodb_data:/data/db
```

For Nodejs container:
*Building Time*:  13.6s |
*Image Size*:  1.17 gb

### 2. Refactor Dockerfile

We optimized the Dockerfile by switching from the default node:18 image to the much lighter node:18-alpine base image
and by using a multi-stage build. This significantly reduced the final image size

*Building Time*:  19s |
*Image Size*:  148mb


### Conclusion

The containerization experiment with `Python`, `Go`, and `Node.js` reveals key insights:

- `Python`:  
  - `python:3.11-alpine` reduced image size from `990MB` → `98.5MB` and build time from `48.9s` → `17.9s`.  
  - Adding `numpy` increased size to `293MB` and time to `27.0s`.  
  - Switching to Debian-based `bullseye` pushed size to `1.16GB` and time to `54.9s`.  
  - Poor file copying (`COPY . .` too early) broke caching and slowed builds.

- `Go`:  
  - Multi-stage build with `scratch` reduced image size from `899MB` → `10.2MB` (build time `45.5s`).  
  - Using `distroless` gave a more practical secure runtime with an image size of `12MB`.

- `Node.js`:  
  - Switching to `node:18-alpine` with multi-stage build dropped size from `1.17GB` → `148MB`.  
  - Build time slightly increased from `13.6s` → `19s`.

    

### Challenges & Explanations

- **Layer caching**: Incorrect Dockerfile structure (e.g., copying files before installing dependencies) caused unnecessary re-installation, increasing build time.
- **Numpy in Alpine**: Required compilation of heavy native dependencies (C/Fortran), which inflated image size and required build tools.
- **Scratch base**: While minimal and secure, it lacks shell/debugging tools — inconvenient for debugging or interactive container use.
- **Distroless**: More secure and includes essential runtime libraries (e.g., CA certificates), but also harder to debug.
- **Database services** (e.g., MongoDB): Even when app images are optimized, container stacks can still be heavy due to DB layers.


**Best Practices**:  
Use `Alpine`, `scratch`, or `distroless` with multi-stage builds for minimal size and enhanced security.  
However, always balance image size, security, and debugging needs, especially when dealing with heavy dependencies  
or external services