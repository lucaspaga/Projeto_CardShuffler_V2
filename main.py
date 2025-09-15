# main.py

import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from gui.main_window import MinhaJanela
from gui.shuffler_window import GameModeWidget
from gui.dealer_window import ContadorWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Crie o QStackedWidget que vai gerenciar as telas
    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle("Embaralhador de Cartas")
    stacked_widget.resize(800, 480)

    # 2. Crie as instâncias das suas telas
    main_page = MinhaJanela(stacked_widget)
    shuffler_page = GameModeWidget(stacked_widget)
    dealer_page = ContadorWidget(stacked_widget)

    # 3. Adicione as telas ao QStackedWidget
    # A ordem em que você adiciona define o índice de cada tela (0, 1, 2...)
    stacked_widget.addWidget(main_page)    
    stacked_widget.addWidget(shuffler_page)
    stacked_widget.addWidget(dealer_page)  

    # Conecte o sinal dos botões para mudar a tela
    main_page.shuffle_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
    main_page.deal_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
    shuffler_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    dealer_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

    # 4. Exiba a janela principal (o QStackedWidget)
    stacked_widget.show()
    sys.exit(app.exec())