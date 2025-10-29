import sys
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
from PySide6.QtCore import QFile, QTextStream, Qt

def load_stylesheet(filepath):
    stylesheet_file = QFile(filepath)
    if not stylesheet_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Erro: Não foi possível abrir o arquivo {filepath}")
        return ""
    
    stylesheet = QTextStream(stylesheet_file).readAll()
    stylesheet_file.close()
    return stylesheet

class GameSetupWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        css_filepath = "./assets/style.css" 
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        
        self.setWindowTitle("Configuração da Partida")
        self.resize(800,480)

        self.game_modes = ["Truco", "Livre"]
        self.current_game_mode_index = 0
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)
        
        self.title_label = QLabel("Escolha o Modo de Jogo")
        
        self.title_label.setObjectName("title_label") 

        carousel_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("<")
        self.game_mode_label = QLabel(self.game_modes[self.current_game_mode_index])
        self.game_mode_label.setObjectName("game_mode_label")
        self.next_button = QPushButton(">")

        carousel_layout.addWidget(self.prev_button)
        carousel_layout.addStretch()
        carousel_layout.addWidget(self.game_mode_label, alignment=QtCore.Qt.AlignCenter)
        carousel_layout.addStretch()
        carousel_layout.addWidget(self.next_button)

        self.prev_button.clicked.connect(self.show_prev_game_mode)
        self.next_button.clicked.connect(self.show_next_game_mode)

        teams_layout = QVBoxLayout()
        teams_layout.setSpacing(10) 

        self.team1_input = QLineEdit()
        self.team1_input.setPlaceholderText("Nome da Equipe 1")

        self.team2_input = QLineEdit()
        self.team2_input.setPlaceholderText("Nome da Equipe 2")
        
        teams_layout.addWidget(self.team1_input)
        teams_layout.addWidget(self.team2_input)

        self.start_button = QPushButton("Iniciar Partida")
        
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addLayout(carousel_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(teams_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.start_button)
        
    def show_prev_game_mode(self):
        self.current_game_mode_index = (self.current_game_mode_index - 1) % len(self.game_modes)
        self.game_mode_label.setText(self.game_modes[self.current_game_mode_index])

    def show_next_game_mode(self):
        self.current_game_mode_index = (self.current_game_mode_index + 1) % len(self.game_modes)
        self.game_mode_label.setText(self.game_modes[self.current_game_mode_index])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = GameSetupWindow()
    janela.show()
    sys.exit(app.exec())