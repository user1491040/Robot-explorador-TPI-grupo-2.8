import time
from components import *

print("ROBOT INICIADO")

modo_seguro = False
ultimo_comando = None

US_ACTIVO = True
IR_ACTIVO = True

DISTANCIA_MAX_US = 40
DISTANCIA_DETENER = 8
DISTANCIA_EVASION = 15
DISTANCIA_PREVENTIVA = 30

def leer_distancia_util():

    if not US_ACTIVO:
        return None

    try:

        distancia = detector_us.get_distance()

        if distancia <= 0:
            return None

        if distancia >= DISTANCIA_MAX_US:
            return None

        return distancia

    except:

        return None

def leer_ir():

    if not IR_ACTIVO:
        return False

    try:

        return detector_ir.read()

    except:

        return False

def hay_obstaculo():

    distancia = leer_distancia_util()

    # Si el ultrasonido no detecta nada útil,
    # ignoramos completamente el IR
    if distancia is None:
        return False

    ir_detectado = leer_ir()

    if distancia <= DISTANCIA_DETENER:

        print("OBSTACULO CRITICO:", distancia, "cm")

        return True

    if distancia <= DISTANCIA_EVASION:

        print("OBSTACULO CERCANO:", distancia, "cm")

        return True

    if distancia <= DISTANCIA_PREVENTIVA and ir_detectado:

        print("OBSTACULO CONFIRMADO:", distancia, "cm")

        return True

    return False

def avanzar():

    motor_frontal_izq.set_speed(60)
    motor_trasero_izq.set_speed(60)

    motor_frontal_der.set_speed(-60)
    motor_trasero_der.set_speed(-60)

def retroceder():

    motor_frontal_izq.set_speed(-60)
    motor_trasero_izq.set_speed(-60)

    motor_frontal_der.set_speed(60)
    motor_trasero_der.set_speed(60)

def girar_izquierda():

    motor_frontal_izq.set_speed(-50)
    motor_trasero_izq.set_speed(-50)

    motor_frontal_der.set_speed(-50)
    motor_trasero_der.set_speed(-50)

def girar_derecha():

    motor_frontal_izq.set_speed(50)
    motor_trasero_izq.set_speed(50)

    motor_frontal_der.set_speed(50)
    motor_trasero_der.set_speed(50)

def detener():

    motor_frontal_izq.stop()
    motor_frontal_der.stop()

    motor_trasero_izq.stop()
    motor_trasero_der.stop()

while True:

    command = control.read_command()

    if command is not None:

        # Evita saturar la terminal
        if command != ultimo_comando:

            print("Comando recibido:", command)

            ultimo_comando = command

        # Modo seguro
        if command == "a":

            detener()

            modo_seguro = True

            print("MODO SEGURO ACTIVADO")
            print("main.py detenido")

            break

        # Avance con detección de obstáculos
        elif command == "up":

            if hay_obstaculo():

                detener()

                print("AVANCE BLOQUEADO")

            else:

                avanzar()

        elif command == "left":

            girar_izquierda()

        elif command == "right":

            girar_derecha()

        elif command == "down":

            retroceder()

        else:

            detener()

    time.sleep(0.05)

detener()

while modo_seguro:

    time.sleep(1)
