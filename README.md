# ecommerce_api_reto_ia

API de ecommerce desarrollada con FastAPI y SQLAlchemy, con MySQL como base de datos.

## Requisitos

- Docker Desktop en ejecución.
- Docker Compose.

## Ejecutar con Docker

1. (Opcional) Copiar `.env.example` como `.env` y ajustar las variables.
2. Desde la carpeta raíz del proyecto, ejecutar:

   ```bash
   docker compose up --build -d
   ```

3. Consultar la documentación interactiva:

   - Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

La API espera a que MySQL supere su healthcheck antes de iniciar. Los datos de MySQL se conservan en el volumen `mysql_data`.

## Detener los servicios

```bash
docker compose down
```

Para eliminar también los datos persistidos de MySQL:

```bash
docker compose down -v
```

## Ejecutar pruebas localmente

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar pruebas:

```bash
pytest -v
```

Medir cobertura:

```bash
pytest --cov=main --cov=database --cov=models --cov=schemas --cov-report=term-missing
```

Las pruebas utilizan SQLite aislado y no requieren un servidor MySQL.

## Endpoints presentes en esta versión

- `POST /users/`: crear usuario.
- `GET /products/`: listar productos.
- `POST /orders/`: procesar pedido.

**Alcance:** esta configuración agrega containerización y pruebas sobre los endpoints existentes. No implementa paginación en productos ni el historial de pedidos por usuario.
