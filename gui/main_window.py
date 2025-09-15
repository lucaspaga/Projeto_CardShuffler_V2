import sys
import random
from PySide6 import QtCore
from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap
from gui.dealer_window import ContadorWidget
from gui.shuffler_window import GameModeWidget
import os

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

class MinhaJanela(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        css_filepath = "./assets/style.css" 
        # Carrega o CSS do arquivo
        stylesheet_content = load_stylesheet(css_filepath)
        self.setStyleSheet(stylesheet_content)
        self.setWindowTitle("Embaralhador de Cartas")
        self.init_ui()

    def init_ui(self):
        # 1. Crie os layouts
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        # 2. Crie os widgets
        self.title_label = QLabel("Embaralhador de Cartas")
        self.shuffle_button = QPushButton("Embaralhar")
        self.deal_button = QPushButton("Distribuir")

        # Suponha que você tenha um arquivo chamado 'logo.png'
        # no mesmo diretório.
        pixmap = QPixmap("./assets/images/naipes.png")

        # Opcionalmente, redimensione a imagem para caber no label
        imagem_redimensionada = pixmap.scaledToWidth(200)

        # Cria um label e define o pixmap
        self.label_imagem = QLabel()
        self.label_imagem.setPixmap(imagem_redimensionada)


        # 3. Adicione os botões ao layout horizontal
        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.deal_button)

        # 4. Adicione os layouts e widgets ao layout principal (vertical)
        # O `addLayout()` é usado para colocar um layout DENTRO de outro.
        main_layout.addStretch()
        main_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label_imagem, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
  

if __name__ == "__main__":
    # Este bloco permite que você execute o arquivo
    # diretamente para testar a janela
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec())
