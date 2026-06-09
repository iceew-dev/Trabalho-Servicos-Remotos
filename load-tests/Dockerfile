FROM python:3.10-slim

WORKDIR /app

# Copia tudo da pasta load-tests (incluindo os stubs que você colou lá)
COPY . .

# Instala apenas o necessário via pip (as bibliotecas de base)
RUN pip install locust zeep lxml grpcio protobuf

EXPOSE 8089
CMD ["locust", "-f", "locustfile.py"]