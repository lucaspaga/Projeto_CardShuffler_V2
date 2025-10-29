from gpiozero import OutputDevice
import time

PIN_IN1 = 5  
PIN_IN2 = 6 

class Embaralhador:
    def __init__(self):       
        self.motor_in1 = OutputDevice(PIN_IN1)
        self.motor_in2 = OutputDevice(PIN_IN2)
        self.parar_motor()

    def parar_motor(self):
        self.motor_in1.off()
        self.motor_in2.off()
        print("Motor parado.")

    def girar_motor_start(self):
        self.motor_in1.on()
        self.motor_in2.off()
        print(f"Motor LIGADO.")