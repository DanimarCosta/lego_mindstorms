from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import json

hub = PrimeHub()

# Define as portas dos motores e variaveis globais
# Motores Grandes
motor_esquerdo = Motor("F")
motor_direito = Motor("B")
motores = MotorPair("B", "F")

# Motores médios
motor_garra_esquerdo = Motor("A")
motor_garra_direito = Motor("D")

# Sensores
sensor_cor_esquerdo = ColorSensor("E")
sensor_cor_direito = ColorSensor("C")

# Reseta a leitura dos motores e sensores
motor_esquerdo.set_degrees_counted(0)
motor_direito.set_degrees_counted(0)
hub.motion_sensor.reset_yaw_angle()

# Desliga os sensores que não estão sendo utilizados
sensor_cor_esquerdo.light_up_all(0)
sensor_cor_direito.light_up_all(0)

# Funções para movimentação do robô
def curva(angulo, velocidade):
    ''' Este bloco esta destinado a realizar curvas com osensor girosópio ecom desaceleração no final da curva melhorar a
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
                # Correção do backlash
                backlash = 0 - hub.motion_sensor.get_yaw_angle()

                motores.start(backlash, velocidade) # Liga os motores para trás

            else:
                '''Para os motores e espera 20 milésimos de segundos com o motor desligado para garantir que o robô esteja
                parado ao final do ciclo, e fecha o loop
                '''
                motores.stop()
                wait_for_seconds(0.2)
                loop = False # Variavel responsavel por fechar o loop

# Funções correspondentes a cada saida do robô
def primeira_saida():
    ''' A primeira saida se desloca para a missão do banco em linha reta
    e volta a base
    '''
    # Mover até a missão
    mover(41, 40)
    mover(3, 10) 

    # Volta a area de inspeção
    wait_for_seconds(0.25)
    mover(37, -100)

def segunda_saida():
    ''' A segunda saida realiza a missão do escorregador e volta a
    area de inspeção
    '''
    # Mover até a missão
    mover(60, 50)
    wait_for_seconds(0.2)

    # Volta a area de inspeção
    mover(15, -10)
    mover(66, -100)

def terceira_saida():
    ''' Esta saida realiza a missão compartilhada e do basquetebol
    e volta a base
    '''
    # Reseta os motores
    motor_garra_esquerdo.set_degrees_counted(0)
    motor_garra_direito.set_degrees_counted(0)

    # Mover até a missão do basketeball
    motor_garra_direito.run_for_degrees(10, -100)
    curva(22, 20)
    mover(88, 75)
    motor_garra_direito.set_degrees_counted(0)
    motor_garra_direito.run_for_degrees(60, 100)
    mover(10, -30)
    curva(-35, 20)
    mover(6, 10)
    mover(20, -30)
    curva(-27, 20)
    mover(27, 30)
    motor_garra_esquerdo.run_for_degrees(2750, -100)
    mover(20, -20)
    curva(-30, 30)
    mover(80, 75)

def quarta_saida():
    ''' Esta saida realiza a missão do contador de passos e da
    esteira
    '''
    mover(110.5, 50)
    wait_for_seconds(0.2)

    mover(20, -40)
    curva(-92.7, 40)
    mover(19, -50)
    mover(10, -100)
    wait_for_seconds(0.5)

    mover(15.35, 40)
    curva(-90.4, 20)
    mover(97.5, -50)
    wait_for_seconds(0.5)

    motor_esquerdo.set_degrees_counted(0)
    motor_esquerdo.run_for_degrees(1800)
    mover(20, 50)
    curva(-6, 30)
    mover(170, 100)

def quinta_saida():
    ''' Realiza a missão da bocha e depois permanece até o final
    do round na missão da dança
    '''
    curva(40, 30)
    mover(97, 75)
    mover(20, -30)
    curva(45, 30)
    mover(22, 30)
    curva(90, 50)
    mover(28, 30)

# Maquina de estado
def maquina_estado():
    ''' Gerenciador de lançamentos do robô
    '''
    contador = 1

    loop = True
    while loop:

        # Controle
        if hub.right_button.was_pressed():
            contador = contador + 1
        
        elif contador > 5:
            contador = contador - 5
        
        # Organiza as saidas
        if contador == 1:
            # identificador
            hub.light_matrix.write('1')

            if hub.left_button.was_pressed():
                primeira_saida()
                contador = contador + 1
        
        elif contador == 2:
            # identificador
            hub.light_matrix.write('2')

            if hub.left_button.was_pressed():
                segunda_saida()
                contador = contador + 1

        elif contador == 3:
            # identificador
            hub.light_matrix.write('3')

            if hub.left_button.was_pressed():
                terceira_saida()
                contador = contador + 1

        elif contador == 4:
            # identificador
            hub.light_matrix.write('4')

            if hub.left_button.was_pressed():
                quarta_saida()
                contador = contador + 1

        elif contador == 5:
            # identificador
            hub.light_matrix.write('5')

            if hub.left_button.was_pressed():
                quinta_saida()
                loop = False

maquina_estado()

# Finalizado
contador = 1
while (contador <= 2):
    hub.light_matrix.write('Finalizado')
    contador = contador + 1

hub.light_matrix.show_image('YES')
