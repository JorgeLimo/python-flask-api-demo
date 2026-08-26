# ============================================================================
# routes.py — Los endpoints de la API: qué pasa cuando llega cada petición
# ============================================================================
from flask import Blueprint, request, jsonify
from models import db, Usuario

# Un Blueprint agrupa un conjunto de rutas relacionadas (aquí, todas las
# de usuarios) para luego "engancharlas" a la app principal en run.py.
usuarios_bp = Blueprint("usuarios", __name__)


def validar_datos_usuario(datos, es_creacion):
    """Revisa que los datos que mandó el cliente tengan sentido antes de
    guardarlos. Devuelve una lista de errores (vacía si todo está bien)."""
    errores = []

    nombre = datos.get("nombre")
    if es_creacion and not nombre:
        errores.append("El campo 'nombre' es obligatorio.")
    elif nombre is not None and not isinstance(nombre, str):
        errores.append("El campo 'nombre' debe ser texto.")

    email = datos.get("email")
    if es_creacion and not email:
        errores.append("El campo 'email' es obligatorio.")
    elif email is not None:
        if not isinstance(email, str) or "@" not in email:
            errores.append("El campo 'email' no tiene un formato válido.")

    if "edad" in datos and datos.get("edad") is not None:
        edad = datos.get("edad")
        if not isinstance(edad, int) or isinstance(edad, bool) or edad < 0:
            errores.append("El campo 'edad' debe ser un entero mayor o igual a 0.")

    return errores


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    """GET /usuarios → devuelve todos los usuarios."""
    usuarios = Usuario.query.order_by(Usuario.id).all()
    return jsonify([u.to_dict() for u in usuarios]), 200


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def obtener_usuario(usuario_id):
    """GET /usuarios/5 → devuelve un solo usuario por id."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": f"No existe un usuario con id {usuario_id}."}), 404
    return jsonify(usuario.to_dict()), 200


@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    """POST /usuarios → crea un usuario nuevo."""
    datos = request.get_json(silent=True)
    if datos is None:
        return jsonify({"error": "Debes enviar un JSON válido en el body."}), 400

    errores = validar_datos_usuario(datos, es_creacion=True)
    if errores:
        return jsonify({"errores": errores}), 400

    nuevo_usuario = Usuario(
        nombre=datos["nombre"].strip(),
        email=datos["email"].strip().lower(),
        edad=datos.get("edad"),
    )

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ya existe un usuario registrado con ese email."}), 409

    return jsonify(nuevo_usuario.to_dict()), 201


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def actualizar_usuario(usuario_id):
    """PUT /usuarios/5 → actualiza los campos enviados de un usuario."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": f"No existe un usuario con id {usuario_id}."}), 404

    datos = request.get_json(silent=True)
    if datos is None:
        return jsonify({"error": "Debes enviar un JSON válido en el body."}), 400

    errores = validar_datos_usuario(datos, es_creacion=False)
    if errores:
        return jsonify({"errores": errores}), 400

    if "nombre" in datos:
        usuario.nombre = datos["nombre"].strip()
    if "email" in datos:
        usuario.email = datos["email"].strip().lower()
    if "edad" in datos:
        usuario.edad = datos["edad"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ya existe un usuario registrado con ese email."}), 409

    return jsonify(usuario.to_dict()), 200


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(usuario_id):
    """DELETE /usuarios/5 → elimina un usuario."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": f"No existe un usuario con id {usuario_id}."}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": f"Usuario {usuario_id} eliminado correctamente."}), 200