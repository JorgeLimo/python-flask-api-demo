# ============================================================================
# run.py — Punto de entrada: aquí se arma la aplicación y se arranca
# ============================================================================
from flask import Flask, jsonify

from config import Config
from models import db
from routes import usuarios_bp

# 1. Crear la aplicación Flask
app = Flask(__name__)

# 2. Cargarle la configuración (conexión a Neon, etc.)
app.config.from_object(Config)

# 3. Conectar SQLAlchemy (models.py) con esta app
db.init_app(app)

# 4. Registrar las rutas de usuarios (routes.py) en la app
app.register_blueprint(usuarios_bp)

# 5. Crear la tabla "usuarios" en la base de datos si no existe todavía
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def inicio():
    """Ruta raíz: muestra qué endpoints existen."""
    return jsonify({
        "mensaje": "API CRUD de Usuarios (Flask + PostgreSQL/Neon)",
        "endpoints": {
            "GET /usuarios": "Lista todos los usuarios",
            "GET /usuarios/<id>": "Obtiene un usuario por su id",
            "POST /usuarios": "Crea un nuevo usuario",
            "PUT /usuarios/<id>": "Actualiza un usuario existente",
            "DELETE /usuarios/<id>": "Elimina un usuario",
        },
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)