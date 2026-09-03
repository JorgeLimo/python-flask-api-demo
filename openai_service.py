import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

CATEGORIAS_DISPONIBLES = [
    "productos",
    "inmuebles",
    "víveres perecibles",
    "horas de personas"
]

def evaluar_requerimiento(requerimiento):

    if not requerimiento:
        raise ValueError(
            "El requerimiento no puede estar vacío"
        )

    prompt = f"""
Analiza el siguiente requerimiento de una ONG.

REQUERIMIENTO:

{requerimiento}


CATEGORÍAS DISPONIBLES:

{json.dumps(CATEGORIAS_DISPONIBLES, ensure_ascii=False)}


INSTRUCCIONES:

1. Analiza cuidadosamente el requerimiento.
2. Selecciona ÚNICAMENTE categorías de la lista proporcionada.
3. No inventes categorías nuevas.
4. Una categoría puede aplicar aunque el requerimiento use sinónimos.
5. Para cada categoría seleccionada explica brevemente el motivo.
6. Si ninguna categoría aplica, devuelve un array vacío.
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "resultado_requerimiento",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "categorias_detectadas": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "categoria": {
                                        "type": "string"
                                    },
                                    "motivo": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "categoria",
                                    "motivo"
                                ],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": [
                        "categorias_detectadas"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    resultado = json.loads(
        response.output_text
    )

    return resultado
