import random
import io
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from docx import Document
from starlette.responses import StreamingResponse

# --- Configuration ---
SHEET_ID = '1bSlKMIBnXdI0R8JrYxzp622HuwYp2Q7xc2Fz3apnHlw'
LINKS_SHEET_NAME = 'links'
EXERCISES_SHEET_NAME = 'ejercicios'

# --- FastAPI App Initialization ---
app = FastAPI(
    title="FA Fitness API",
    description="API for generating personalized workout routines.",
    version="1.0.0"
)

# --- Data Loading ---
def load_data(sheet_name: str):
    """Loads data from a public Google Sheet."""
    try:
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        df = pd.read_csv(url)
        # Use a local cache for faster development and offline access
        df.to_csv(f'../assets/{sheet_name}_cache.csv', index=False)
        return df
    except Exception:
        # Fallback to local cache if Google Sheets is unavailable
        try:
            return pd.read_csv(f'../assets/{sheet_name}_cache.csv')
        except FileNotFoundError:
            # If cache is also unavailable, return an empty dataframe
            return pd.DataFrame()

# Load data on startup
df_exercises = load_data(EXERCISES_SHEET_NAME)
df_links = load_data(LINKS_SHEET_NAME)

# --- Pydantic Models ---
class RoutineConfig(BaseModel):
    tipo_rutina: str = "Rápida"
    duracion: str = "30 segundos"
    tiempo_descanso: int = 10
    vueltas: int = 3
    musculo: str | None = None

class Exercise(BaseModel):
    group: str
    name: str
    duration: int
    instruction: str

class Routine(BaseModel):
    config: RoutineConfig
    routine: list[Exercise]

# --- Helper Functions ---
def crear_ejercicios_rutina(ejercicios_seleccionados, duracion_str):
    rutina = []
    for _, ejercicio in ejercicios_seleccionados.iterrows():
        if duracion_str == "Ambos aleatorios":
            tiempo = random.choice([30, 40])
        else:
            tiempo = int(duracion_str.split()[0])

        rutina.append({
            "group": ejercicio['Categoría'],
            "name": f"{ejercicio['Icono Unicode']} {ejercicio['Ejercicio']}",
            "duration": tiempo,
            "instruction": ejercicio['Descripción']
        })
    return rutina

def generar_rutina_logic(config: RoutineConfig):
    rutina_base = []

    if config.tipo_rutina == "Rápida":
        categorias = df_exercises['Categoría'].unique()
        for categoria in categorias:
            ejercicios_categoria = df_exercises[df_exercises['Categoría'] == categoria]
            # Ensure we don't sample more than available exercises
            n_samples = min(2, len(ejercicios_categoria))
            if n_samples > 0:
                ejercicios_seleccionados = ejercicios_categoria.sample(n=n_samples)
                rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, config.duracion))

    elif config.tipo_rutina == "HIIT":
        ejercicios_hiit = df_exercises[(df_exercises['Categoría'] == 'Aeróbico') & (df_exercises['Nivel'] == 'Avanzado')]
        n_samples = min(8, len(ejercicios_hiit))
        if n_samples > 0:
            ejercicios_seleccionados = ejercicios_hiit.sample(n=n_samples)
            rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, config.duracion))

    elif config.tipo_rutina == "Músculo" and config.musculo:
        ejercicios_musculo = df_exercises[df_exercises['Grupo Muscular'].str.contains(config.musculo, na=False)]
        n_samples = min(8, len(ejercicios_musculo))
        if n_samples > 0:
            ejercicios_seleccionados = ejercicios_musculo.sample(n=n_samples)
            rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, config.duracion))

    return rutina_base

# --- API Endpoints ---
@app.post("/api/v1/routines", response_model=list[Exercise])
async def create_routine(config: RoutineConfig):
    """
    Generates a workout routine based on the provided configuration.
    """
    return generar_rutina_logic(config)

@app.get("/api/v1/links/random")
async def get_random_link():
    """
    Returns a random workout link from the database.
    """
    if not df_links.empty:
        return df_links.sample(n=1).to_dict('records')[0]
    return {}

@app.post("/api/v1/routines/download")
async def download_routine_as_word(routine: list[Exercise]):
    """
    Takes a routine and returns it as a downloadable Word document.
    """
    doc = Document()
    doc.add_heading('FA Fitness - Tu Rutina Personalizada', 0)

    for i, exercise in enumerate(routine, 1):
        doc.add_paragraph(f"Ejercicio {i}: {exercise['group']} - {exercise['name']} ({exercise['duration']} segundos)")
        doc.add_paragraph(f"Instrucción: {exercise['instruction']}")
        doc.add_paragraph("---")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=FA_FITNESS_Rutina.docx"}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the FA Fitness API!"}
