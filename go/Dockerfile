FROM golang:1.21.0 AS builder

WORKDIR /app
COPY . .
RUN go mod download && CGO_ENABLED=0 GOOS=linux go build -o /myapp

FROM gcr.io/distroless/static:nonroot
COPY --from=builder /myapp /myapp

EXPOSE 8080
CMD ["/myapp", "serve"]