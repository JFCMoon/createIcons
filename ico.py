from PIL import Image, ImageDraw, ImageFont
import os


#convertir texto a icono.ico
def crear_icono_desde_texto(texto, nombre_archivo_ico="icono_texto.ico", tamano_base=(256, 256), color_fondo=(0, 0, 0, 0), color_texto=(255, 255, 255, 255)):
    print(nombre_archivo_ico)
   
    """
    Crea un archivo .ico a partir de un texto dado.

    Args:
        texto (str): El texto que se mostrará en el icono.
        nombre_archivo_ico (str): El nombre del archivo .ico de salida.
        tamano_base (tuple): El tamaño base de la imagen (ancho, alto) en píxeles.
                              Se recomienda 256x256 para una buena calidad.
        color_fondo (tuple): Color de fondo de la imagen (R, G, B, A).
                             (0, 0, 0, 0) es transparente.
        color_texto (tuple): Color del texto (R, G, B, A).

    """
    try:
        # Intenta cargar una fuente TrueType. Si no se encuentra, usa la fuente por defecto de Pillow.
        # Puedes especificar la ruta a una fuente .ttf en tu sistema.
        # Por ejemplo: font_path = "C:/Windows/Fonts/arial.ttf"
        # O para Linux: font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_path = "sans serif" # Deja en None para usar la fuente por defecto de Pillow
        try:
            # Prueba con una fuente común si existe
            if os.name == 'nt': # Windows
                font_path = "C:/Windows/Fonts/segoeui.ttf" # Una fuente común de Windows 11
            elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"): # Linux
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            elif os.path.exists("/System/Library/Fonts/SFCompactText-Regular.otf"): # macOS
                font_path = "/System/Library/Fonts/SFCompactText-Regular.otf"

            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size=80) # Tamaño inicial de la fuente
            else:
                print("Advertencia: No se encontró una fuente TrueType específica. Usando la fuente por defecto de Pillow.")
                font = ImageFont.load_default()
        except IOError:
            print("Advertencia: Error al cargar la fuente TrueType. Usando la fuente por defecto de Pillow.")
            font = ImageFont.load_default()


        # Crear una imagen con fondo transparente
        img = Image.new('RGBA', tamano_base, color_fondo)
        draw = ImageDraw.Draw(img)

        # Ajustar el tamaño de la fuente para que el texto quepa
        font_size = 1
        while True:
            if font_path:
                font = ImageFont.truetype(font_path, size=font_size)
            else:
                font = ImageFont.load_default(size=font_size)

            bbox = draw.textbbox((0, 0), texto, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width < tamano_base[0] * 0.9 and text_height < tamano_base[1] * 0.9:
                font_size += 1
            else:
                font_size -= 1
                if font_path:
                    font = ImageFont.truetype(font_path, size=font_size)
                else:
                    font = ImageFont.load_default(size=font_size)
                break

        # Calcular la posición para centrar el texto
        bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (tamano_base[0] - text_width) / 2
        y = (tamano_base[1] - text_height) / 2 - bbox[1] # Ajuste para el offset del bbox

        # Dibujar el texto
        draw.text((x, y), texto, font=font, fill=color_texto)

        # Tamaños comunes para iconos de Windows (en orden descendente para mejor calidad)
        # Pillow puede generar un .ico con múltiples tamaños automáticamente.
        # Los tamaños más comunes son 256x256, 48x48, 32x32, 16x16.
        # Al guardar, Pillow intentará generar estos tamaños a partir de la imagen base.
        img.save(nombre_archivo_ico, sizes=[(256, 256), (48, 48), (32, 32), (16, 16)])

        print(f"Icono '{nombre_archivo_ico}' creado exitosamente.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
#convertir .png a .ico
def convertir_png_a_ico(ruta_png, ruta_ico_salida, tamanos_ico=None):
    """
    Convierte una imagen PNG a formato ICO usando Pillow.

    Args:
        ruta_png (str): La ruta completa al archivo PNG de entrada.
        ruta_ico_salida (str): La ruta completa donde se guardará el archivo ICO de salida.
        tamanos_ico (list, optional): Una lista de tuplas (ancho, alto) para los tamaños
                                     que se incluirán en el archivo ICO.
                                     Si es None, se usarán tamaños comunes para Windows:
                                     [(256, 256), (48, 48), (32, 32), (16, 16)].
    Returns:
        bool: True si la conversión fue exitosa, False en caso contrario.
    """
    try:
        # Abre la imagen PNG
        img = Image.open(ruta_png)

        # Asegúrate de que la imagen tenga un canal alfa para transparencia
        # Si la imagen es RGB, convertirla a RGBA
        if img.mode == 'RGB':
            img = img.convert('RGBA')

        # Define los tamaños por defecto si no se especifican
        if tamanos_ico is None:
            tamanos_ico = [(256, 256), (48, 48), (32, 32), (16, 16)]

        # Guarda la imagen como ICO, incluyendo los diferentes tamaños
        img.save(ruta_ico_salida, sizes=tamanos_ico)

        print(f"'{ruta_png}' convertido exitosamente a '{ruta_ico_salida}'.")
        return True

    except FileNotFoundError:
        print(f"Error: El archivo PNG no se encontró en la ruta: '{ruta_png}'.")
        return False
    except Exception as e:
        print(f"Ocurrió un error al convertir '{ruta_png}' a ICO: {e}")
        return False

# --- EJEMPLOS DE USO ---

# Ejemplo 1: Icono simple con texto "PY"
# crear_icono_desde_texto("PY", "icono_py.ico", color_fondo=(0, 0, 0, 0), color_texto=(255, 255, 0, 255))

# Ejemplo 2: Icono con texto "DEV" y fondo azul
# crear_icono_desde_texto("DEV", "icono_dev.ico", color_fondo=(30, 144, 255, 255), color_texto=(255, 255, 255, 255))

# Ejemplo 3: Icono para "Cursos de Programación" (puede que necesite un tamaño de fuente más pequeño o una imagen base más grande)
# Para texto más largo, considera usar un tamaño de base más grande o un texto más corto.
# crear_icono_desde_texto("Cursos\nProg.", "icono_cursos_prog.ico", tamano_base=(512, 512), color_fondo=(0, 0, 0, 0), color_texto=(0, 200, 0, 255))

# Ejemplo 4: Icono con un símbolo de corchetes
# crear_icono_desde_texto("{ }", "icono_brackets.ico", color_fondo=(0, 0, 0, 0), color_texto=(135, 206, 250, 255))
#icono latex
crear_icono_desde_texto("TeX", "LaTeX.ico", color_fondo=(0, 0, 0, 0), color_texto=(255, 226, 250, 255))
