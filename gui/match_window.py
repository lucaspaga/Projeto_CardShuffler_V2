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

class GameSetupWindow(QWidget):
    """
    Janela para configurar a partida, escolhendo o modo de jogo
    e definindo os nomes das equipes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Carrega a folha de estilos, mantendo o padrão do projeto
        css_filepath = "./assets/style.css" 
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        
        self.setWindowTitle("Configuração da Partida")
        self.resize(800,480)
        # Lista de modos de jogo para o carrossel
        self.game_modes = ["Truco", "Livre"]
        self.current_game_mode_index = 0
        
        self.init_ui()

    def init_ui(self):
        """
        Inicializa e organiza os componentes da interface gráfica.
        """
        main_layout = QVBoxLayout(self)

        # 1. Layout para o botão de voltar no canto superior esquerdo
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addStretch()  # Empurra o botão para a esquerda

        main_layout.addLayout(top_layout)
        
        # --- Título ---
        self.title_label = QLabel("Escolha o Modo de Jogo")
        # Define um nome de objeto para permitir estilização específica via CSS
        
        self.title_label.setObjectName("title_label") 

        # --- Carrossel de Modo de Jogo ---
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

        # Conecta os sinais dos botões do carrossel aos slots (funções)
        self.prev_button.clicked.connect(self.show_prev_game_mode)
        self.next_button.clicked.connect(self.show_next_game_mode)

        # --- Nomes das Equipes ---
        teams_layout = QVBoxLayout()
        teams_layout.setSpacing(10) # Espaçamento entre os widgets de equipe

        self.team1_input = QLineEdit()
        self.team1_input.setPlaceholderText("Nome da Equipe 1")

        self.team2_input = QLineEdit()
        self.team2_input.setPlaceholderText("Nome da Equipe 2")
        
        # Agrupa os campos de texto para melhor organização
        teams_layout.addWidget(self.team1_input)
        teams_layout.addWidget(self.team2_input)

        # --- Botão de Iniciar ---
        self.start_button = QPushButton("Iniciar Partida")
        
        # --- Montagem do Layout Principal ---
        # Adiciona espaçadores para centralizar o conteúdo verticalmente
        
       
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addLayout(carousel_layout)
        main_layout.addSpacing(20) # Espaço entre o carrossel e os nomes
        main_layout.addLayout(teams_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.start_button)
        
    def show_prev_game_mode(self):
        """
        Atualiza o label do carrossel para exibir o modo de jogo anterior na lista.
        """
        self.current_game_mode_index = (self.current_game_mode_index - 1) % len(self.game_modes)
        self.game_mode_label.setText(self.game_modes[self.current_game_mode_index])

    def show_next_game_mode(self):
        """
        Atualiza o label do carrossel para exibir o próximo modo de jogo na lista.
        """
        self.current_game_mode_index = (self.current_game_mode_index + 1) % len(self.game_modes)
        self.game_mode_label.setText(self.game_modes[self.current_game_mode_index])

if __name__ == "__main__":
    # Bloco para permitir a execução direta do arquivo para testes
    app = QApplication(sys.argv)
    janela = GameSetupWindow()
    janela.show()
    sys.exit(app.exec())