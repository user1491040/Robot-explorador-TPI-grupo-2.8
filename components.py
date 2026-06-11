from libraries import LedRGB, Servo, Ultrasound, Infrared, WalkerBotV1

# -------------------------
# Motores
# -------------------------

SERVO_FR_PIN = 45
SERVO_FL_PIN = 9
SERVO_BR_PIN = 48
SERVO_BL_PIN = 10

# -------------------------
# Sensores
# -------------------------

US_TRIGGER_PIN = 1
US_ECHO_PIN = 2

IR_IZQ_PIN = 3
IR_DER_PIN = 4

# -------------------------
# Inicialización de motores
# -------------------------

motor_frontal_der = Servo(
    SERVO_FR_PIN,
    continuous=True
)

motor_frontal_izq = Servo(
    SERVO_FL_PIN,
    continuous=True
)

motor_trasero_der = Servo(
    SERVO_BR_PIN,
    continuous=True
)

motor_trasero_izq = Servo(
    SERVO_BL_PIN,
    continuous=True
)
# -------------------------
# Control remoto WalkerBot
# -------------------------

control = WalkerBotV1()
