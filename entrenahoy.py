import streamlit as st
import random
import time
import io
import pandas as pd



# Ocultar elementos predeterminados y ajustar estilos
hide_st_style = """
    <style>
    /* Ocultar el menú principal, el pie de página y el encabezado */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Configurar el fondo en negro y eliminar márgenes */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        background-color: #000000;
    }

    body {
        background-color: #000000;
        color: white;
    }

    .stApp {
        margin: 0;
        padding: 0;
    }

    /* Asegurar que el contenido ocupe toda la altura */
    .main .block-container {
        max-width: 100%;
        padding-top: 0;
        padding-bottom: 0;
        height: 100vh;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Estilos personalizados para los botones
button_style = """
    <style>
    div.stButton > button {
        width: 100%;
        height: 100px;
        font-size: 24px;
        padding: 0px;
        background-color: #f9d90a;  /* Color de fondo verde */
        color: #000000; /* Texto en blanco */
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #ffffff;  /* Color más oscuro al pasar el mouse */
    }
    </style>
    """
st.markdown(button_style, unsafe_allow_html=True)

def clear_page():
    """Limpia el contenido de la página actual"""
    st.empty()
    
def load_data(pagina):
    try:
        sheet_id = '1bSlKMIBnXdI0R8JrYxzp622HuwYp2Q7xc2Fz3apnHlw'
        df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={pagina}')
        # Guardar en caché local
        df.to_csv('local_cache.csv', index=False)
        return df
    except Exception as e:
        st.warning("No se pudo cargar datos de Google Sheets. Intentando cargar desde caché local.")
        try:
            return pd.read_csv('local_cache.csv')
        except FileNotFoundError:
            st.error("No se pudo cargar datos. Por favor, verifica tu conexión a internet.")
            return pd.DataFrame()

df = load_data('ejercicios')

def crear_ejercicios_rutina(ejercicios_seleccionados, duracion):
    rutina = []
    for _, ejercicio in ejercicios_seleccionados.iterrows():
        if duracion == "Ambos aleatorios":
            tiempo = random.choice([30, 40])
        else:
            tiempo = int(duracion.split()[0])
        
        rutina.append((
            ejercicio['Categoría'],
            f"{ejercicio['Icono Unicode']} {ejercicio['Ejercicio']}",
            tiempo,
            ejercicio['Descripción']
        ))
    return rutina

def mostrar_link():
    links=load_data('links')
    random_row = links.sample(n=1).iloc[0]
    # Mostrar el comentario y propietario
    
    # Mostrar el video en Streamlit
    video_link = random_row['link']
    st.video(video_link)
    st.title(f"{random_row['comentario']} - ({random_row['propietario']})")
    # Mostrar el link para abrir en otra ventana
    st.markdown(f"[Abrir video en otra ventana]({video_link})")

def mostrar_banner():
    banners = ["entrena.png"]  # Agrega todos tus banners aquí
    # Selecciona un banner al azar
    banner_aleatorio = random.choice(banners)
    # Muestra el banner al azar
    st.image(banner_aleatorio, use_column_width=True)

def mostrar_logo():
    if 'logo_mostrado' not in st.session_state:
        st.session_state.logo_mostrado = False

    if not st.session_state.logo_mostrado:
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.image('logo.jpg')
            st.session_state.logo_mostrado = True

def generar_rutina_con_config(tipo_rutina, duracion=None, tiempo_descanso=None, vueltas=None, musculo=None):
    # Usar valores predeterminados si no se proporcionan
    tipo_rutina = tipo_rutina or "Rápida"
    duracion = duracion or "30 segundos"
    tiempo_descanso = tiempo_descanso or 10
    vueltas = vueltas or 3

    with st.spinner("Generando rutina personalizada..."):
        time.sleep(2)  # Espera 2 segundos
        st.session_state.rutina = generar_rutina(tipo_rutina, duracion, tiempo_descanso, vueltas, musculo)
        st.session_state.duracion = duracion
        st.session_state.tiempo_descanso = tiempo_descanso
        st.session_state.vueltas = vueltas
        st.session_state.rutina_generada = True
    st.success("¡Rutina generada con éxito!")
    st.rerun()
    
def generar_rutina(tipo_rutina, duracion, tiempo_descanso, vueltas, musculo=None):
    load_data
    rutina_base = []
    
    if tipo_rutina == "Rápida":
        categorias = df['Categoría'].unique()
        for categoria in categorias:
            ejercicios_categoria = df[df['Categoría'] == categoria]
            ejercicios_seleccionados = ejercicios_categoria.sample(n=2)
            rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, duracion))
    
    elif tipo_rutina == "HIIT":
        ejercicios_hiit = df[(df['Categoría'] == 'Aeróbico') & (df['Nivel'] == 'Avanzado')]
        ejercicios_seleccionados = ejercicios_hiit.sample(n=min(8, len(ejercicios_hiit)))
        rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, duracion))
    
    elif tipo_rutina == "Músculo":
        ejercicios_musculo = df[df['Grupo Muscular'].str.contains(musculo, na=False)]
        ejercicios_seleccionados = ejercicios_musculo.sample(n=min(8, len(ejercicios_musculo)))
        rutina_base.extend(crear_ejercicios_rutina(ejercicios_seleccionados, duracion))
    
    rutina_completa = []
    for vuelta in range(1, vueltas + 1):
        for i, ejercicio in enumerate(rutina_base, 1):
            categoria, nombre_ejercicio, tiempo, instruccion = ejercicio
            rutina_completa.append((categoria, nombre_ejercicio, tiempo, instruccion, vuelta, i, len(rutina_base)))
            if i < len(rutina_base):
                rutina_completa.append(("Descanso", "Descanso entre ejercicios", tiempo_descanso, "Toma un breve descanso antes del siguiente ejercicio", vuelta, None, None))
        if vuelta < vueltas:
            rutina_completa.append(("Descanso", "Descanso entre vueltas", tiempo_descanso * 5, "Toma un descanso más largo antes de la siguiente vuelta", vuelta, None, None))
    
    return rutina_completa

def mostrar_rutina(rutina):
    st.title("🏋️ Fitness - Rutina Personalizada")
    vuelta_actual = 1
    for grupo, ejercicio, duracion, instruccion, vuelta, num_ejercicio, total_ejercicios in rutina:
        if vuelta != vuelta_actual:
            st.write("---")
            st.write(f"Vuelta {vuelta}")
            vuelta_actual = vuelta
        if grupo == "Descanso":
            if ejercicio == "Descanso entre vueltas":
                st.write(f"Descanso entre vueltas: {duracion} segundos")
            else:
                st.write(f"Descanso: {duracion} segundos")
        else:
            st.write(f"Ejercicio {num_ejercicio}/{total_ejercicios}: {grupo} - {ejercicio}: {duracion} segundos")
            st.write(f"Instrucción: {instruccion}")

def temporizador(rutina):
    #st.title("🏋️ FITNESS - A entrenar !")
    st.image("entrena2.png", use_column_width=True)
    if 'ejercicio_actual' not in st.session_state:
        st.session_state.ejercicio_actual = 0
        st.session_state.tiempo_restante = rutina[0][2]
    
    grupo, ejercicio, duracion, instruccion, vuelta, num_ejercicio, total_ejercicios = rutina[st.session_state.ejercicio_actual]
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        #if grupo != "Descanso":
            #st.markdown(f"<h3 style='text-align: center;'>Vuelta {vuelta}/{st.session_state.vueltas} - Ejercicio {num_ejercicio}/{total_ejercicios}</h3>", unsafe_allow_html=True)
        
        if grupo == "Descanso":
            if ejercicio == "Descanso entre vueltas":
                st.markdown(f"<h3 style='text-align: center;'>Vuelta {vuelta}/{st.session_state.vueltas} - Ejercicio {num_ejercicio}/{total_ejercicios}</h3>", unsafe_allow_html=True)
                st.markdown("<h1 style='text-align: center;'>Descanso entre vueltas</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='text-align: center;'>Descanso</h1>", unsafe_allow_html=True)
            # Mostrar el próximo ejercicio
            proximo_indice = st.session_state.ejercicio_actual + 1
            if proximo_indice < len(rutina):
                proximo_ejercicio = rutina[proximo_indice][1]
                st.markdown(f"<h3 style='text-align: center;'>Próximo ejercicio: {proximo_ejercicio}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center;'>{grupo}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>{ejercicio}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{instruccion}</p>", unsafe_allow_html=True)
        
        progress = st.progress(0)
        tiempo_texto = st.empty()
        
        if st.button("Pausar/Reanudar", key="pausar_reanudar"):
            st.session_state.timer_running = not st.session_state.timer_running
    
    if st.session_state.timer_running:
        progress.progress(1 - st.session_state.tiempo_restante / duracion)
        tiempo_texto.markdown(f"<h3 style='text-align: center;'>{st.session_state.tiempo_restante} segundos</h3>", unsafe_allow_html=True)
        time.sleep(1)
        st.session_state.tiempo_restante -= 1
        
        if st.session_state.tiempo_restante < 0:
            st.session_state.ejercicio_actual += 1
            if st.session_state.ejercicio_actual < len(rutina):
                st.session_state.tiempo_restante = rutina[st.session_state.ejercicio_actual][2]
            else:
                st.success("¡Felicidades! Has completado tu rutina.")
                if st.button("Volver al inicio", key="volver_inicio"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
                return
        
        st.rerun()

def spotify_link(text, url):
    return st.markdown(f"🎵 [{text}]({url})")

def generar_rutina_interface():
    # df = load_data('ejercicios')  # Ya se ha movido al inicio del script

    if 'rutina_generada' not in st.session_state:
        st.session_state.rutina_generada = False

    if 'mostrar_config' not in st.session_state:
        st.session_state.mostrar_config = False

    if not st.session_state.rutina_generada:
        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button("Rutina Rápida", key="rutina_rapida"):
                generar_rutina_con_config(tipo_rutina="Rápida", duracion="40 segundos", tiempo_descanso=10, vueltas=3)

        with col2:
            if st.button("⚙️", key="configuracion"):
                st.session_state.mostrar_config = not st.session_state.mostrar_config

        if st.session_state.mostrar_config:
            with st.expander("Configuración", expanded=True):
                st.title("PROXIMAMENTE ...")
                pass

    else:
        if 'timer_running' not in st.session_state:
            st.image("entrena3.png", use_column_width=True)
            if st.button("Comenzar Rutina", key="comenzar_rutina"):
                st.session_state.timer_running = True
                st.session_state.ejercicio_actual = 0
                st.session_state.tiempo_restante = st.session_state.rutina[0][2]
                st.rerun()

            st.title("Poné Musica ... ")
            st.image("spotify.png", width=200)
            st.markdown("La música se abrirá en la aplicación, debes volver para hacer clic en COMENZAR RUTINA")
            spotify_playlist_url1 = "https://open.spotify.com/intl-es/track/7BExBy99xIVD7moauE290a?si=5d08e19cd3fd4cd2"
            spotify_link("Lista de reproducción Inglés", spotify_playlist_url1)

            spotify_playlist_url2 = "https://open.spotify.com/intl-es/track/1hWpzhGIPOQ7gKz3ut5eVs?si=f3891cf314774ac0"
            spotify_link("Lista de reproducción Latino", spotify_playlist_url2)

        else:
            temporizador(st.session_state.rutina)

        if st.button("Generar nueva rutina"):
            st.session_state.rutina_generada = False
            st.session_state.timer_running = False
            if 'rutina' in st.session_state:
                del st.session_state.rutina
            st.rerun()

def main():
    # Crear un menú lateral para seleccionar el tema

    # Mostrar el banner
    mostrar_logo()

    # Inicializar estado si no existe
    if 'selected_action' not in st.session_state:
        st.session_state.selected_action = None

    # Lógica para manejar el clic del botón y actualización inmediata del estado
    if st.session_state.selected_action is None:
        if st.button("Entrenar por link de YouTube"):
            st.session_state.selected_action = "mostrar_link"
            st.rerun()  # Forzar la recarga inmediata para ejecutar la función seleccionada

        if st.button("Generar rutina de entrenamiento"):
            st.session_state.selected_action = "generar_rutina"
            st.rerun()  # Forzar la recarga inmediata para ejecutar la función seleccionada

    # Ejecutar la función seleccionada
    if st.session_state.selected_action == "mostrar_link":
        clear_page()
        mostrar_link()

    elif st.session_state.selected_action == "generar_rutina":
        clear_page()
        generar_rutina_interface()

if __name__ == "__main__":
    main()
