"""Sesión de estudio interactiva en la terminal: usa los tres agentes en cadena.

Uso:  python -m scripts.sesion_estudio "Fotosíntesis"
"""
import sys

from app.agentes.evaluador import evaluar
from app.agentes.planificador import planificar
from app.agentes.tutor import generar_material
from app.esquemas import RespuestaUsuario
from app.llm import ErrorAgente


def main() -> None:
    tema = " ".join(sys.argv[1:]) or input("¿Qué tema quieres estudiar? ")
    print("\n[Planificador] creando plan...")
    plan = planificar(tema)
    print(f"\nObjetivo: {plan.objetivo}")
    for s in plan.subtemas:
        print(f"  {s.orden}. {s.titulo} - {s.descripcion}")

    eleccion = input("\nNúmero del subtema a estudiar (Enter = 1): ").strip() or "1"
    subtema = next((s for s in plan.subtemas if str(s.orden) == eleccion), plan.subtemas[0])

    print(f"\n[Tutor] preparando material de '{subtema.titulo}'...")
    material = generar_material(tema, subtema.titulo)
    print("\n" + material.explicacion)
    print("\nPuntos clave:")
    for p in material.puntos_clave:
        print(f"  * {p}")

    respuestas = []
    for pregunta in material.preguntas:
        r = input(f"\nPregunta {pregunta.id}: {pregunta.enunciado}\n> ")
        respuestas.append(RespuestaUsuario(id=pregunta.id, respuesta=r))

    print("\n[Evaluador] revisando tus respuestas...")
    ev = evaluar(material, respuestas)
    for r in ev.resultados:
        marca = "OK" if r.correcta else "X "
        print(f"  [{marca}] Pregunta {r.id}: {r.puntaje}/10 - {r.retroalimentacion}")
    print(f"\nPuntaje total: {ev.puntaje_total}/100")
    print(f"Recomendación: {ev.recomendacion}")


if __name__ == "__main__":
    try:
        main()
    except ErrorAgente as e:
        sys.exit(f"\nError: {e}")
