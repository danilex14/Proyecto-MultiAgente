"""Modelos de datos que se intercambian entre la API y los agentes."""
from pydantic import BaseModel, Field


# ---------- Agente planificador ----------
class Subtema(BaseModel):
    titulo: str
    descripcion: str
    orden: int


class Plan(BaseModel):
    tema: str
    objetivo: str
    subtemas: list[Subtema]


# ---------- Agente tutor ----------
class Pregunta(BaseModel):
    id: int
    enunciado: str
    respuesta_esperada: str = Field(description="Respuesta modelo para el evaluador")


class Material(BaseModel):
    subtema: str
    explicacion: str = Field(description="Explicación clara en Markdown")
    puntos_clave: list[str]
    preguntas: list[Pregunta]


# ---------- Agente evaluador ----------
class EvaluacionPregunta(BaseModel):
    id: int
    correcta: bool
    puntaje: int = Field(description="0 a 10")
    retroalimentacion: str


class Evaluacion(BaseModel):
    resultados: list[EvaluacionPregunta]
    puntaje_total: int = Field(description="0 a 100")
    recomendacion: str


# ---------- Peticiones de la API ----------
class PeticionPlan(BaseModel):
    tema: str
    nivel: str = "principiante"
    num_subtemas: int = Field(default=5, ge=2, le=10)


class PeticionMaterial(BaseModel):
    tema: str
    subtema: str
    nivel: str = "principiante"
    num_preguntas: int = Field(default=3, ge=1, le=10)


class RespuestaUsuario(BaseModel):
    id: int
    respuesta: str


class PeticionEvaluacion(BaseModel):
    material: Material
    respuestas: list[RespuestaUsuario]
