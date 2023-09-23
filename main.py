import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def normalizar_valores(data):
    max_value = np.max(data)
    if max_value != 0:
        return data / max_value
    else:
        return data

def obtener_amplitud_maxima_en_rango(magnitude_normalized, freqs, frecuencia_objetivo, delta):
    """
    Obtiene la amplitud máxima en un rango de frecuencias de una señal normalizada en el dominio de la frecuencia.

    :param magnitude_normalized: Magnitud normalizada de la señal en el dominio de la frecuencia (transformada de Fourier).
    :param freqs: Array de frecuencias correspondientes a magnitude_normalized.
    :param frecuencia_objetivo: Frecuencia de interés en Hz.
    :param delta: Valor para definir el rango de frecuencias (Hz).
    :return: Amplitud máxima en el rango de frecuencias especificado.
    """
    # Calcular las frecuencias fronteras
    frecuencia_inferior = frecuencia_objetivo - delta
    frecuencia_superior = frecuencia_objetivo + delta

    # Encontrar los índices de las frecuencias dentro del rango
    indices_rango = np.where((freqs >= frecuencia_inferior) & (freqs <= frecuencia_superior))

    # Obtener la magnitud normalizada en el rango de frecuencias
    magnitudes_rango = magnitude_normalized[indices_rango]

    # Encontrar la amplitud máxima en el rango de frecuencias
    amplitud_maxima = np.max(magnitudes_rango)

    return amplitud_maxima

def plot_wav_file_and_fourier(file_path, frecuencia_objetivo, delta, num_armonicos, guardar_imagen=False):
    try:
        # Leer el archivo WAV
        sample_rate, data = wavfile.read(file_path)

        # Obtener la duración del archivo en segundos
        duration = len(data) / sample_rate

        # Crear un array de tiempo para el eje X
        time = np.linspace(0, duration, len(data))

        # Calcular la transformada de Fourier
        fft_data = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(fft_data), 1/sample_rate)

        # Normalizar la magnitud de la transformada de Fourier
        magnitude = np.abs(fft_data)
        magnitude_normalized = normalizar_valores(magnitude)

        # Obtener la amplitud máxima en el rango de frecuencias
        amplitud_maxima = obtener_amplitud_maxima_en_rango(magnitude_normalized, freqs, frecuencia_objetivo, delta)

        # Crear la figura y los subplots
        plt.figure(figsize=(10, 6))

        # Subplot 1: Forma de onda en el dominio del tiempo
        plt.subplot(2, 1, 1)
        plt.plot(time, data)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title("Forma de onda de archivo WAV")
        plt.grid()

        # Subplot 2: Magnitud de la transformada de Fourier normalizada en el dominio de la frecuencia
        plt.subplot(2, 1, 2)
        plt.plot(freqs, magnitude_normalized)
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud Normalizada")
        plt.title("Transformada de Fourier Normalizada")
        plt.grid()
        plt.xlim(0, 5000)  # Establecer el límite en el eje X hasta 5000 Hz

        # Marcador para la frecuencia objetivo
        plt.scatter(frecuencia_objetivo, amplitud_maxima, color='red', marker='o', label=f'Max en {frecuencia_objetivo} Hz')
        plt.legend()

        # Calcular y mostrar armónicos dinámicamente
        for i in range(1, num_armonicos + 1):
            frecuencia_arm = frecuencia_objetivo * i
            amplitud_arm = obtener_amplitud_maxima_en_rango(magnitude_normalized, freqs, frecuencia_arm, delta)
            plt.scatter(frecuencia_arm, amplitud_arm, color='blue', marker='o', label=f'Armónico {i} en {frecuencia_arm} Hz')

        plt.legend()

        plt.tight_layout()

        if guardar_imagen:
            # Guardar la figura en un archivo PNG
            plt.savefig("imagen.png", bbox_inches='tight')

        # Mostrar la figura en pantalla
        plt.show()

        # Mostrar el valor de amplitud máxima en el rango de frecuencias
        print(f"Amplitud máxima en el rango de {frecuencia_objetivo - delta} Hz a {frecuencia_objetivo + delta} Hz: {amplitud_maxima}")

    except Exception as e:
        print("Error al procesar el archivo WAV:", str(e))

# Llamar a la función con la ruta de tu archivo WAV, la frecuencia objetivo, el delta y el número de armónicos
archivo_wav = "archivo.wav"  # Reemplaza con la ruta de tu archivo
frecuencia_objetivo = 263  # Hz (frecuencia central del rango)
delta = 100  # Hz (ancho del rango)
num_armonicos = 13  # Número de armónicos a mostrar
plot_wav_file_and_fourier(archivo_wav, frecuencia_objetivo, delta, num_armonicos, guardar_imagen=True)