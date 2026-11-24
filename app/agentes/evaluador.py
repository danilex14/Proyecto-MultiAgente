"""Agente 3: evalúa las respuestas del estudiante."""
import json

from app.esquemas import Evaluacion, Material, RespuestaUsuario
from app.llm import preguntar

SISTEMA = (
    "Eres un evaluador justo. Comparas cada respuesta del estudiante con la respuesta "
    "esperada, valoras la comprensión (no la redacción exacta), das un puntaje de 0 a 10 "
    "por pregunta, un puntaje total de 0 a 100 y una recomendación breve de qué repasar. "
    "Responde siempre en español."
)


def evaluar(material: Material, respuestas: list[RespuestaUsuario]) -> Evaluacion:
    datos = {
        "subtema": material.subtema,
        "preguntas": [p.model_dump() for p in material.preguntas],
        "respuestas_del_estudiante": [r.model_dump() for r in respuestas],
    }
    mensaje = json.dumps(datos, ensure_ascii=False, indent=2)
    return preguntar(SISTEMA, mensaje, Evaluacion)
