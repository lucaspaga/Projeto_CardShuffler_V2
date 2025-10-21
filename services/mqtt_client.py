import paho.mqtt.client as mqtt
import json
import sys

# --- Configurações do Broker MQTT ---
# Use um broker público para testes ou instale um localmente (ex: Mosquitto)
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "scoreboard/match_results"

class MqttClient:
    """
    Uma classe wrapper para simplificar a utilização do cliente Paho-MQTT,
    com gestão de estado da conexão.
    """
    def __init__(self, broker="broker.hivemq.com", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.is_connected = False

    def _on_connect(self, client, userdata, flags, rc, properties):
        """Callback para a conexão."""
        if rc == 0:
            print("Cliente MQTT conectado ao Broker com sucesso!")
            self.is_connected = True
        else:
            print(f"Falha na conexão, código de erro: {rc}\n")
            self.is_connected = False
            
    def _on_disconnect(self, client, userdata, flags, rc, properties):
        """Callback para a desconexão."""
        print("Cliente MQTT desconectado.")
        self.is_connected = False

    def connect(self):
        """Conecta-se ao broker MQTT."""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()  # Inicia um loop em segundo plano
        except ConnectionRefusedError:
            print("ERRO CRÍTICO: A conexão foi recusada. Verifique o seu firewall ou rede.")
            self.is_connected = False
        except Exception as e:
            print(f"Erro ao conectar ao broker MQTT: {e}")
            self.is_connected = False

    def publish(self, topic, payload):
        """Publica uma mensagem num tópico, verificando a conexão primeiro."""
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
        """Desconecta-se do broker."""
        self.client.loop_stop()
        self.client.disconnect()
