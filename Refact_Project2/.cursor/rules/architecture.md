# QR Microservice Architecture
- Layered approach: Models -> Interfaces -> Repositories -> Services.
- In-Memory storage is used for all data.
- Thread-safety must be ensured using threading.Lock.
- No external APIs or Databases allowed.