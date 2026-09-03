import json
import os

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


CATEGORIAS_DISPONIBLES = [
    {
        "nombre": "productos",
        "descripcion": "Bienes físicos como computadoras, ropa, muebles, equipos, herramientas, etc."
    },
    {
        "nombre": "inmuebles",
        "descripcion": "Locales, terrenos, edificios, oficinas, almacenes o espacios físicos."
    },
    {
        "nombre": "víveres perecibles",
        "descripcion": "Alimentos o productos de consumo que pueden deteriorarse o tienen fecha de vencimiento."
    },
    {
        "nombre": "horas de personas",
        "descripcion": "Tiempo de voluntarios, profesionales, trabajadores o personas que brindan apoyo."
    }
]


def evaluar_requerimiento(requerimiento):

    if not requerimiento:
        raise ValueError(
            "El requerimiento no puede estar vacío"
        )

    categorias_texto = json.dumps(
        CATEGORIAS_DISPONIBLES,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Analiza el siguiente requerimiento de una ONG.

REQUERIMIENTO:

{requerimiento}


CATEGORÍAS DISPONIBLES:

{categorias_texto}


INSTRUCCIONES:

1. Analiza cuidadosamente el requerimiento.
2. Selecciona únicamente categorías de la lista proporcionada.
3. NO inventes categorías nuevas.
4. Una categoría puede aplicar aunque el texto utilice sinónimos.
5. Para cada categoría seleccionada, explica brevemente por qué aplica.
6. Si ninguna categoría aplica, devuelve un array vacío.
7. La categoría devuelta debe coincidir exactamente con el campo "nombre"
   de una de las categorías disponibles.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "categorias_detectadas": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "categoria": {
                                    "type": "STRING"
                                },
                                "motivo": {
                                    "type": "STRING"
                                }
                            },
                            "required": [
                                "categoria",
                                "motivo"
                            ]
                        }
                    }
                },
                "required": [
                    "categorias_detectadas"
                ]
            }
        )
    )

    return json.loads(response.text)
