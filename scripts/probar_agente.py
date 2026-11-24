"""Ejecuta un solo agente para probarlo o depurarlo.

Uso:
  python -m scripts.probar_agente planificador "Álgebra lineal"
  python -m scripts.probar_agente tutor "Álgebra lineal" "Vectores"
  python -m scripts.probar_agente evaluador      (usa un ejemplo fijo)
"""
import sys

from app.agentes.evaluador import evaluar
from app.agentes.planificador import planificar
from app.agentes.tutor import generar_material
from app.esquemas import Material, Pregunta, RespuestaUsuario
from app.llm import ErrorAgente


def main() -> None:
    agente = sys.argv[1] if len(sys.argv) > 1 else "planificador"
    args = sys.argv[2:]

    if agente == "planificador":
        resultado = planificar(args[0] if args else "Fotosíntesis")
    elif agente == "tutor":
        tema = args[0] if args else "Fotosíntesis"
        subtema = args[1] if len(args) > 1 else "La fase luminosa"
        resultado = generar_material(tema, subtema)
    elif agente == "evaluador":
        material = Material(
            subtema="Capitales de Sudamérica",
            explicacion="",
            puntos_clave=[],
            preguntas=[
                Pregunta(id=1, enunciado="¿Cuál es la capital de Chile?", respuesta_esperada="Santiago"),
                Pregunta(id=2, enunciado="¿Cuál es la capital de Perú?", respuesta_esperada="Lima"),
            ],
        )
        respuestas = [RespuestaUsuario(id=1, respuesta="Santiago"), RespuestaUsuario(id=2, respuesta="Cusco")]
        resultado = evaluar(material, respuestas)
    else:
        sys.exit(f"Agente desconocido: {agente}. Usa planificador, tutor o evaluador.")

    print(resultado.model_dump_json(indent=2))


if __name__ == "__main__":
    try:
        main()
    except ErrorAgente as e:
        sys.exit(f"Error: {e}")
