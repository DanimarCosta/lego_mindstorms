from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
timer = Timer()

hub = PrimeHub()

# Define as portas dos motores e variaveis globais
# Motores Grandes
motor_esquerdo = Motor("E")
motor_direito = Motor("F")
motores = MotorPair("E", "F")
cache = 0

# Motores médios
motor_garra_esquerdo = Motor("C")
motor_garra_direito = Motor("D")
motores_garra = MotorPair("C", "D")

# Sensores
sensor_cor_esquerdo = ColorSensor("A")
sensor_cor_direito = ColorSensor("B")

# Reseta a leitura dos motores e sensores
motor_esquerdo.set_degrees_counted(0)
motor_direito.set_degrees_counted(0)

motor_garra_esquerdo.set_degrees_counted(0)
motor_garra_direito.set_degrees_counted(0)
hub.motion_sensor.reset_yaw_angle()

# Desliga os sensores que não estão sendo utilizados
sensor_cor_esquerdo.light_up_all(0)
sensor_cor_direito.light_up_all(0)

def direcao():
    direcao_robo = cache + 90

    if direcao_robo <= -89:
        if direcao_robo >= -95:
            print('Oeste')
    
    elif direcao_robo >= 89:
        if direcao_robo <= 95:
            print('Leste')
    
    elif direcao_robo >= -10:
        if direcao_robo <= 10:
            print('Norte')
    
    elif direcao_robo >= 350:
        if direcao_robo <= 360:
            print('Sul')

# Funções para movimentação do robô
def curva(angulo, velocidade):
    ''' Este bloco esta destinado a realizar curvas com osensor girosópio ecom desaceleração no final da curva melhorar a
    precisão
    '''

    # Reseta o sensor de rotação dos motores e sensores
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    global cache

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
                    cache =hub.motion_sensor.get_yaw_angle() + cache
                    print(cache)

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
                    cache = hub.motion_sensor.get_yaw_angle() + cache
                    print(cache)

def mover(distancia, velocidade):
    ''' Este bloco esta destinado a realizar o movimento do robô com correção do backlash utilizando o sensor de movimento e
    se move utilizando a transformação em centimetros
    '''
    # Reseta a leitura dos motores e sensores
    global cache
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    # Converções necessarias para o bom funcionamento do código
    graus = (distancia/(6.1 * 3.14159265) * 360)
    loop = True

    while loop:
        if velocidade <= 0:
            if motor_esquerdo.get_degrees_counted() <= graus:
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
                cache = hub.motion_sensor.get_yaw_angle() + cache
                print(cache)

        else:
            if motor_direito.get_degrees_counted() <= graus:
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
                cache = hub.motion_sensor.get_yaw_angle() + cache
                print(cache)

def garra(graus, velocidade):
    loop = True
    v_oposta = velocidade * -1
    while loop:
        if velocidade <= 0:
            if motor_garra_direito.get_degrees_counted() < graus:
                motor_garra_esquerdo.start(velocidade)
                motor_garra_direito.start(v_oposta)
            
            else:
                motor_garra_esquerdo.stop()
                motor_garra_direito.stop()
                loop = False
        
        else:
            if motor_garra_esquerdo.get_degrees_counted() < graus:
                motor_garra_esquerdo.start(velocidade)
                motor_garra_direito.start(v_oposta)

            else:
                motor_garra_esquerdo.stop()
                motor_garra_direito.stop()
                loop = False

# Funções correspondentes a cada saida do robô
def primeira_saida():
    ''' A primeira saida se desloca para a missão do banco em linha reta
    e volta a base
    '''
    # Mover até a missão
    mover(41, 40)
    mover(3, 20) 

    # Volta a area de inspeção
    wait_for_seconds(0.25)
    mover(37, -100)

def segunda_saida():
    ''' Esta saida realiza a missão compartilhada e do basquetebol
    e volta a base
    '''
    # Reseta a contagem de graus dos motores
    motor_garra_esquerdo.set_degrees_counted(0)
    motor_garra_direito.set_degrees_counted(0)

    curva(24, 20)
    mover(90, 75)
    motor_garra_direito.run_for_degrees(60, -100)

    mover(15, -50)
    curva(-29, 30)
    mover(14, 20)

    mover(15, -50)
    curva(-31, 10)
    mover(23, 50)
    motor_garra_esquerdo.run_for_degrees(2850, -100)

    mover(16, -20)
    curva(-30, 30)
    mover(70, 100)

def terceira_saida():
    ''' A segunda saida realiza a missão do escorregador e volta a
    area de inspeção
    '''
    # Mover até a missão
    mover(60, 50)
    wait_for_seconds(0.2)

    # Volta a base
    mover(15, -10)
    mover(66, -100)

def quarta_saida():
    ''' Esta saida realiza a missão do contador de passos e da
    esteira
    garra(300, -100)
    '''

    # Realiza a missão do contador de passos
    mover(85, 75)
    mover(23, 35)
    cache = 0

    mover(20, -50)
    curva(-92.7, 40)
    mover(19, -75)
    wait_for_seconds(0.5)
    
    # Passa por baixo do arco
    curva(15, 20)
    mover(75, 80)
    mover(15, -50)

    curva(90, 50)
    mover(15, 20)

    garra(250, -100)
    mover(30, -100)
    garra(4, 50)

    # Realiza a missão de puxar o peso
    curva(-23, 20)
    mover(45, 75)
    curva(88, 50)
    mover(7, 20)
    curva(-86, 50)
    mover(4, 20)

    garra(475, -100)
    mover(20, -100)
    garra(5, 100)

    # Realiza a missão de gira o pneu
    curva(80, 50)
    mover(15.2, 50)
    curva(92, 50)
    mover(43, -50)
    motor_direito.stop()
    motor_esquerdo.run_for_degrees(2100, 50)

    # Volta a base
    mover(205, 100)

def quinta_saida():
    ''' Realiza a missão da bocha e depois permanece até o final
    do round na missão da dança
    '''
    # Realiza a missão da bocha
    curva(40, 30)
    mover(97, 75)

    # Fica pendurado na barra até o final do round
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

# Status do final do round
contador = 1
while (contador <= 2):
    hub.light_matrix.write('Finalizado')
    contador = contador + 1

hub.light_matrix.show_image('YES')
