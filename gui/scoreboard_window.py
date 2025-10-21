import sys
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import QFile, QTextStream

# Assumindo que o mqtt_client.py está na pasta 'services'
from services.mqtt_client import MqttClient 

def load_stylesheet(filepath):
    """
    Função para ler um arquivo CSS e retornar seu conteúdo como uma string.
    """
    stylesheet_file = QFile(filepath)
    if not stylesheet_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Erro: Não foi possível abrir o arquivo {filepath}")
        return ""
    
    stylesheet = QTextStream(stylesheet_file).readAll()
    stylesheet_file.close()
    return stylesheet

class ScoreboardWindow(QWidget):
    """
    Janela que exibe o placar da partida, com controles
    para incrementar e decrementar a pontuação.
    """
    def __init__(self, team1_name="Equipe 1", team2_name="Equipe 2", game_mode=1, parent=None):
        super().__init__(parent)
        
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_score = 0
        self.team2_score = 0
        self.resize(800,480)
        self.game_mode = game_mode

        # --- Conexão MQTT ---
        # 1. Inicializa e conecta o cliente MQTT
        self.mqtt_client = MqttClient()
        self.mqtt_client.connect()

        # Carrega a folha de estilos
        css_filepath = "./assets/style.css" 
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        
        self.setWindowTitle("Placar do Jogo")
        self.init_ui()

    def init_ui(self):
        """
        Inicializa e organiza os componentes da interface gráfica.
        """
        main_layout = QVBoxLayout(self)

        # Layout superior para o botão de voltar
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        self.back_button.setObjectName("backButton")
        top_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        scores_layout = QHBoxLayout()

        # --- Coluna da Equipe 1 ---
        team1_layout = QVBoxLayout()
        self.team1_name_label = QLabel(self.team1_name)
        self.team1_name_label.setObjectName("teamNameLabel")
        
        self.team1_score_label = QLabel(str(self.team1_score))
        self.team1_score_label.setObjectName("scoreLabel")

        team1_buttons_layout = QHBoxLayout()
        self.team1_increment_button = QPushButton("+")
        self.team1_decrement_button = QPushButton("-")
        team1_buttons_layout.addWidget(self.team1_decrement_button)
        team1_buttons_layout.addWidget(self.team1_increment_button)

        team1_layout.addWidget(self.team1_name_label, alignment=QtCore.Qt.AlignCenter)
        team1_layout.addWidget(self.team1_score_label, alignment=QtCore.Qt.AlignCenter)
        team1_layout.addLayout(team1_buttons_layout)

        # --- Coluna da Equipe 2 ---
        team2_layout = QVBoxLayout()
        self.team2_name_label = QLabel(self.team2_name)
        self.team2_name_label.setObjectName("teamNameLabel")

        self.team2_score_label = QLabel(str(self.team2_score))
        self.team2_score_label.setObjectName("scoreLabel")

        team2_buttons_layout = QHBoxLayout()
        self.team2_increment_button = QPushButton("+")
        self.team2_decrement_button = QPushButton("-")
        team2_buttons_layout.addWidget(self.team2_decrement_button)
        team2_buttons_layout.addWidget(self.team2_increment_button)

        team2_layout.addWidget(self.team2_name_label, alignment=QtCore.Qt.AlignCenter)
        team2_layout.addWidget(self.team2_score_label, alignment=QtCore.Qt.AlignCenter)
        team2_layout.addLayout(team2_buttons_layout)
        
        # --- Adiciona as colunas ao layout de placares ---
        scores_layout.addLayout(team1_layout)
        separator = QLabel("|") 
        separator.setObjectName("separatorLabel")
        scores_layout.addWidget(separator, alignment=QtCore.Qt.AlignCenter)
        scores_layout.addLayout(team2_layout)

        # --- Montagem do Layout Principal ---
        self.title_label = QLabel("Placar")
        self.title_label.setObjectName("title_label")
        
        bottom_layout = QHBoxLayout()
        self.save_button = QPushButton("Finalizar Partida")
        self.save_button.setObjectName("saveButton")
        bottom_layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)

        main_layout.addStretch()
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addLayout(scores_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()

        # --- Conectar Sinais aos Slots ---
        self.team1_increment_button.clicked.connect(self.increment_team1_score)
        self.team1_decrement_button.clicked.connect(self.decrement_team1_score)
        self.team2_increment_button.clicked.connect(self.increment_team2_score)
        self.team2_decrement_button.clicked.connect(self.decrement_team2_score)

        # Define o estado inicial dos botões
        # 2. Conecta o botão de finalizar ao novo método
        self.save_button.clicked.connect(self.finish_match)
        self.update_button_states()

    def update_button_states(self):
        """Atualiza o estado dos botões com base no modo de jogo e placar."""
        if self.game_mode == 0:  # Modo Truco
            if self.team1_score >= 12 or self.team2_score >= 12:
                self.team1_increment_button.setEnabled(False)
                self.team2_increment_button.setEnabled(False)
                self.save_button.setEnabled(True)
            else:
                self.team1_increment_button.setEnabled(True)
                self.team2_increment_button.setEnabled(True)
                self.save_button.setEnabled(False)
        else:  # Modo Livre (game_mode == 1)
            self.save_button.setEnabled(True)
            self.team1_increment_button.setEnabled(True)
            self.team2_increment_button.setEnabled(True)

    def setup_match(self, team1_name, team2_name, game_mode):
        """Configura ou reinicia a partida com novos nomes e placar zerado."""
        self.game_mode = game_mode
        self.team1_name = team1_name if team1_name else "Equipe 1"
        self.team2_name = team2_name if team2_name else "Equipe 2"
        
        self.team1_score = 0
        self.team2_score = 0

        self.team1_name_label.setText(self.team1_name)
        self.team2_name_label.setText(self.team2_name)
        
        self.team1_score_label.setText(str(self.team1_score))
        self.team2_score_label.setText(str(self.team2_score))

        # Garante que o estado dos botões seja reiniciado corretamente
        self.update_button_states()

    def increment_team1_score(self):
        self.team1_score += 1
        self.team1_score_label.setText(str(self.team1_score))
        self.update_button_states()

    def decrement_team1_score(self):
        if self.team1_score > 0:
            self.team1_score -= 1
            self.team1_score_label.setText(str(self.team1_score))
            self.update_button_states()

    def increment_team2_score(self):
        self.team2_score += 1
        self.team2_score_label.setText(str(self.team2_score))
        self.update_button_states()

    def decrement_team2_score(self):
        if self.team2_score > 0:
            self.team2_score -= 1
            self.team2_score_label.setText(str(self.team2_score))
            self.update_button_states()
    
    def finish_match(self):
        """
        3. Reúne os dados da partida e publica via MQTT.
        """
        print("A finalizar a partida...")
        self.save_button.setText("A Enviar...")
        self.save_button.setEnabled(False)

        match_data = {
            "team1_name": self.team1_name,
            "team1_score": self.team1_score,
            "team2_name": self.team2_name,
            "team2_score": self.team2_score,
            "game_mode": "Truco" if self.game_mode == 0 else "Livre"
        }
        
        # Publica os dados no tópico MQTT
        self.mqtt_client.publish("scoreboard/match_results", match_data)

        # Opcional: Dar feedback ao utilizador e reativar o botão
        # (Neste caso, pode ser melhor o botão "Voltar" fazer esta limpeza)
        self.save_button.setText("Resultado Enviado!")

    def closeEvent(self, event):
        """Garante que o cliente MQTT é desconectado ao fechar a janela."""
        self.mqtt_client.disconnect()
        event.accept()

if __name__ == "__main__":
    # Bloco para permitir a execução direta do arquivo para testes
    app = QApplication(sys.argv)
    # Teste com game_mode=0 (Truco)
    janela = ScoreboardWindow(team1_name="Nós", team2_name="Eles", game_mode=1)
    janela.show()
    sys.exit(app.exec())

