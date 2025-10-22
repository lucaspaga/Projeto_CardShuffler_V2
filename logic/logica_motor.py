# logic/logica_motor.py

from gpiozero import OutputDevice
import time

# As portas GPIO para o motor (USE A NUMERAÇÃO BCM)
PIN_IN1 = 5  # (Antigo 29 BOARD)
PIN_IN2 = 6  # (Antigo 31 BOARD)

class Embaralhador:
    def __init__(self):
        # ... (sem mudanças)
        self.motor_in1 = OutputDevice(PIN_IN1)
        self.motor_in2 = OutputDevice(PIN_IN2)
        self.parar_motor()

    def parar_motor(self):
        # ... (sem mudanças)
        self.motor_in1.off()
        self.motor_in2.off()
        print("Motor parado.")

    # ------ MUDANÇA AQUI ------
    # Esta função agora só LIGA o motor e retorna imediatamente.
    # Ela não usa mais time.sleep()
    def girar_motor_start(self):
        """
        Apenas LIGA o motor. O timer da GUI vai pará-lo.
        """
        self.motor_in1.on()
        self.motor_in2.off()
        print(f"Motor LIGADO.")
        
    # A função antiga 'girar_motor' não é mais necessária
    # ou pode ser removida.