import paho.mqtt.client as mqtt
import json
import os
import sys
import psycopg2
from dotenv import load_dotenv

def start_database_service():
    """
    Função principal que configura e inicia o cliente MQTT para escutar
    e guardar os dados na base de dados.
    """
    load_dotenv()

    # --- Configurações ---
    MQTT_BROKER = "broker.hivemq.com"
    MQTT_PORT = 1883
    MQTT_TOPIC = "scoreboard/match_results"
    DATABASE_URL = os.getenv("DATABASE_URL")

    def save_to_database(match_data):
        """Conecta à base de dados PostgreSQL e insere os dados da partida."""
        print("[DB Service] A guardar dados da partida...")
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            sql_command = """
                INSERT INTO matches (team1_name, team1_score, team2_name, team2_score, game_mode)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(sql_command, (
                match_data.get('team1_name'), match_data.get('team1_score'),
                match_data.get('team2_name'), match_data.get('team2_score'),
                match_data.get('game_mode')
            ))
            conn.commit()
            print(f"[DB Service] SUCESSO: Partida guardada!")
            cursor.close()
        except psycopg2.Error as e:
            print(f"[DB Service] !!! ERRO DE BASE DE DADOS: {e}")
            if conn: conn.rollback()
        finally:
            if conn: conn.close()

    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"[DB Service] Conectado ao MQTT Broker e a subscrever o tópico: '{MQTT_TOPIC}'")
            client.subscribe(MQTT_TOPIC)
        else:
            print(f"[DB Service] !!! Falha na conexão com o MQTT, código: {rc}")

    def on_message(client, userdata, msg):
        print("\n[DB Service] -----------------------------------------")
        print(f"[DB Service] Mensagem recebida no tópico: {msg.topic}")
        try:
            payload = json.loads(msg.payload.decode())
            save_to_database(payload)
        except Exception as e:
            print(f"[DB Service] !!! ERRO ao processar a mensagem: {e}")

    if not DATABASE_URL:
        print("[DB Service] ERRO CRÍTICO: Variável de ambiente DATABASE_URL não encontrada.")
        return # Sai da função se a URL não estiver definida
        
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"[DB Service] !!! ERRO CRÍTICO ao conectar ao broker MQTT: {e}")
        return

    # Este laço mantém o serviço a escutar em segundo plano
    client.loop_forever()