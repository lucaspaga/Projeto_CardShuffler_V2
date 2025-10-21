# main.py

import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from gui.main_window import MinhaJanela
from gui.shuffler_window import GameModeWidget
from gui.dealer_window import ContadorWidget
from gui.match_window import GameSetupWindow
from gui.scoreboard_window import ScoreboardWindow


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
    match_page = GameSetupWindow(stacked_widget)
    scoreboard_page = ScoreboardWindow(stacked_widget)

    # 3. Adicione as telas ao QStackedWidget
    # A ordem em que você adiciona define o índice de cada tela (0, 1, 2...)
    stacked_widget.addWidget(main_page)    
    stacked_widget.addWidget(shuffler_page)
    stacked_widget.addWidget(dealer_page)  
    stacked_widget.addWidget(match_page)
    stacked_widget.addWidget(scoreboard_page)

    def start_match():
        # Pega os nomes da tela de configuração
        team1 = match_page.team1_input.text()
        team2 = match_page.team2_input.text()
        game_mode = match_page.current_game_mode_index
        
        # Chama o método para configurar o placar com os nomes
        scoreboard_page.setup_match(team1, team2, game_mode)
        
        # Muda para a tela do placar
        stacked_widget.setCurrentIndex(4)

    # Conecte o sinal dos botões para mudar a tela
    main_page.shuffle_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
    main_page.deal_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
    main_page.match_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))
    shuffler_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    dealer_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    match_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    scoreboard_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))

    match_page.start_button.clicked.connect(start_match)

    # 4. Exiba a janela principal (o QStackedWidget)
    stacked_widget.show()
    sys.exit(app.exec())