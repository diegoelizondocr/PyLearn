# Python Endpoint

API REST para consultar y administrar usuarios y roles en Oracle Database. Está construida con FastAPI y Uvicorn.

## Requisitos

- Python instalado para ejecutar la API localmente.
- Una instancia de Oracle Database accesible desde la API.
- Docker Desktop y Docker Compose para ejecutar la API en un contenedor.

## Instalación local

Desde la carpeta del proyecto, crea y activa un entorno virtual en PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

La aplicación lee la configuración de Oracle desde variables de entorno o desde un archivo `.env` en la raíz. Los valores predeterminados son:

```env
ORACLE_USER=MyTestDB
ORACLE_PASSWORD=MyTestDB123
ORACLE_DSN=localhost:1521/FREEPDB1
```

Configura estos valores para que coincidan con tu base de datos. No subas credenciales reales al repositorio.

## Ejecutar y depurar

En VS Code, selecciona la configuración **FastAPI (local)** en Run and Debug y presiona F5. Esta configuración inicia Uvicorn en `http://127.0.0.1:8001`.

También puedes iniciar la API desde PowerShell:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

La base de datos debe estar disponible antes de llamar a rutas que consultan usuarios o roles. FastAPI obtiene una conexión mediante `get_db` antes de ejecutar esas rutas.

## Rutas principales

La documentación interactiva está disponible en `http://127.0.0.1:8001/docs` cuando ejecutas localmente.

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/` | Estado básico de la API |
| `GET` | `/health` | Comprueba la conexión con Oracle |
| `GET` | `/users` | Lista usuarios |
| `GET` | `/users/{username}` | Obtiene un usuario |
| `POST` | `/users` | Crea un usuario |
| `PATCH` | `/users/{username}/active` | Actualiza el estado activo |
| `DELETE` | `/users/{username}` | Elimina un usuario |
| `GET` | `/roles` | Lista roles |
| `POST` | `/email` | Envía un correo electrónico |

El endpoint `POST /email` recibe un JSON con `to`, `subject` y `html`. Por ejemplo:

```json
{
  "to": "destinatario@example.com",
  "subject": "Asunto del correo",
  "html": "<p>Contenido del correo</p>"
}
```

## Docker Compose

El `docker-compose.yml` inicia solo la API y la publica en el puerto `8000`. Espera que ya exista una red Docker externa llamada `oracle-net` y que Oracle sea accesible desde esa red como `oracle-free:1521/FREEPDB1`.

Si la red todavía no existe, créala una vez:

```powershell
docker network create oracle-net
```

Con Oracle ya conectado a esa red, inicia la API:

```powershell
docker compose up --build
```

En modo Docker, abre `http://localhost:8000/docs`. Este modo no usa automáticamente los breakpoints de la configuración local de VS Code; para depurar con F5, ejecuta la API localmente y usa el puerto `8001`.