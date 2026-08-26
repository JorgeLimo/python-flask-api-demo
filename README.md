# API CRUD de Usuarios — Flask + PostgreSQL (Neon)

Este proyecto es una introducción práctica a cómo construir una API REST
con Python. El código está separado en unos pocos archivos, cada uno con
una responsabilidad clara, para que sea fácil de seguir.

## 1. Conceptos básicos

- **API**: un programa que recibe peticiones y responde con datos (en
  nuestro caso, en formato JSON).
- **REST**: un estilo de diseño de APIs que usa los métodos HTTP para
  indicar la acción que se quiere hacer:
  - `GET` → leer datos
  - `POST` → crear algo nuevo
  - `PUT` → actualizar algo que ya existe
  - `DELETE` → borrar algo
- **CRUD**: Create, Read, Update, Delete — las 4 operaciones básicas que
  casi todas las APIs implementan. Eso es justo lo que hace este proyecto,
  sobre una tabla de "usuarios".
- **Endpoint**: una URL específica de la API a la que le puedes hacer una
  petición. Ejemplo: `GET /usuarios` es un endpoint.
- **JSON**: el formato de texto que usamos para enviar y recibir datos.
  Se ve así: `{"nombre": "Ana", "edad": 25}`.
- **ORM (SQLAlchemy)**: en vez de escribir SQL a mano
  (`SELECT * FROM usuarios`), escribimos código Python
  (`Usuario.query.all()`) y la librería SQLAlchemy lo traduce a SQL.

## 2. Cómo están organizados los archivos

| Archivo             | ¿Qué hace?                                                        |
|----------------------|--------------------------------------------------------------------|
| `run.py`             | Punto de entrada. Arma la app y arranca el servidor.               |
| `config.py`          | Configuración y conexión a la base de datos (Neon).                |
| `models.py`          | Define cómo se ve la tabla "usuarios".                             |
| `routes.py`          | Los endpoints: qué pasa cuando llega cada petición.                 |
| `requirements.txt`   | Lista de librerías que hay que instalar.                            |
| `.env`               | Tu cadena de conexión secreta a Neon (tú la creas, no se comparte). |

**Cómo se conectan entre sí:** `config.py` no depende de nada.
`models.py` solo depende de Flask-SQLAlchemy. `routes.py` usa lo que
define `models.py`. `run.py` junta todo (`config.py` + `models.py` +
`routes.py`) y corre el servidor.

## 3. Crear la base de datos en Neon (gratis)

[Neon](https://neon.tech) es un servicio que te da una base de datos
PostgreSQL en la nube, sin instalar nada en tu computadora.

1. Entra a **https://neon.tech** y crea una cuenta gratuita.
2. Crea un nuevo proyecto (cualquier nombre está bien).
3. En el dashboard busca la sección **"Connection String"** (a veces
   aparece como "Connection Details").
4. Copia la URL. Se ve más o menos así:

   ```
   postgresql://usuario:contraseña@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## 4. Configurar el proyecto

```bash
# 1. Entra a la carpeta del proyecto
cd flask-crud-simple

# 2. Crea un entorno virtual (aísla las librerías de este proyecto)
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 3. Instala las librerías necesarias
pip install -r requirements.txt

# 4. Crea tu archivo de variables de entorno
cp .env.example .env

# 5. Abre .env y pega tu cadena de conexión de Neon en DATABASE_URL
```

Tu archivo `.env` debe quedar así (con tus datos reales):

```
DATABASE_URL=postgresql://usuario:contraseña@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

> ⚠️ El archivo `.env` **nunca** se sube a Git ni se comparte: ahí está la
> contraseña de tu base de datos. Por eso ya está incluido en `.gitignore`.

## 5. Ejecutar la API

```bash
python run.py
```

Verás algo como:

```
 * Running on http://127.0.0.1:5001
```

La primera vez que corres el proyecto, se crea automáticamente la tabla
`usuarios` en tu base de datos de Neon (no necesitas escribir SQL para
eso — lo hace `db.create_all()` en `run.py`).

Abre `http://127.0.0.1:5001/` en tu navegador: verás un mensaje con la
lista de endpoints disponibles.

## 6. Probar los endpoints

Puedes usar `curl` desde la terminal, o herramientas como **Postman** o
**Insomnia** si prefieres una interfaz visual.

### Crear un usuario
```bash
curl -X POST http://127.0.0.1:5001/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ana Torres", "email": "ana@example.com", "edad": 25}'
```

### Listar todos los usuarios
```bash
curl http://127.0.0.1:5001/usuarios
```

### Obtener un usuario por id
```bash
curl http://127.0.0.1:5001/usuarios/1
```

### Actualizar un usuario
```bash
curl -X PUT http://127.0.0.1:5001/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"edad": 26}'
```

### Eliminar un usuario
```bash
curl -X DELETE http://127.0.0.1:5001/usuarios/1
```

## 7. Tabla de endpoints

| Método | Ruta              | ¿Qué hace?                     |
|--------|-------------------|---------------------------------|
| GET    | `/usuarios`       | Lista todos los usuarios        |
| GET    | `/usuarios/<id>`  | Obtiene un usuario por id       |
| POST   | `/usuarios`       | Crea un nuevo usuario           |
| PUT    | `/usuarios/<id>`  | Actualiza un usuario existente  |
| DELETE | `/usuarios/<id>`  | Elimina un usuario              |

## 8. Códigos de respuesta que vas a ver

| Código | Significado                                              |
|--------|--------------------------------------------------------------|
| 200    | OK — todo salió bien                                          |
| 201    | Created — se creó el recurso correctamente                    |
| 400    | Bad Request — los datos enviados están mal o incompletos      |
| 404    | Not Found — el usuario que pediste no existe                  |
| 409    | Conflict — ya existe un usuario con ese email                  |

## 9. Preguntas frecuentes

**¿Por qué usamos `.env` en vez de escribir la contraseña en el código?**
Porque si subes el código a GitHub (o lo compartes), no quieres que tu
contraseña quede expuesta. El archivo `.env` se queda solo en tu
computadora.

**¿Qué pasa si cierro la terminal y vuelvo a correr `python run.py`?**
Tus datos siguen ahí: están guardados en Neon (en la nube), no en tu
computadora, así que no se pierden.

**¿Puedo ver mis datos directamente en Neon?**
Sí. En el dashboard de Neon hay un "SQL Editor" donde puedes correr
`SELECT * FROM usuarios;` y ver tus filas directamente.