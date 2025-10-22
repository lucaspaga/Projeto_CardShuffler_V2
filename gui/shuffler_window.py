import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import QFile, QTextStream

# Importa a classe da lógica do motor
from logic.logica_motor import Embaralhador

def load_stylesheet(filepath):
    stylesheet_file = QFile(filepath)
    if not stylesheet_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Erro: Não foi possível abrir o arquivo {filepath}")
        return ""
    
    stylesheet = QTextStream(stylesheet_file).readAll()
    stylesheet_file.close()
    return stylesheet

class GameModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.modos_tempos = {
            "Truco": 10,
            "Dois Baralhos": 15,
            "Um Baralho": 20
        }
        self.modos = list(self.modos_tempos.keys())
        self.indice_atual = 0
        self.tempo_restante = self.modos_tempos[self.modos[self.indice_atual]]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_timer)

        # 1. Adiciona a instância do motor
        self.motor = Embaralhador()

        css_filepath = "./assets/style.css" 
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        self.init_ui()
        self.display_timer.setText(str(self.tempo_restante))


    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # 1. Layout para o botão de voltar no canto superior esquerdo
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addStretch()  # Empurra o botão para a esquerda

        main_layout.addLayout(top_layout)
        
        self.title_label = QLabel("Modo de jogo: ")
        self.title_label.setObjectName("titleLabel")

        self.display = QLabel(self.modos[0])
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setObjectName("display")
        self.display.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #E0E0E0;
            background-color: #A9A9A9;
            border-radius: 5px;
            padding: 10px;
            width: 30px
        """)
        
        self.display_timer = QLabel(str(self.tempo_restante))
        self.display_timer.setAlignment(Qt.AlignCenter)
        self.display_timer.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #E0E0E0;
            background-color: #A9A9A9;
            border-radius: 5px;
            padding: 10px;
            width: 30px
        """)

        botoes_layout = QHBoxLayout()
        botoes_layout.setAlignment(Qt.AlignCenter)

        self.botao_decremento = QPushButton("-")
        self.botao_decremento.clicked.connect(self.decrementar)
        botoes_layout.addWidget(self.botao_decremento)

        botoes_layout.addWidget(self.display)

        self.botao_incremento = QPushButton("+")
        self.botao_incremento.clicked.connect(self.incrementar)
        botoes_layout.addWidget(self.botao_incremento)

        self.shuffle_button = QPushButton("Embaralhar")
        self.shuffle_button.clicked.connect(self.iniciar_timer_atual)

        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addLayout(botoes_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.display_timer)
        main_layout.addStretch()
        main_layout.addWidget(self.shuffle_button, alignment=Qt.AlignCenter)

    def incrementar(self):
        self.timer.stop()
        self.shuffle_button.setEnabled(True)
        self.indice_atual = (self.indice_atual + 1) % len(self.modos)
        self.display.setText(self.modos[self.indice_atual])
        self.tempo_restante = self.modos_tempos[self.modos[self.indice_atual]]
        self.display_timer.setText(str(self.tempo_restante))

    def decrementar(self):
        self.timer.stop()
        self.shuffle_button.setEnabled(True)
        self.indice_atual = (self.indice_atual - 1 + len(self.modos)) % len(self.modos)
        self.display.setText(self.modos[self.indice_atual])
        self.tempo_restante = self.modos_tempos[self.modos[self.indice_atual]]
        self.display_timer.setText(str(self.tempo_restante))

    def iniciar_timer_atual(self):
        self.timer.stop()
        palavra_atual = self.modos[self.indice_atual]
        self.tempo_restante = self.modos_tempos[palavra_atual]
        self.display_timer.setText("Tempo Restante: " + str(self.tempo_restante))
        self.timer.start(1000)
        self.shuffle_button.setEnabled(False)
        self.botao_decremento.setEnabled(False)
        self.botao_incremento.setEnabled(False)
        self.back_button.setEnabled(False)

        tempo_total = self.modos_tempos[palavra_atual]
        motor_thread = threading.Thread(target=self.motor.girar_motor, args=(tempo_total,))
        motor_thread.start()

    def atualizar_timer(self):
        self.tempo_restante -= 1
        self.display_timer.setText("Tempo Restante: " + str(self.tempo_restante))

        if self.tempo_restante <= 0:
            self.timer.stop()
            self.display_timer.setText("Tempo Esgotado!")
            self.shuffle_button.setEnabled(True)
            self.botao_decremento.setEnabled(True)
            self.botao_incremento.setEnabled(True)
            self.back_button.setEnabled(True)   

if __name__ == "__main__":
    # Este bloco permite que você execute o arquivo
    # diretamente para testar a janela
    app = QApplication(sys.argv)
    janela = GameModeWidget()
    janela.show()
    sys.exit(app.exec())