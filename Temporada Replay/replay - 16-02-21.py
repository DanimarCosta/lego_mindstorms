from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
hub = PrimeHub()

# Define as portas dos motores e variaveis globais
motor_esquerdo = Motor("F")
motor_direito = Motor("B")
motores = MotorPair("B", "F")

# Reseta a leitura dos motores e sensores
motor_esquerdo.set_degrees_counted(0)
motor_direito.set_degrees_counted(0)
hub.motion_sensor.reset_yaw_angle()

# Funções para movimentação do robô
def curva(angulo, velocidade):
    ''' Este bloco esta destinado a realizar curvas com o  sensor girosópio ecom desaceleração no final da curva melhorar a 
    precisão
    '''

    # Reseta o sensor de rotação dos motores e sensores
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    angle = (angulo / 4) * 3 # Define a curva primaria

    # Fator de coreção do robô
    if angulo >= 0:
        angulo = angulo - 2.45

    else:
        angulo = angulo + 2.45

# Inicia o loop e encerra quando a varriavel loop for False

    loop = True
    while loop:
        # Realiza a curva para a direita
        if angulo >= 0:
            if hub.motion_sensor.get_yaw_angle() <= angle:
                motor_esquerdo.start(velocidade * -1)

            else:
                if hub.motion_sensor.get_yaw_angle() <= angulo:
                    motor_esquerdo.start(-10)

                else:
                    motores.stop()
                    loop = False

        # Realiza a curva para esquerda
        else:
            if hub.motion_sensor.get_yaw_angle() >= angle:
                motor_direito.start(velocidade)

            else:
                if hub.motion_sensor.get_yaw_angle() >= angulo:
                    motor_direito.start(10)

                else:
                    motores.stop()
                    loop = False

def mover(distancia, velocidade):
    ''' Este bloco esta destinado a realizar o movimento do robô com correção do backlash utilizando o sensor de movimento e 
    se move utilizando a transformação em centimetros
    '''
    # Reseta a leitura dos motores e sensores
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    # Converções necessarias para o bom funcionamento do código
    graus = (distancia/(6.1 * 3.14159265) * 360)
    velocidade = velocidade * -1
    loop = True

    while loop:
        if velocidade <= 0:
            if motor_direito.get_degrees_counted() <= graus:
                # Correção do backlash com o sensor de movimento
                backlash = hub.motion_sensor.get_yaw_angle() + 0

                motores.start(backlash, velocidade) # Liga os motores para frente

            else:
                '''Para os motores e espera 20 milésimos de segundos com o motor desligado para garantir que o robô esteja
                parado ao final do ciclo, e fecha o loop
                '''
                motores.stop()
                wait_for_seconds(0.2)
                loop = False # Variavel responsavel por fechar o loop

        else:
            if motor_esquerdo.get_degrees_counted() <= graus:
                print('menor')
                # Correção do backlash
                backlash = 0 - hub.motion_sensor.get_yaw_angle()

                motores.start(backlash, velocidade) # Liga os motores para trás

            else:
                '''Para os motores e espera 20 milésimos de segundos com o motor desligado para garantir que o robô esteja
                parado ao final do ciclo, e fecha o loop
                '''
                print('maior')
                motores.stop()
                wait_for_seconds(0.2)
                loop = False # Variavel responsavel por fechar o loop

# Funções correspondentes a cada saida do robô
def primeira_saida():
    # Mover para a missão
    mover(37, 40)
    mover(7, 10)

    # volta a area de inspeção
    wait_for_seconds(0.25)
    mover(37, -100)

# Maquina de estado
primeira_saida() # Primeira saida do robô