# Planificador de estudio multiagente

Un ecosistema sencillo de tres agentes de IA (cada uno usa **Google Gemini**, con su plan gratuito) que trabajan en cadena:

| Agente | Archivo | Qué hace |
|---|---|---|
| **Planificador** | `app/agentes/planificador.py` | Divide un tema en subtemas ordenados de lo básico a lo avanzado |
| **Tutor** | `app/agentes/tutor.py` | Para un subtema, escribe la explicación, los puntos clave y preguntas de práctica |
| **Evaluador** | `app/agentes/evaluador.py` | Corrige tus respuestas, da puntaje y te dice qué repasar |

```
tema ──► Planificador ──► subtemas ──► Tutor ──► material + preguntas ──► (tú respondes) ──► Evaluador ──► puntaje
```

Cada agente es una función de Python con su propio *prompt de sistema* (sus instrucciones). Todos comparten `app/llm.py`,
que llama a Gemini y obliga a que la respuesta tenga un formato fijo (definido en `app/esquemas.py`).
`app/main.py` los expone como una API web con FastAPI.

## Estructura

```
planificador-estudio/
├── app/
│   ├── main.py            # API (FastAPI)
│   ├── llm.py             # conexión con Gemini (compartida)
│   ├── esquemas.py        # formatos de datos
│   ├── static/index.html  # interfaz web
│   └── agentes/           # los tres agentes
├── scripts/
│   ├── sesion_estudio.py  # sesión completa en la terminal
│   └── probar_agente.py   # ejecutar un solo agente
├── .vscode/               # depuración, tareas y extensiones
├── pruebas.http           # peticiones de ejemplo (REST Client)
├── Dockerfile             # para desplegar en la nube
└── render.yaml            # despliegue en Render con un clic
```

## 1. Requisitos

- Python 3.10 o superior
- Una clave gratuita de Google Gemini (ver el paso 2)
- Visual Studio Code (opcional, recomendado)

## 2. Conseguir tu clave gratuita de Gemini

Una "clave de API" es como una contraseña que le dice a Google que las peticiones vienen de ti.
El plan gratuito no pide tarjeta de crédito; solo tiene un límite de peticiones por minuto y por día,
de sobra para estudiar.

1. Entra a https://aistudio.google.com/apikey e inicia sesión con tu cuenta de Google.
2. Acepta los términos si te los pide.
3. Pulsa **Create API key** (Crear clave de API). Si te pregunta por un proyecto, deja el que viene por defecto.
4. Copia la clave que aparece (es un texto largo que empieza con `AIza...`).

Ahora guárdala en el proyecto. En VS Code, en el explorador de archivos de la izquierda:

1. Haz clic derecho en `.env.example` → **Copiar**, luego clic derecho en un espacio vacío → **Pegar**.
2. Renombra la copia a `.env` (exactamente así, con el punto al inicio).
3. Ábrela y reemplaza `pega-aqui-tu-clave` por tu clave. Guarda con `Ctrl+S`.

O desde la terminal:

```powershell
Copy-Item .env.example .env; notepad .env
```

`.env` está en `.gitignore`, así que tu clave nunca se sube al repositorio. No la compartas con nadie.

## 3. Correrlo localmente

### Desde Visual Studio Code

1. Abre la carpeta: `code planificador-estudio`. Acepta instalar las **extensiones recomendadas**.
2. `Ctrl+Shift+P` → **Tasks: Run Task** → *Crear entorno e instalar dependencias* (solo la primera vez).
3. `Ctrl+Shift+P` → **Python: Select Interpreter** → elige `.venv`.
4. Ve a **Ejecutar y depurar** (`Ctrl+Shift+D`) y elige una configuración:
   - **API (FastAPI con recarga)**: levanta la API en http://localhost:8000/docs
   - **Sesión de estudio completa**: los tres agentes en la terminal, te pide un tema
   - **Agente: planificador / tutor / evaluador**: prueba un agente por separado
5. Pon *breakpoints* en cualquier agente y presiona `F5` para depurarlo paso a paso.
6. Con la API corriendo, abre `pruebas.http` y haz clic en **Send Request** sobre cada petición.

### Desde la terminal

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
```

```powershell
.venv\Scripts\python -m uvicorn app.main:app --reload
```

Abre **http://localhost:8000** para usar la interfaz web (te guía paso a paso: tema → plan → estudiar → nota).
La página técnica de la API está en http://localhost:8000/docs. Otras opciones:

```powershell
.venv\Scripts\python -m scripts.sesion_estudio "Fotosíntesis"
```

```powershell
.venv\Scripts\python -m scripts.probar_agente tutor "Fotosíntesis" "La fase luminosa"
```

## 4. Endpoints de la API

| Método | Ruta | Agente | Cuerpo de ejemplo |
|---|---|---|---|
| GET | `/` | — | Interfaz web para estudiar |
| GET | `/salud` | — | Comprueba que la API está viva |
| POST | `/planificar` | Planificador | `{"tema": "Fotosíntesis", "nivel": "principiante", "num_subtemas": 5}` |
| POST | `/material` | Tutor | `{"tema": "Fotosíntesis", "subtema": "La fase luminosa", "num_preguntas": 3}` |
| POST | `/evaluar` | Evaluador | `{"material": <respuesta de /material>, "respuestas": [{"id": 1, "respuesta": "..."}]}` |

## 5. Desplegar en la nube

La app se empaqueta con el `Dockerfile`, así que funciona igual en cualquier servicio que corra contenedores.
En todos los casos la clave va en las **variables de entorno del servicio**, nunca en el código.

Primero sube la carpeta a un repositorio de GitHub (el `.env` no se sube):

```powershell
git init; git add .; git commit -m "Planificador de estudio"
```

### Opción A: Render (la más simple, tiene plan gratis)

1. En https://render.com → **New** → **Blueprint** → elige tu repositorio. Render lee `render.yaml`.
2. Cuando te lo pida, pega tu `GEMINI_API_KEY`.
3. Al terminar tendrás una URL como `https://planificador-estudio.onrender.com/docs`.

### Opción B: Railway

1. En https://railway.app → **New Project** → **Deploy from GitHub repo**. Detecta el `Dockerfile`.
2. En **Variables** agrega `GEMINI_API_KEY`.
3. En **Settings → Networking** pulsa **Generate Domain**.

### Opción C: Google Cloud Run

Con la [CLI de gcloud](https://cloud.google.com/sdk/docs/install) instalada y un proyecto creado:

```powershell
gcloud run deploy planificador-estudio --source . --region us-central1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=TU_CLAVE
```

(Para algo más seguro, guarda la clave en Secret Manager y usa `--set-secrets`.)

## 6. Personalizar

- **Cambiar el comportamiento de un agente:** edita la constante `SISTEMA` en su archivo.
- **Cambiar el modelo:** variable `GEMINI_MODEL` en `.env` (por defecto `gemini-3.5-flash`;
  si está saturado, la app prueba sola otros modelos Flash gratuitos).
- **Si ves "límite gratuito":** espera un minuto; el plan gratis permite pocas peticiones por minuto.
- **Agregar un agente nuevo:** crea un archivo en `app/agentes/`, define su formato en `esquemas.py`,
  llama a `preguntar(...)` y expón un endpoint en `main.py`.

> Nota: la API no tiene autenticación ni guarda datos; es un punto de partida. Si la dejas pública
> en internet, cualquiera con la URL puede gastar tu cuota gratuita de Gemini.
