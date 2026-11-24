"""Agente 1: divide un tema en subtemas ordenados."""
from app.esquemas import Plan
from app.llm import preguntar

SISTEMA = (
    "Eres un planificador de estudio. Divides un tema en subtemas ordenados de lo "
    "básico a lo avanzado, cada uno estudiable en una sesión de 30 a 60 minutos. "
    "Responde siempre en español."
)


def planificar(tema: str, nivel: str = "principiante", num_subtemas: int = 5) -> Plan:
    mensaje = f"Tema: {tema}\nNivel del estudiante: {nivel}\nCantidad de subtemas: {num_subtemas}"
    return preguntar(SISTEMA, mensaje, Plan)
