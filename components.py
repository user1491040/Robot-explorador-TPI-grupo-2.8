from libraries import LedRGB, Servo, Ultrasound, Infrared, WalkerBotV1

# Motores
SERVO_FR_PIN = 45
SERVO_FL_PIN = 9
SERVO_BR_PIN = 48
SERVO_BL_PIN = 10

# LED RGB
RGB_RED_PIN = 5
RGB_GREEN_PIN = 6
RGB_BLUE_PIN = 7

# Ultrasonido
US_TRIGGER_PIN = 4
US_ECHO_PIN = 11

# Infrarrojo
INFRARED_PIN = 12

motor_frontal_der = Servo(SERVO_FR_PIN, continuous=True)
motor_frontal_izq = Servo(SERVO_FL_PIN, continuous=True)
motor_trasero_der = Servo(SERVO_BR_PIN, continuous=True)
motor_trasero_izq = Servo(SERVO_BL_PIN, continuous=True)

led = LedRGB(RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN)
detector_us = Ultrasound(US_TRIGGER_PIN, US_ECHO_PIN)
detector_ir = Infrared(INFRARED_PIN)

control = WalkerBotV1()