from gpiozero import OutputDevice
import time

# As portas GPIO para o motor
PIN_IN1 = 29
PIN_IN2 = 31

class Embaralhador:
    def __init__(self):
        self.motor_in1 = OutputDevice(PIN_IN1)
        self.motor_in2 = OutputDevice(PIN_IN2)
        self.parar_motor()

    def parar_motor(self):
        self.motor_in1.off()
        self.motor_in2.off()
        print("Motor parado.")

    def girar_motor(self, tempo_segundos):
        """
        Gira o motor pelo tempo especificado e depois o para.
        O timer é gerenciado pela GUI, não por esta função.
        """
        self.motor_in1.on()
        self.motor_in2.off()
        print(f"Motor girando por {tempo_segundos} segundos.")
        
        # O motor gira por todo o tempo, sem um loop de 1s
        time.sleep(tempo_segundos)

        self.parar_motor()