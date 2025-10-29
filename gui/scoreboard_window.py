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

from services.mqtt_client import MqttClient 

def load_stylesheet(filepath):
    stylesheet_file = QFile(filepath)
    if not stylesheet_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Erro: Não foi possível abrir o arquivo {filepath}")
        return ""
    
    stylesheet = QTextStream(stylesheet_file).readAll()
    stylesheet_file.close()
    return stylesheet

class ScoreboardWindow(QWidget):
    def __init__(self, team1_name="Equipe 1", team2_name="Equipe 2", game_mode=1, parent=None):
        super().__init__(parent)
        
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_score = 0
        self.team2_score = 0
        self.resize(800,480)
        self.game_mode = game_mode

        self.mqtt_client = MqttClient()
        self.mqtt_client.connect()

        css_filepath = "./assets/style.css" 
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        
        self.setWindowTitle("Placar do Jogo")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        self.back_button.setObjectName("backButton")
        top_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        scores_layout = QHBoxLayout()

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
        
        scores_layout.addLayout(team1_layout)
        separator = QLabel("|") 
        separator.setObjectName("separatorLabel")
        scores_layout.addWidget(separator, alignment=QtCore.Qt.AlignCenter)
        scores_layout.addLayout(team2_layout)

        self.title_label = QLabel("Placar")
        self.title_label.setObjectName("title_label")
        
        bottom_layout = QHBoxLayout()
        self.new_game_button = QPushButton("Nova Partida")
        self.new_game_button.setObjectName("newGameButton")
        
        self.save_button = QPushButton("Finalizar Partida")
        self.save_button.setObjectName("saveButton")
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.new_game_button)
        bottom_layout.addWidget(self.save_button)
        bottom_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addLayout(scores_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()


        self.team1_increment_button.clicked.connect(self.increment_team1_score)
        self.team1_decrement_button.clicked.connect(self.decrement_team1_score)
        self.team2_increment_button.clicked.connect(self.increment_team2_score)
        self.team2_decrement_button.clicked.connect(self.decrement_team2_score)
        
        self.save_button.clicked.connect(self.finish_match)
        self.new_game_button.clicked.connect(self.start_new_match)

        self.update_button_states()

    def start_new_match(self):
        print("A iniciar nova partida...")
        self.setup_match(self.team1_name, self.team2_name, self.game_mode)

    def update_button_states(self):
        if self.game_mode == 0:
            is_game_over = self.team1_score >= 12 or self.team2_score >= 12
            if is_game_over:
                self.team1_increment_button.setEnabled(False)
                self.team2_increment_button.setEnabled(False)
                self.save_button.setEnabled(True)
            else:
                self.team1_increment_button.setEnabled(True)
                self.team2_increment_button.setEnabled(True)
                self.save_button.setEnabled(False)
        else:
            self.save_button.setEnabled(True)
            self.team1_increment_button.setEnabled(True)
            self.team2_increment_button.setEnabled(True)

    def setup_match(self, team1_name, team2_name, game_mode):
        self.game_mode = game_mode
        self.team1_name = team1_name if team1_name else "Equipe 1"
        self.team2_name = team2_name if team2_name else "Equipe 2"
        
        self.team1_score = 0
        self.team2_score = 0

        self.team1_name_label.setText(self.team1_name)
        self.team2_name_label.setText(self.team2_name)
        
        self.team1_score_label.setText(str(self.team1_score))
        self.team2_score_label.setText(str(self.team2_score))

        self.save_button.setText("Finalizar Partida")
        self.new_game_button.setEnabled(True)
        self.update_button_states()

    def increment_team1_score(self):
        if self.game_mode == 0 and self.team1_score >= 12: return
        self.team1_score += 1
        self.team1_score_label.setText(str(self.team1_score))
        self.update_button_states()

    def decrement_team1_score(self):
        if self.team1_score > 0:
            self.team1_score -= 1
            self.team1_score_label.setText(str(self.team1_score))
            self.update_button_states()

    def increment_team2_score(self):
        if self.game_mode == 0 and self.team2_score >= 12: return
        self.team2_score += 1
        self.team2_score_label.setText(str(self.team2_score))
        self.update_button_states()

    def decrement_team2_score(self):
        if self.team2_score > 0:
            self.team2_score -= 1
            self.team2_score_label.setText(str(self.team2_score))
            self.update_button_states()
    
    def finish_match(self):
        print("A finalizar a partida...")
        self.save_button.setText("A Enviar...")
        self.save_button.setEnabled(False)
        self.new_game_button.setEnabled(False)

        match_data = {
            "team1_name": self.team1_name,
            "team1_score": self.team1_score,
            "team2_name": self.team2_name,
            "team2_score": self.team2_score,
            "game_mode": "Truco" if self.game_mode == 0 else "Livre"
        }
        
        success = self.mqtt_client.publish("scoreboard/match_results", match_data)

        if success:
            self.save_button.setText("Resultado Enviado!")
            self.new_game_button.setEnabled(True) 
        else:
            self.save_button.setText("Erro ao Enviar")
            self.save_button.setEnabled(True)
            self.new_game_button.setEnabled(True)

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ScoreboardWindow(team1_name="Nós", team2_name="Eles", game_mode=1)
    janela.show()
    sys.exit(app.exec())
