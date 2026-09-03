# ============================================================================
# routes.py — Los endpoints de la API: qué pasa cuando llega cada petición
# ============================================================================
from flask import Blueprint, request, jsonify
from models import db, Usuario
from gemini_service import evaluar_requerimiento

# Un Blueprint agrupa un conjunto de rutas relacionadas (aquí, todas las
# de usuarios) para luego "engancharlas" a la app principal en run.py.
usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    """GET /usuarios → devuelve todos los usuarios."""
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def buscar_usuario(usuario_id):
    """GET /usuarios/5 → busca y devuelve un solo usuario por id."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404
    return jsonify(usuario.to_dict())


@usuarios_bp.route("/usuarios", methods=["POST"])
def agregar_usuario():
    """POST /usuarios → agrega un usuario nuevo."""
    datos = request.get_json()

    nuevo_usuario = Usuario(
        nombre=datos["nombre"],
        email=datos["email"],
        edad=datos.get("edad"),
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.to_dict()), 201


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def editar_usuario(usuario_id):
    """PUT /usuarios/5 → edita los datos de un usuario existente."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404

    datos = request.get_json()

    usuario.nombre = datos.get("nombre", usuario.nombre)
    usuario.email = datos.get("email", usuario.email)
    usuario.edad = datos.get("edad", usuario.edad)

    db.session.commit()

    return jsonify(usuario.to_dict())


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(usuario_id):
    """DELETE /usuarios/5 → elimina un usuario."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado correctamente."})

@usuarios_bp.route("/evaluar-requerimiento", methods=["POST"])
def evaluar_requerimiento_ong():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Debe enviar un JSON"
            }), 400

        requerimiento = data.get("requerimiento")

        if not requerimiento:
            return jsonify({
                "success": False,
                "message": "El campo requerimiento es obligatorio"
            }), 400

        resultado = evaluar_requerimiento(
            requerimiento=requerimiento
        )

        return jsonify({
            "success": True,
            "data": resultado
        }), 200

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:

        print("ERROR EN /evaluar-requerimiento:", repr(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
