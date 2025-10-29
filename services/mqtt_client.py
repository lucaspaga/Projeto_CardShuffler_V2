import paho.mqtt.client as mqtt
import json
import sys

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "scoreboard/match_results"

class MqttClient:
    def __init__(self, broker="broker.hivemq.com", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.is_connected = False

    def _on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("Cliente MQTT conectado ao Broker com sucesso!")
            self.is_connected = True
        else:
            print(f"Falha na conexão, código de erro: {rc}\n")
            self.is_connected = False
            
    def _on_disconnect(self, client, userdata, flags, rc, properties):
        print("Cliente MQTT desconectado.")
        self.is_connected = False

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except ConnectionRefusedError:
            print("ERRO CRÍTICO: A conexão foi recusada. Verifique o seu firewall ou rede.")
            self.is_connected = False
        except Exception as e:
            print(f"Erro ao conectar ao broker MQTT: {e}")
            self.is_connected = False

    def publish(self, topic, payload):
        if not self.is_connected:
            print("Não foi possível publicar: cliente MQTT não está conectado.")
            return False # Indica falha

        try:
            json_payload = json.dumps(payload)
            result = self.client.publish(topic, json_payload)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Mensagem publicada com sucesso no tópico '{topic}'")
                return True
            else:
                print(f"Falha ao publicar mensagem no tópico '{topic}' (código: {result.rc})")
                return False
        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")
            return False

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
