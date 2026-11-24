"""API del planificador de estudio. Orquesta los tres agentes."""
from fastapi import FastAPI, HTTPException

from app.agentes.evaluador import evaluar
from app.agentes.planificador import planificar
from app.agentes.tutor import generar_material
from app.esquemas import Evaluacion, Material, PeticionEvaluacion, PeticionMaterial, PeticionPlan, Plan
from app.llm import ErrorAgente

app = FastAPI(title="Planificador de estudio multiagente")


def _ejecutar(funcion, *args):
    try:
        return funcion(*args)
    except ErrorAgente as e:
        raise HTTPException(status_code=e.codigo, detail=str(e))


@app.get("/")
def salud():
    return {"estado": "ok", "docs": "/docs"}


@app.post("/planificar", response_model=Plan)
def endpoint_planificar(p: PeticionPlan):
    """Agente planificador: tema -> subtemas."""
    return _ejecutar(planificar, p.tema, p.nivel, p.num_subtemas)


@app.post("/material", response_model=Material)
def endpoint_material(p: PeticionMaterial):
    """Agente tutor: subtema -> explicación + preguntas."""
    return _ejecutar(generar_material, p.tema, p.subtema, p.nivel, p.num_preguntas)


@app.post("/evaluar", response_model=Evaluacion)
def endpoint_evaluar(p: PeticionEvaluacion):
    """Agente evaluador: preguntas + respuestas -> puntaje y retroalimentación."""
    return _ejecutar(evaluar, p.material, p.respuestas)
