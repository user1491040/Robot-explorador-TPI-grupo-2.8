import time
from components import *

print("ROBOT INICIADO")

modo_seguro = False
ultimo_comando = None
modo_turbo = False

VELOCIDAD_AVANCE_NORMAL = 55
VELOCIDAD_GIRO_NORMAL = 45

VELOCIDAD_AVANCE_TURBO = 80
VELOCIDAD_GIRO_TURBO = 65

vel_motor_frontal_izq = 0
vel_motor_frontal_der = 0
vel_motor_trasero_izq = 0
vel_motor_trasero_der = 0

def obtener_velocidad_avance():

    if modo_turbo:
        return VELOCIDAD_AVANCE_TURBO

    return VELOCIDAD_AVANCE_NORMAL

def obtener_velocidad_giro():

    if modo_turbo:
        return VELOCIDAD_GIRO_TURBO

    return VELOCIDAD_GIRO_NORMAL

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

    velocidad = obtener_velocidad_avance()

    ajustar_motores(
        motor_frontal_izq_vel=velocidad,
        motor_frontal_der_vel=-velocidad,
        motor_trasero_izq_vel=velocidad,
        motor_trasero_der_vel=-velocidad
    )

def retroceder():

    velocidad = obtener_velocidad_avance()

    ajustar_motores(
        motor_frontal_izq_vel=-velocidad,
        motor_frontal_der_vel=velocidad,
        motor_trasero_izq_vel=-velocidad,
        motor_trasero_der_vel=velocidad
    )

def girar_izquierda():

    velocidad = obtener_velocidad_giro()

    ajustar_motores(
        motor_frontal_izq_vel=-velocidad,
        motor_frontal_der_vel=-velocidad,
        motor_trasero_izq_vel=-velocidad,
        motor_trasero_der_vel=-velocidad
    )

def girar_derecha():

    velocidad = obtener_velocidad_giro()

    ajustar_motores(
        motor_frontal_izq_vel=velocidad,
        motor_frontal_der_vel=velocidad,
        motor_trasero_izq_vel=velocidad,
        motor_trasero_der_vel=velocidad
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

    global modo_seguro
    global modo_turbo

    if modo_seguro:

        detener()
        return

    if command == "a":

        detener()
        modo_seguro = True

        print("MODO SEGURO ACTIVADO")
        print("Robot detenido completamente")

    elif command == "b":

        modo_turbo = not modo_turbo

        if modo_turbo:
            print("MODO TURBO ACTIVADO")
        else:
            print("MODO TURBO DESACTIVADO")

        detener()

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

while True:

    command = control.read_command()

    if modo_seguro:

        detener()
        time.sleep(1)
        continue

    if command is not None:

        if command != ultimo_comando:

            print("Comando recibido:", command)

            ultimo_comando = command

        ejecutar_comando(command)

    time.sleep(0.05)
