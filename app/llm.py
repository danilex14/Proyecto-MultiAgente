"""Cliente compartido de Gemini (Google) para todos los agentes."""
import os
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, ValidationError

load_dotenv()  # lee GEMINI_API_KEY desde .env en local

# Modelo principal (plan gratuito). Si está saturado o ya no existe, se prueban los de respaldo.
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
RESPALDOS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite"]
_cliente: genai.Client | None = None
T = TypeVar("T", bound=BaseModel)


class ErrorAgente(Exception):
    """Error con un mensaje claro para mostrar al usuario."""

    def __init__(self, mensaje: str, codigo: int = 503):
        super().__init__(mensaje)
        self.codigo = codigo


def cliente() -> genai.Client:
    global _cliente
    if _cliente is None:
        clave = os.getenv("GEMINI_API_KEY")
        if not clave:
            raise ErrorAgente("Falta GEMINI_API_KEY: créala en .env (local) o en el panel de tu nube.")
        _cliente = genai.Client(api_key=clave)
    return _cliente


def preguntar(sistema: str, mensaje: str, formato: type[T]) -> T:
    """Llama a Gemini y devuelve la respuesta validada contra el modelo `formato`."""
    config = types.GenerateContentConfig(
        system_instruction=sistema,
        response_mime_type="application/json",
        response_schema=formato,
    )
    modelos = list(dict.fromkeys([MODELO, *RESPALDOS]))  # sin repetidos, el principal primero
    respuesta = None
    for modelo in modelos:
        try:
            respuesta = cliente().models.generate_content(model=modelo, contents=mensaje, config=config)
            break
        except errors.ClientError as e:
            if e.code == 429:
                raise ErrorAgente("Llegaste al límite gratuito de Gemini; espera un minuto y reintenta.", 429)
            if e.code in (400, 401, 403) and "API key" in str(e):
                raise ErrorAgente("La GEMINI_API_KEY no es válida. Revisa tu archivo .env.", 401)
            if e.code != 404:  # 404 = modelo inexistente: probamos el siguiente
                raise ErrorAgente(f"Gemini rechazó la petición: {e}", 502)
        except errors.ServerError:
            pass  # modelo saturado (503): probamos el siguiente
    if respuesta is None:
        raise ErrorAgente("Gemini está saturado ahora mismo; reintenta en un minuto.", 503)

    if isinstance(respuesta.parsed, formato):
        return respuesta.parsed
    try:
        return formato.model_validate_json(respuesta.text or "")
    except ValidationError:
        raise ErrorAgente("Gemini devolvió una respuesta con un formato inesperado; reintenta.", 502)
