import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile, QTextStream

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

class ContadorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.valor = 0
        css_filepath = "./assets/style.css" 
        # Carrega o CSS do arquivo
        stylesheet_content = load_stylesheet(css_filepath)
        self.resize(800,480)
        self.setStyleSheet(stylesheet_content)
        self.init_ui()

    def init_ui(self):
        """Configura a interface do widget de contador."""
        main_layout = QVBoxLayout(self)

        self.title_label = QLabel("Número de Jogadores: ")

        # 1. Layout para o botão de voltar no canto superior esquerdo
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Voltar")
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addStretch()  # Empurra o botão para a esquerda

        main_layout.addLayout(top_layout)


        # 1. Display do contador
        self.display = QLabel(str(self.valor))
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #E0E0E0;
            background-color: #A9A9A9;
            border-radius: 5px;
            padding: 10px;
            width: 30px
        """)
        
        # 2. Layout para os botões (horizontal)
        botoes_layout = QHBoxLayout()

        # Botão de Decremento
        self.botao_decremento = QPushButton("-")
        self.botao_decremento.clicked.connect(self.decrementar)
        botoes_layout.addWidget(self.botao_decremento, alignment=Qt.AlignCenter)

        botoes_layout.addWidget(self.display, alignment=Qt.AlignCenter)

        # Botão de Incremento
        self.botao_incremento = QPushButton("+")
        self.botao_incremento.clicked.connect(self.incrementar)
        botoes_layout.addWidget(self.botao_incremento, alignment=Qt.AlignCenter)

        self.shuffle_button = QPushButton("Distribuir")
        self.shuffle_button.clicked.connect(self.embaralhar)

        # Adiciona o layout dos botões ao layout principal
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addLayout(botoes_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.shuffle_button, alignment=Qt.AlignCenter)

    def incrementar(self):
        """Método para incrementar o valor do contador."""
        if self.valor >=0 and self.valor<4:    
            self.valor += 1
            self.display.setText(str(self.valor))
        else:
            self.display.setText(str(self.valor))

    def decrementar(self):
        """Método para decrementar o valor do contador."""
        if self.valor >0:  
            self.valor -= 1
            self.display.setText(str(self.valor))
        else:
            self.display.setText(str(self.valor))
    
    def embaralhar(self):
        print(self.valor) 


if __name__ == "__main__":
    # Este bloco permite que você execute o arquivo
    # diretamente para testar a janela
    app = QApplication(sys.argv)
    janela = ContadorWidget()
    janela.show()
    sys.exit(app.exec())