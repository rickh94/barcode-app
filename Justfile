build:
  docker buildx build --platform linux/amd64,linux/arm64 -t rickh94/barcode-app:latest -t rickh94/barcode-app:21.12.0 --push .
