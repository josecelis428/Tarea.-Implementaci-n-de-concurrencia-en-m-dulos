import threading
import time
import random
from queue import Queue


tamaño_buffer = 5

buffer = Queue(maxsize=tamaño_buffer)

espacios = threading.Semaphore(tamaño_buffer)
datos = threading.Semaphore(0)

mutex = threading.Lock()


def productor(nombre, tipo):

    for i in range(8):

        if tipo == "vehiculos":
            cantidad = random.randint(5, 50)
            informacion = f"Vehiculos detectados: {cantidad}"

        elif tipo == "semaforo":
            estado = random.choice(["VERDE", "AMARILLO", "ROJO"])
            informacion = f"Semaforo: {estado}"

        elif tipo == "velocidad":
            velocidad = random.randint(20, 80)
            informacion = f"Velocidad: {velocidad} km/h"

        espacios.acquire()

        with mutex:
            buffer.put((nombre, informacion))
            print(f"[PRODUCTOR] {nombre}: {informacion}")

        datos.release()

        time.sleep(random.uniform(0.5, 1.5))


def consumidor(nombre):

    for i in range(12):

        datos.acquire()

        with mutex:
            sensor, informacion = buffer.get()

            print(
                f"[CONSUMIDOR] {nombre} esta procesando: "
                f"{sensor} - {informacion}"
            )

        espacios.release()

        time.sleep(random.uniform(0.8, 1.5))


sensor_vehiculos = threading.Thread(
    target=productor,
    args=("Sensor de vehiculos", "vehiculos")
)

sensor_semaforo = threading.Thread(
    target=productor,
    args=("Sensor de semaforos", "semaforo")
)

sensor_velocidad = threading.Thread(
    target=productor,
    args=("Sensor de velocidad", "velocidad")
)


analizador = threading.Thread(
    target=consumidor,
    args=("Analizador de trafico",)
)

detector = threading.Thread(
    target=consumidor,
    args=("Detector de congestion",)
)


print("\n===== SIGET =====")
print("Iniciando simulacion...\n")


sensor_vehiculos.start()
sensor_semaforo.start()
sensor_velocidad.start()

analizador.start()
detector.start()


sensor_vehiculos.join()
sensor_semaforo.join()
sensor_velocidad.join()

analizador.join()
detector.join()


print("\n===== SIMULACION TERMINADA =====")
print("Todos los datos fueron procesados.")
