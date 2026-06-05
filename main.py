import time
from components import *

print("ROBOT INICIADO")

modo_seguro = False
ultimo_comando = None
sensores_activos = True

VELOCIDAD_AVANCE = 55
VELOCIDAD_GIRO = 45

DISTANCIA_MINIMA_FRONTAL = 20

vel_motor_frontal_izq = 0
vel_motor_frontal_der = 0
vel_motor_trasero_izq = 0
vel_motor_trasero_der = 0

def leer_distancia_frontal():

    if not sensores_activos:
        return None

    try:
        distancia = detector_us.get_distance()

        if distancia <= 0:
            return None

        return distancia

    except:
        return None

def obstaculo_frontal():

    if not sensores_activos:
        return False

    distancia = leer_distancia_frontal()

    if distancia is None:
        return False

    if distancia <= DISTANCIA_MINIMA_FRONTAL:

        print("OBSTACULO FRONTAL:", distancia, "cm")

        return True

    return False

def obstaculo_izquierda():

    if not sensores_activos:
        return False

    try:
        return detector_ir_izq.read()

    except:
        return False

def obstaculo_derecha():

    if not sensores_activos:
        return False

    try:
        return detector_ir_der.read()

    except:
        return False

def ajustar_motores(
    motor_frontal_izq_vel,
    motor_frontal_der_vel,
    motor_trasero_izq_vel,
    motor_trasero_der_vel,
    pasos=5,
    delay_ms=10
):

    global vel_motor_frontal_izq
    global vel_motor_frontal_der
    global vel_motor_trasero_izq
    global vel_motor_trasero_der

    if (
        vel_motor_frontal_izq == motor_frontal_izq_vel and
        vel_motor_frontal_der == motor_frontal_der_vel and
        vel_motor_trasero_izq == motor_trasero_izq_vel and
        vel_motor_trasero_der == motor_trasero_der_vel
    ):
        return

    inicio_frontal_izq = vel_motor_frontal_izq
    inicio_frontal_der = vel_motor_frontal_der
    inicio_trasero_izq = vel_motor_trasero_izq
    inicio_trasero_der = vel_motor_trasero_der

    for paso in range(1, pasos + 1):

        vel_motor_frontal_izq = int(
            inicio_frontal_izq +
            (motor_frontal_izq_vel - inicio_frontal_izq) * paso / pasos
        )

        vel_motor_frontal_der = int(
            inicio_frontal_der +
            (motor_frontal_der_vel - inicio_frontal_der) * paso / pasos
        )

        vel_motor_trasero_izq = int(
            inicio_trasero_izq +
            (motor_trasero_izq_vel - inicio_trasero_izq) * paso / pasos
        )

        vel_motor_trasero_der = int(
            inicio_trasero_der +
            (motor_trasero_der_vel - inicio_trasero_der) * paso / pasos
        )

        motor_frontal_izq.set_speed(vel_motor_frontal_izq)
        motor_frontal_der.set_speed(vel_motor_frontal_der)
        motor_trasero_izq.set_speed(vel_motor_trasero_izq)
        motor_trasero_der.set_speed(vel_motor_trasero_der)

        time.sleep_ms(delay_ms)

    vel_motor_frontal_izq = motor_frontal_izq_vel
    vel_motor_frontal_der = motor_frontal_der_vel
    vel_motor_trasero_izq = motor_trasero_izq_vel
    vel_motor_trasero_der = motor_trasero_der_vel

def avanzar():

    if obstaculo_frontal():

        detener()
        print("AVANCE BLOQUEADO POR SENSOR US")
        return

    ajustar_motores(
        motor_frontal_izq_vel=VELOCIDAD_AVANCE,
        motor_frontal_der_vel=-VELOCIDAD_AVANCE,
        motor_trasero_izq_vel=VELOCIDAD_AVANCE,
        motor_trasero_der_vel=-VELOCIDAD_AVANCE
    )

def retroceder():

    ajustar_motores(
        motor_frontal_izq_vel=-VELOCIDAD_AVANCE,
        motor_frontal_der_vel=VELOCIDAD_AVANCE,
        motor_trasero_izq_vel=-VELOCIDAD_AVANCE,
        motor_trasero_der_vel=VELOCIDAD_AVANCE
    )

def girar_izquierda():

    if obstaculo_izquierda():

        detener()
        print("GIRO IZQUIERDA BLOQUEADO POR IR IZQUIERDO")
        return

    ajustar_motores(
        motor_frontal_izq_vel=-VELOCIDAD_GIRO,
        motor_frontal_der_vel=-VELOCIDAD_GIRO,
        motor_trasero_izq_vel=-VELOCIDAD_GIRO,
        motor_trasero_der_vel=-VELOCIDAD_GIRO
    )

def girar_derecha():

    if obstaculo_derecha():

        detener()
        print("GIRO DERECHA BLOQUEADO POR IR DERECHO")
        return

    ajustar_motores(
        motor_frontal_izq_vel=VELOCIDAD_GIRO,
        motor_frontal_der_vel=VELOCIDAD_GIRO,
        motor_trasero_izq_vel=VELOCIDAD_GIRO,
        motor_trasero_der_vel=VELOCIDAD_GIRO
    )

def detener():

    ajustar_motores(
        motor_frontal_izq_vel=0,
        motor_frontal_der_vel=0,
        motor_trasero_izq_vel=0,
        motor_trasero_der_vel=0
    )

    motor_frontal_izq.stop()
    motor_frontal_der.stop()
    motor_trasero_izq.stop()
    motor_trasero_der.stop()

def ejecutar_comando(command):

    global sensores_activos

    if command == "a":

        detener()
        return "modo_seguro"

    elif command == "b":

        sensores_activos = not sensores_activos

        if sensores_activos:
            print("SENSORES ACTIVADOS")
        else:
            print("SENSORES DESACTIVADOS")

    elif command == "up":

        avanzar()

    elif command == "left":

        girar_izquierda()

    elif command == "right":

        girar_derecha()

    elif command == "down":

        retroceder()

    else:

        detener()

    return "normal"

while True:

    command = control.read_command()

    if command is not None:

        if command != ultimo_comando:

            print("Comando recibido:", command)

            ultimo_comando = command

        estado = ejecutar_comando(command)

        if estado == "modo_seguro":

            modo_seguro = True

            print("MODO SEGURO ACTIVADO")
            print("main.py detenido")

            break

    time.sleep(0.05)

detener()

while modo_seguro:

    time.sleep(1)
