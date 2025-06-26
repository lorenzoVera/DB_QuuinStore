import schedule
import time
import subprocess
import sys
import os

# --- Configuración del Planificador ---
T = 1  # Define la frecuencia de ejecución del ETL en minutos

def run_etl_job():
    print(f"\n--- Ejecutando el proceso ETL en: {time.ctime()} ---")
    # Ruta al intérprete de Python
    python_executable = sys.executable
    # Ruta al script main.py
    script_path = os.path.join(os.path.dirname(__file__), 'main.py')

    try:
        result = subprocess.run(
            [python_executable, script_path],
            capture_output=True,
            text=True,
            check=True # Lanza CalledProcessError si el comando retorna un código de error
        )
        print("Salida del ETL:")
        print(result.stdout)
        if result.stderr:
            print("Errores del ETL (stderr):")
            print(result.stderr)
        print(f"--- Proceso ETL completado exitosamente en: {time.ctime()} ---")

    except subprocess.CalledProcessError as e:
        print(f"--- ERROR: El proceso ETL falló en: {time.ctime()} ---")
        print(f"Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except FileNotFoundError:
        print(f"--- ERROR: No se encontró el intérprete de Python o main.py en {script_path}. Asegúrate de que las rutas sean correctas. ---")
    except Exception as e:
        print(f"--- ERROR Inesperado durante la ejecución del ETL: {e} en {time.ctime()} ---")


if __name__ == "__main__":
    print("Iniciando el planificador de ETL...")
    print(f"El proceso ETL se ejecutará cada {T} minuto(s).")
    print("Presiona Ctrl+C para detener el planificador.")

    # Programa la tarea para que se ejecute cada 'INTERVAL_MINUTES' minutos
    schedule.every(T).minutes.do(run_etl_job)

    # Bucle principal que ejecuta las tareas programadas
    while True:
        schedule.run_pending()
        time.sleep(1) # Pausa por 1 segundo
