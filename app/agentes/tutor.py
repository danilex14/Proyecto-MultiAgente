"""Agente 2: genera material de estudio y preguntas para un subtema."""
from app.esquemas import Material
from app.llm import preguntar

SISTEMA = (
    "Eres un tutor paciente. Para el subtema indicado escribes una explicación clara "
    "con ejemplos, una lista de puntos clave y preguntas de práctica abiertas, cada una "
    "con su respuesta modelo. Numera las preguntas desde 1. Responde siempre en español."
)


def generar_material(tema: str, subtema: str, nivel: str = "principiante", num_preguntas: int = 3) -> Material:
    mensaje = (
        f"Tema general: {tema}\nSubtema: {subtema}\nNivel: {nivel}\n"
        f"Cantidad de preguntas: {num_preguntas}"
    )
    return preguntar(SISTEMA, mensaje, Material)
