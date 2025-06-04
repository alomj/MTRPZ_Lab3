FROM golang:1.21.0 AS builder

WORKDIR /app
COPY . .
RUN go mod download && CGO_ENABLED=0 GOOS=linux go build -o /myapp

FROM scratch

COPY --from=builder /myapp /myapp
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
CMD ["/myapp", "serve"]