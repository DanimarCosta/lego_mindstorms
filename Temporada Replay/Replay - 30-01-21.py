from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import greater_than
import json

# Define o Spike Prime como Hub
hub = PrimeHub()

# Meus Blocos

def Mover(Distancia, Velocidade):
    # Configurações primarias do motor
    graus = (Distancia/(6.1 * 3.14159265) * 360)
    motor_pair = MotorPair('B', 'F')
    motor_b = Motor('F')
    motor_c = Motor('B')

    # Reseta os sensores
    motor_b.set_degrees_counted(0)
    motor_c.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    # Movimentação
    loop = True
    while loop:

        if Velocidade <= 0:
            speed = Velocidade * -1

            if (motor_b.get_degrees_counted() <= graus):
                angle = (hub.motion_sensor.get_yaw_angle() * -1)
                motor_pair.start(angle, speed)
            
            else:
                loop = False
                motor_pair.stop()
        
        else:
            speed = Velocidade * -1
            print(graus)

            if ((motor_b.get_degrees_counted() * -1) <= graus):
                print(motor_b.get_degrees_counted())
                angle = (hub.motion_sensor.get_yaw_angle())
                motor_pair.start(angle, speed)

            else:
                loop = False
                motor_pair.stop()

def Curva(Angulo, Velocidade):
    # Configurações dos motores
    motor_pair = MotorPair('F', 'B')
    motor_b = Motor('F')
    motor_c = Motor('B')

    motor_b.set_degrees_counted(0)
    motor_c.set_degrees_counted(0)

    # Configurações do sensor de movimento
    hub.motion_sensor.reset_yaw_angle()
    corecao = Angulo / 11
    Angulo = Angulo - corecao
    print(Angulo, "Angulo")

    # Movimento de curva
    loop = True
    while loop:
        if hub.motion_sensor.get_yaw_angle() <= Angulo:
            motor_b.start(Velocidade * -1)
            print(hub.motion_sensor.get_yaw_angle())

        
        else:
            motor_pair.stop()
            loop = False

# Programação
Curva(45, 25)
wait_for_seconds(0.25)